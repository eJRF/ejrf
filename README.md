Installation
------------
* Postgres should be running and after cloning adjust localsettings.py accordingly for db setup 

##Git

        git clone https://github.com/eJRF/ejrf.git

        cd ejrf

        mkvirtualenv ejrf

        pip install -r pip-requirements.txt

        python manage.py syncdb --noinput

        python manage.py migrate

        python manage.py runserver
        
==

* run test and harvest

Done!! you're good to go :)

Filenaming convention:
* for tests: test_[[OBJECT]]_[[ACTION]].py
e.g: test_location_form.py, test_location_model.py, test_location_views.py

====

[![Build Status](https://snap-ci.com/nugDMDbuoqEhkrLFarm6FuwsT60surg6vsh0z4B8KT4/build_image)](https://snap-ci.com/projects/eJRF/ejrf/build_history)
[![Coverage Status](https://coveralls.io/repos/eJRF/ejrf/badge.png?branch=master)](https://coveralls.io/r/eJRF/ejrf?branch=master)