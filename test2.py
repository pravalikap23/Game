import pygame
import time
 
pygame.init()
pygame.font.init()
 
# Screen width and height
sw = 1000
sh = 350
 
run = True

# Score
score = 0

# Time
allocatedTime = 60
startTime = time.time()
gameOver = False

while gameOver == False:
    time.sleep(1)

    elapsedTime = time.time() - startTime
    if elapsedTime >= allocatedTime:
        gameOver = True

print("Game Over!")

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Assets/amongus.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.isJump = False
        self.jumpCount = 10
        self.vel = 7
 
        self.start_x = 0
        self.start_y = sh - self.rect.height
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.ground_level = self.start_y
 
    def update(self, keys):
        x = self.rect.x
        y = self.rect.y
 
        if keys[pygame.K_LEFT] and x > self.vel:
            x -= self.vel
 
        if keys[pygame.K_RIGHT] and x < sw - self.rect.width - self.vel:
            x += self.vel
 
        if not self.isJump:
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

# Lives
class Live(pygame.sprite.Sprite):
    def __init__(self):
        super(Live, self).__init__()
        self.image = pygame.image.load("assets/heart.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
 
class Candy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Candy, self).__init__()
        self.image = pygame.image.load("assets/candy.webp").convert_alpha()
        self.image = pygame.transform.scale(self.image, (85, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

screen = pygame.display.set_mode((sw, sh))
pygame.display.set_caption("Game")
 
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
 
platforms = [
    pygame.Rect(80, 300, 150, 100),
    pygame.Rect(290, 300, 150, 100),
    pygame.Rect(500, 300, 150, 100),
    pygame.Rect(700, 300, 150, 100),
    pygame.Rect(900, 300, 250, 100),
]

candies = [
    Candy(110, 235),
    Candy(320, 235),
    Candy(530, 235),
    Candy(730, 235),
    Candy(900, 235)
]
 
lava_rect = pygame.Rect(45, sh-15, sw, 15)
 
lives = 5
live_sprites = pygame.sprite.Group()
for i in range(lives):
    live = Live()
    live.rect.x = 10 + i * 25
    live.rect.y = 10
    live_sprites.add(live)
 
game_over = False
 
while run:
    pygame.time.delay(50)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
 
    # Background
    screen.fill((173,216,230))
 
    # Brown
    pygame.draw.rect(screen, (111, 78, 55), (0, sh-15, sw,15), width = 0)
 
    # Draw lava
    pygame.draw.rect(screen, (255, 0, 0), lava_rect, width = 0)
 
    if player.rect.bottom > lava_rect.top and player.rect.centerx > lava_rect.left and player.rect.centerx < lava_rect.right:
        lives -= 1
        player.rect.x = player.start_x
        player.rect.y = player.start_y
        if len(live_sprites) > 0:
            live_sprites.remove(live_sprites.sprites()[-1])
        
        if len(live_sprites) == 0:
            lives = 0
 
        if lives == 0:
            game_over = True
            run = False
 
    # Draw green rectangles (platforms)
    for platform in platforms:
        pygame.draw.rect(screen, (34, 139, 24), platform, width = 0)
 
        if player.rect.colliderect(platform):
            player.rect.bottom = platform.top
            player.isJump = False
            player.jumpCount = 10

    # Candy
    for candy in candies:
        screen.blit(candy.image, candy.rect)
        candy_rect = candy.rect
        if player.rect.bottom > candy_rect.top and player.rect.centerx > candy_rect.left and player.rect.centerx < candy_rect.right:
            score += 1
            candies.remove(candy)

    my_font = pygame.font.SysFont('Comic Sans MS', 20)
    text_surface = my_font.render(f"Score: {score}", False, (0, 0, 0))
    screen.blit(text_surface, (150,5))

    # Draw player
    screen.blit(player.surf, player.rect)
 
    # Draw lives
    live_sprites.draw(screen)
 
    if game_over:
        font = pygame.font.SysFont('arial', 40)
        game_over_text = font.render('Game Over', True, (255, 255, 255))
        screen.blit(game_over_text, (sw/2 - game_over_text.get_width()/2, sh))
 
    pygame.display.flip()
 
pygame.quit()