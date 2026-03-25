#!/bin/bash

# Step 1: Create new proxy
voms-proxy-init -voms cms -valid 192:00
PROXY_SRC=$(voms-proxy-info -path)

# Step 2: Destination (hard coded)
PROXY_DST="/afs/cern.ch/user/c/cgiordan/.x509up_u142167"

# Step 3: Copy
cp "$PROXY_SRC" "$PROXY_DST"
chmod 600 "$PROXY_DST"

echo "Proxy copied to: $PROXY_DST"