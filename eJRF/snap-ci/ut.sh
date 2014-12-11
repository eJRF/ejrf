#!/bin/sh
set -e
source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
coverage run manage.py test
coveralls