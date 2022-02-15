#!/bin/bash -e
CURRENT_DIR=$(pwd)
TEMP=$(mktemp -d)
git clone file://$CURRENT_DIR --depth 1 $TEMP
scp -rp $TEMP $CONTROLLER:~/DevOps-Course-Starter
rm -rf $TEMP