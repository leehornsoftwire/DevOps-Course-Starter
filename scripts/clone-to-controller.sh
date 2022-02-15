#!/bin/bash -e
if [ -z ${CONTROLLER+x} ]; then
    echo 'No $CONTROLLER variable set. Please set $CONTROLLER to the form user@host'
    exit 1
fi
CURRENT_DIR=$(pwd)
TEMP=$(mktemp -d)
git clone file://$CURRENT_DIR --depth 1 $TEMP
scp -rp $TEMP $CONTROLLER:~/DevOps-Course-Starter
rm -rf $TEMP