import pygame
import random


width = 1920  # Size x side
height = 1080  # Size y side
game_speed = 1000  # Speed spawn meteorites

player_size = 150  # Player size
player_speed = 1.7  # Player move speed
player_x = (width - player_size) / 2  # Player position x
player_y = 840   # Player position y
player_move_count = 1  # Player move animation

meteorite_size = 200  # Meteorites size
meteorite_speed = 3  # Meteorites speed
meteorite_x = random.randint(0, width - meteorite_size)  # Meteorites x position
meteorite_y = -100  # Meteorites y position
meteorite_in_game = []  # Meteorite in game

bullet_y = player_y  # Bullet y position
bullets = []  # Bullets in game
bullet_speed = 5  # Bullets speed
bullet_reload = True  # Bullet reload

heart = []  # Heart in game
heart_size = 50  # Heart size
heart_x = 100  # Heart x position
heart_y = 50  # Heart y position
heart_margin = 0  # Heart margin

scores = 0  # Scores
score_x = width - 200  # Scores x position
score_y = 50  # Scores y position

bg_speed = 0.5  # Background speed
bg_y = 0  # Background y position


def bullet_spawn():
    global meteorite_in_game, scores
    if bullets:
        for (i, el) in enumerate(bullets):
            if gameplay:
                screen.blit(bullet, (el.x, el.y))
            el.y -= bullet_speed

            if el.y == -50:
                bullets.pop(i)

            for (i, meteorite) in enumerate(meteorite_in_game):
                if el.colliderect(meteorite):
                    remove_meteorite_sound.play()
                    scores += 50
                    if meteorite_in_game:
                        meteorite_in_game.pop(i)
                    if bullets:
                        bullets.pop(-1)


def meteorite_spawn(player_rect):
    global scores, gameplay

    if meteorite_in_game:
        scores += 0.1
        for (i, el) in enumerate(meteorite_in_game):
            if gameplay:
                screen.blit(meteorite, el)  # Add meteorite
            el.y += meteorite_speed

            if el.y > 1080:
                meteorite_in_game.pop(i)

            if player_rect.colliderect(el):
                if scores - 100 > 0:
                    scores -= 100
                else:
                    scores = 0

                heart.pop()
                meteorite_in_game.pop(i)

                if not heart:
                    finish_sound.play(-1)
                    pygame.mixer.music.pause()

                    gameplay = False
                else:
                    lost_sound.play()


def player_control():
    global player_x, player_move_count, scores
    screen.blit(player_move[player_move_count],
                (player_x, player_y))  # Add user model

    keys = pygame.key.get_pressed()  # Get all keys

    if keys[pygame.K_LEFT]:
        if player_x > 0:
            player_x -= player_speed  # Change position x

        player_move_count = 2  # Change animation image left
    elif keys[pygame.K_RIGHT]:
        if player_x < width - player_size:
            player_x += player_speed  # Change position x

        player_move_count = 0  # Change animation image right
    else:
        player_move_count = 1  # Change animation image general


def heart_check():
    global heart_margin
    for (i, el) in enumerate(heart):
        heart_margin += 70
        if heart_margin == len(heart) * 70:
            heart_margin = 0

        screen.blit(heart[i], (heart_x + heart_margin, heart_y))


def gameplay_check(gameplay):
    player_rect = player_move[1].get_rect(
        topleft=(player_x, player_y))  # Create sprite

    meteorite_spawn(player_rect)
    player_control()
    heart_check()
    bullet_spawn()


pygame.init()  # Initialization app

screen = pygame.display.set_mode((width, height))  # Set display size
pygame.display.set_caption("Lesson #3")  # Set title app
pygame.mouse.set_visible(False)  # Hide coursor

icon = pygame.image.load("images/logo.png").convert_alpha()  # Load logo app
# Load background image
bg = pygame.image.load("images/background.jpg").convert()
bullet = pygame.image.load("images/bullet.png").convert_alpha()
player_move = [
    pygame.transform.scale(pygame.image.load(
        "images/player/playerLeft.png"), (player_size, player_size)).convert_alpha(),
    pygame.transform.scale(pygame.image.load(
        "images/player/player.png"), (player_size, player_size)).convert_alpha(),
    pygame.transform.scale(pygame.image.load(
        "images/player/playerRight.png"), (player_size, player_size)).convert_alpha()
]  # Load rocket images with reduced sizes

meteorite = pygame.image.load("images/meteorite.png").convert_alpha()  # Load meteorite image
heart_image = pygame.image.load("images/heart.png").convert_alpha()  # Load heeart image
heart_image = pygame.transform.scale(heart_image, (heart_size, heart_size))  # Load change size
meteorite = pygame.transform.scale(meteorite, (meteorite_size, meteorite_size))  # Load change size


pygame.mixer.music.load("song/song.mp3")  # Load background song
pygame.mixer.music.set_volume(0.2)  # Change volum
pygame.mixer.music.play(-1)  # Set infinite background song

shot_sound = pygame.mixer.Sound("song/vine-boom.mp3")  # Load shot sound
lost_sound = pygame.mixer.Sound("song/Ha Ha.mp3")  # Load lost sound
finish_sound = pygame.mixer.Sound("song/cry.mp3")  # Load finish sound
remove_meteorite_sound = pygame.mixer.Sound("song/eBoi.mp3")  # Load finish sound


pygame.display.set_icon(icon)  # Set logo app

# Change background image scale
bg = pygame.transform.scale(bg, (width, height))

finishFont = pygame.font.Font('fonts/Anton-Regular.ttf', 100)  # Connect font
scoreFont = pygame.font.Font('fonts/Anton-Regular.ttf', 50)  # Connect font
restartFont = pygame.font.Font('fonts/Anton-Regular.ttf', 50)  # Connect font

gameover_text = finishFont.render(
    'GAME OVER', True, (255, 255, 255))  # Create finish text
restart_text = restartFont.render(
    'press Left Shift to restart', True, (255, 255, 255))  # Create restart text


meteorite_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteorite_timer, game_speed)

heart = [heart_image] * 5
running = True
gameplay = True

while running:
    screen.blit(bg, (0, bg_y))  # Set background image
    screen.blit(bg, (0, bg_y - height))  # Set second background image for animation

    if scores > 20 and not bullet_reload:
        bullet_reload = True
        scores -= 20

    if not heart:
        keys = pygame.key.get_pressed()  # Get all keys
        if keys[pygame.K_LSHIFT]:
            gameplay = True
            heart = [heart_image] * 5
            meteorite_in_game.clear()
            scores = 0
            bullets.clear()
            finish_sound.stop()
            pygame.mixer.music.unpause()

        # Set finish text in coordinates
        screen.blit(gameover_text, (width / 2 - 200, height / 2 - 100))
        # Set finish text in coordinates
        screen.blit(restart_text, (width / 2 - 220, height / 2 + 100))

    score_text = scoreFont.render(f"{int(scores)}", True, (255, 255, 255))  # Create scores count
    # Set finish text in coordinates
    screen.blit(score_text, (score_x, score_y))

    bg_y += bg_speed
    if bg_y == height:
        bg_y = 0

    if gameplay:
        gameplay_check(gameplay)

    pygame.display.update()  # Update game

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == meteorite_timer:
            meteorite_x = random.randint(0, width - meteorite_size)
            meteorite_in_game.append(meteorite.get_rect(
                topleft=(meteorite_x, meteorite_y)))
        if gameplay and event.type == pygame.KEYUP\
            and event.key == pygame.K_SPACE and bullet_reload:
            shot_sound.play()
            bullet_reload = False

            bullet_x = player_x + (player_size / 2) - 50  # 50 half size bullet
            bullets.append(bullet.get_rect(
                topleft=(bullet_x, bullet_y)))  # Add bullet