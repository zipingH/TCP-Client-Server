# TCP Centralized Client-Server Network 

# Name: Ziping Huang (916155583)
# General description of the project:
In this project, I have created a MultiThreading TCP Server with sockets which can handle multiple connections from the client. The client will be prompted to provide a name to the server and the connection will be established. Once the client is connected to the server, the server will send a menu and the client will send back the options that is selected which will be processed by the server and send back to the client. Overall, this project shows what a TCP Network is like by sending and receving data between server and client.

# External Python modules/libraries: 
No external libraries was used. Used import sys to append sys path. So in client_handler.py class, need to change and append sys.path to the path of the client folder that contains menu.py

# Python version:
* python 3.81
* To run server: python3 server.py 
* To run client: python3 client.py

# Attach screenshots or videos to this file to ilustrate how your program works for all the options in the menu:
 # When server is listening/running:
   * Make sure to run to a client then run another client, if running more than one client at the same time, there are bugs.
   ![Server is listening](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/severlisten.png)
  
 # 1. Option 1:
   * Option 1 will give a list of clients that are connected to the server.
   ![Option1](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option1.png)
      
 # 2. Option2:
   * Option 2 will let you send message to another client by sending to the server first, then server will send the message to
   * the id of that client.
   
   ![Option2](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option2.png)
  
 # 3. Option3:
   * Option 3 will let you check your unreaded messages you received from another client. If you checked/read your unreaded message, the unreaded messages will be cleared.
   ![Option3](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option3.png)
 
 # 4. Option4:
   * Option 4 will create a room id but the owner of the room will still need to join room with option 5.
   ![Option4](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option4.png)
 
 # 5. Option5:
  * Join a chat room with exisiting room id.
  ![Option5](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option5.png)
  
 # 6. Option6:
  * Disconnect from the server and your information will be removed from the server.
  ![Option6](https://github.com/sfsu-joseo/csc645-computer-networks-spring-2020-myreplica/blob/master/Projects/TCP-Client-Server-Centralized-Network/screenshots/option6.png)
 

# Challenges:
* There are many challenges I had to deal with in this project since working with sockets is hard and especially since im still new with python and sockets.

* One of the problem I had to deal with is making the server able to handle multiple clients by threading and sometimes one of the client just hangs. I was able to kind of resolve this issue by checking where I put my locks and check if the server is sending the data to the client or vice versa because if no data has been sent, the client will continue to hang and try to receive that data which is why I need to make sure there is an acknowledge being sent back. There is also a problem when my clients are trying to connect to the server at the same time so it will only work when a client is connected then connect another client.

* For the chat room, I wasn't sure how to implement it but for option 4, I just send the server a room id and for option 5 if that room id is exist, I made it that the server and clients are sending data back to each other. I had to use thread to make a live chat so that the client can send and receive data at the same time. Overall, there are issue with the chat room since I didn't really know if I have to make a new connection to create a chat room.


