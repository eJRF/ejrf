#!/bin/bash
echo "starting script"
cd /srv/checkout
source ejrfvenv/bin/activate
python manage.py runserver 0.0.0.0:8000
