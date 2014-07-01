#/usr/bin/bash
sudo apt-get install python-dev libmysqlclient-dev mysql-server python-pip && \
sudo pip install virtualenv && \

## Change to directory location of this script
cd "$(dirname "$0")"
rm -R ./venv/
virtualenv venv && \
source venv/bin/activate && \
pip install -r requirements.txt

