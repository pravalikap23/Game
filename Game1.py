import pygame
import random
from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

pygame.init()
pygame.font.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((75,25))
        #self.surf.fill((0,255,0))
        self.surf = pygame.image.load("ninja.jpg").convert()
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect()
    
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0,-1)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0,1)
        elif pressed_keys[K_LEFT]:
            self.rect.move_ip(-1,0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(1,0)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > sw:
            self.rect.right = sw
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > sh:
            self.rect.bottom = sh

sw = 1280
sh = 720
score = 10
screen = pygame.display.set_mode([sw,sh])
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        
        elif event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    for en in all_sprites:
        screen.blit(en.surf, en.rect)

    screen.fill((255,255,255))
    pygame.display.flip()

pygame.quit()