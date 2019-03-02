#!/bin/bash

socat -d TCP4-LISTEN:7878,reuseaddr,fork,keepalive exec:./run.sh,pty
