# Installing dependencies:
- Install XCode (includes python3 and more) through app store
- Install Mac Ports https://www.macports.org/install.php
- Download SQLLite https://www.sqlite.org/download.html . Unzip and place into your path.
- Install gunicorn: pip install gunicorn
- Install foreman: gem install foreman
- Install brew: /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
- Install httpie: brew install httpie
- Install hub, sqlite python libs: python3 -m pip install hug sqlite-utils greenstalk boto3
- Install haproxy: brew install haproxy
- Install beanstalkd: sudo port install beanstalkd
- Install Java runtime, https://java.com/en/download/
- Install AWS cli (right hand side of page), https://aws.amazon.com/cli/

# Initializing the project (do 1 time)
- Run this to initialize sqlite tables: ./bin/init.sh
    - Must run from the root of the twitter-clone directory.
    - This deletes the sqlite db and recreates it
- Run this to initialize dynamo tables: ./initawsdb.sh
- Initialize AWS cli by running (for using dynamo locally):  aws configure
    - Enter "AWS Access Key ID": fakeMyKeyId
    - Enter "AWS Secret Access Key": fakeSecretAccessKey
    - Enter "region name": us-west-2
    - Enter "output format": json

# Launching HAProxy.
The regular haproxy.cfg makes assumptions that are not valid for mac. This cut down config should work.

Run this command to start the proxy. It will start it in the background.
- sudo haproxy -f haproxy.simple-mac.cfg
You can verify it is running with:
- ps aux | grep haproxy 
- You should see a process listed with the command "haproxy -f haproxy.simple-mac.cfg"
- If you see multiple haproxys (obviously ignore the 'grep' entry, then kill the extra ones)

You'll need to restart haproxy if you make a change to the cfg file.
No good command for that? Find the process ID using `ps aux | grep haproxy`, then kill it with `sudo kill <the pid>`

# Launching foreman
- See the command at the bottom of the file named "Procfile"

# Launching beakstalkd
- This is managed by foreman. See the Procfile for the command if you want to run manually.

# Launching a local DynamoDB
- This is managed by foreman. See the Procfile for the command if you want to run manually.