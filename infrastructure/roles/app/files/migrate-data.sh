#!/bin/bash
cd /srv/checkout/
source ejrfvenv/bin/activate
python manage.py questionnaire migrate 0050
python manage.py questionnaire migrate