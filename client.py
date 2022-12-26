import socket
import pickle

nickname = "_NICKNAME_"

HOST = '127.0.0.1'
PORT = 55555

client = None


def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))


nicknames = ["WHITE", "BLACK"]
color = "W"
hostC= "W"
moves = []

def receive():
    global color, hostC
    while True:
        try:
            message = client.recv(1024).decode("ascii")
            if message == "NICKNAME":
                client.send(nickname.encode('ascii'))
            elif message[0:7] == "PLAYERS":
                nicknames[0] = message[8:message.index("_")]
                nicknames[1] = message[message.index("_")+1:]
            elif message[0:5] == "COLOR":
                color = message[5]
            elif message[0:4] == "MOVE":
                coord = message[4:]
                moves.append(coord)
            elif message[0:5] == "HOSTC":
                hostC = message[5:]
            else:
                print(message)
                pass
        except:
            #print("An error occurred.")
            client.close()
            break


def write():
    while True:
        message = f'{nickname}:{input("")}'
        client.send(message.encode('ascii'))


"""receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
"""

