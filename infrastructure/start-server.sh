#!/bin/bash
#sudo initctl reload-configuration
#sudo restart djangoservice
echo "starting"
cd /srv/checkout
source ejrfvenv/bin/activate
pwd
touch ejrf.out
nohup python manage.py runserver 172.31.12.84:8000 >ejrf.err 2>ejrf.out & echo $1 > run.pid
echo "finishing"
