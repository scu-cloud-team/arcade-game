import random
import socket
import pickle
from _thread import *
import pygame
import threading

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
        self.m2x = None
        self.m2y = None


class Game:
    def __init__(self):
        self.coordMessage = CoordMessage()
        self.coordMessage.p1x = 50
        self.coordMessage.p1y = windowHeight * random.random()  # 350
        self.coordMessage.p2x = windowWidth - 50 - 60  # Ship Width
        self.coordMessage.p2y = windowHeight * random.random()  # 350
        self.coordMessage.m1x = windowWidth * random.random()
        self.coordMessage.m1y = -25
        self.coordMessage.m2x = windowWidth * random.random()
        self.coordMessage.m2y = -25

        self.speed1 = 5 * random.random() + 5
        self.speed2 = 5 * random.random() + 5

        self.playerWidth = 60
        self.playerWeight = 20
        self.playerImage = pygame.Surface((self.playerWidth, self.playerWeight))
        self.playerMask = pygame.mask.from_surface(self.playerImage)

        self.meteorWidth = 20
        self.meteorHeight = 20
        self.meteorImage = pygame.Surface((self.meteorWidth, self.meteorHeight))
        self.meteorMask = pygame.mask.from_surface(self.meteorImage)

    def updatePlayerOne(self, move_msg):
        self.coordMessage.p1x += move_msg.px
        self.coordMessage.p1y += move_msg.py
        if self.coordMessage.p1x < 0:
            self.coordMessage.p1x = 0
        elif self.coordMessage.p1x > p1horzBorder:
            self.coordMessage.p1x = p1horzBorder
        if self.coordMessage.p1y < 0:
            self.coordMessage.p1y = 0
        elif self.coordMessage.p1y > vertBorder:
            self.coordMessage.p1y = vertBorder

    def updatePlayerTwo(self, move_msg):
        self.coordMessage.p2x += move_msg.px
        self.coordMessage.p2y += move_msg.py
        if self.coordMessage.p2x < p2horzBorder:
            self.coordMessage.p2x = p2horzBorder
        elif self.coordMessage.p2x > p2horzBorder2:
            self.coordMessage.p2x = p2horzBorder2
        if self.coordMessage.p2y < 0:
            self.coordMessage.p2y = 0
        elif self.coordMessage.p2y > vertBorder:
            self.coordMessage.p2y = vertBorder

    def updateMeteor(self):
        self.coordMessage.m1y += self.speed1
        if self.coordMessage.m1y > windowHeight:
            self.coordMessage.m1x = windowWidth * random.random()
            self.coordMessage.m1y = -25
            self.speed1 = 5 * random.random() + 5
        self.coordMessage.m2y += self.speed2
        if self.coordMessage.m2y > windowHeight:
            self.coordMessage.m2x = windowWidth * random.random()
            self.coordMessage.m2y = -25
            self.speed2 = 5 * random.random() + 5

    def checkCollisionOne(self):
        if self.playerMask.overlap(self.meteorMask, (int(round(self.coordMessage.m1x - self.coordMessage.p1x)), int(round(self.coordMessage.m1y - self.coordMessage.p1y)))) or self.playerMask.overlap(self.meteorMask, (int(round(self.coordMessage.m2x - self.coordMessage.p1x)), int(round(self.coordMessage.m2y - self.coordMessage.p1y)))):
            self.coordMessage.p1x = 50
            self.coordMessage.p1y = windowHeight * random.random()  # 350
            return True
        else:
            return False

    def checkCollisionTwo(self):
        if self.playerMask.overlap(self.meteorMask, (int(round(self.coordMessage.m1x - self.coordMessage.p2x)), int(round(self.coordMessage.m1y - self.coordMessage.p2y)))) or self.playerMask.overlap(self.meteorMask, (int(round(self.coordMessage.m2x - self.coordMessage.p2x)), int(round(self.coordMessage.m2y - self.coordMessage.p2y)))):
            self.coordMessage.p2x = windowWidth - 50 - 60  # Ship Width
            self.coordMessage.p2y = windowHeight * random.random()  # 350
            return True
        else:
            return False


class MoveMessage:
    def __init__(self, x, y):
        self.px = x
        self.py = y


game = Game()

SERVER_IP = 'ec2-54-215-117-138.us-west-1.compute.amazonaws.com'
SERVER_IP = '0.0.0.0'
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


def threaded_client(playernum):
    if playernum == 1:
        while True:
            try:
                recv_data = playerConnections[0].recv(BUFFER_SIZE)
            except Exception as cli_e:
                break
            if not recv_data:
                break
            move_message = pickle.loads(recv_data)
            game.updatePlayerOne(move_message)
            send_data = pickle.dumps(game.coordMessage)
            playerConnections[0].send(send_data)
        playerConnections[0].close()
        print(playerConnections[0], "exited")
        playerConnections[0] = None
    elif playernum == 2:
        while True:
            try:
                recv_data = playerConnections[1].recv(BUFFER_SIZE)
            except:
                break
            if not recv_data:
                break
            move_message = pickle.loads(recv_data)
            game.updatePlayerTwo(move_message)
            send_data = pickle.dumps(game.coordMessage)
            playerConnections[1].send(send_data)
        playerConnections[1].close()
        print(playerConnections[1], "exited")
        playerConnections[1] = None


def threaded_game_mechanics():
    while True:
        pygame.time.delay(50)
        game.updateMeteor()
        if game.checkCollisionOne():
            print("Hit Player 1")
        if game.checkCollisionTwo():
            print("Hit Player 2")


playerConnections = [None, None]
gameStarted = [False]

try:
    start_new_thread(threaded_game_mechanics, ())
    while True:
        if not playerConnections[0]:
            playerConnections[0], addr = sock.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(threaded_client, (1,))
            ThreadCount += 1
            print('Thread Number: ' + str(ThreadCount))
        elif not playerConnections[1]:
            playerConnections[1], addr = sock.accept()
            print('Connected to: ' + addr[0] + ':' + str(addr[1]))
            start_new_thread(threaded_client, (2,))
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
