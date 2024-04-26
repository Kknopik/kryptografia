import socket, hashlib, os

users = {}

def add_user(username, password):
    #sól
    salt = os.urandom(16)
    salted_password = password.encode() + salt
    #skrót hasła z salt
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    users[username] = {'salt': salt, 'password': hashed_password}


def authenticate(username, password):
    if username in users:
        stored_password = users[username]['password']
        salt = users[username]['salt']
        #skrót hasła 
        salted_password = password.encode() + salt
        hashed_password = hashlib.sha256(salted_password).hexdigest()
        if hashed_password == stored_password:
            return True
    return False

def handle_client(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            parts = message.split(':')
            if len(parts) != 3:
                conn.sendall(b"ERROR: Invalid request format")
                continue
            command, username, password = parts
            if command == "ADD_USER":
                add_user(username, password)
                conn.sendall(b"SUCCESS: User added successfully")
            elif command == "LOGIN":
                if authenticate(username, password):
                    conn.sendall(b"SUCCESS: Authentication successful")
                else:
                    conn.sendall(b"ERROR: Authentication failed")
            else:
                conn.sendall(b"ERROR: Invalid command")

def start_server():
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on', (HOST, PORT))
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)

start_server()
