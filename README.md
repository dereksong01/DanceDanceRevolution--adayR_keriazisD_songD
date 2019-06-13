
# DanceDanceRevolution--adayR_keriazisD_songD

Ryan Aday- Server
Derek Song- Frontend
Daniel Keriazis- Backend

Watch our video demo here: https://youtu.be/bXy-10tEfa4

## Dependencies
- An Ubuntu 18.04 server
- Apache 2
- mod_wsgi
- Flask


To install all of these, run:
```bash
$ sudo apt update
$ sudo apt install apache2
$ sudo ufw app list
$ sudo ufw allow 'Apache'
$ sudo ufw status
$ sudo systemctl status apache2
```
Check that the Apache 2 server is running by typing in your IP address.

```bash
$ sudo apt-get install libapache2-mod-wsgi python-dev
$ sudo a2enmod wsgi
$ cd /var/www
$ sudo mkdir FlaskApp
$ cd FlaskApp
$ git clone https://github.com/dereksong01/DanceDanceRevolution--adayR_keriazisD_songD.git
$ mv DanceDanceRevolution--adayR_keriazisD_songD FlaskApp
$ sudo nano __init__.py
```

Make sure you add the host number in your __init__.py file:

```
if __name__ == "__main__":
    app.debug = False
    app.run(host="0.0.0.0")
```

```bash
$ sudo /var/www/FlaskApp/FlaskApp
$ apt-get install python-pip3
$ sudo pip3 install virtualenv
$ sudo virtualenv venv
$ source venv/bin/activate
$ sudo pip3 install Flask
$ sudo python3 __init__.py
$ sudo nano /etc/apache2/sites-available/FlaskApp.conf
```
Make sure your .conf file is in this format:

```
<VirtualHost *:80>
		ServerName ip_address
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```
```bash
$ sudo a2ensite FlaskApp
$ cd /var/www/FlaskApp
$ sudo nano flaskapp.wsgi
```

Make sure the .wsgi format is like this:
```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
```
```bash
$ sudo service apache2 restart
```

Then type in your IP address:5000 to access your website.

## Running our Project
Once all of the dependencies have been installed and the git repo has been updated, run these commands after the server is running:
```bash
# while venv is active
$ cd /var/www/FlaskApp/FlaskApp
$ git pull
$ source venv/bin/activate
$ sudo python3 __init__.py

```
##Functionality
WIP
Basic multiplayer works (people can join and create rooms, can both draw)
Game for local multiplayer for now, have to manually choose what to draw.
Will Try to make that part of website by Sat.  
PM and Daniel were AFK during this, hopefully they come back to fix it.
