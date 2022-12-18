#!/bin/bash

add_user(){
    local username=$1
    local password=$2

    prosodyctl --config /config/prosody.cfg.lua register $username xmpp_server $password \
        && return 0

    return 1
}

# Add basic users
USERS=("admin" "test" "agent")
PASSWORDS=("admin" "test" "agent")

for i in ${!USERS[@]}; do
    USER=${USERS[$i]}
    PASSWORD=${PASSWORDS[$i]}

    add_user $USER $PASSWORD && echo "Added $USER:$PASSWORD"
done

# Fix DB permissions
chmod +r /data/prosody.sqlite
