#!/usr/bin/env bash
# Installs, configures, and starts the web server
SERVER_CONFIG="error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    # Default event-related configurations
}

http {
    server {
        listen 80;

        server_name _;
        index index.html index.htm;
        error_page 404 /404.html;
        add_header X-Served-By \$hostname;

        location / {
                root /var/www/html/;
                try_files \$uri \$uri/ =404;
        }

        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files \$uri \$uri/ =404;
        }

        if (\$request_filename ~ redirect_me) {
                rewrite ^ https://sketchfab.com/bluepeno/models permanent;
        }

        location = /404.html {
                root /var/www/error/;
                internal;
        }
    }
}"
HOME_PAGE="<!DOCTYPE html>
<html lang='en-US'>
        <head>
                <title>Home - AirBnB Clone</title>
        </head>
        <body>
                <h1>Welcome to AirBnB!</h1>
        <body>
</html>
"
# shellcheck disable=SC2230
if ! command -v nginx &> /dev/null
then
    sudo apt update
    sudo apt install -y nginx
fi

#Create folders
directories=(
    "/data/web_static/releases/test"
    "/data/web_static/shared"
    "/var/www/html"
    "/var/www/error"
)
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        sudo mkdir -p "$dir"
    else
        echo "Directory already exists: $dir"
    fi
done
sudo chmod -R 755 /var/www
echo 'Hello World!' | sudo tee /var/www/html/index.html
echo -e "Ceci n\x27est pas une page" | sudo tee /var/www/error/404.html

echo -e "$HOME_PAGE" | sudo tee /data/web_static/releases/test/index.html
[ -d /data/web_static/current ] && sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data
bash -c "echo -e '$SERVER_CONFIG' | sudo  tee /etc/nginx/sites-available/default"
sudo nginx -s stop
sudo nginx -c /etc/nginx/sites-available/default
