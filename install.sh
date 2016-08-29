#!/bin/bash
sudo raspi-config
sudo apt-get update
sudo apt-get install python-dev -y
cd /home/pi/Documents/Teplica
sudo pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install Flask
pip install slackclient
pip install Rpi.GPIO
#git clone https://github.com/Hodov/py-spidev
cd /home/pi/Documents/Teplica/py-spidev
python setup.py install
cd /home/pi/Documents/Teplica/
#git clone https://github.com/Hodov/lib_nrf24
cp /home/pi/Documents/Teplica/lib_nrf24/lib_nrf24.py /home/pi/Documents/Teplica/
cd /home/pi/Documents/Teplica/
chmod +x start.sh


#Apache
#sudo apt-get install apache2 -y
#sudo apt-get install libapache2-mod-wsgi -y
#sudo a2enmod wsgi
#sudo cp /home/pi/Documents/greenhouse/Apache/greenhouse.conf /etc/apache2/sites-available/greenhouse.conf
#sudo mkdir /var/www/greenhouse
#cp /home/pi/Documents/greenhouse/Apache/greenhouse.wsgi /var/www/greenhouse/greenhouse.wsgi
#sudo a2ensite greenhouse
#sudo service apache2 restart

#FOR NGINX
#sudo apt-get install nginx -y
#sudo apt-get install libpcre3 libpcre3-dev
#pip install uwsgi


#uwsgi -s /tmp/uwsgi.sock --manage-script-name --mount /teplica=teplica:app
#uwsgi --virtualenv /home/pi/Documents/greenhouse/venv --enable-threads --catch-exception --socket 0.0.0.0:8000 --protocol=http -w testApp