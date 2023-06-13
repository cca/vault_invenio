# Notes on InvenioRDM

Goals:

- [x] basic custom templates
https://inveniordm.docs.cern.ch/customize/look-and-feel/templates/
https://github.com/inveniosoftware/invenio-app-rdm/tree/master/invenio_app_rdm/theme/templates/semantic-ui/invenio_app_rdm
- [x] convert to local services, containerized development is too slow
- [x] remove fields from upload form (e.g. funders)
- [x] add custom field (CCA Academic Programs?)
- [ ] add a static page (tried, did not work)
https://inveniordm.docs.cern.ch/customize/static_pages/
- [x]  add a custom view
https://inveniordm.docs.cern.ch/develop/howtos/custom_code/
- [ ] custom resource types
https://inveniordm.docs.cern.ch/customize/vocabularies/resource_types/
https://discord.com/channels/692989811736182844/724974365451747329/1065248477505929246
- [ ] conditional fields based on resource type
https://discord.com/channels/692989811736182844/704625518552547329/1091254152182640660
- [x] add (and make default?) a Copyright license field
- [x] test the file integrity check report
- [ ] permissions & groups: how granular? can we create groups that see certain items?
permissions available to react form components:
https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/requests_ui/views/requests.py#L62
- [ ] **SSO**
- [ ] test CalTech "change_owner" script
https://github.com/caltechlibrary/caltechdata/tree/main/scripts
"requires invenio_utilities_tuw" so will have to add that to Pipfile (but it's not listed in CalTech's Pipfile?)
https://gitlab.tuwien.ac.at/fairdata/invenio-utilities-tuw amazingly this isn't on GitHub
- [ ] admin panel
https://inveniordm.docs.cern.ch/develop/topics/administration_panel/

## Running InvenioRDM

To start:

- open Docker Desktop
- run `invenio-cli services start` to start the db, search, task queue, & redis cache
- run `invenio-cli run` to run the app (may want to put this in the background)

RabbitMQ admin interface: http://localhost:15672 credentials "guest/guest"
Elasticsearch: http://localhost:9200/rdmrecords/ transitioning from ES to Open Search
pgAdmin (db): http://127.0.0.1:5050/login credentials "phette23@gmail.com/cca-vault" or look in docker-services.yml
I disabled the OpenSearch Dashboard in the docker-services.yml file but it could be added here as well
May need to set the postgres host to "host.docker.internal" e.g. in docker/pgadmin/servers.json
API end points: https://127.0.0.1:5000/api/records | https://127.0.0.1:5000/api/users

Note that, if you're running the app locally the main URLs (for website and REST API) are on localhost:5000 while if you run the app on a container then you do not need the port and the website, background worker, and API are all on different containers each with a copy of the application code (but no static files for the worker & API).

## Example Sites

TU Wien https://researchdata.tuwien.ac.at/
https://gitlab.tuwien.ac.at/fairdata/invenio-theme-tuw
TU Graz https://repository.tugraz.at/
https://github.com/tu-graz-library/invenio-theme-tugraz

Example sites: https://data.caltech.edu/ | https://invenio.itam.cas.cz/
https://github.com/caltechlibrary/caltechdata
Zenodo: https://github.com/zenodo/zenodo-rdm | https://zenodo.org/
CERN Document Server: https://github.com/CERNDocumentServer/cds-rdm might have some useful bits under site (e.g. see cli command to delete a record)

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

There was an npm error when running `invenio-cli assets build`, I fixed it by _downgrading_ npm to v6. `invenio-cli check-requirements --development` complains if you have npm > 7.

The instructions for setting up with services do not work because the CLI never recognizes that the opensearch container has started. But if you run `invencio-cli services start` first, wait for it to end even if it says search never came online, check the search container and URL (port 9200), then you can run `invenio-cli services setup` to initialize everything and load the demo data.

## Customization

Lots of UI variables to override and you can specify an additional stylesheet.

https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/config.py

Create a template in the same path as existing one e.g. /templates/semantic-ui/invenion_app_rdm/frontpage.html pretty easy but does make me worry about continual updates

SSO: https://inveniordm.docs.cern.ch/customize/authentication/
SSO is supported but isn't well tested https://inveniordm.docs.cern.ch/customize/authentication/#saml-integration the CERN instances use ORCID & GitHub for authentication

Develop own module: https://invenio.readthedocs.io/en/maint-3.0/tutorial-module/index.html

**static pages** (added in v11) will be useful
https://inveniordm.docs.cern.ch/customize/static_pages/

### Remove fields from upload form

https://inveniordm.docs.cern.ch/develop/howtos/override_components/

- find the field's `Overridable` component on the deposit form https://github.com/inveniosoftware/invenio-app-rdm/blob/master/invenio_app_rdm/theme/assets/semantic-ui/js/invenio_app_rdm/deposit/RDMDepositForm.js
- copy the `id` attribute
- in assets/js/invenio_app_rdm/overridableRegistry/mapping.js add a line to the `overriddenComponents` hash:

```js
export const overriddenComponents = {
    "InvenioAppRdm.Deposit.FundingField.layout": () => null,
}
```

Waiting on [a PR](https://github.com/inveniosoftware/invenio-app-rdm/pull/2087) to make it so you can remove the parent AccordionField as well.

### Custom Fields

Simplest: https://inveniordm.docs.cern.ch/customize/custom_fields/records/
Reference: https://inveniordm.docs.cern.ch/reference/widgets/#autocompletedropdown
Build your own: https://inveniordm.docs.cern.ch/develop/howtos/custom_fields/

Managed to build a custom "Academic Programs" field in around an hour that uses a vocabulary, autocompletes on the form, and has a custom display template linking to search results sharing the same value (similar to how we do it in VAULT). The only thing that did not work is that the search facet does not appear, but the indexing clearly works because the hyperlinked search returns results.

One other disappointment is that, though I defined a bunch of properties in for each term in the related programs vocab, it only records the `id` and `title` in the record.

## Roadmap

Notable in the roadmap: https://inveniosoftware.org/products/rdm/roadmap/

- Custom fields will be important for us (**released in 10.0 this October**)
- Metadata "Back office" / admin will also, I assume that's a Manage Resources equivalent. Did this disappear off of the roadmap? Says "completed by CERN in Sept 2023"
- OCFL: not hugely important for us but most serious repositories are standardizing around OCFL so this could be important for migration later

Without those two features Invenio lags behind a it, or will be more work to customize.

This is a more detailed roadmap with an issue for each feature: https://github.com/inveniosoftware/product-rdm/issues

### Digital Preservation

OCFL is being worked on but right now there is only a tool to export Invenio files to OCFL, they are not stored in that layout. Still, their layout is _similar_ — files are stored in venv root > /var/instance/data > then a tree like this:
├── 1b
│   └── 3c
│       └── 2deb-40cd-46ed-9097-0b44fc0aa2ef
│           └── data

#### File Integrity Check

The v11 file integrity check report is wonderful, something obviously missing from EQUELLA. It took me some time to figure out what the `CELERY_BEAT_SCHEDULE` settings had to look like (see celery_beat.py in this dir):

```python
from datetime import datetime
from invenio_app_rdm.config import CELERY_BEAT_SCHEDULE
CELERY_BEAT_SCHEDULE = {
    **CELERY_BEAT_SCHEDULE,
    'file-checks': {
        'task': 'invenio_files_rest.tasks.schedule_checksum_verification',
        'schedule': datetime.timedelta(seconds=60),
        'kwargs': {
            'batch_interval': {
                'hours': 1
            },
            'frequency': {
                'days': 14
            },
            'max_count': 0,
            'files_query': 'invenio_app_rdm.utils.files.checksum_verification_files_query'
        }
    },
    'file-integrity-report': {
        'task': 'invenio_app_rdm.tasks.file_integrity_report',
        'schedule': datetime.timedelta(seconds=120)
    }
}
```

This sets the check to run every minute and the report to mail every other minute, if you then enter into the instance data dir and mess with one of the files (e.g. `echo 'blah' >> 1b/3c/2deb-40cd-46ed-9097-0b44fc0aa2ef/data`) it'll trigger the check and print an email to your console.

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
