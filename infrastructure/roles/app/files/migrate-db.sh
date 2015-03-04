#!/bin/bash
cd /srv/checkout/app/
source ../ejrfvenv/bin/activate
python manage.py migrate questionnaire