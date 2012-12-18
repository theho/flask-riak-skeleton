# flask-riak-skeleton
===================

Skeleton of a Python Flask project, combining flask, riak, and html5boilerplate/twitter bootstrap.

The intention is to create a skeleton for my own projects where I will be using riak, flask, and html5 as the standard framework.  Aim is to get to a good enough code base such that I could kick start any project development and deployment very quickly.

NOTE: This is not production ready, and is rather rough.

## Components (so far)
* flask
* initializr - html5boilerplate + twitter bootstrap.  See [initializr](http://www.initializr.com/)
* riak-python-client - official client
* schematics - using schematics for data models.  It supports json schema as well!

### Coming soon
* flask-login
* [python-geohash](https://github.com/simplegeo/python-geohash) - to support geospatial search in riak

### Not coming soon (as I have not yet decide what to use yet) but worth considering depending on individual projects
* flask-security - to support API token key type authentication/authorisation
* authentication - such as oauth 2.0 and openid
* [schematics](https://github.com/j2labs/schematics) - to model data into json
* wtf forms - so simple (and great)
* (auto) deployment scripts - for nginx (maybe fast cgi), VPS (linode)

> The source is rather rough and with very little comments.  However it should be self explanatory enough to get started.

## Setup
* set environment variable FLASK_ENV to either DEV, TEST or PROD
* run python runserver.py

## Protobuf
Download protobuf from http://code.google.com/p/protobuf/
tar -xvzf protobuf-2.4.1.tar.gz 
./configure
make
sudo make install
