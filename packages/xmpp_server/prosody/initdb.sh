#!/bin/bash

USERS=("admin" "test" "agent0" "agent1" "agent2" "agent3" "agent4" "agent5" "agent6" "agent7" "agent8" "agent9" "agent10" "agent11" "agent12")
PASSWORDS=("admin" "test" "agent0" "agent1" "agent2" "agent3" "agent4" "agent5" "agent6" "agent7" "agent8" "agent9" "agent10" "agent11" "agent12")

for i in ${!USERS[@]}; do
    USER=${USERS[$i]}
    PASSWORD=${PASSWORDS[$i]}

    prosodyctl --config /config/prosody.cfg.lua register $USER xmpp_server $PASSWORD \
        && echo "Added $USER:$PASSWORD"
done

