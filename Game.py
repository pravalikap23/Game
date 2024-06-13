import pygame
import time
from threading import Thread

run = True

# Time
allocatedTime = 31
startTime = time.time()
gameOver = False
seconds = 0

def timer():
    global gameOver
    global startTime
    global allocatedTime
    global seconds
    global run
    while run:
        if not gameOver:
            time.sleep(1)
            seconds += 1

            elapsedTime = time.time() - startTime
            if elapsedTime >= allocatedTime:
                gameOver = True

t = Thread(target=timer, daemon=True)
t.start()

pygame.init()
pygame.font.init()
 
# Screen width and height
sw = 1000
sh = 350
 
# Score
score = 0

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Assets/amongus.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.reset()

    def reset(self):
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

candies = []
 
lava_rect = pygame.Rect(45, sh-15, sw, 15)
 
def reset():
    global lives
    global live_sprites
    global candies
    global player
    global startTime
    global elapsedTime
    global score
    global seconds

    elapsedTime = 0
    startTime = time.time()
    seconds = 0

    score = 0
    lives = 5
    live_sprites = pygame.sprite.Group()
    for i in range(lives):
        live = Live()
        live.rect.x = 10 + i * 25
        live.rect.y = 10
        live_sprites.add(live)
 
    candies = [
        Candy(110, 235),
        Candy(320, 235),
        Candy(530, 235),
        Candy(730, 235),
        Candy(900, 235)
    ]

    player.reset()

reset()

won = False

while run:
    pygame.time.delay(50)
 
    if lives == 0:
        gameOver = True

    if len(candies) == 0:
        gameOver = True
        won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
 
    if not gameOver:
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
        text_surface = my_font.render(f"Score: {score} Time: {seconds}", False, (0, 0, 0))
        screen.blit(text_surface, (150,5))

        # Draw player
        screen.blit(player.surf, player.rect)
    
        # Draw lives
        live_sprites.draw(screen)

    if gameOver:
        font = pygame.font.SysFont('arial', 40)
        if won:
            game_over_text = font.render('You Win!', True, (255, 255, 255))
        else:
            game_over_text = font.render('Game over!', True, (255, 255, 255))
        screen.blit(game_over_text, (sw/2 - game_over_text.get_width()/2, 0))

        font = pygame.font.SysFont('arial', 25)
        button_rect = pygame.Rect(sw/2-100/2, 55, 100, 30)
        pygame.draw.rect(screen, (255, 255, 255), button_rect, width = 0)
  
        button_text = font.render('Start again', True, (0, 0, 0))
        screen.blit(button_text, button_rect)

        mouseX, mouseY = pygame.mouse.get_pos()

        if mouseX > button_rect.x and mouseX < button_rect.x + button_rect.width:
            if mouseY > button_rect.y and mouseY < button_rect.y + button_rect.height:
                if pygame.mouse.get_pressed()[0]:
                    reset()
                    gameOver = False
 
    pygame.display.flip()
 
pygame.quit()