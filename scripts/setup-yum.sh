#!/bin/bash -e
sudo yum install 'python3 >= 3.7'
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
source $HOME/.poetry/env
poetry install