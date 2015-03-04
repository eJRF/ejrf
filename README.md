Installation on a developer box
-----------------------
* Postgres should be running and after cloning adjust localsettings.py accordingly for db setup

###Git

        git clone https://github.com/eJRF/ejrf.git
### Setup the devlopment evironment
        mkvirtualenv destination-path-for-the-virtualenv/ejrf
        
		 source path-to-virtualenv/bin/activate
		  
        pip install -r pip-requirements.txt
        
        npm install #install javscript dependencies (mainly for js tests)

### Run Tests
        python manage.py test #unit tests
        python manage.py harvest #functional tests
        
        ./test.js # javascript tests
### Run The application
        python manage.py syncdb --noinput

        python manage.py migrate
        python manage.py createsuperuser
        
		 ./manage.py loaddata questionnaire/fixtures/2013-core-jrf.json

        python manage.py runserver


Installation in a vagrant box.
-----------------------------
## Requirements

   * [Ansible] (https://github.com/ansible/ansible)
   * [Vagrant] (www.vagrantup.com/downloads.html)
   * [ubuntu-14.box image](https://www.dropbox.com/s/gw89y2vcix5cnj9/ubuntu-14.04.box?dl=0)
   * [Virtualbox] (https://www.virtualbox.org/wiki/Downloads)
   * A stable internet conncetion.


## Steps
		git clone https://github.com/eJRF/ejrf.git
		cd ejrf
		vagrant plugin install vagrant-cachier
		vagrant up
If you get any issues due to say an internet connection, you can resume the provisioning proccess by running:

      vagrant provsion

Now you can access the application at the private IP address of the vagrant box on port 80.

       http://192.168.50.4



###Filenaming convention:
* for tests: test_[[OBJECT]]_[[ACTION]].py
e.g: test_location_form.py, test_location_model.py, test_location_views.py

====

[![Build Status](https://snap-ci.com/nugDMDbuoqEhkrLFarm6FuwsT60surg6vsh0z4B8KT4/build_image)](https://snap-ci.com/projects/eJRF/ejrf/build_history)
[![Coverage Status](https://coveralls.io/repos/eJRF/ejrf/badge.png?branch=master)](https://coveralls.io/r/eJRF/ejrf?branch=master)
