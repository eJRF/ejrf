#!/bin/bash
cd /srv/checkout/
source ejrfvenv/bin/activate
python manage.py questionnaire migrate
