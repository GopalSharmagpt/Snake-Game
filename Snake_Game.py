import pygame
import time
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
red = (213, 50, 80)
blue = (50, 153, 213)
black = (0, 0, 0)

# Display settings
dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by ChatGPT')

clock = pygame.time.Clock()
snake_block = 20  # Size of the snake
snake_speed = 10  # Decrease speed

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load background image
def load_background():
    try:
        background = pygame.image.load('background_image.jpg')  # Adjust the path if necessary
        background = pygame.transform.scale(background, (dis_width, dis_height))
        return background
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        return pygame.Surface((dis_width, dis_height)).fill(blue)  # Default background color

background = load_background()

# Load sounds
def load_sound(file_name):
    try:
        sound = pygame.mixer.Sound(file_name)
        return sound
    except pygame.error as e:
        print(f"Error loading sound file {file_name}: {e}")
        return None

eat_sound = load_sound('eat_sound.mp3')  # Ensure the correct path and file format
game_over_sound = load_sound('game_over_sound.mp3')  # Ensure the correct path and file format

def draw_snake(snake_block, snake_list, snake_ate_food, food_position):
    for index, segment in enumerate(snake_list):
        if index == 0:  # Draw the head of the snake
            pygame.draw.rect(dis, white, [segment[0], segment[1], snake_block, snake_block])  # Snake head
            
            if snake_ate_food and food_position == segment:
                # Draw eyes
                pygame.draw.circle(dis, black, (segment[0] + snake_block // 4, segment[1] + snake_block // 4), 5)  # Left eye
                pygame.draw.circle(dis, black, (segment[0] + 3 * snake_block // 4, segment[1] + snake_block // 4), 5)  # Right eye
                
                # Draw mouth
                mouth_width = snake_block
                mouth_height = snake_block // 2
                pygame.draw.rect(dis, black, [segment[0], segment[1] + snake_block // 2, mouth_width, mouth_height])  # Mouth base

        else:  # Draw the body of the snake
            # Gradually change color to white based on the length of the snake
            color_intensity = min(255, 255 * (index / len(snake_list)))  # Scale from 0 to 255
            snake_color = (color_intensity, color_intensity, color_intensity)  # Gradually white
            
            pygame.draw.rect(dis, snake_color, [segment[0], segment[1], snake_block, snake_block])

def message(messages, color, background_color):
    dis.fill(background_color)  # Fill the background color
    for i, msg in enumerate(messages):
        mesg = font_style.render(msg, True, color)
        mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + i * 30))  # Adjust vertical spacing
        dis.blit(mesg, mesg_rect)

def gameLoop():
    game_over = False
    game_close = False
    game_over_sound_played = False  # Flag to check if game over sound has played

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    snake_ate_food = False  # Flag to indicate if snake ate food
    score = 0  # Initialize score

    # Initial food coordinates
    foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

    # Big food state
    big_foodx = None
    big_foody = None
    big_food_size = snake_block  # Normal size initially
    big_food_start_time = 0  # Timestamp when big food appeared
    big_food_duration = 7000  # Duration to show big food (in milliseconds)
    big_food_interval = 5000  # Interval to randomly show big food (in milliseconds)
    last_big_food_time = pygame.time.get_ticks()

    while not game_over:
        while game_close:
            dis.blit(background, (0, 0))
            final_score_message = f"Final Score: {score}"
            messages = [
                "You Lost! Press Q-Quit or C-Play Again",
                final_score_message
            ]
            message(messages, yellow, blue)
            pygame.display.update()
            if not game_over_sound_played and game_over_sound:
                game_over_sound.play()
                game_over_sound_played = True  # Set the flag to True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.blit(background, (0, 0))
        if big_foodx is not None and big_foody is not None:
            pygame.draw.rect(dis, red, [big_foodx, big_foody, big_food_size, big_food_size])  # Big food is the same piece
        else:
            pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])  # Regular food

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Flag to show if the snake ate food
        snake_ate_food = False
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            snake_ate_food = True  # Set flag to True when food is eaten
            score += 1  # Increase score for small food
            big_foodx = None  # Ensure no big food when regular food is eaten
            big_foody = None
            big_food_size = snake_block  # Reset size to normal
            if eat_sound:
                eat_sound.play()

        if big_foodx is not None and big_foody is not None:
            if (x1 >= big_foodx and x1 <= big_foodx + big_food_size) and (y1 >= big_foody and y1 <= big_foody + big_food_size):
                Length_of_snake += 5  # Increase the snake length significantly
                big_foodx = None
                big_foody = None
                big_food_size = snake_block  # Reset size to normal after being eaten
                score += 5  # Increase score for big food
                if eat_sound:
                    eat_sound.play()

        # Handle big food appearance
        current_time = pygame.time.get_ticks()
        if big_foodx is None and big_foody is None:  # Only create big food if there is none on the screen
            if current_time - last_big_food_time > big_food_interval:
                if random.choice([True, False]):  # Occasionally choose to show big food
                    big_foodx = round(random.randrange(0, dis_width - snake_block * 2) / 20.0) * 20.0
                    big_foody = round(random.randrange(0, dis_height - snake_block * 2) / 20.0) * 20.0
                    big_food_size = snake_block * 2  # Increase size of the big food
                    big_food_start_time = current_time  # Record the time when big food appeared
                    last_big_food_time = current_time

        # Remove big food after 7 seconds
        if big_foodx is not None and big_foody is not None:
            if current_time - big_food_start_time > big_food_duration:
                big_foodx = None
                big_foody = None
                big_food_size = snake_block  # Reset size to normal
                big_food_start_time = 0

        draw_snake(snake_block, snake_List, snake_ate_food, [foodx, foody])

        pygame.display.update()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
