import hashlib
from client import create_account, login, send_message

def test_authentication():
    print("1. Dodawanie nowego użytkownika:")
    print(create_account('user1', 'password123'))
    
    print("2. Logowanie z poprawnym hasłem:")
    print(login('user1', 'password123'))

    print("3. Logowanie z nieprawidłowym hasłem:")
    print(login('user1', 'wrongpassword'))


test_authentication()
