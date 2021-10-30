import random
import socket
import pickle
from _thread import *

windowWidth = 500
windowHeight = 400
p1horzBorder = windowWidth // 2 - 5 - 60  # Half of Border and Ship Width
p2horzBorder = windowWidth // 2 + 5  # Half of Border and Ship Width
p2horzBorder2 = windowWidth - 60  # Half of Border and Ship Width
vertBorder = windowHeight - 20  # Ship Height


def move(self, movexy):
    self.x += movexy[0]
    self.y += movexy[1]
    if self.x < 0:
        self.x = 0
    elif self.x > self.rightBorder:
        self.x = self.rightBorder
    if self.y < 0:
        self.y = 0
    elif self.y > self.bottomBorder:
        self.y = self.bottomBorder


class CoordMessage:
    def __init__(self):
        self.p1x = None
        self.p1y = None
        self.p2x = None
        self.p2y = None
        self.m1x = None
        self.m1y = None

    def updatePlayerOne(self, move_msg):
        self.p1x += move_msg.px
        self.p1y += move_msg.py
        if self.p1x < 0:
            self.p1x = 0
        elif self.p1x > p1horzBorder:
            self.p1x = p1horzBorder
        if self.p1y < 0:
            self.p1y = 0
        elif self.p1y > vertBorder:
            self.p1y = vertBorder

    def updatePlayerTwo(self, move_msg):
        self.p2x += move_msg.px
        self.p2y += move_msg.py
        if self.p2x < p2horzBorder:
            self.p2x = p2horzBorder
        elif self.p2x > p2horzBorder2:
            self.p2x = p2horzBorder2
        if self.p2y < 0:
            self.p2y = 0
        elif self.p2y > vertBorder:
            self.p2y = vertBorder

    def updateMeteor(self):
        self.m1y += 5
        if self.m1y > windowHeight:
            self.m1x = windowWidth * random.random()
            self.m1y = -25


class MoveMessage:
    def __init__(self, x, y):
        self.px = x
        self.py = y


coord_message = CoordMessage()
coord_message.p1x = 50
coord_message.p1y = 350
coord_message.p2x = windowWidth - 50 - 60  # Ship Width
coord_message.p2y = 350
coord_message.m1x = windowWidth * random.random()
coord_message.m1y = -25

SERVER_IP = '127.0.0.1'
PORT = 5555
BUFFER_SIZE = 1024

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
try:
    sock.bind((SERVER_IP, PORT))
except socket.error as e:
    str(e)

sock.listen(2)
ThreadCount = 0
print("Started Server")


def threaded_client(connection, playernum):
    while True:
        recv_data1 = None
        try:
            recv_data = connection.recv(BUFFER_SIZE)
        except:
            break
        if not recv_data:
            break

        move_message = pickle.loads(recv_data)
        if playernum == 1:
            coord_message.updatePlayerOne(move_message)
        elif playernum == 2:
            coord_message.updatePlayerTwo(move_message)

        send_data = pickle.dumps(coord_message)
        connection.send(send_data)
    connection.close()


p1conn = None
p2conn = None

try:
    while True:
        if not p1conn:
            p1conn, addr = sock.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(threaded_client, (p1conn, 1,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))
        elif not p2conn:
            p2conn, addr = sock.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(threaded_client, (p2conn, 2,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))

except Exception as e:
    print(e)
finally:
    try:
        sock.close()
    except Exception as e:
        print(e)

print("Done")
