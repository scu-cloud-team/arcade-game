import pygame
import random
import re
import socket
import pickle


playerName = input("Enter your name: ")
playerName = re.sub('[^0-9a-zA-Z]+', '', playerName)
if len(playerName) > 20:
    playerName = playerName[:20]

windowWidth = 500
windowHeight = 400
horzBorder = windowWidth // 2 - 5

pygame.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Online Game - Praveen Vandeyar")
font = pygame.font.SysFont("comicsans", 20, True)


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
        self.s1 = None
        self.s2 = None


class MoveMessage:
    def __init__(self, x, y):
        self.px = x
        self.py = y


class Player:
    def __init__(self):
        self.x = 50
        self.y = 350
        self.width = 60
        self.height = 20
        self.speed = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 100, 255))
        self.right = True
        self.shot = False

    def move(self, movexy):
        self.x += movexy[0]
        self.y += movexy[1]

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Meteor:
    def __init__(self):
        self.x = windowWidth * random.random()
        self.y = 0
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 200, 0))

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class MidBorder:
    def __init__(self):
        self.x = horzBorder
        self.y = 0
        self.width = 10
        self.height = windowHeight
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Game:
    def __init__(self):
        self.player = Player()
        self.player2 = Player()
        self.meteor = Meteor()
        self.meteor2 = Meteor()
        self.midBorder = MidBorder()
        self.score1 = None
        self.score2 = None
        self.highscore = None

    def draw(self):
        window.fill((0, 0, 0))

        self.midBorder.draw()

        score_text1 = font.render('Score: ' + str(self.score1), True, (255, 255, 255))
        score_text2 = font.render('Highest: ' + str(self.highscore), True, (200, 200, 200))
        score_text3 = font.render('Score: ' + str(self.score2), True, (255, 255, 255))
        window.blit(score_text1, (10, 10))
        window.blit(score_text2, (170, 10))
        window.blit(score_text3, (410, 10))

        self.player.draw()
        self.player2.draw()
        self.meteor.draw()
        self.meteor2.draw()

        pygame.display.update()

    def update(self, coord_msg):
        self.player.x = coord_msg.p1x
        self.player.y = coord_msg.p1y
        self.player2.x = coord_msg.p2x
        self.player2.y = coord_msg.p2y
        self.meteor.x = coord_msg.m1x
        self.meteor.y = coord_msg.m1y
        self.meteor2.x = coord_msg.m2x
        self.meteor2.y = coord_msg.m2y
        self.score1 = coord_msg.s1
        self.score2 = coord_msg.s2
        self.highscore = coord_msg.hs
        self.draw()


#SERVER_IP = '127.0.0.1'
SERVER_IP = 'ec2-54-215-117-138.us-west-1.compute.amazonaws.com'
PORT = 5555
BUFFER_SIZE = 1024

game = Game()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((SERVER_IP, PORT))

    send_data = pickle.dumps(playerName)
    sock.send(send_data)

    run = True
    while run:
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        moveXY = [0, 0]
        if keys:
            if keys[pygame.K_LEFT]:
                moveXY[0] -= 5
            if keys[pygame.K_RIGHT]:
                moveXY[0] += 5
            if keys[pygame.K_UP]:
                moveXY[1] -= 5
            if keys[pygame.K_DOWN]:
                moveXY[1] += 5
        move_message = MoveMessage(moveXY[0], moveXY[1])
        send_data = pickle.dumps(move_message)
        sock.send(send_data)

        recv_data = sock.recv(BUFFER_SIZE)
        coord_message = pickle.loads(recv_data)
        game.update(coord_message)
    sock.close()

except Exception as e:
    print(e)
    sock.close()
