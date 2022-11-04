#!/usr/bin/env fish
docker cp app_data invenio-web-ui-1:/opt/invenio/src
echo "entering docker container so you can run the command"
echo "invenio rdm-records fixtures && invenio rdm-records rebuild-index (it's on your clipboard)"
echo "invenio rdm-records fixtures && invenio rdm-records rebuild-index" | pbcopy
echo "but Eric why don't you just 'docker exec' the command in this script?"
echo "great question, it's because docker is a piece of shit & that inexplicably doesn't work"
docker exec -it invenio-web-ui-1 /bin/bash
