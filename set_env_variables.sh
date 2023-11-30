#!/bin/zsh

# Set environmental variables
export HBNB_ENV='test'
export HBNB_TYPE_STORAGE='db'
export HBNB_MYSQL_USER='hbnb_dev'
export HBNB_MYSQL_PWD='hbnb_dev_pwd'
export HBNB_MYSQL_HOST='localhost'
export HBNB_MYSQL_DB='hbnb_dev_db'

# Additional variables if needed
# export OTHER_VARIABLE=value

echo "Environmental variables set:"
echo "HBNB_ENV=${HBNB_ENV}"
echo "HBNB_TYPE_STORAGE=${HBNB_TYPE_STORAGE}"
echo "HBNB_MYSQL_USER=${HBNB_MYSQL_USER}"
echo "HBNB_MYSQL_PWD=${HBNB_MYSQL_PWD}"
echo "HBNB_MYSQL_HOST=${HBNB_MYSQL_HOST}"
echo "HBNB_MYSQL_DB=${HBNB_MYSQL_DB}"
