#!/bin/sh
echo "starting functional tests"
source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
echo "setup for tests done"
./manage.py harvest --tag=-WIP -v 2 --with-xunit --xunit-file=test-results.xml
echo "functional test complete"
