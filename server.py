import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            print(f"ERROR: {e}")
            index = clients.index(client)
            broadcast(f"{nicknames[index]} has left the chat\n".encode('utf-8'))
            nicknames.remove(nicknames[index])
            clients.remove(client)
            client.close()


def receive():
    while True:
        client, address = server.accept()
        print(f"NEWCONN: Connected with {str(address)}\n")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        if nickname == "\\QUIT":
            client.close()
            continue
        
        clients.append(client)
        nicknames.append(nickname)

        print(f"NICK: Nickname of client is {nickname}")
        broadcast(f"{nickname} has connected\n".encode('utf-8'))
        client.send("Connected to the server successfully".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def handle(client):
    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            
            if message.startswith("\\PRIV"):
                tmp = message.split(" ")
                recipient = tmp[1]
                private_message = " ".join(tmp[2:])
                try:
                    index = nicknames.index(recipient)
                    private_client = clients[index]
                    private_client.send(f"{nicknames[clients.index(client)]} (private): {private_message}".encode('utf-8'))
                except ValueError:
                    client.send("ERR: Recipient not valid!".encode('utf-8'))

            elif message == "\\QUIT":
                break

            else:
                broadcast(message.encode('utf-8'))
    except Exception as e:
        print(f"ERROR: {e}")

    finally:
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            if index < len(nicknames):
                left_user = nicknames.pop(index)
                broadcast(f"{left_user} has left the chat\n".encode('utf-8'))
                



print("SERVER RUNNING ...")
receive()
server.close()
