import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

data_store = {}

def broadcast(message):
    for client in clients:
        client.send(message)

def receive():
    while True:
        client, address = server.accept()
        print(f"NEWCONN: Connected with {str(address)}\n")

        # even though we are not the client, we have to use the client's socket
        # for sending messages to the client
        # server socket is just for accepting client connections
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        clients.append(client)
        nicknames.append(nickname)
        data_store[str(nickname)] = address

        print(data_store)

        # print is just on server-side other clients don't see it
        print(f"NICK: Nickname of client is {nickname}")
        broadcast(f"{nickname} has connected\n".encode('utf-8'))
        client.send("Connected to the server successfully".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(f"{nicknames[clients.index(client)]}: {message}")

            # \CHAT <nickname> <message>
            if message.startswith("\\CHAT"):
                tmp = message.split(" ")
                nick = tmp[1]
                private_message = " ".join(tmp[2:])

                try:
                    index = nicknames.index(nick)
                    private_client = clients[index]
                    private_client.send(f"{nicknames[clients.index(client)]} (private): {private_message}".encode('utf-8'))
                except ValueError:
                    client.send("ERR: Nickname not valid!".encode('utf-8'))

            else:
                broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.remove(nicknames[index])
            break

print("SERVER RUNNING ...")
receive()
server.close()
