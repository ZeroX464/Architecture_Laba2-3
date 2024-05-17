#Server

import socket
import sqlite3
import threading

def handle_client(client_socket):
    with client_socket:
        request = client_socket.recv(1024).decode('utf-8')
        _, username, password = request.split(',')
        if request.startswith('register'):
            if not checkUsernameIsExistInDB(username):
                register_user(username, password)
                client_socket.sendall(b'Registration successful')
            else:
                client_socket.sendall(b'Username is already taken')
        else: # Авторизация
            if authenticate_user(username, password):
                client_socket.sendall(b'Login successful')
            else:
                client_socket.sendall(b'Login failed')

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()

    conn.close()

    return user is not None

def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

    conn.close()
    
def checkUsernameIsExistInDB(username): # Проверка, что логин есть в БД
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username=?', (username,))
    answer = cursor.fetchone()[0] # 0 - записи нету, 1 - запись есть
    conn.close()
    return answer

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print('Server listening on port 9999')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()