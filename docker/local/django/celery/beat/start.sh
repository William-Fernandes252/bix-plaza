#!/bin/bash

set -o errexit
set -o nounset


rm -f './celerybeat.pid'
cd ./src
exec watchfiles --filter python celery.__main__.main --args '-A config beat -l INFO'
