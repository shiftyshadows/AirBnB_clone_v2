#!/usr/bin/puppet apply
# AirBnB clone web server setup and configuration
# Define class for nginx installation and configuration
class web_server {
    # Install nginx package
    package { 'nginx':
        ensure => installed,
    }

    # Define nginx service
    service { 'nginx':
        ensure  => running,
        enable  => true,
        require => Package['nginx'],
    }

    # Define nginx server configuration
    file { '/etc/nginx/sites-available/default':
        ensure  => file,
        content => "error_log  /var/log/nginx/error.log notice;
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
}",
        require => Package['nginx'],
        notify  => Service['nginx'],
    }

    # Create directories
    $directories = [
        '/data/web_static/releases/test',
        '/data/web_static/shared',
        '/var/www/html',
        '/var/www/error',
    ]

    # Ensure directories are present
    ensure_resource('file', $directories, { ensure => directory })

    # Set permissions
    file { '/var/www':
        ensure  => directory,
        mode    => '0755',
        recurse => true,
        owner   => 'ubuntu',
        group   => 'ubuntu',
    }

    # Define default index.html
    file { '/var/www/html/index.html':
        ensure  => file,
        content => 'Hello World!',
        owner   => 'ubuntu',
        group   => 'ubuntu',
    }

    # Define 404.html
    file { '/var/www/error/404.html':
        ensure  => file,
        content => "Ceci n'est pas une page",
        owner   => 'ubuntu',
        group   => 'ubuntu',
    }

    # Define symbolic link for static content
    file { '/data/web_static/current':
        ensure => link,
        target => '/data/web_static/releases/test',
        owner  => 'ubuntu',
        group  => 'ubuntu',
    }

    # Define homepage index.html
    file { '/data/web_static/releases/test/index.html':
        ensure  => file,
        content => "<!DOCTYPE html>
<html lang='en-US'>
        <head>
                <title>Home - AirBnB Clone</title>
        </head>
        <body>
                <h1>Welcome to AirBnB!</h1>
        <body>
</html>",
        owner   => 'ubuntu',
        group   => 'ubuntu',
        require => File['/data/web_static/current'],
    }
}

# Apply web_server class
include web_server
