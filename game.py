import pygame
import random

white = pygame.color.THECOLORS["white"]
black = pygame.color.THECOLORS["black"]
red = pygame.color.THECOLORS["red"]
dispWidth = 600
dispHeight = 800
display = pygame.display.set_mode((dispWidth, dispHeight))
gravity = 0.05
platformList = []
playerList = []



class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.xSpeed = 0
        self.ySpeed = 3
        self.jump = False
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)

        playerList.append(self)


    def update(self):

        self.xSpeed *= 0.93

        if self.y + (self.height // 2) >= dispHeight:
            self.jump = True
        if self.jump:
            self.ySpeed = -20
            self.jump = False

        if self.ySpeed > -0.9 and self.ySpeed < 0:
            self.ySpeed *= -1
        if self.ySpeed > 0:
            self.ySpeed += gravity*self.ySpeed
        if self.ySpeed < -0.9:
            self.ySpeed -= gravity*self.ySpeed

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.xSpeed = -5
        if key[pygame.K_RIGHT]:
            self.xSpeed = +5

        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x < -self.width:
            self.x = dispWidth

        if self.x > dispWidth + self.width:
            self.x = 0


        if controller.cameraSpeed == 0:
            self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        else:
            self.rect = pygame.Rect(self.x - (self.width // 2), 0.3*dispHeight - (self.height // 2), self.width, self.height)
        self.draw()

    def draw(self):
        pygame.draw.rect(display, white, self.rect)


class Platform:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 5
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        platformList.append(self)

    def update(self):

        for player in playerList:
            if player.ySpeed > 0 and self.rect.colliderect(player.rect):
                player.jump = True

        if self.y - self.height > dispHeight:
            platformList.remove(self)

        self.y += controller.cameraSpeed
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        self.draw()

    def draw(self):
        pygame.draw.rect(display, white, self.rect)


class Controller:

    def __init__(self):
        self.cameraSpeed = 3
        plat1 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        plat2 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        plat3 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        plat4 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        plat5 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        plat6 = Platform(random.randint(0, dispWidth), random.randint(0, dispHeight))
        player1 = Player(dispWidth//2, dispHeight//2)

    def update(self):
        for i in playerList:
            i.update()
            if i.y < 0.3*dispHeight:
                self.cameraSpeed = -i.ySpeed
            else:
                self.cameraSpeed = 0
        for i in platformList:
            i.update()
        if len(platformList) < 6:
            Platform(random.randint(0, dispWidth), 0)


title = "test game"
clock = pygame.time.Clock()
quitGame = False
pygame.init()
pygame.display.set_caption(title)

controller = Controller()

while not quitGame:
    display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitGame = True
        print(event)
    controller.update()
    pygame.display.update()
    clock.tick(100)

pygame.quit()
quit()
