#!/usr/bin/puppet apply
# AirBnB clone web server setup and configuration
exec { 'apt-get-update':
  command => '/usr/bin/apt-get update',
  path    => '/usr/bin:/usr/sbin:/bin',
}

exec { 'remove-current':
  command => 'sudo rm -rf /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
}

package { 'nginx':
  ensure  => installed,
  require => Exec['apt-get-update'],
}

file { '/var/www':
  ensure  => directory,
  mode    => '0755',
  recurse => true,
  require => Package['nginx'],
}

file { '/var/www/html/index.html':
  content => 'Hello, World!',
  require => File['/var/www'],
}

file { '/var/www/error/404.html':
  content => "Ceci n'est pas une page",
  require => File['/var/www'],
}

exec { 'make-static-files-folder':
  command => 'sudo mkdir -p /data/web_static/releases/test /data/web_static/shared',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Package['nginx'],
}

file { '/data/web_static/releases/test/index.html':
  content =>
"<!DOCTYPE html>
<html lang='en-US'>
	<head>
		<title>Home - AirBnB Clone</title>
	</head>
	<body>
		<h1>Welcome to AirBnB!</h1>
	<body>
</html>
",
  replace => true,
  require => Exec['make-static-files-folder'],
}

exec { 'link-static-files':
  command => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => [
    Exec['remove-current'],
    File['/data/web_static/releases/test/index.html'],
  ],
}

exec { 'change-data-owner':
  command => 'chown -hR ubuntu:ubuntu /data',
  path    => '/usr/bin:/usr/sbin:/bin',
  require => Exec['link-static-files'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => present,
  mode    => '0644',
  content =>
"error_log  /var/log/nginx/error.log notice;
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
        add_header X-Served-By $hostname;

        location / {
                root /var/www/html/;
                try_files $uri $uri/ =404;
        }

        location /hbnb_static/ {
                alias /data/web_static/current/;
                try_files $uri $uri/ =404;
        }

        if ($request_filename ~ redirect_me) {
                rewrite ^ https://sketchfab.com/bluepeno/models permanent;
        }

        location = /404.html {
                root /var/www/error/;
                internal;
        }
    }
}",
  require => [
    Package['nginx'],
    File['/var/www/html/index.html'],
    File['/var/www/error/404.html'],
    Exec['change-data-owner']
  ],
}

exec { 'start_nginx':
  command => 'nginx -c /etc/nginx/sites-available/default',
  path    => '/usr/sbin:/usr/bin:/bin',
  require => [
    Package['nginx'],
    File['/data/web_static/releases/test/index.html'],
  ],
  unless  => 'ps -ef | grep nginx | grep -v grep | grep -q "nginx -c /etc/nginx/sites-available/default"',

}

exec { 'reload_nginx':
  command => 'nginx -s reload',
  path    => '/usr/sbin:/usr/bin:/bin',
  refreshonly => true,
}

Exec['reload-nginx']
