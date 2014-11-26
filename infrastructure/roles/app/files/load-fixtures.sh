#!/bin/bash
cd /srv/checkout/
source ejrfvenv/bin/activate
python manage.py loaddata questionnaire/fixtures/questionnaire_core_2013.json
python manage.py loaddata questionnaire/fixtures/permission.json
python manage.py loaddata questionnaire/fixtures/organization_region_location.json
