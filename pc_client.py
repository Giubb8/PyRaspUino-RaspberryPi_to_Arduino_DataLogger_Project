import sys
import hashlib as hl
from enum import Enum
import socket


class CODES(Enum):
    OK_CODE = 400
    ERROR_CODE = -300


class Profile:
    def __init__(self,username,hashed_password):
        self.username=username
        self.hashed_password=hashed_password

    def check_hash(self,hash_to_test)->bool:
        if(hash_to_test==self.hashed_password):
            return True
        else:
            return False

def login(connection):
    sha256 = hl.sha256()
    username = input("USERNAME\n")
    sha256.update(input("PASSWORD\n").encode('utf-8'))
    password = sha256.hexdigest()
    session_profile = Profile(username, password)

    #send profile info to the server
    connection.send(username.encode("utf-8"))
    connection.send(password.encode("utf-8"))
    #receive reply from server to see if im logged or not
    server_reply=connection.recv(1024).decode()

    #checking the reply
    if(server_reply==str(CODES.ERROR_CODE.value)):
        print("PASSWORD DO NOT MATCH,RETRY")
        login(connection)
    else:
        return session_profile

def connect_to_raspberry():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect( ("127.0.0.1",5000))
    return s

def setup():
    with open("./setup.txt","r") as setupfile:
        pass

if __name__=='__main__':
    setup_parameters=setup()
    connection=connect_to_raspberry()
    session_profile=login(connection)






