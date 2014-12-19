#!/bin/sh

source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py

echo "booting sauce connect tunnel"

CONNECT_URL="https://saucelabs.com/downloads/sc-4.3.5-linux.tar.gz"
CONNECT_DIR="/tmp/sauce-connect-$RANDOM"
CONNECT_DOWNLOAD="Sauce_Connect.zip"
READY_FILE="connect-ready-$RANDOM"

mkdir -p $CONNECT_DIR
cd $CONNECT_DIR
curl -L $CONNECT_URL > $CONNECT_DOWNLOAD
tar -xvzf $CONNECT_DOWNLOAD
rm $CONNECT_DOWNLOAD

sc-4.3.5-linux/bin/sc -u $SAUCE_USERNAME -k $SAUCE_ACCESS_KEY --readyfile $READY_FILE &

while [ ! -f $READY_FILE ]; do
  sleep .5
done

echo "sauce connect tunnel established"

cd -

echo "starting functional tests"
source ../ejrf_env/bin/activate
cp eJRF/snap-ci/snap-settings.py eJRF/localsettings.py
echo "setup for tests done"

./manage.py harvest -t-sauce --tag=-WIP --tag=-Upload --tag=-IE