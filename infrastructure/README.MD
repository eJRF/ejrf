eJRF Server Confuguration and deployment
---
###Requirements

* [Ansible] (https://github.com/ansible/ansible)
* A stable internet conncetion.

###Steps
    git clone https://github.com/eJRF/ejrf.git
    cd ejrf
    cp hosts.ini.example hosts.ini

 edit `hosts.ini` appropriately, then run:

    ansible-playbook -i hosts.ini --private-key=~/path/to-your-private-key infrastructure/server.yml -vv

Note
---
If you are provisioning a vagrant box, please refer to the general project [README] (https://github.com/eJRF/ejrf/blob/master/README.md)
