#!/bin/bash

USERS=("admin" "test")
PASSWORDS=("admin" "test")

for i in ${!USERS[@]}; do
    USER=${USERS[$i]}
    PASSWORD=${PASSWORDS[$i]}
    prosodyctl --config /config/prosody.cfg.lua register $USER xmpp_server $PASSWORD
    echo "Added $USER:$PASSWORD"
done
