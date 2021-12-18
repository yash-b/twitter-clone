Twitter clone API - backend
===============================
This project contains two RESTful back-end microservices that are production ready using Hug routing, HTTP access and Hug's authentication, sqlite3 embedded database, Web Service Gateway Interface, Gunicorn, Foreman, and HAProxy HTTP load balancer.

Contributors of the group project:  
---------------------------------- 
1) Yash Bhambhani
2) Hanyue Zheng
3) Sijan Rijal  
  
Technologies      
===============================
1) Python  
2) Hug  
3) Beanstsalk
4) Greenstalk
5) Foreman  
6) HTTPie  
7) HAProxy
8) hey
9) Redis and redis-py
10) DynamoDB
11) Boto3

Install Technologies (Ubuntu)  
===============================
1) Foreman, httpie, beanstalkd, yes, redis, redis-py
   ``` $ sudo apt install --yes python3-pip ruby-foreman httpie beanstalkd hey redis python3-hiredis awscli python3-boto3```
2) Hug and greenstalk  
   ``` $ python3 -m pip install hug greenstalk ```  
3) HAProxy and Gunicorn servers
   ``` $ sudo apt install --yes haproxy gunicorn```

Additional Files and Instructions
----------------------------------
- haproxy.cfg
   - This file needs to temporarily replace ``` /etc/haproxy/haproxy.cfg ``` for the HAProxy load balancer to create a single front-end at port 1936 for four instances of our microservices.
   - Run ``` sudo service haproxy restart ``` on command line to start haproxy service with the new config file.
- Look at HAProxy load balancer's metrics and health of our microserver's instances.
   - This can be done by visiting ``` localhost:1935 ``` with username = user and password = password as credentials to access the site. 

How to run project:
--------------------  
1) git clone ``` https://github.com/yash-b/twitter-clone.git ```
   1.1) READ Additional Files and Instructions above!      
2) To initialize the database
   - Launch the terminal and start the initializing file 
      ``` cd twitter-clone ```  
      ``` $ ./bin/init.sh``` 
      ``` $ ./initawsdb.sh``` 
3) To start the microservices    
   - In the terminal type:  
      ``` $ foreman start -m users=1,timeline=3,likes=1 -p 5000 ```  
4) Open a new terminal and test the twitter clone-backend using the methods listed below.

Methods  
--------------  
Methods  
-------------- 
- Likes
To create a like for a post asynchronously, we use the the endpoint /likeasync and give a username and password

Example: http POST localhost:1936/likeasync username="rye" postid="1"

This would like the post if the post id is found in the database else it would send a notification using a worker.

- Posts
To create a post that contains link to polls, we use the endpoint /create/post_async like mentioned below:

Example: http POST localhost:1936/create/post_async username="rye", useremail="rye@gmail.com" post_text="Hello, world http://localhost:1936/results/1"

**Performance**
All the performance difference using synchronous and asynchronous documentation can be found under hey_performance_notes folder
