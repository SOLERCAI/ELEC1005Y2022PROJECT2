# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT

from game import Game

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

game = Game()
rect_len = game.settings.rect_len
snake = game.snake
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound('./sound/crash.wav')
pygame.mixer.music.load("./sound/gaming_bgm.mp3")
pygame.mixer.music.play(loops=-1)

food_sound = pygame.mixer.Sound('./sound/food_bgm.wav')
bomb_sound = pygame.mixer.Sound('./sound/bgm_for_mad_dog.wav')
reverse_sound = pygame.mixer.Sound('./sound/bgm_for_reversing.wav')
reduce_sound = pygame.mixer.Sound('./sound/bgm_for_reducing_length.wav')

background_img = pygame.image.load(r'./images/background_img.jpg')
screen.blit(background_img, (0,0))

def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('comicsansms', 50)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)


def quitgame():
    pygame.quit()
    quit()


def crash():
    pygame.mixer.Sound.play(crash_sound)
    message_display('crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(1)

def eat_food():
    pygame.mixer.Sound.play(food_sound)    

def eat_bomb():
    pygame.mixer.Sound.play(bomb_sound) 
    
def eat_reverse():
    pygame.mixer.Sound.play(reverse_sound)
    
def eat_reduce():
    pygame.mixer.Sound.play(reduce_sound)

def initial_interface():
    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        
        message_display('Gluttonous', game.settings.width / 2 * 15, game.settings.height / 4 * 15)

        button('Go!', 280, 440, 80, 40, green, bright_green, game_loop, 'human')
        button('Quit', 480, 440, 80, 40, red, bright_red, quitgame)

        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=10):
    game.restart_game()
    fps = 5
    while not game.game_end():

        pygame.event.pump()

        move = human_move()
        

        game.do_move(move)

        screen.fill(black)
        screen.blit(background_img, (0,0))

        game.snake.blit(rect_len, screen)
        game.strawberry.blit(screen)
        game.blit_score(white, screen)
        
        if game.snake.score >= 20:
            fps = 20
        elif game.snake.score < 10:
            fps = 5
        else:
            fps = 10    
        

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()
def human_move():
    direction = snake.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    initial_interface()
