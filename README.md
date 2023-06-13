# VAULT InvenioRDM

Welcome to your InvenioRDM instance.

## Getting started

See [Installation docs](https://inveniordm.docs.cern.ch/install/). We recommend the "local" or "services" setup which runs the main Invenio Flask application on your host machine using the code in this repository, while the database, search engine, task queue, and redis cache are run as Docker containers.

```sh
# to build fresh, answering configuration questions
invenio-cli init rdm -c 11.0
invenio-cli install
invenio-cli services setup
invenio-cli run
```

To start:

- run Docker
- run `invenio-cli services start` to start the db, search, task queue, & redis cache
- run `invenio-cli run` to run the app (may want to put this in the background)

The above commands first builds the application docker image and afterwards starts the application and related services (database, Elasticsearch, Redis and RabbitMQ). The build and boot process will take some time to complete, especially the first time as docker images have to be downloaded during the process.

Once running, visit https://127.0.0.1 in your browser. **Note**: The server is using a self-signed SSL certificate, so your browser will issue a warning that you will have to by-pass.

## Overview

Following is an overview of the generated files and folders:

| Name | Description |
|---|---|
| ``Dockerfile`` | Dockerfile used to build your application image. |
| ``Pipfile`` | Python requirements installed via [pipenv](https://pipenv.pypa.io) |
| ``Pipfile.lock`` | Locked requirements (generated on first install). |
| ``app_data`` | Application data such as vocabularies. |
| ``assets`` | Web assets (CSS, JavaScript, LESS, JSX templates) used in the Webpack build. |
| ``docker`` | Example configuration for NGINX and uWSGI. |
| ``docker-compose.full.yml`` | Example of a full infrastructure stack. |
| ``docker-compose.yml`` | Backend services needed for local development. |
| ``docker-services.yml`` | Common services for the Docker Compose files. |
| ``invenio.cfg`` | The Invenio application configuration. |
| ``logs`` | Log files. |
| ``static`` | Static files that need to be served as-is (e.g. images). |
| ``templates`` | Folder for your Jinja templates. |
| ``.invenio`` | Common file used by Invenio-CLI to be version controlled. |
| ``.invenio.private`` | Private file used by Invenio-CLI *not* to be version controlled. |

## Documentation

To learn how to configure, customize, deploy and much more, visit the [InvenioRDM Documentation](https://inveniordm.docs.cern.ch/).
