import socket
import concurrent.futures

class Profile:
    def __init__(self,username,hashed_password):
        self.username=username
        self.hashed_password=hashed_password

    def check_hash(self,hash_to_test)->bool:
        if(hash_to_test==self.hashed_password):
            return True
        else:
            return False

def create_socket():
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',5000))
    s.listen(3)
    return s

def login(hashpass,connection):
    username = connection.recv(1024).decode()
    password = connection.recv(1024).decode()
    print(f"UTENTE {username} PASSWORD {password}")
    if(hashpass==password):
        print("LE PASSWORD MATCHANO PREGO")
    else:
        print("UNLUCKY")
        print(hashpass)
        print(password)

def handle_connection(connection,address,hashpass):
    print('Connesso a', address)
    login(hashpass,connection)
    connection.close()


def setup():
    with open("./setup.txt",'r') as setupfile:
        hashpass=setupfile.readline()
        return hashpass
        #print("letto"+hashpass)


if __name__=="__main__":
    hashpass=setup()
    connection=create_socket()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        while True:
            conn, address = connection.accept()
            executor.submit(handle_connection, conn, address,hashpass)
