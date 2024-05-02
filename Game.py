import pygame
import random
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    )

pygame.init()
pygame.font.init()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        #self.surf = pygame.Surface((20,10))
        #self.surf.fill((255,0,0))
        self.surf = pygame.image.load("missile2.png").convert()
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            center = (random.randint(sw + 20, sw + 100), random.randint(0,sh))
            )
        self.speed = random.randint(1,1)

    def update(self):
        global score
        self.rect.move_ip(-self.speed,0)
        if self.rect.right < 0:
            self.kill()
            score += 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        #self.surf = pygame.Surface((75,25))
        #self.surf.fill((0,255,0))
        self.surf = pygame.image.load("jet3.png").convert()
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

my_font = pygame.font.SysFont('Comic Sans MS', 20)

player = Player()

enemies = pygame.sprite.Group()
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

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    enemies.update()
    
    screen.fill((255,255,255))
    #pygame.draw.circle(screen, (255,0,0),(sw/2,sh/2),100)
    #surf = pygame.Surface((75,50))
    #surf.fill((0,0,0))
    for en in all_sprites:
        screen.blit(en.surf, en.rect)
##    if pygame.sprite.spritecollideany(player,enemies):
##        player.kill()
##        running = False

    if pygame.sprite.spritecollideany(player,enemies):
        score -= 10
        for entity in enemies:
            entity.kill()
    if score <= 0:
        player.kill()
        running = False
    text_surface = my_font.render(str(score), False, (255, 0, 0))
    screen.blit(text_surface, (sw-30,10))
    pygame.display.flip()

pygame.quit()