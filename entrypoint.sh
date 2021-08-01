#!/bin/bash

if [ ! -f domains ]; then
  wget --no-check-certificate https://trustpositif.kominfo.go.id/assets/db/domains
fi
./generate-config.py -f ./domains -d /outdir -r ${REDIRECT:-127.0.1.1}
