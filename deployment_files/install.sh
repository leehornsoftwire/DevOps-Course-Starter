#!/bin/bash -e 
python3 -m venv venv
. venv/bin/activate
pip install --force-reinstall ~/todo_app/todo_app-0.1.0-py3-none-any.whl
pip install waitress
