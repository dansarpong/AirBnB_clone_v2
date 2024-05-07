#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/releases/test/ /data/web_static/shared/
echo "This is a test" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -Rh ubuntu:ubuntu /data/
new_conf="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n}"
sudo sed -i "s|^\}$|${new_conf}|g" /etc/nginx/sites-available/default
sudo service nginx restart
