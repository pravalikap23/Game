import pygame
import random
import PIL

pygame.init()
pygame.font.init()

# Screen width and height
sw = 1000
sh = 350

run = True

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("assets/amongus.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
        self.isJump = False
        self.jumpCount = 10
        self.vel = 5

    def update(self, keys):
        x = self.rect.bottomleft[0]
        y = self.rect.bottomleft[1]
        height = self.rect.h

        if keys[pygame.K_LEFT] and x > self.vel:
            x -= self.vel

        if keys[pygame.K_RIGHT] and x < 500 - self.vel - sw:
            x += self.vel

        if not(self.isJump):
            if keys[pygame.K_UP] and y > self.vel:
                y -= self.vel

            if keys[pygame.K_DOWN] and y < 500 - height - self.vel:
                y += self.vel

            if  keys[pygame.K_SPACE]:
                self.isJump = True

            else:
                if self.jumpCount >= -10:
                    y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
                    self.jumpCount -= 1
                else: 
                    self.jumpCount = 10
                    self.isJump = False

win = pygame.display.set_mode((sw,sh))

player = Player()

all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    player.update(keys)
    for en in all_sprites:
        win.blit(en.surf, en.rect)

    pygame.display.flip()