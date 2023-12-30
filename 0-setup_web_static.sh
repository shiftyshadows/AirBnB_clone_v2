#!/usr/bin/env bash
#Script that sets up your web servers for the deployment of web_static

SERVER_CONFIG="user nginx;
worker_processes auto;

error_log /var/log/nginx/error.log notice;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;    # Default event-related configurations
}

http {
    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        server_name _;
        index index.html index.htm;
        error_page 404 /404.html;
        add_header X-Served-By \$hostname;

        location / {
            root /var/www/html/;
            try_files \$uri \$uri/ =404;
        }

        location /redirect_me {
            return 301 https://www.example.com/;
        }

        location /hbnb_static/ {
            alias /data/web_static/current/;
            try_files \$uri \$uri/ =404;
        }

        location = /404.html {
            root /var/www/html;
            internal;
        }
    }
}"

HTML_HOME="<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Hello World!</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
"

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    # Update source list
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] https://nginx.org/packages/ubuntu/ focal nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
    echo "deb-src [arch=amd64 signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] https://nginx.org/packages/ubuntu/ focal nginx" | sudo tee -a /etc/apt/sources.list.d/nginx.list
    # Recieve signing keys
    sudo gpg --keyserver keyserver.ubuntu.com --recv-keys ABF5BD827BD9BF62
    sudo gpg --export --armor ABF5BD827BD9BF62 | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg
    # Update package list
    sudo apt-get update
    # Install nginx
    sudo apt-get install -y nginx
fi

#Create folders
directories=(
    "/data/web_static/releases/test"
    "/data/web_static/shared"
    "/var/run/nginx"
    "/var/www/html"
    "/var/www/error"
    "/etc/nginx/site-available/"
)
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        sudo mkdir -p "$dir"
    else
        echo "Directory already exists: $dir"
    fi
done
echo -e "$HTML_HOME" | tee /data/web_static/releases/test/index.html > /dev/null
sudo chmod -R 755 /var/www /var/run/nginx /etc/nginx/site-available/

# Create symbolic link
symbolic_link="/data/web_static/current"
target_folder="/data/web_static/releases/test/"
sudo ln -sf "$target_folder" "$symbolic_link"

#Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

#Update the Nginx configuration
nginx_config="/etc/nginx/site-available/default"
echo -e "$SERVER_CONFIG"| sudo tee "$nginx_config" > /dev/null
sudo nginx -c "$nginx_config" -s reload

# Restart Nginx
sudo service nginx restart
