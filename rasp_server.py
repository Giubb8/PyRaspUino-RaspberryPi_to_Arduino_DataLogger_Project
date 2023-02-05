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
    s.bind('0.0.0.0',5000)
    s.listen(3)
    return s

def handle_connection(connection,address):
    print('Connesso a', address)
    username=connection.recv(1024)
    password=connection.recv(1024)
    print(f"ricevuto {username} {password}")
    connection.close()

if __name__=="__main__":
    connection=create_socket()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            conn, address = connection.accept()
            executor.submit(handle_connection, conn, address)
