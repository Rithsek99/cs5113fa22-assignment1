import random
from concurrent import futures
import logging
import socket
from time import sleep

import grpc
import guessing_game_pb2
import guessing_game_pb2_grpc

num = 100
class GuessingGame(guessing_game_pb2_grpc.GuessingGameServicer):
    global flag 
    def __init__(self):
        self.number = random.randint(1, num)
        print(f'Number is {self.number}')
        self.winner = 0
    def reply(self, request, context):
        if request.guess == self.number:
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
            self.winner += 1
        return guessing_game_pb2.Name(name=request.name)
    
def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=15))
    guessing_game_pb2_grpc.add_GuessingGameServicer_to_server(GuessingGame(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()
    
def Bob():
    guess = random.randint(1, num)
    with grpc.insecure_channel('server:50051') as channel:
        stub = guessing_game_pb2_grpc.GuessingGameStub(channel) # grpc send request to server
        guess = random.randint(1, num)
        while True:
            response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
            name = stub.tell_name(guessing_game_pb2.Name(name='Bob'))
            print(f"Guess:           {guess}")
            if response.feedback == 'high':
                guess = random.randint(1, guess-1)
            elif response.feedback == 'low':
                guess = random.randint(guess+1, num)
            else:
                print('I am done!')
                channel.close()
                exit(0)
def Alice():
    guess = random.randint(1, num)
    with grpc.insecure_channel('server:50051') as channel:
        stub = guessing_game_pb2_grpc.GuessingGameStub(channel) # grpc send request to server
        while True:
            response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
            name = stub.tell_name(guessing_game_pb2.Name(name='Alice'))
            print(f"Guess:           {guess}")
            if response.feedback == 'high':
                guess = random.randint(1, guess-1)
            elif response.feedback == 'low':
                guess = random.randint(guess+1, num)
            else:
                print('I am done!')
                channel.close()
                exit(0)
# command line main
if __name__ == '__main__':
    logging.basicConfig()
    if (socket.gethostname() == 'server'):
        print(f'{socket.gethostname()} has started!')
        server()
    elif (socket.gethostname() == 'alice'):
        Alice()
    else:
        Bob()

