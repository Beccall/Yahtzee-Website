#!/bin/bash

# double click the file from Finder to run it

# run this if need to log into server:
# ssh -p 2222 -i /Users/rebeccawatkins/yahtzee/deploy_to_server/useast2_20171030.pem ubuntu@levell.xyz

# set up variables
local_app_location=/Users/rebeccawatkins/yahtzee/app
server_app_location=ubuntu@levell.xyz:/home/ubuntu/becca/yahtzee
server_key=/Users/rebeccawatkins/yahtzee/deploy_to_server/useast2_20171030.pem

# copy to server
scp -P 2222 -r -i $server_key $local_app_location $server_app_location
