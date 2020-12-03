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
object_map = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
rect = pygame.Rect((0, 0), (32, 32))  # First tuple is position, second is size.
image = pygame.Surface((32, 32))  # The tuple represent size.
image.fill(WHITE)  # We fill our surface with a nice white color (by default black).

TreeImg = pygame.image.load("overworld/single_tree.png")

class Settings_object:
      def __init__(self, width, height):
          self.width = width
          self.height = height
          
def decode_settings():
    with open("misc/settings.json", "r") as read_file:
        settings_data = json.load(read_file)
        return settings_data
          
def settings_logic():
    settings_data = decode_settings()
    settings = Settings_object(settings_data["width"],settings_data["height"])
    return settings

def decode_score():
    with open("misc/score.json", "r") as read_file:
        score_data = json.load(read_file)
        return score_data["Score"]
    
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

def get_level_list():
    name_list = os.listdir('map')
    i = 1
    level_list = []
    for x in name_list:
        name = x.split('.')[0]
        level = (name,i) 
        level_list.append(level)
        i = i + 1    
    return level_list
            
def menu():
    #score submenu
    score_menu = pygame_menu.Menu(settings.height, settings.width, 'Score', theme=pygame_menu.themes.THEME_DARK)
    for data in score_data:
        score_menu.add_label(data)
    score_menu.add_button('Back', pygame_menu.events.BACK)
    
    #settings submenu
    settings_menu = pygame_menu.Menu(settings.height, settings.width, 'Settings', theme=pygame_menu.themes.THEME_DARK)
    for attr, value in settings.__dict__.items():
        settings_menu.add_text_input(f"{attr} : ", default= value)
    settings_menu.add_button('Back', pygame_menu.events.BACK)
    
    #main menu
    menu = pygame_menu.Menu(settings.height, settings.width, 'Souls', theme=pygame_menu.themes.THEME_DARK)
    menu.add_text_input('Name :', default='John Doe', onchange= set_username,)
    menu.add_selector('Level Selection :', level_list, onchange=set_map)
    menu.add_button('Play', start_playing)
    menu.add_button('High Score', score_menu)
    menu.add_button('Settings', settings_menu)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(gameDisplay)
    
def apply_settings(value):
    print(value)
    pass    

def pause_menu():
    menu = pygame_menu.Menu(settings.height/2, settings.width/2, 'Pause', theme=pygame_menu.themes.THEME_BLUE)
    menu.add_button('Resume', pygame_menu.events.CLOSE)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(gameDisplay)
    
def set_map(value, map):
    global current_map
    current_map = []
    filename = f"map/{value[0]}.csv"
    matrice = decode_csv(filename)
    for line in matrice:
        current_map.append(line)

def set_username(value):
    pass

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.destructible = False
        
class World(object):
    wall_list = None
    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        
def start_playing(): 
    map_convertor(current_map)
    Loaded_world()
    game = GameMain()
    game.main_loop()

def map_convertor(matrice):
    global object_map
    object_map = []
    row_index = 0
    value_index = 0
    for row in matrice:
        value_index = 0
        for value in row:
            if value == -1:
                object_map.append(Wall(row_index*50, value_index*50, TreeImg))
            value_index = value_index + 1
        row_index = row_index + 1
    return object_map
        
class Loaded_world(World):
    def __init__(self):
        World.__init__(self)
        walls = object_map
        for wall in walls:
            self.wall_list.add(wall)
            
class GameMain():
    done = False
   
    def __init__(self):
        self.width, self.height = settings.width, settings.height
        self.color_x = 252
        self.color_y = 216
        self.color_z = 168
        self.link = Link(200,500,"UP",False,False,False,False,False,False,False)        
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.link)
        self.clock = pygame.time.Clock()
        self.current_x = 0
        self.current_y = 0
        self.rooms = [[Loaded_world()]]
        self.current_room = self.rooms[self.current_y][self.current_x]
        self.link.walls = self.rooms[self.current_y][self.current_x].wall_list
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
                  
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN and self.link.can_move == True:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_z:
                    print("z")
                    self.link.upKeyPressed = True
                    self.link.downKeyPressed = False
                    self.link.DIRECTION = self.link.UP
                elif event.key == pygame.K_s:
                    self.link.downKeyPressed = True
                    self.link.upKeyPressed = False
                    self.link.DIRECTION = self.link.DOWN
                    self.link.change_y = 5
                elif event.key == pygame.K_q:
                    self.link.leftKeyPressed = True
                    self.link.rightKeyPressed = False
                    self.link.DIRECTION = self.link.LEFT
                elif event.key == pygame.K_d:
                    self.link.rightKeyPressed = True
                    self.link.leftKeyPressed = False
                    self.link.DIRECTION = self.link.RIGHT
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.link.upKeyPressed = False
                    if self.link.rightKeyPressed:
                        self.link.DIRECTION = self.link.RIGHT
                    elif self.link.leftKeyPressed:
                        self.link.DIRECTION = self.link.LEFT
                        
                elif event.key == pygame.K_s:
                    self.link.downKeyPressed = False
                    if self.link.rightKeyPressed:
                        self.link.DIRECTION = self.link.RIGHT
                    elif self.link.leftKeyPressed:
                        self.link.DIRECTION = self.link.LEFT
                        
                elif event.key == pygame.K_q:
                    self.link.leftKeyPressed = False
                    if self.link.upKeyPressed:
                        self.link.DIRECTION = self.link.UP
                    elif self.link.downKeyPressed:
                        self.link.DIRECTION = self.link.DOWN
                        
                elif event.key == pygame.K_d:
                    self.link.rightKeyPressed = False
                    if self.link.upKeyPressed:
                        self.link.DIRECTION = self.link.UP
                    elif self.link.downKeyPressed:
                        self.link.DIRECTION = self.link.DOWN

    def main_loop(self):
        while not self.done:
            self.draw()
            self.clock.tick(60)
            self.handle_events()
            self.all_sprite_list.update()

        
    def draw(self):
        self.screen.fill((self.color_x, self.color_y, self.color_z))
        self.all_sprite_list.draw(self.screen)
        self.current_room.wall_list.draw(self.screen)
        pygame.display.flip()      
        
class Link(pygame.sprite.Sprite):
    
    def __init__(self, x, y,DIRECTION,upKeyPressed,downKeyPressed,leftKeyPressed,rightKeyPressed, spacePressed,has_sword,has_bombs):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("link/link_up1.png")
        self.right1 = pygame.image.load("link/walk_right1.png")
        self.right2 = pygame.image.load("link/link_right2.png")
        self.left1 = pygame.image.load("link/link_left1.png")
        self.left2 = pygame.image.load("link/link_left2.png")
        self.up1 = pygame.image.load("link/link_up1.png")
        self.up2 = pygame.image.load("link/link_up2.png")
        self.down1 = pygame.image.load("link/link_down1.png")
        self.down2 = pygame.image.load("link/link_down2.png")
        self.attack_right = pygame.image.load("link/attack_right.png")
        self.attack_left = pygame.image.load("link/attack_left.png")
        self.attack_up = pygame.image.load("link/attack_up.png")
        self.attack_down = pygame.image.load("link/attack_down.png")
        self.right_walk = [self.right1,self.right2]
        self.left_walk = [self.left1, self.left2]
        self.up_walk = [self.up1, self.up2]
        self.down_walk = [self.down1,self.down2]
        self.ticker = 0
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x_left = 0
        self.change_x_right = 0
        self.change_y_up = 0
        self.change_y_down = 0
        self.walls = None
        self.can_move = True
        self.DIRECTION = DIRECTION
        self.upKeyPressed = upKeyPressed
        self.downKeyPressed = downKeyPressed
        self.leftKeyPressed = leftKeyPressed
        self.rightKeyPressed = rightKeyPressed
        self.spacePressed = spacePressed
        self.WALKRATE = 5
        self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
        self.action = 'walking'
    
    def update(self):
        
        if self.downKeyPressed:
            self.rect.y += 5
            self.image = self.down_walk[self.current_frame]
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.bottom = wall.rect.top

        elif self.upKeyPressed:
            self.rect.y -= 5
            self.image = self.up_walk[self.current_frame]
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)

            for wall in wall_hit_list:
               self.rect.top = wall.rect.bottom
                
        elif self.leftKeyPressed:
            self.rect.x -= 5
            self.image = self.left_walk[self.current_frame]
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.left = wall.rect.right

        elif self.rightKeyPressed:
            self.rect.x += 5
            self.image = self.right_walk[self.current_frame]
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.right = wall.rect.left
        elif self.spacePressed:
            if self.action == "attacking":
                pass
        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame = (self.current_frame + 1) % 2

def program_logic():
    pygame.init()
    menu()
    
score_data = decode_score()
level_list = get_level_list()
settings = settings_logic()
gameDisplay = pygame.display.set_mode((settings.width, settings.height)) 
program_logic()