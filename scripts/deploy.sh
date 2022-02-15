#!/bin/bash -e
poetry build
ansible-playbook -i ansible/inventory ansible/playbook.yml