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
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.isJump = False
        self.jumpCount = 10
        self.vel = 7
 
        self.rect.x = 0
        self.rect.y = sh - self.rect.height
        self.ground_level = self.rect.y
 
    def update(self, keys):
        x = self.rect.x
        y = self.rect.y
 
        if keys[pygame.K_LEFT] and x > self.vel:
            x -= self.vel
 
        if keys[pygame.K_RIGHT] and x < sw - self.rect.width - self.vel:
            x += self.vel
 
        if not self.isJump:
            # Remove the up key condition
            # if keys[pygame.K_UP] and y > self.vel:
            #     y -= self.vel
 
            if keys[pygame.K_DOWN] and y < sh - self.rect.height - self.vel:
                y += self.vel
 
            if keys[pygame.K_SPACE]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                y -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1
            else:
                self.jumpCount = 10
                self.isJump = False
                y = self.ground_level
 
        if y < 0:
            y = 0
        elif y > sh - self.rect.height:
            y = sh - self.rect.height
 
        self.rect.x = x
        self.rect.y = y
 
screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Game")
 
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
 
while run:
    pygame.time.delay(50)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Background
    screen.fill((173,216,230))

    
    pygame.draw.rect(screen, (111, 78, 55), (0, sh-15, sw,15), width = 0)
 
    # Draw lava
    pygame.draw.rect(screen, (255, 0, 0), (45, sh-15, sw, 15), width = 0)
 
    if player.rect.colliderect((45, sh-15, sw, 15)):
        if pressed_keys[pygame.K_RIGHT]:
            player.rect.bottomleft = (0, sh-15)
 
    # Draw green rectangles (platforms)
    pygame.draw.rect(screen, (34, 139, 24), (80, 300, 150, 100))
    pygame.draw.rect(screen, (34, 139, 24), (290, 300, 150, 100))
    pygame.draw.rect(screen, (34, 139, 24), (500, 300, 150, 100))
    pygame.draw.rect(screen, (34, 139, 24), (700, 300, 150, 100))
    pygame.draw.rect(screen, (34, 139, 24), (900, 300, 250, 100))
 
    # Draw player
    screen.blit(player.surf, player.rect)
 
    pygame.display.flip()
 
pygame.quit()
