# Running Invenio

This document is about managing a running Invenio instance. See **Getting Started** in [develop.md](develop.md) for how to setup and start the app.

## Services

| Service | URL | Notes |
|---------|-----|-------|
| RabbitMQ admin interface | http://localhost:15672 | credentials "guest/guest"
| Elasticsearch | http://localhost:9200/_cat/indices?v |
| Postgres db | localhost:5432 | username, password, & db name are all "invenio-vault", run `./notes/code-samples/dbconnect`
| pgAdmin (db) | http://127.0.0.1:5050/login | credentials "ephetteplace@cca.edu/invenio-vault" or look in docker-services.yml
| API | https://127.0.0.1:5000/api/records | same port as app if running locally

The Postgres database is another service but is not exposed, use pgAdmin to interact with it.

The OpenSearch Dashboard is disabled in the docker-services.yml but could be added.

You may need to set the postgres host to "host.docker.internal" e.g. in docker/pgadmin/servers.json.

If you're running the app locally the main URLs (for website and REST API) are localhost:5000 while if you run the fully containerized app then you do not need the port and the website, background worker, and API are all on different containers. Each of these three has the application code, but there are no static files for the worker & API.

## Elasticsearch vs. OpenSearch

The project is transitioning from Elasticsearch (licensing concerns) to OpenSearch (AWS fork of ES). We may want to stick with ES anyways. @TODO confirm ES will be supported going forward

The instructions on ES docker configuration are outdated, link to this ES which is more current https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html#docker-prod-prerequisites but `docker-machine` is deprecated and even after installing it I'm not able to successfully run `docker-machine ssh`

## Setup Troubles

Setup failed with an error but the containers did come up. Trying to do basic things (login, access records via API) fails with database errors, it looks like nothing was initialized. Interestingly, the website still displays (it's not fully reliant on the database), but trying to _do_ almost anything leads to an error.

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

The instructions for setting up with services do not work because the CLI never recognizes that the opensearch container has started. But if you run `invencio-cli services start` first, wait for it to end even if it says search never came online, check the search container and URL (port 9200), then you can run `invenio-cli services setup` to initialize everything and load the demo data.

There was an npm error when running `invenio-cli assets build`, I fixed it by _downgrading_ npm to v6. `invenio-cli check-requirements --development` complains if you have npm > 7.
