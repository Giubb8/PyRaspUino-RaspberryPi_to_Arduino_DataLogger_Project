import socket
import concurrent.futures
from enum import Enum

#Enum for communication
class CODES(Enum):
    OK_CODE="400"
    ERROR_CODE="-300"

#Class that identify the user trying to connect to the server
class Profile:
    def __init__(self,username,hashed_password):
        self.username=username
        self.hashed_password=hashed_password

    def check_hash(self,hash_to_test)->bool:
        if(hash_to_test==self.hashed_password):
            return True
        else:
            return False

#create the socket connection and return it
def create_socket():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',5000))
    s.listen(3)
    return s

#function used to login the user,check tha hashed password with the one parsed from the file,given as argument
def login(hashpass,connection):
    username = connection.recv(1024).decode()
    password = connection.recv(1024).decode()
    print(f"USER {username} PASSWORD {password}")

    if(hashpass==password):
        print("PASSWORD MATCH")
        connection.send(bytes(CODES.OK_CODE.value,"utf-8"))
        print("mandato")
    else:
        print("PASSWORD DO NOT MATCH TRY AGAIN")
        connection.send(bytes(CODES.ERROR_CODE.value,"utf-8"))
        login(hashpass,connection)



def mesure_temp_and_hum():
    pass

def see_th_measurement():
    pass


def show_txt():
    pass


def handle_connection(connection,address,hashpass):
    print('Connected to', address)
    login(hashpass,connection)
    input=""
    while(input!="EXIT"):
        input=connection.recv(1024).decode()
        match input:
            case "EXIT":
                break
            case "MESURE_TEMPERATURE_AND_HUMIDITY":
                mesure_temp_and_hum()
            case "SEE_TH_MEASUREMENT":
                see_th_measurement()
            case "SHOW_TXT":
                show_txt()

    connection.close()


def setup():
    with open("./setup.txt",'r') as setupfile:
        hashpass=setupfile.readline()
        return hashpass



if __name__=="__main__":
    hashpass=setup()
    connection=create_socket()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        while True:
            conn, address = connection.accept()
            executor.submit(handle_connection, conn, address,hashpass)
