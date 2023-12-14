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
    client.send(message)

def recieve():
  while True:
    client, address = server.accept()
    print(f"NEWCONN: Connected with {str(address)}")

    # even though we are not the client, we have to use the client's socket
    # for sending messages to the client
    # server socket is just for accepting client connections
    client.send('NICK'.encode('utf-8'))
    nickname = client.recv(1024).decode('utf-8')
    
    clients.append(client)
    nicknames.append(nickname)

    # print is just on server-side other clients don't see it
    print(f"NICK: Nickname of client is {nickname}")
    broadcast(f"{nickname} has connected".encode('utf-8'))
    client.send("Connected to the server successfully".encode('utf-8'))

    thread = threading.Thread(target=handle, args=(client,))
    thread.start()

def handle(client):
  while True:
    try:
      message = client.recv(1024)
      print(f"{nicknames[clients.index(client)]}: {message}")
      broadcast(message)
    except:
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nicknames.remove(nicknames[index])
      break

print("SERVER RUNNING ...")
recieve()
server.close()