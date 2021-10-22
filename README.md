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
3) SQLite3  
4) SQL  
5) Foreman  
6) HTTPie  
7) HAProxy

Install Technologies (Ubuntu)  
===============================
1) Foreman, httpie, sqlite3
   ``` $ sudo apt install --yes python3-pip ruby-foreman httpie sqlite3  ```
2) Hug and SQLite plugin for hug  
   ``` $ python3 -m pip install hug sqlite-utils ```  
3) HAProxy and Gunicorn servers
   ``` $ sudo apt install --yes haproxy gunicorn```

How to run project:
--------------------  
1) git clone ``` https://github.com/yash-b/twitter-clone.git ```      
2) To initialize the database
   - Launch the terminal and start the initializing file 
      ``` cd twitter-clone ```  
      ``` $ ./bin/init.sh```  
3) To start the microservices    
   - In the terminal type:  
      ``` $ foreman start -m users=1,timeline=3 -p 5000 ```  
4) Open a new terminal in the same directory and use the methods listed below;

Additional Files and Instructions
----------------------------------
- haproxy.cfg
   - This file needs to temporarily replace ``` /etc/haproxy/haproxy.cfg ``` for the HAProxy load balancer to create a single front-end at port 1936 for four instances of our microservices.
- Look at HAProxy load balancer's metrics and health of our microserver's instances.
   - This can be done by visiting ``` localhost:1935 ``` with username = user and password = password as credentials to access the site. 

Methods  
--------------  
- Sign up  
   - Signup function creates a new user, which requires arguments for username, password, email, and bio.  
      - Example  
      ``` $ http POST localhost:1936/signup/ username="ProfAvery" password="csufbackendclass" email="ProfAvery@gmail.com" ```  

- Verify User  
   -  verifyUser functon takes in the arguemnets of a username and password and authenticate it with the database.  
      - Example  
      ``` $ http GET localhost:1936/verifyUser username="rye" password="rye"```  

- Add Follower   
   - Follow function takes in the argument for yourUsername and followingUsername. This method cannot be called by an unauthorized user.  
      - Example  
      ``` $ http -a rye:rye POST localhost:1936/follow/ yourUsername="rye" followingUsername="thedeparted" ```  

- Get followers
   - get_following function takes in the argument of the username and displays everyone the user follows.  
      - Example  
      ``` $ http GET localhost:1936/get_following username="rye" ```  

- User Timeline  
   - user_timeline gets all of the posts of the signed in user. This method cannot be called by an unauthorized user.
      - Example  
      ``` $ http -a rye:rye GET localhost:1936/user_timeline username="rye" ```  

- Home Timeline  
   - home_timeline displays all of the users posts. This method cannot be called by an unauthorized user.  
      - Example  
      ``` $ http -a rye:rye GET localhost:1936/home_timeline username="rye" ```    

- Public Timeline  
   - public_timeline displays all the post in the database in reverse-chronological order.  
      - Example  
      ``` $ http GET localhost:1936/public_timeline ```    

- Create Post  
   - create_post function allows users to post a tweet to their timeline. It requires the username, post_text, and an optional repost arguments. This method can also be used to repost an older post. This method cannot be called by an unauthorized user.
      - Example (original post)
      ``` $ http -a rye:rye POST localhost:1936/create_post username="rye" post_text="Watching Love Island is probably the worst use of your time."```
      - Example (repost)
      ``` http -a rye:rye POST localhost:1936/create_post username="rye" post_text="She thought there'd be sufficient time if she hid her watch." repost=6 ```
