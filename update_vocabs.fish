#!/usr/bin/env fish
# waiting to have this add_to_fixture cmd so we don't have to rebuild fixtures every time they change
# https://github.com/inveniosoftware/invenio-rdm-records/pull/1303
docker cp app_data invenio-web-ui-1:/opt/invenio/src
echo "entering docker container so you can run the command"
echo "invenio rdm-records fixtures && invenio rdm-records rebuild-index (it's on your clipboard)"
echo "invenio rdm-records fixtures && invenio rdm-records rebuild-index" | pbcopy
# `docker run` the command above does not work for some reason, env vars?
docker exec -it invenio-web-ui-1 /bin/bash
