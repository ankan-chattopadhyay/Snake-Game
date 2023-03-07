import os.path
import pygame
import random

pygame.mixer.init()
pygame.init()

# colours
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Creating window
screen_width = 800
screen_height = 600
gamewindow = pygame.display.set_mode((screen_width, screen_height))

# background image
wlcmimg = pygame.image.load("welcome.jpg")
wlcmimg = pygame.transform.scale(wlcmimg, (screen_width, screen_height)).convert_alpha()

bgimg = pygame.image.load("background.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

gmovrimg = pygame.image.load("gameover.jpg")
gmovrimg = pygame.transform.scale(gmovrimg, (screen_width, screen_height)).convert_alpha()

# Game title
pygame.display.set_caption("SnakeGame")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


def screen_score(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x, y])


def plot_snake(gamewindow, color, snakelist, snakehead):
    for x, y in snakelist:
        pygame.draw.rect(gamewindow, color, [x, y, snakehead, snakehead])


def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.blit(wlcmimg, (0, 0))
        screen_score("Welcome to a Snake Game by Ankan", black, 160, 120)
        screen_score("Press SpaceBar to play", blue, 220, 160)
        screen_score("use arrow keys to control the snakes", black, 80, 480)
        screen_score("don't touch the outline", red, 80, 520)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()
            pygame.display.update()
            clock.tick(60)


def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_head = 15
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_list = []
    snake_length = 1
    fps = 30

    # check highscore file exist
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(0, screen_width)
    food_y = random.randint(0, screen_height)

    # Gameloop
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gamewindow.blit(gmovrimg, (0, 0))
            screen_score("Press ENTER to play again", red, 220, 400)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('back.mp3')
                        pygame.mixer.music.play()
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 7
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = - 7
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = - 7
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = 7
                        velocity_x = 0
                    # CheatCode
                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 1
                '''print("your score is ", score)
                pygame.mixer.music.load('bite.mp3')
                pygame.mixer.music.play()'''
                food_x = random.randint(20, 400)
                food_y = random.randint(20, 300)
                snake_length += 1
                if score > int(highscore):
                    highscore = score

            gamewindow.blit(bgimg, (0, 0))
            screen_score("Score: " + str(score) + "  HighScore: " + str(highscore), white, 5, 5)
            pygame.draw.rect(gamewindow, green, [food_x, food_y, snake_head, snake_head])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            '''if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()'''

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()

            plot_snake(gamewindow, blue, snake_list, snake_head)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


welcome()
