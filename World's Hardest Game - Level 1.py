from typing import List
import pygame
import sys

pygame.init()
deaths = 0
font = pygame.font.SysFont("monospace", 35)
WIDTH = 1000  # Dimensions of screen
HEIGHT = 700

WHITE = (255, 255, 255)  # Colours
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
SPEED = 5  # speed of player is 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def main():
    global deaths

    direction1 = 'right'  # direction for blocks that start at the left and move right
    direction2 = 'left'  # direction for blocks that start at the right and move left

    player_size = 40  # should be 40
    enemy_size = 30  # 30

    p_x = 200
    p_y = 500 - player_size
    player_pos = [p_x, p_y]  # Initial position of player

    i = (50 - enemy_size) // 2   # i = 10
    enemy_list = [[300, 400 + i], [650, 350 + i], [300, 300 + i], [650, 250 + i], [300, 200 + i], [650, 150 + i]]

    enemy_speed = 10  # speed of enemy is 10

    game_over = False
    clock = pygame.time.Clock()

    def draw_enemies1():  # Draw blue boxes to screen
        for i in enemy_list:
            pygame.draw.rect(screen, BLUE, (i[0], i[1], enemy_size, enemy_size))

    def update_enemy_positions():
        """
        Update position of the blue boxes.
        """
        global direction1
        global direction2
        # Updates position of enemies
        for i in range (0, 6):
            if i % 2 == 0:
                if enemy_list[i][0] < 301:
                    direction1 = 'right'
                elif enemy_list[i][0] > 649:
                    direction1 = 'left'

                if direction1 == 'right':
                    enemy_list[i][0] += enemy_speed  # move blue boxes right
                elif direction1 == 'left':
                    enemy_list[i][0] -= enemy_speed  # move blue boxes left
            else:  # if i is odd
                if enemy_list[i][0] > 649:
                    direction2 = 'left'
                elif enemy_list[i][0] < 301:
                    direction2 = 'right'
                if direction2 == 'right':
                    enemy_list[i][0] += enemy_speed  # move blue boxes right
                elif direction2 == 'left':
                    enemy_list[i][0] -= enemy_speed  # move blue boxes left

    # Bottom left of grid: (250, 500)

    def draw_grid1():  # draws 8 x 8 grid (400 x 400 pixels)
        for i in range(200, 800, 50):
            pygame.draw.line(screen, WHITE, (i, 150), (i, 500))  # Vertical lines
        for i in range(150, 500, 50):
            pygame.draw.line(screen, WHITE, (200, i), (750, i))  # Horizontal lines
        pygame.draw.line(screen, WHITE, (200, 500), (350, 500))  # Horizontal line
        pygame.draw.rect(screen, BLACK, (351, 503, 400, -50))  # Black rectangle
        pygame.draw.rect(screen, BLACK, (701, 450, 50, -300))
        pygame.draw.rect(screen, BLACK, (199, 449, 100, -350))  # Long black rectangle (left side)
        pygame.draw.rect(screen, GREEN, (650, 100, 150, 50))  # White rectangle (top right)
        pygame.draw.rect(screen, WHITE, (650, 100, 150, 50), 2)  # White rectangle (top right)
        for i in range(700, 850, 50):
            pygame.draw.line(screen, WHITE, (i, 100), (i, 150))  # Draws two vertical white lines

        pygame.draw.rect(screen, RED, (300, 150, 400, 300), 3)  # Red

    def collision_check(enemy_list: List[List[int]], player_pos: List[int]) -> bool:
        """
        :param enemy_list: List of blue boxes
        :param player_pos: Position of player
        :return: True iff the player has collided with one of the blue boxes
        """
        for enemy_pos in enemy_list:
            if detect_collision(player_pos, enemy_pos):
                return True
        return False

    def detect_collision(player_pos: List[int], enemy_pos: List[int]) -> bool:
        p_x = player_pos[0]
        p_y = player_pos[1]

        e_x = enemy_pos[0]
        e_y = enemy_pos[1]

        if (p_x <= e_x <= (p_x + player_size)) or (e_x <= p_x <= (e_x + enemy_size)):
            if (p_y <= e_y <= (p_y + player_size)) or (e_y <= p_y <= (e_y + enemy_size)):
                return True
        return False

    while not game_over:  # main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # if Esc key is pressed, exit
            sys.exit()

        p_x = player_pos[0]
        p_y = player_pos[1]
        if keys[pygame.K_LEFT] and ((p_x > 200 and p_y >= 450) or (p_x > 300 and 150 <= p_y) or (p_x > 650 and 100 <= p_y <= 150)):
            p_x -= SPEED
        if (keys[pygame.K_RIGHT]) and ((p_x <= 348 - player_size) or (p_y <= 450 - player_size and p_x < 700 - player_size) or (p_y <= 150 - player_size and 650 <= p_x < 800 - player_size)):
            p_x += SPEED
        if (keys[pygame.K_UP]) and ((p_y > 450 and p_x <= 350 - player_size) or (p_x >= 300 and p_y > 150) or (p_x >= 650 and p_y > 100)):
            p_y -= SPEED
        if (keys[pygame.K_DOWN]) and ((p_y < 496 - player_size and p_x <= 350 - player_size) or (p_y < 450 - player_size and 700 - player_size >= p_x >= 300) or (p_y < 150 - player_size and p_x >= 650)):
            p_y += SPEED
        if 700 < p_x < 850 and 100 <= p_y <= 150 - player_size:  # If player reaches green area
            print ("Well done!")
            game_over = True

        player_pos = [p_x, p_y]
        screen.fill(BLACK)  # Clear screen
        draw_grid1()
        update_enemy_positions()

        if collision_check(enemy_list, player_pos):  # Check for collision
            deaths += 1
            text = "Deaths: " + str(deaths)  # Display number of deaths
            label = font.render(text, 1, WHITE)
            screen.blit(label, (0, 50))
            pygame.display.update()
            game_over = True
            main()  # Resets game

        draw_enemies1()
        pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))
        text = "Deaths: " + str(deaths)  # Display number of deaths
        label = font.render(text, 1, WHITE)
        screen.blit(label, (0, 50))
        clock.tick(30)  # 30 frames per second
        pygame.display.update()  # Update screen


main()
