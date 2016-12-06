import pygame
import random

title = "test game"

white = pygame.color.THECOLORS["white"]
black = pygame.color.THECOLORS["black"]
red = pygame.color.THECOLORS["red"]



class Player:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.xSpeed = 0
        self.ySpeed = 3
        self.jump = False
        self.death = False
        self.image = pygame.image.load('player_sprite.png').convert()
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)

        game.playerList.append(self)

    def update(self):

        self.xSpeed *= 0.93

        if self.y + (self.height // 2) >= game.dispHeight:
            self.jump = True
        if self.jump:
            self.ySpeed = -20
            self.jump = False

        if self.ySpeed > -0.9 and self.ySpeed < 0:
            self.ySpeed *= -1
        if self.ySpeed > 0:
            self.ySpeed += game.gravity*self.ySpeed
        if self.ySpeed < -0.9:
            self.ySpeed -= game.gravity*self.ySpeed

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.xSpeed = -5
        if key[pygame.K_RIGHT]:
            self.xSpeed = +5

        self.x += self.xSpeed
        self.y += self.ySpeed

        if self.x < -self.width:
            self.x = game.dispWidth

        if self.x > game.dispWidth + self.width:
            self.x = 0



        if game.cameraSpeed == 0:
            self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        else:
            self.rect = pygame.Rect(self.x - (self.width // 2), 0.3*game.dispHeight - (self.height // 2), self.width, self.height)
        self.draw()

    def draw(self):
        game.display.blit(self.image, self.rect)
        #pygame.draw.rect(game.display, white, self.rect)


class Platform:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 5
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        game.platformList.append(self)

    def draw(self):
        game.display.blit(self.image, self.rect)
        #pygame.draw.rect(game.display, self.color, self.rect)


class Solid (Platform):

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.color = white
        self.name = "Solid"
        self.image = pygame.image.load('cloud_sprite.png')

    def update(self):

        if self.y - self.height > game.dispHeight:
            game.platformList.remove(self)

        for player in game.playerList:
            if player.ySpeed > 0 and self.rect.colliderect(player.rect):
                player.jump = True
                game.platformList.remove(self)
                game.score += 1

        self.y += game.cameraSpeed
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        self.draw()


class Broken (Platform):

    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.color = red
        self.name = "Broken"
        self.image = pygame.image.load('cloud_sprite.png')

    def update(self):

        if self.y - self.height > game.dispHeight:
            game.platformList.remove(self)

        for player in game.playerList:
            if player.ySpeed > 0 and self.rect.colliderect(player.rect):
                game.platformList.remove(self)
                return

        self.y += game.cameraSpeed
        self.rect = pygame.Rect(self.x - (self.width // 2), self.y - (self.height // 2), self.width, self.height)
        self.draw()

class Main:

    def __init__(self):
        self.cameraSpeed = 0
        self.score = 0
        self.dispWidth = 600
        self.dispHeight = 800
        self.display = pygame.display.set_mode((self.dispWidth, self.dispHeight))
        self.gravity = 0.05
        self.platformList = []
        self.playerList = []
        self.playerNo = 1
        self.platformNo = 7
        self.quit = False
        self.backColor = pygame.Color(230, 242, 255)
        self.frame_count = 0
        self.frame_rate = 100
        self.font = pygame.font.Font(None, 30)
        self.deathMessage = self.font.render("U ded", True, white)



    def start(self):
        for i in range(self.playerNo):
            Player(self.dispWidth // 2, self.dispHeight // 2)

        Solid((self.dispWidth // 2), (self.dispHeight *(3/4)))

        for i in range(self.platformNo):
            Solid(random.randint(0, self.dispWidth), (self.dispHeight - (self.dispHeight/self.platformNo)*i))

    def update(self):
        self.display.fill(self.backColor)


        for player in self.playerList:
            player.update()

        for player in self.playerList:
            if player.y < 0.3*self.dispHeight:
                self.cameraSpeed = -player.ySpeed
            else:
                self.cameraSpeed = 0

        for platform in self.platformList:
            platform.update()

        for player in self.playerList:
            if player.y > self.platformList[1].y:
                player.death = True


        if len(self.platformList) < self.platformNo:
            Solid(random.randint(0, self.dispWidth), 0)

            if self.platformList[-1].name == "Broken" and self.platformList[-1].name == "Broken":
                Solid(random.randint(0, self.dispWidth), 0)
            else:
                if (random.random()*100) < self.score:
                    Broken(random.randint(0, self.dispWidth), 0)

        self.backColor = pygame.Color((230-3*self.score), (242-3*self.score), 255)

        self.frame_count += 1

        self.total_seconds = self.frame_count // self.frame_rate
        self.minutes = self.total_seconds // 60
        self.seconds = self.total_seconds % 60

        self.timeString = "Time: {0:02}:{1:02}".format(self.minutes, self.seconds)
        self.timeText = font.render(self.timeString, True, white)

        self.scoreString = "Score: {}".format(self.score*100 + self.frame_count)
        self.scoreText = font.render(self.scoreString, True, white)

        game.display.blit(self.timeText, [10, 10])
        game.display.blit(self.scoreText, [(self.dispWidth-200), 10])

        for player in self.playerList:
            if player.death == True:
                game.display.blit(self.deathMessage, [self.dispWidth/2, self.dispHeight/2])












clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(title)

game = Main()
game.start()
font = pygame.font.Font(None,30)

while not game.quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit = True
        print(event)
    game.update()
    pygame.display.update()

    clock.tick(100)

pygame.quit()
quit()
