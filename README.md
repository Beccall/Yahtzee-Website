# Yahtzee

A web program for the game of Yahtzee.

## Getting Started

### Prerequisites
Program runs using `Python3.7`  
Required packages: `flask`, `flask_session`, `werkzeug`

### Install packages
`pip install -r requirements.txt`

### Run Application

**Deploy to server:** 
 
`deploy_to_server/deploy_to_server.sh <commit hash here>`

**Local:** 

export app to flask: `export FlASK_APP=app.py`  
 
turn on debug mode: `export FLASK_ENV=development` 
 
run app: `flask run`