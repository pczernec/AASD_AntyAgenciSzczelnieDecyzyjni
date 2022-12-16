#!/bin/bash

DATABASE=/data/prosody.sqlite

# touch $DATABASE
chown prosody:prosody /data
# chmod +r $DATABASE

CMD="$@"

su -s /bin/bash - prosody -c "prosody $CMD"
