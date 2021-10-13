import pygame
import random
import time

windowWidth = 500
windowHeight = 400

pygame.init()
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Learning PyGame - Praveen Vandeyar")


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
        self.fire = fireRate

    def move(self, x, y):
        self.x += x
        self.y += y

    def mask(self):
        return pygame.mask.from_surface(self.image)

    def draw(self):
        window.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, speed):
        self.x = windowWidth * random.random()
        self.y = 0
        self.width = 20
        self.height = 20
        self.speed = speed
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 200, 0))

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def mask(self):
        return pygame.mask.from_surface(self.image)

    def move(self):
        self.y += self.speed


class Bullet:
    def __init__(self, x, y, speed=5,):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.speed = speed
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((150, 255, 50))

    def draw(self):
        window.blit(self.image, (self.x, self.y))

    def mask(self):
        return pygame.mask.from_surface(self.image)

    def move(self):
        self.x += self.speed


score = 0
font = pygame.font.SysFont("comicsans", int(round(windowHeight / 15)), True)
font1 = pygame.font.SysFont("comicsans", int(round(windowHeight / 10)), True)


def draw_window():
    window.fill((0, 0, 0))
    player.draw()
    obstacle1.draw()
    obstacle2.draw()
    for bullet in bullets:
        bullet.draw()
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))
    pygame.display.update()


def draw_end():
    window.fill((0, 0, 0))
    player.draw()
    obstacle1.draw()
    obstacle2.draw()
    score_text = font1.render('Game Over', True, (255, 100, 100))
    window.blit(score_text, (170, windowHeight//2-int(round(windowHeight / 10))))
    score_text = font1.render('Score: ' + str(score), True, (255, 255, 255))
    window.blit(score_text, (170, windowHeight//2))
    pygame.display.update()


bulletLimit = 5
fireRate = 20
player = Player()
bullets = []
increment = 0.8
speed1 = 3
speed2 = 1.5
obstacle1 = Obstacle(3)
obstacle2 = Obstacle(1.5)

gameOver = False
run = True
while run:
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if player.shot:
        player.fire -= 1
        if player.fire <= 0:
            player.fire = fireRate
            player.shot = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > player.speed:
        player.move(-player.speed, 0)

    if keys[pygame.K_RIGHT] and player.x < windowWidth - player.speed:
        player.move(player.speed, 0)

    if keys[pygame.K_UP] and player.y > player.speed:
        player.move(0, -player.speed)

    if keys[pygame.K_DOWN] and player.y < windowHeight - player.speed:
        player.move(0, player.speed)

    if keys[pygame.K_SPACE]:
        if len(bullets) < bulletLimit and player.fire == fireRate:
            bullets.append(Bullet(player.x+player.width-5, player.y+5))
            player.shot = True

    i = 0
    while i < len(bullets):
        bullets[i].move()

        if bullets[i].mask().overlap(
                obstacle1.mask(), (int(round(obstacle1.x - bullets[i].x)), int(round(obstacle1.y - bullets[i].y)))
        ):
            score += 1
            speed1 -= speed1 // 4
            speed2 -= speed2 // 4
            obstacle1 = Obstacle(speed1)

        if bullets[i].mask().overlap(
                obstacle2.mask(), (int(round(obstacle2.x - bullets[i].x)), int(round(obstacle2.y - bullets[i].y)))
        ):
            score += 1
            speed1 -= speed1 // 4
            speed2 -= speed2 // 4
            obstacle2 = Obstacle(speed2)

        if bullets[i].x > windowWidth:
            bullets.pop(i)
        else:
            i += 1

    obstacle1.move()
    if obstacle1.y > windowHeight:
        score += 1
        speed1 += increment ** 1.1
        obstacle1 = Obstacle(speed1)

    if player.mask().overlap(obstacle1.mask(), (int(round(obstacle1.x - player.x)), int(round(obstacle1.y - player.y)))):
        gameOver = True
        run = False

    obstacle2.move()
    if obstacle2.y > windowHeight:
        score += 1
        speed2 += increment ** 2
        obstacle2 = Obstacle(speed2)

    if player.mask().overlap(obstacle2.mask(), (int(round(obstacle2.x - player.x)), int(round(obstacle2.y - player.y)))):
        run = False

    draw_window()

if gameOver:
    run = True
    draw_end()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    run = False
                    break

pygame.quit()
