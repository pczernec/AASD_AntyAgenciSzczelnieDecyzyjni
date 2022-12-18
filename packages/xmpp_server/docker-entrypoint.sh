#!/bin/bash

chown prosody:prosody /data

/config/init.sh &

CMD="$@"

su -s /bin/bash - prosody -c "prosody $CMD"
