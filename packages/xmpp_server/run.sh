#!/bin/bash

chown ubuntu:ubuntu /data

su - ubuntu -c 'prosody --config /config/prosody.cfg.lua'
