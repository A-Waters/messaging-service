# Messageing Service
This project was made by me, Alexander Waters, in about 4 hours for a current class I am 
currently taking in college. It is a simple Messaging program using a dedicated server, 
using packet framing, TCP sockets, JSONs, and 'utf-8' encodeing. Stylization of pep8


## How to run
The first thing your going to want to look at is the 'global_var.py' file. 
You can think of this as a config file. In there you will find the ports 
the server and client both operate on and and the host. 


## How to run the server
1. run 'server.py'


## How to run the client
1. run 'client.py'

## How to use (as client)
### Naming 
This will be the first thing you see after stating up the client. Here simply enter a name.

<b> Note: Nameing is only alpha numeric. </b>


### Sending Messages

#### <b>Broadcast: </b>

to preforma broadcast message simply type in the console and hit enter

#### <b>private: </b>

to preform a private message simply add @username in the begining of your message and hit enter

```@john how was your day?```

#### <b>Exit: </b>

to exit simply type ```!exit``` in chat and hit enter





### reciving messages

#### <b>Broadcast: </b>

Broadcast messages will be seen by everyone from one user.

joining the server will broadcast the message: ```Server: user has joined the Server```

leaving the server will broadcast the message: ```Server: user Has left the server```

#### <b>private: </b>

private messages will only be sent to one user and be seen in the folloing format  

```server \<Private>: message```

if the private message was not properly sent, an invalid message will return to the sender

```server <Private>: INVALID FORMAT```

#### <b>Exit: </b>

to exit simply type ```!exit``` in chat and hit enter

## How to use (as server):
1. run 'server.py'
2. watch terminal

data will be logged in the terminal only. data only cosist of users joining and leaving.





# things to note
1. This project does not contain compression or encryption of that data meaning that it is 
very easily vulnerable to attacks.

2. recomendation: dont use this as your primary messaing service.

3. there is a minor bug: if the cleint loses connection due to to the server reastating or 
closing suddenly the client program will not end. the solution is to restart the client.
