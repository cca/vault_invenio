# Notes on running Invenio RDM

To start:

- open Docker Desktop
- run `invenio-cli containers start`

https://github.com/inveniosoftware/training

RabbitMQ admin interface: http://localhost:15672 credentials "guest/guest"
Elasticsearch: http://localhost:9200/rdmrecords/ transitioning from ES to Open Search
pgAdmin (db): http://127.0.0.1:5050/login credentials "phette23@gmail.com/cca-vault" or look in docker-services.yml
May need to set the postgres host to "host.docker.internal" e.g. in docker/pgadmin/servers.json
API end points: https://127.0.0.1/api/records | https://127.0.0.1/api/users

Some documentation shows port 5000 on API requests; ignore this, it's for running services locally, not using containers.

Example sites: https://data.caltech.edu/ | https://invenio.itam.cas.cz/
https://github.com/caltechlibrary/caltechdata/tree/main

Decent docs https://inveniordm.docs.cern.ch/ the reference https://inveniordm.docs.cern.ch/reference/ and customize https://inveniordm.docs.cern.ch/customize/ sections are the most useful.

## Setup Troubles

Setup failed with an error but the containers did come up. Trying to do basic things (login, access records via API) fails with database errors, it looks like nothing was initialized. Interestingly, the website still displays (it's not fully reliant on the database), but trying to _do_ almost anything leads to an error.

Could not figure out how to do the Elasticsearch Docker config. Their instructions are outdated, link to this ES which is more current https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html#docker-prod-prerequisites but `docker-machine` is deprecated and even after installing it I'm not able to successfully run `docker-machine ssh`

Eventually I figured out how to enter one of the  containers (I think either invenio-web-api or invenio-worker are OK) which have the app's python environment and `invenio` CLI available to initialize everything that wasn't built. You can sort of see what the cli should have done in the `_setup()` function here https://github.com/inveniosoftware/invenio-cli/blob/master/invenio_cli/commands/containers.py#L93

`invenio-cli containers setup` should do below...

```sh
docker exec -it $ID /bin/bash
invenio db init create
invenio files location create --default default-location ${INVENIO_INSTANCE_PATH}/data
invenio roles create admin
invenio access allow superuser-access role admin
invenio index init
# if you try to upload it still won't work until you do this
invenio rdm-records fixtures
# submits a background task to create some demo records?
invenio rdm-records demo
# may be necessary after the two commands above
invenio rdm-records rebuild-index
# initialize custom fields
invenio rdm-records custom-fields init
```

Admin user (admin@inveniosoftware.org) should have password `password` based on `RDM_RECORDS_USER_FIXTURE_PASSWORDS` in invenio.cfg. If not, reset it as described here: https://inveniordm.docs.cern.ch/customize/vocabularies/users/

I don't know what the last step of `invenio-cli containers start --lock --build --setup`, `update_services_setup`, does and I couldn't figure out how to do it.

Can't create a user because it requires email activation but no emails are sent. The `invenio users` command doesn't seem to offer a way around this. Disable email activation in invenio.cfg with `SECURITY_CONFIRMABLE = False` and `SECURITY_LOGIN_WITHOUT_CONFIRMATION = True`. As of v11 there is a `--confirm` flag so you can `invenio users create -c` to automatically confirm the created user.

Can't create records with the API because requests are rejected for not having a referrer.

After adding a logo image and editing invenio.cfg, the new image wasn't copied to the nginx frontend server after a `invenio-cli containers rebuild`.

There was an npm error when running `invenio-cli assets build`, I fixed it by downgrading npm to v6.

## Customization

Lots of UI variables to override and you can specify an additional stylesheet.

https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py

Create a template in the same path as existing one e.g. /templates/semantic-ui/invenion_app_rdm/frontpage.html pretty easy but does make me worry about continual updates

SSO: https://inveniordm.docs.cern.ch/customize/authentication/
SSO is supported but isn't well tested https://inveniordm.docs.cern.ch/customize/authentication/#saml-integration the CERN instances use ORCID & GitHub for authentication

**static pages** (added in v11) will be useful
https://inveniordm.docs.cern.ch/customize/static_pages/

### Custom Fields

I tried to follow the custom fields documentation closely to create a couple, but the TextCF one for a rich text artists' statement didn't work, it threw an error related to receiving multiple `field_cls` parameters.

The VocabularyCF for CCA academic programs technically built but then when I go to actually add one to an upload, there's an AJAX error during the autocomplete. I'm not sure what could be the matter (something's not indexed, my vocabulary YAML is not formatted correctly) nor how to easily rebuild just that vocabulary & not the whole app.

Removing unneeded fields from the app sounds like it is not a straightforward process:
https://discord.com/channels/692989811736182844/724974365451747329/1038081675474780280

## Roadmap

Notable in the roadmap: https://inveniosoftware.org/products/rdm/roadmap/

- Custom fields will be important for us (**released in 10.0 this October**)
- Metadata "Back office" / admin will also, I assume that's a Manage Resources equivalent
- OCFL: not hugely important for us but most serious repositories are standardizing around OCFL so this could be important for migration later

Without those two features Invenio lags behind a it, or will be more work to customize.

This is a more detailed roadmap with an issue for each feature: https://github.com/inveniosoftware/product-rdm/issues

## 10.0.0 upgrade

Edited Pipfile to reference Invenio 10.0.0

`invenio-cli containers build` failed with errors related to webpack and missing assets from the new custom fields feature

Had to edit .invenio, add `search = elasticsearch7` line

on web-ui container

```sh
cd /opt/invenio/src
vim .invenio # add "search = elasticsearch7" line under [cookiecutter]
pipenv install invenio-cli==1.0.6
invenio-cli packages update 10.0.0
invenio-cli assets build
```

none of the invenio or invenio-cli commands work on the container because they expect pipenv to have made a virtualenv but the Dockerfile installs the dependencies into the system python environment

exit and `invenio-cli containers build` on the host

## 11.0.0 upgrade

https://inveniordm.docs.cern.ch/releases/upgrading/upgrade-v11.0/

Stop containers
Edit Dockerfile to reference the new CERN base image
Update invenio-cli in the venv
Edit Pipfile to set invenio version to 11
`invenio-cli packages update 11.0.0`
`invenio-cli containers build`
`invenio-cli containers start`
then, inside the web-ui container, `invenio alembic upgrade`
the "data migration" step is another one that doesn't make sense if you're using containers, it asks you to run `pipenv` commands but the way the containers are `pipenv` is using the system site packages and not a venv. So I used `python -m site` to find my python's site packages and then found the script being referred to and ran
`invenio shell /usr/local/lib/python3.9/site-packages/invenio_app_rdm/upgrade_scripts/migrate_10_0_to_11_0.py`

```sh
vim Pipfile # update invenio-cli and invenio versions
pipenv install
invenio-cli packages update 11.0.0
invenio-cli containers build
invenio-cli containers start
docker exec -it invenio-web-ui-1 /bin/bash
invenio alembic upgrade
invenio shell /usr/local/lib/python3.9/site-packages/invenio_app_rdm/upgrade_scripts/migrate_10_0_to_11_0.py
```
