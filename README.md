# Jira-poc

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

Jira poc is a template to get started developing an atlassian-connect plugin using python and flask.

  - Handles JWT Authentication
  - Includes an API explorer when in development mode
  - Configured to run on Heroku

# New Features!

  - API Explorer
### Requirements
  - ngrok
  - herku cli
  - sql database

### Installation

Install the dependencies and devDependencies and start the server.

To run locally create the .env with the following environmental variables:
```
APP_SECRET=
APP_SETTINGS="config.DevelopmentConfig"
DATABASE_URL=
NGROK_URL=
```
Then on the command line
```sh
$ cd jira-poc
$ pip install -r requirements.txt
$ npm install
$ bower install
$ heroku local:run python manage_db.py db upgrade
```
