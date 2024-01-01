import pygame
from enemy import EnemyManager
from pygame import mixer

pygame.init()

# GAME WINDOW
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Space Invaders")

# FONT STYLE
font = pygame.font.Font('font/Revamped.otf', 15)

# TO SHOW SCORE ON WQINDOW
def show_score(x,y):
    score = font.render(f"Score: {enemy_manager.score}", True, (255,255,255))
    screen.blit(score, (x,y))

# TO SHOW LEVEL ON WINDOW
def show_level(x,y):
    level = font.render(f"Level: {enemy_manager.level}", True, (255,255,255))
    screen.blit(level, (x,y))

# TO SHOW LIVES OF PLAYER ON WINDOW
def show_lives(x,y):
    heart = pygame.image.load('images/heart.png')
    lives = font.render(f"Lives:", True, (255,255,255))
    screen.blit(lives, (x,y))
    for i in range(1, player_lives+1):
        screen.blit(heart, ((x+50)+(i*30), y-5))


# TO SHOW INFO HOW TO PLAY
def show_info(x,y):
    pygame.draw.rect(screen, (146, 84, 158, 127), (190, 230, 500, 200))  # Info box background
    ypos = y
    text = ['Press LEFT arrow key to move left', 'Press RIGHT arrow key to move right', 'Press SPACE key to fire']
    for line in text:
        info = font.render(line, True, (240,240,240))
        screen.blit(info, (x,ypos))
        ypos += 30

# TO PAUSE THE GAME
def pause_game(x,y):
    pause = pygame.image.load('images/pause.png')
    screen.blit(pause, (x,y))

# TO SHOW GAME OVER
def gameover():
    global is_game_over
    is_game_over = True
    font = pygame.font.Font('font/Revamped.otf', 55)
    over = font.render("Game Over!", True, (255,255,255))
    screen.blit(over, (250, 300))
    mixer.music.stop()
    sound = mixer.Sound('music/gameover.wav')
    sound.play()

# TO SHOW IF PLAYER WINS
def player_win():
    global is_player_win
    is_player_win = True
    font = pygame.font.Font('font/Revamped.otf', 55)
    win = font.render("You win!", True, (255,255,255))
    screen.blit(win, (300, 300))
    mixer.music.stop()
    sound = mixer.Sound('music/Victory.wav')
    sound.play()

# STATE VARIABLES
is_game_on = True
is_game_over = False
is_player_win = False
can_show_info = False
paused = False
is_level_upgrader = [False, False, False]


# NECESSARY IMAGE VARIABLES
background = pygame.image.load('images/background.jpg')
shipship = pygame.image.load('images/spaceship.png')
bullet = pygame.image.load('images/bullet.png')

# BUTTONS
info_text = font.render('Info', True, (255,255,255))
info_btn = info_text.get_rect(center=(600, 28))
pause_text = font.render('Pause/Resume', True, (255,255,255))
pause_btn = pause_text.get_rect(center=(770, 28))


# PLAYER - POSITIONS AND FUNCTIONS
def player(x, y):
    screen.blit(shipship, (x,y))

playerX = 420
playerY = 580
playerX_change = 0
player_lives = 3
size = 45
def draw_ignition(x, y, size):
    ignition_surface = pygame.Surface((size, size), pygame.SRCALPHA) 
    pygame.draw.circle(ignition_surface,(255, 210, 0, 150), (size // 2, size // 2), size // 2) 
    screen.blit(pygame.transform.smoothscale(ignition_surface, (size, size)), (x + 30 - size // 2, y + 60 - size // 2))

# ENEMIES - CREATING ENEMY MANAGER INSTANCE
enemy_manager = EnemyManager()
enemy_manager.create_enemies()

# BULLET - POSITIONS AND FUNCTIONS
bullet_state = "ready"
bulletX = 0
bulletY = 580
bulletY_change = 4
def fire_bullet(x,y):
    screen.blit(bullet, (x+15,y-10))


# GAME LOOP
while is_game_on:
    screen.fill((255,255,255))
    screen.blit(background, (0,0))

    # PLAYING MUSIC DEPEND ON THE GAME LEVEL
    if enemy_manager.level == 1 and not is_level_upgrader[0]:
        mixer.music.load('music/space journey.mp3')
        mixer.music.play(-1)
        is_level_upgrader[0] = True
    elif enemy_manager.level == 2 and not is_level_upgrader[1]:
        mixer.music.stop()
        mixer.music.load('music/boss.wav')
        mixer.music.play(-1)
        is_level_upgrader[1] = True
    elif enemy_manager.level == 3 and not is_level_upgrader[2]:
        mixer.music.stop()
        mixer.music.load('music/boss2.wav')
        mixer.music.play(-1)
        is_level_upgrader[2] = True

    # DISPLAYING NECESSARY DETAILS
    show_score(20,20)
    show_level(430 ,20)
    show_lives(200, 20 )
    screen.blit(info_text, info_btn)
    screen.blit(pause_text, pause_btn)

    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_game_on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not (is_game_over or paused):
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT and not (is_game_over or paused):
                playerX_change = 0.5
            if event.key == pygame.K_SPACE and not (is_game_over or paused):
                if bullet_state == "ready":
                    sound = mixer.Sound('music/laser1.wav')
                    sound.play()
                    bulletX = playerX
                    bullet_state = 'fire'
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if info_btn.collidepoint(mouse_pos):
                can_show_info = not can_show_info
            if pause_btn.collidepoint(mouse_pos):
                paused = not paused
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # BOUNDARIES FOR SPACESHIP
    if playerX<=0:
        playerX=0
    elif playerX>=840:
        playerX=840

    playerX += playerX_change
    size -= 1  
    if size < 10:
        size = 45
    draw_ignition(playerX, playerY, size)
    player(playerX, playerY)

    # ENEMIES MOVEMENT
    is_enemy_reached_territory = enemy_manager.enemy_movement(screen, is_game_over, playerX, playerY, is_player_win, paused)
    if is_enemy_reached_territory:
        player_lives -= 1
        enemy_manager.create_enemies()
    
    
    # BULLET MOVEMENT
    if bullet_state == "fire":
        bulletY -= bulletY_change
        fire_bullet(bulletX, bulletY)
        if bulletY <=0:
            bullet_state="ready"
            bulletY = 580
    if enemy_manager.bullet_collided(bulletX, bulletY):
        sound = mixer.Sound('music/explosion.wav')
        sound.play()
        bullet_state = 'ready'
        bulletY=580

    # MOVING ONTO NEXT LEVEL IF ENEMIES HAVE BEEN KILLED
    if len(enemy_manager.enemies) == 0:
            print('level upgraded')
            enemy_manager.level += 1
            enemy_manager.create_enemies()

    # CHECKING IF PLAYER GOT ATTACKED
    is_player_attacked = enemy_manager.laser_collided(playerX, playerY)
    if is_player_attacked:
        player_lives -= 1
        sound = mixer.Sound('music/mechanical_explosion.wav')
        sound.play()

    is_fireball_attacked = enemy_manager.fireball_collided(playerX, playerY)
    if is_fireball_attacked:
        player_lives -= 1
        sound = mixer.Sound('music/mechanical_explosion.wav')
        sound.play()

    # SHOWING STATES OF THE GAME
    if can_show_info:
        show_info(250,300)

    if paused:
        pause_game(370,250)

    # GAME OVER CONDITIONS
    if player_lives <= 0:
        gameover()
    if enemy_manager.level == 3 and enemy_manager.boss.energy <=0:
        player_win()

    # UPDATING THE SCREEN
    pygame.display.update()


