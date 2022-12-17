#!/bin/bash

/config/init.sh &

CMD="$@"

su -s /bin/bash - prosody -c "prosody $CMD"
