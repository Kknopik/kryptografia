import socket, hashlib

def send_message(message):
    HOST = '127.0.0.1'
    PORT = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(message.encode())
            data = s.recv(1024)
            return data.decode()
        except ConnectionRefusedError:
            return "ERROR: Connection refused"
        except Exception as e:
            return f"ERROR: {str(e)}"

def create_account(username, password):
    #skrót hasła
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    #wysłanie do servera
    response = send_message(f"ADD_USER:{username}:{hashed_password}")
    return response

def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    response = send_message(f"LOGIN:{username}:{hashed_password}")
    return response

