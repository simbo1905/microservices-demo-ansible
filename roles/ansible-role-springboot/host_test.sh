#!/bin/sh
HOSTNAME=$(hostname -f)
VARS=$1
if echo $VARS | grep $HOSTNAME; then
    echo HOSTNAME_LISTED
else 
    echo HOSTNAME_NOT_LISTED
fi
