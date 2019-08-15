# Central Dogma API

## Description

This is the backend service API for the Central Dogma project
Its purpose is to collect and store game completion information and question
responses from the users that is sent from the web frontend.

## Installation and Requirements

This is a Flask application, you will need
  
  - Flask, flask_cors, flask_jwt_extended
  - MySQLdb
  - argon2-cffi

Due to our server infrastructure this should be run on Python 2, even though
it should in principle  be possible to run in a Python 3 environment

Please use the included cdogma.sql to populate a MySQL database
and edit cdogma/settings.cfg to match your database settings.

## Running

If you run this on your development machine it should be possible
to run the backend by running 

```
  $ ./run.sh
```

The application will then be available under localhost:5000

## Example application

In the example folder is a demo to show how to use the included Javscript
module in order to connect to the API


