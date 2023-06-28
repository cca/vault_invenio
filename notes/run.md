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

The API uses the search indices. If you go to visit every page (e.g. search, dashboard, etc.) but see errors and 500 HTTP responses from the API, then the search indices probably have not been created. `invenio index init` lets you visit various pages, but there will be no contents, because the indices are empty.

If the `invenio-cli services setup` command fails, we can sort of see what the cli should have done in the `_setup()` function: https://github.com/inveniosoftware/invenio-cli/blob/master/invenio_cli/commands/containers.py#:~:text=def%20_setup

```sh
invenio db init create
# on a local instance the INVENIO_INSTANCE_PATH is the venv + var/instance/data so
# (pipenv --venv)/var/instance/data
invenio files location create --default default-location ${INVENIO_INSTANCE_PATH}/data
# @TODO are these needed here? I think rdm-records fixtures creates them
invenio roles create admin
invenio access allow superuser-access role admin
invenio index init
# initialize custom fields
invenio rdm-records custom-fields init
invenio communities custom-fields init
# app is semi-usable without errors now but uploads still won't work
# until you load fixtures because they contains all the vocabs (resource types, subjects, etc.)
invenio rdm fixtures
# app is usable but has no content
# this submits a background task to create demo records, will take time
invenio rdm-records demo
# may be necessary after the two commands above?
invenio rdm-records rebuild-index
# Invenio v12 also adds this step
invenio queues declare
```

The instructions for setting up with services do not work because the CLI never recognizes that the opensearch container has started. But if you run `invencio-cli services start` first, wait for it to end even if it says search never came online, check the search container and URL (port 9200), then you can run `invenio-cli services setup` to initialize everything and load the demo data.

There was an npm error when running `invenio-cli assets build`, I fixed it by _downgrading_ npm to v6. `invenio-cli check-requirements --development` complains if you have npm > 7.
