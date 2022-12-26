import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = None
hostColor="White"

def host():
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))


clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            #print(f"{nicknames[index]} left the chat.".encode('ascii'))
            nicknames.pop(index)


def receive():
    while True:
        client, address = server.accept()
        #print(f"Connected with {str(address)}.")

        client.send("NICKNAME".encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        clients.append(client)
        nicknames.append(nickname)
        if hostColor == "White" and len(nicknames) == 1:
            client.send("COLORW".encode("ascii"))
        elif hostColor == "Black" and len(nicknames) == 1:
            client.send("COLORB".encode("ascii"))
        elif hostColor == "White" and len(nicknames) == 2:
            client.send("COLORB".encode("ascii"))
        elif hostColor == "Black" and len(nicknames) == 2:
            client.send("COLORW".encode("ascii"))
        client.send(("HOSTC"+hostColor).encode("ascii"))

        #print(f"Nickname of the client is {nickname}.")
        #client.send("Connected to the server.".encode('ascii'))
        #broadcast(f"{nickname} joined the chat!".encode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def sendPlayers():
    msg = "PLAYERS-"+nicknames[0]+"_"+nicknames[1]
    for c in clients:
        c.send(msg.encode("ascii"))
