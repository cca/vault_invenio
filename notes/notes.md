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

Some documentation will show port 5000 on API requests; ignore this, it is for running the services locally, not using containers.

Example sites: https://data.caltech.edu/ | https://invenio.itam.cas.cz/

## Setup Troubles

Setup failed with an error but the containers did come up. Trying to do basic things (login, access records via API) fails with database errors, it looks like nothing was initialized. Interestingly, the website still displays (it's not fully reliant on the database), but trying to _do_ almost anything leads to an error.

Could not figure out how to do the Elasticsearch Docker config. Their instructions are outdated, link to this ES which is more current https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html#docker-prod-prerequisites but `docker-machine` is deprecated and even after installing it I'm not able to successfull run `docker-machine ssh`

Eventually I figured out how to enter one of the  containers (I think either invenio-web-api or invenio-worker are OK) which have the app's python environment and `invenio` CLI available to initialize everything that wasn't built. You can sort of see what the cli should have done in the `_setup()` function here https://github.com/inveniosoftware/invenio-cli/blob/master/invenio_cli/commands/containers.py#L93

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
```

I don't know what the last step of `invenio-cli containers start --lock --build --setup`, `update_services_setup`, does and I couldn't figure out how to do it. It also required at least another couple of commands (the final two above).

Can't create a user because it requires email activation but no emails are sent. The `invenio users` command doesn't seem to offer a way around this. Disable email activation in invenio.cfg with `SECURITY_CONFIRMABLE = False` and `SECURITY_LOGIN_WITHOUT_CONFIRMATION = True`.

Can't create records with the API because requests are rejected for not having a referrer.

SSO is supported but isn't well tested https://inveniordm.docs.cern.ch/customize/authentication/#saml-integration the CERN instances use ORCID & GitHub for authentication

After adding a logo image and editing invenio.cfg, the new image wasn't copied to the nginx frontend server after a `invenio-cli containers rebuild`.

There was an npm error when running `invenio-cli assets build`, I fixed it by downgrading npm to v6.

## Customization

Lots of UI variables to override and you can specify an additional stylesheet.

https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py

Create a template in the same path as existing one e.g. /templates/semantic-ui/invenion_app_rdm/frontpage.html pretty easy but does make me worry about continual updates

Notable in the roadmap: https://inveniosoftware.org/products/rdm/roadmap/

- Custom fields will be important for us (**released in 10.0 this October**)
- Metadata "Back office" / admin will also, I assume that's a Manage Resources equivalent
- OCFL: not hugely important for us but most serious repositories are standardizing around OCFL so this could be important for migration later

Without those two features Invenio lags behind a it, or will be more work to customize.
5039884357 #3

## 10.0.0 upgrade

Edited Pipfile to reference Invenion 10.0.0

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
