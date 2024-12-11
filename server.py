import threading
import socket

host = "127.0.0.1" # loopback
port = 41820

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast_message(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast_message(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)

            broadcast(f'{nickname} has left the chat.'.encode('ascii'))
            break

def receive():
    client, address = server.accept()
    print(f'Connected with {str(address)}')

    client.send('NICK'.encode('ascii'))

    nickname = client.recv(1024).decode('ascii')

    nicknames.append(nickname)
    clients.append(client)

    print(f'Client ({client}) nickname is: {nickname}')
    broadcast_message(f'{nickname} joined the chat.'.encode('ascii'))
    client.send('Connected to the server.'.encode('ascii'))

    thread = threading.Thread(target=handle_client, args=(client,))
    thread.start()

receive()