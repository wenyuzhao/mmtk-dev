#!/bin/bash

echo Initializing running directory.

if [[ ! -f  bin/RunConfig.pm ]]; then
  echo Creating RunConfig.pm from sample
  cp bin/RunConfig.pm.sample bin/RunConfig.pm
fi
