#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 16:59:40 2020

@author: blanquie
"""

import pygame
import pygame_menu
import os
import json
import time
import random

#successes, failures = pygame.init()
#print("{0} successes and {1} failures".format(successes, failures))

FPS = 60  # This variable will define how many frames we update per second.

current_map = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
rect = pygame.Rect((0, 0), (32, 32))  # First tuple is position, second is size.
image = pygame.Surface((32, 32))  # The tuple represent size.
image.fill(WHITE)  # We fill our surface with a nice white color (by default black).
        
def menu(level_list, score_data, settings, gameDisplay):
    #score submenu
    score_menu = pygame_menu.Menu(settings["height"], settings["width"], 'Score', theme=pygame_menu.themes.THEME_DARK)
    for data in score_data:
        score_menu.add_label(data)
    score_menu.add_button('Back', pygame_menu.events.BACK)
    
    #settings submenu
    settings_menu = pygame_menu.Menu(settings["height"], settings["width"], 'Settings', theme=pygame_menu.themes.THEME_DARK)
    for data in settings:
        settings_menu.add_text_input(f"{data} : ", default= settings[data])
    #settings_menu.add_button('Apply', apply_settings, selector_id = "id_width")
    settings_menu.add_button('Back', pygame_menu.events.BACK)
    
    #main menu
    menu = pygame_menu.Menu(settings["height"], settings["width"], 'Souls', theme=pygame_menu.themes.THEME_DARK)
    menu.add_text_input('Name :', default='John Doe', onchange= set_username,)
    menu.add_selector('Level Selection :', level_list, onchange=set_map)
    menu.add_button('Play', game, settings, gameDisplay)
    menu.add_button('High Score', score_menu)
    menu.add_button('Settings', settings_menu)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(gameDisplay)
        
def apply_settings(value):
    print(value)
    pass
    
def pause_menu(settings, gameDisplay):
    menu = pygame_menu.Menu(settings["height"]/2, settings["width"]/2, 'Pause', theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Back', pygame_menu.events.CLOSE)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(gameDisplay)
    
def set_map(value, map):
    filename = f"map/{value[0]}.csv"
    matrice = decode_csv(filename)
    for line in matrice:
        print(line)

def set_username(value):
    pass

#Decode the csv file
def decode_csv(fileName):
    initial_matrice = []
    with open(fileName, "r") as file:
        #take out the first line
        first_line = file.readline()
        first_line.replace('\n', '').split(",")
        for line in file :
            data = line.replace('\n', '').split(",")
            data = [int(i) for i in data]
            initial_matrice.append(data)
    file.close
    return initial_matrice
    
def decode_score():
    with open("misc/score.json", "r") as read_file:
        score_data = json.load(read_file)
        return score_data["Score"]
    
def decode_settings():
    with open("misc/settings.json", "r") as read_file:
        settings_data = json.load(read_file)
        return settings_data
    
def startup():
    name_list = os.listdir('map')
    i = 1
    level_list = []
    for x in name_list:
        name = x.split('.')[0]
        level = (name,i) 
        level_list.append(level)
        i = i + 1    
    return level_list
        
def game(settings, gameDisplay):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    rect.move_ip(0, -2)
                elif event.key == pygame.K_s:
                    rect.move_ip(0, 2)
                elif event.key == pygame.K_q:
                    rect.move_ip(-2, 0)
                elif event.key == pygame.K_d:
                    rect.move_ip(2, 0)
                elif event.key == pygame.K_p:
                    pause_menu(settings, gameDisplay) 
                elif event.key == pygame.K_n:
                    pygame.display.quit() 
                    pygame.quit()
    
        gameDisplay.fill(BLACK)
        gameDisplay.blit(image, rect)
        pygame.display.update()  # Or pygame.display.flip()
                            
def program_logic():
    level_list = startup()
    score_data = decode_score()
    settings = decode_settings()
    pygame.init()
    gameDisplay = pygame.display.set_mode((settings["width"], settings["height"])) 
    menu(level_list, score_data, settings, gameDisplay)

program_logic()