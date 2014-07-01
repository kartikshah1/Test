# Creating tables and populating them.
python manage.py syncdb
python manage.py migrate
mysql -u root -p elearning_academy < server_setup.sql

