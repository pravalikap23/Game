import pygame
import random
import PIL

from pygame.locals import(
    KEYDOWN,
    K_ESCAPE,
    # K_UP,
    # K_DOWN,
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
        self.surf = pygame.image.load("assets/amongus.png").convert_alpha()
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            center = (0, 300)
        )
        self.jump = False
        self.fall_down = False

        self.jump_height = -20
        self.jump_vel = 1
        self.jump_start_y = None
        self.gravity = 5
        # pygame.transform.scale(self.surf, (16, 32))

    def update(self, pressed_keys):
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0,1)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-1,0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(1,0)
        elif pressed_keys[pygame.K_SPACE] and self.jump == False and self.fall_down == False:
            self.jump = True
            self.jump_start_y = self.rect.y
            # self.rect.move_ip(0,-1)

        if self.jump:
            if self.rect.y <= (self.jump_start_y + self.jump_height):
                self.jump = False
                self.fall_down = True
                #print("here")
                
            #if self.rect.y >= (self.jump_start_y + self.jump_height):
            self.rect.move_ip(0,-1)
                    # self.fall_down = True
        # if self.fall_down:
        #     self.jump = False
        #     if (self.rect.y >= self.jump_start_y):
        #         self.rect.y -= self.gravity
        if self.fall_down:
            self.rect.move_ip(0,1)
            if not self.rect.y <= self.jump_start_y:
                self.fall_down = False
            

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > sw:
            self.rect.right = sw
        elif self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > sh:
            self.rect.bottom = sh

# Screen width and height
sw = 1000
sh = 350

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
        # if event.type == KEYDOWN:
        #     if event.key == K_ESCAPE:
        #         running = False
        
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.fill((173,216,230))
    pygame.draw.rect(screen, (255, 0, 0), (35, sh-15, sw, 15), width = 0)

    for en in all_sprites:
        screen.blit(en.surf, en.rect)

    pygame.display.flip()

pygame.quit()