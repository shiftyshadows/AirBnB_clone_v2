#!/usr/bin/env bash
#Script that sets up your web servers for the deployment of web_static
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
sudo cp index.html /data/web_static/releases/test
sudo chmod -R 755 /var/run/nginx /var/run/nginx /etc/nginx/site-available/

# Create symbolic link
symbolic_link="/data/web_static/current"
target_folder="/data/web_static/releases/test/"
sudo ln -sf "$target_folder" "$symbolic_link"

#Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

#Update the Nginx configuration
nginx_config="/etc/nginx/site-available/default"
sudo cp nginx_configuration "$nginx_config"
sudo nginx -s reload
sudo nginx -c "$nginx_config"

# Restart Nginx
sudo service nginx restart
