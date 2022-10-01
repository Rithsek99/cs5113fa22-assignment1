import socket
import random
from concurrent import futures
import logging
from time import sleep

import grpc
import guessing_game_pb2
import guessing_game_pb2_grpc

class GuessingGame(guessing_game_pb2_grpc.GuessingGameServicer):
    def __init__(self):
        self.number = random.randint(1, 4)
        self.name = ''
        self.winner = 0
    def reply(self, request, context):
        print(f'GuessingGame.GuessNumber called with {request}')
        if request.guess == self.number:
            self.name = request.name
            self.winner += 1
            return guessing_game_pb2.Feedback(
                feedback='You guessed correctly!')
        elif request.guess < self.number:
            return guessing_game_pb2.Feedback(
                feedback='low')
        else:
            return guessing_game_pb2.Feedback(
                feedback='high')  
    def tell_name(self, request, context):
        if(self.winner == 1):
            print(f'{request.name} won the game!')
        return guessing_game_pb2.Name(name=request.name)
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    guessing_game_pb2_grpc.add_GuessingGameServicer_to_server(GuessingGame(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    # try:
    #     while True:
    #         time.sleep(100)
    # except:
    #     server.stop(0)
    
    server.wait_for_termination()
    
def Bob():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    sleep(50)
    guess = random.randint(1, 4)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = guessing_game_pb2_grpc.GuessingGameStub(channel) # grpc send request to server
        guess = random.randint(1, 4)
        while True:
            response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
            print(f"Bob's guess: {guess}")
            if response.feedback == 'high':
                guess = random.randint(1, guess)
            elif response.feedback == 'low':
                guess = random.randint(guess, 4)
            else:
                print('I am done!')
                channel.close()
                exit(0)
def Alice():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    sleep(50)
    guess = random.randint(1, 4)
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = guessing_game_pb2_grpc.GuessingGameStub(channel) # grpc send request to server
        while True:
            response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
            print(f"Alice's guess: {guess}")
            if response.feedback == 'high':
                guess = random.randint(1, guess)
            elif response.feedback == 'low':
                guess = random.randint(guess, 4)
            else:
                print('I am done!')
                channel.close()
                exit(0)
# command line main
if __name__ == '__main__':
    logging.basicConfig()
    
    print(socket.gethostname())
    if (socket.gethostname() == 'server'):
        server()
    elif (socket.gethostname() == 'alice'):
        Alice()
    else:
        Bob()
        
# how do we make sure that the server is started before the client?
# how do we stop the server after the client is done?
# how do we stop client?
        

