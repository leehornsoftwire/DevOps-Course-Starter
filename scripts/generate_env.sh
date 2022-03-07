#!/bin/bash -e
# docker compose requires env file to exist even though we don't use it for this command
touch deployment_files/.env
docker compose run generate-env