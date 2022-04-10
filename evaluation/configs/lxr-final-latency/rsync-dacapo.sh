#!/usr/bin/env bash
set -x

rsync -azR --no-i-r -h --info=progress2 ~/./dacapo $1.moma:/home/wenyuz/