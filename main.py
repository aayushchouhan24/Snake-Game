import pygame
import random
import os
import time

pygame.mixer.init()
pygame.init()


# Colors
green = (0, 200, 0)
color = (120, 9, 38)

# Creating window
screen_width = 1080/1.2
screen_height = 660/1.2
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background Image
background_image = pygame.image.load("assets/images/Background.jpg")
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height))

# Game over Image
over_image = pygame.image.load("assets/images/Gameover.jpg")
over_image = pygame.transform.scale(over_image, (screen_width, screen_height))

# Front Image
menu_image = pygame.image.load("assets/images/Menu.jpg")
menu_image = pygame.transform.scale(menu_image, (screen_width, screen_height))

# Food Image
food_image = pygame.image.load('assets/images/Food.png')
food_image = pygame.transform.scale(food_image, (45, 50))

# Icon
icon_image = pygame.image.load('assets/images/Icon.png')

# Game Title
pygame.display.set_caption("Snakes with Aayush")

pygame.display.set_icon(icon_image)

pygame.display.update()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 25)


def food(food_x, food_y):
    gameWindow.blit(food_image, (food_x, food_y))


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def music():
    pygame.mixer.music.load('assets/sounds/back.mp3')
    pygame.mixer.music.play()


def crashed():
    pygame.mixer.music.load('assets/sounds/over.mp3')
    pygame.mixer.music.play()


def quit():
    pygame.quit()
    quit()


def button(x, y, w, h, action, action2):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y and click[0] == 1:
        action2()
        action()


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    music()
                    gameloop()
        gameWindow.fill(0)
        gameWindow.blit(menu_image, (0, 0))

        button(int(screen_width-345), int(screen_height-140),
               497/2, 135/2, gameloop, music)
        button(int(screen_width-345), int(screen_height-70),
               497/2, 135/2, quit, music)

        pygame.display.update()
        clock.tick(10)


# Game Loop
def gameloop():

    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_list = []
    snake_length = 1
    snake_size = 40
    mode = 0
    score = 0
    velocity_x = 0
    velocity_y = 0
    init_velocity = 2
    fps = 60
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    # Check if high_score file exists
    if (not os.path.exists("assets/high_score.txt")):
        with open("assets/high_score.txt", "w") as f:
            f.write("0")

    with open("assets/high_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            with open("assets/high_score.txt", "w") as f:
                f.write(str(high_score))
            crashed()
            gameWindow.fill(0)
            gameWindow.blit(over_image, (0, 0))
            pygame.display.update()
            time.sleep(2)
            game_intro()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Food Location Change
                        food_x = random.randrange(5, screen_width-90)
                        food_y = random.randrange(5, screen_height-100)

                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Snake Speed UP
                        init_velocity += 1

                    if event.key == pygame.K_UNDERSCORE or event.key == pygame.K_MINUS and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Snake Speed DOWN
                        if init_velocity > 1:
                            init_velocity -= 1

                    if event.key == pygame.K_m and pygame.key.get_mods() & pygame.KMOD_CTRL:  # Toggle Snake Self body crash
                        mode = 0 if mode == 1 else 1

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 35 and abs(snake_y - food_y) < 35:

                score += 10

                food_x = random.randint(20, screen_width / 2)

                food_y = random.randint(20, screen_height / 2)

                snake_length += 10

                init_velocity += 0.3

                if score > int(high_score):

                    high_score = score

            gameWindow.fill(0)

            gameWindow.blit(background_image, (0, 0))

            text_screen("Top Score: " + str(high_score) +
                        "         Score: " + str(score), color, screen_width/2-155, 63)

            food(food_x, food_y)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]


            if head in snake_list[:-1] and mode == 0:
                game_over = True

            if snake_x < 0 or snake_x > screen_width-snake_size or snake_y < 0 or snake_y > screen_height-snake_size:
                game_over = True

            plot_snake(gameWindow, green, snake_list, snake_size)
            pygame.display.update()
            clock.tick(fps)


game_intro()
pygame.quit()
quit()
