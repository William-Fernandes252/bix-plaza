#!/bin/bash

set -o errexit
set -o nounset

cd ./src
exec watchfiles --filter python celery.__main__.main --args '-A config worker -l INFO'
