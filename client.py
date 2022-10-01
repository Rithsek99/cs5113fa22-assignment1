import socket
import random
from concurrent import futures
import logging

import grpc
import guessing_game_pb2
import guessing_game_pb2_grpc

def Bob():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = guessing_game_pb2_grpc.GuessingGameStub(channel) # grpc send request to server
        guess = random.randint(1, 10)
        while True:
            try:
                response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
                print(f"Bob's guess: {guess}")
                if response.feedback == 'high':
                    guess = random.randint(1, guess)
                elif response.feedback == 'low':
                    guess = random.randint(guess, 10)
                else:
                    print('I am done!')
                    channel.close()
                    exit(0)
            except grpc.RpcError as e:
                response = stub.reply(guessing_game_pb2.Guess(guess=guess)) # grpc send request to server
                
            #response_name = stub.tell_name(guessing_game_pb2.Name(name='Bob'))
            #if response_name.name != 'Bob':
            #   print('I am done!')
            #   channel.close()
            #   exit(0)
               
if __name__ == '__main__':
    logging.basicConfig()
    Bob()