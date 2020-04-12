#!/bin/bash


# 6 digit commit hash in GitHub
commit_hash=$1

repo_url=https://github.com/Beccall/yahtzee0.git
server_app_location=/home/ubuntu/becca/yahtzee
server_secret_key=/Users/rebeccawatkins/yahtzee/deploy_to_server/useast2_20171030.pem


ssh -tt -p 2222 -i $server_secret_key ubuntu@levell.xyz <<ENDSSH

# kill old server instance
kill $(ps aux | grep '[f]lask run' | awk '{print $2}')

# delete old folder
sudo rm -r $server_app_location

# clone/checkout hash
git clone $repo_url $server_app_location
cd $server_app_location
git checkout $commit_hash

# run requirements
pip3 install -r requirements.txt

# start server
export FLASK_APP=app/app.py
nohup flask run --host=0.0.0.0 --port=5000 &

# hack - flask run needs a little time
sleep 5
exit

ENDSSH