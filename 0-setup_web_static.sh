#!/usr/bin/env bash
#Script that sets up your web servers for the deployment of web_static

SERVER_CONFIG="server {
    listen 80;
    server_name 100.26.53.148;

    location / {
        root /var/www/html/;
        index index.html;
    }

    location /redirect_me {
        return 301 https://www.example.com/;
    }

    location /hbnb_static/ {
        alias /data/web_static/current/;
        autoindex off;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /var/www/html;
        internal;
    }
}
"

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
    "/etc/nginx/site-available/"
)
for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        sudo mkdir -p "$dir"
    else
        echo "Directory already exists: $dir"
    fi
done
echo -e '$HTML_HOME' | tee /data/web_static/releases/test/index.html
sudo chmod -R 755 /var/run/nginx /var/run/nginx /etc/nginx/site-available/

# Create symbolic link
symbolic_link="/data/web_static/current"
target_folder="/data/web_static/releases/test/"
sudo ln -sf "$target_folder" "$symbolic_link"

#Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

#Update the Nginx configuration
nginx_config="/etc/nginx/site-available/default"
echo -e '$SERVER_CONFIG'| sudo tee "$nginx_config"
#sudo nginx -c "$nginx_config"
#sudo nginx -s reload

if [ "$(pgrep -c nginx)" -le 0 ]; then
	service nginx start
else
	service nginx restart
fi

# Restart Nginx
sudo service nginx restart
