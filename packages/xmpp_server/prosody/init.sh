#!/bin/bash

add_user(){
    local username=$1
    local password=$2

    prosodyctl --config /config/prosody.cfg.lua register $username xmpp_server $password \
        && return 0

    return 1
}

# Fix DB permissions
DATABASE=/data/prosody.sqlite

# chown prosody:prosody $DATABASE
chmod +r $DATABASE

# Add basic users
USERS=("admin" "test")
PASSWORDS=("admin" "test")

for i in ${!USERS[@]}; do
    USER=${USERS[$i]}
    PASSWORD=${PASSWORDS[$i]}

    add_user $USER $PASSWORD && echo "Added $USER:$PASSWORD"
done

# Add agent users, since allow_registration=true in Prosody doesn't work :/
for i in {0..127}; do
    USER="agent_$i"
    PASSWORD="agent_$i"

    add_user $USER $PASSWORD && echo "Added $USER:$PASSWORD"
done
