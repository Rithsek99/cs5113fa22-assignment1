Name: Rithsek Ngem
Run code: docker-compose up --build (must cd to code directory)

##Assumption:
 - docker-compose is the manager that allow containers communite 
 - each client has a presever message call, meaning the order is guarantee
 - clients (Bob and Alice) have a fair remote procedure call, no client is more priority than other
 - Server keep the port listen to any call and will terminate if no call make in some grace period. 

 Bugs expected: 
 - implementation of terminating Server when both clients guess correctly is not complete, when running program, Server might not exit or exit before all client finish. 
 - depend on the environment, running code might expect connection error if client's container start before server's (even though it works fine on local Mac machine with time.sleep() on client)
 - Server sometimes get called asynchronousely between two clients, it rare case that server announce both clients as winner. 
 
 Bugs and challenges while developing the project:
 - connection error occur as the clients' container start before server's 
 - connection error when trying to connect localhost instead server's port 
 - both functions (reply and tell_name) have to be called at the same time from clients to make sure server can output who is the winner correctly. 

##Walk through node.py

- class GuessingGame: interit guessing_game_pb2_grpc.GuessingGameServicer, that generate random secrete number implement both functions that can be called by clients
- function reply: take three paramaters(self, request, context). This function check if the guess of request is correct, return message feed (low, high and correct)
- function tell_name: this function announce the winner if they guess correctly and return Name message. 

- function server: this function create a server with a port and service GuessGame which keep listening for any call from clients

- function Bob: this the client function reprensenting Bob that make a local call from Bob container and grpc connectthis call to server via chanel and port. It keep guessing until correct. 

- function Alice: Another client represenint Alice which does the same thing as Bob function. 

##Demo.Gif:

when running the command above, the docker-compose will create three containers and each run the node.py file which call server, Bob and Alice repectively. Then each client will make remote process call to Server and ouput the number they guess and if they finish. After all clients guess correctly, all container stop. 


