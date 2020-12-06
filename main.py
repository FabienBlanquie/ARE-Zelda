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
import random

#successes, failures = pygame.init()
#print("{0} successes and {1} failures".format(successes, failures))

FPS = 60  # This variable will define how many frames we update per second.

current_map = []
player_starting_position = []

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
rect = pygame.Rect((0, 0), (32, 32))  # First tuple is position, second is size.
image = pygame.Surface((32, 32))  # The tuple represent size.
image.fill(WHITE)  # We fill our surface with a nice white color (by default black).

BushImg = pygame.image.load("overworld/bush.png")
BushImg = pygame.transform.scale(BushImg, (55, 55))
StoneWallImg = pygame.image.load("overworld/wall.png")
StoneWallImg = pygame.transform.scale(StoneWallImg, (55, 55))
FireCampImg = pygame.image.load("overworld/firecamp.png")
FireCampImg = pygame.transform.scale(FireCampImg, (55, 55))
DoorImg = pygame.image.load("overworld/door.png")
DoorImg = pygame.transform.scale(DoorImg, (55, 55))

class SettingsObject:
      def __init__(self, width, height):
          self.width = width
          self.height = height
          
def decode_settings():
    with open("misc/settings.json", "r") as read_file:
        settings_data = json.load(read_file)
        return settings_data
          
def settings_logic():
    settings_data = decode_settings()
    settings = SettingsObject(settings_data["width"],settings_data["height"])
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

def get_plate_walk_right():
    name_list = os.listdir('player/plate/walk/d')
    i = 1
    walk_cycle_right = []
    for x in name_list:
        right = pygame.image.load(f"player/plate/walk/d/{x}")
        walk_cycle_right.append(right)
        i = i + 1    
    return walk_cycle_right

def get_plate_walk_left():
    name_list = os.listdir('player/plate/walk/q')
    i = 1
    walk_cycle_left = []
    for x in name_list:
        left = pygame.image.load(f"player/plate/walk/q/{x}")
        walk_cycle_left.append(left)
        i = i + 1    
    return walk_cycle_left

def get_plate_walk_up():
    name_list = os.listdir('player/plate/walk/z')
    i = 1
    walk_cycle_up = []
    for x in name_list:
        up = pygame.image.load(f"player/plate/walk/z/{x}")
        walk_cycle_up.append(up)
        i = i + 1    
    return walk_cycle_up

def get_plate_walk_down():
    name_list = os.listdir('player/plate/walk/s')
    i = 1
    walk_cycle_down = []
    for x in name_list:
        down = pygame.image.load(f"player/plate/walk/s/{x}")
        walk_cycle_down.append(down)
        i = i + 1    
    return walk_cycle_down
            
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
        
def first_map(level_list):
    global current_map
    current_map = []
    filename = f"map/{level_list[0][0]}.csv"
    matrice = decode_csv(filename)
    for line in matrice:
        current_map.append(line)

def set_username(value):
    print(value)
    pass

class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.destructible = False
        
class Background(pygame.sprite.Sprite):
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class World(object):
    wall_list = None
    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.mobs_list = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        
def start_playing(): 
    LoadedWorld()
    GameMain().main_loop()

def map_convertor(matrice, game):
    object_map = []
    mob_map = []
    row_index = 0
    value_index = 0
    for row in matrice:
        value_index = 0
        for value in row:
            if value == -1:
                object_map.append(Wall(value_index*55, row_index*55, BushImg))
            if value == -2:
                object_map.append(Wall(value_index*55, row_index*55, StoneWallImg))
            if value == 1:
                object_map.append(Wall(value_index*55, row_index*55, FireCampImg))
            if value == 2:
                object_map.append(Background(value_index*55, row_index*55, DoorImg))
            if value == 22:
                mob_map.append(Mob(value_index*55, row_index*55, 3, game))
            if value == 0:
                player_starting_position.append(Player(value_index*55, row_index*55,"UP",False,False,False,False,False))
            value_index = value_index + 1
        row_index = row_index + 1
    return object_map, mob_map
        
class LoadedWorld(World):
    
    def __init__(self):
        World.__init__(self)
        walls, mobs = map_convertor(current_map, self)        
        for wall in walls:
            self.wall_list.add(wall)
        for mob in mobs:
            mob.walls = self.wall_list
            self.mobs_list.add(mob)
            
class GameMain():
    done = False
   
    def __init__(self):
        self.width, self.height = settings.width, settings.height
        self.color_x = 252
        self.color_y = 216
        self.color_z = 168
        self.player = player_starting_position[0]     
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.clock = pygame.time.Clock()
        self.current_x = 0
        self.current_y = 0
        self.rooms = [[LoadedWorld()]]
        self.current_room = self.rooms[self.current_y][self.current_x]
        self.player.walls = self.rooms[self.current_y][self.current_x].wall_list
        self.player.mobs = self.rooms[self.current_y][self.current_x].mobs_list
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        
    def main_loop(self):
        while not self.done:
            self.draw()
            self.clock.tick(60)
            self.player.mobs.update()
            self.handle_events()
            self.current_room.arrows.update()
            self.all_sprite_list.update()
            arrow_hit_list = self.current_room.arrows
            for arrow in arrow_hit_list:
                    if pygame.sprite.collide_rect(self.player, arrow) and self.player.action == "attacking":
                        arrow.kill()
                    elif pygame.sprite.collide_rect(self.player, arrow) and self.player.action == "walking":
                        self.player.kill()
                    elif pygame.sprite.spritecollideany(arrow,self.player.walls):
                        arrow.kill()
            
    def draw(self):
        self.screen.fill((self.color_x, self.color_y, self.color_z))
        self.all_sprite_list.draw(self.screen)
        self.current_room.wall_list.draw(self.screen)
        self.current_room.arrows.draw(self.screen)
        self.current_room.mobs_list.draw(self.screen)
        pygame.display.flip()  
                  
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN and self.player.can_move == True:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                elif event.key == pygame.K_z:
                    self.player.upKeyPressed = True
                    self.player.downKeyPressed = False
                    self.player.DIRECTION = self.player.UP
                elif event.key == pygame.K_s:
                    self.player.downKeyPressed = True
                    self.player.upKeyPressed = False
                    self.player.DIRECTION = self.player.DOWN
                    self.player.change_y = 5
                elif event.key == pygame.K_q:
                    self.player.leftKeyPressed = True
                    self.player.rightKeyPressed = False
                    self.player.DIRECTION = self.player.LEFT
                elif event.key == pygame.K_d:
                    self.player.rightKeyPressed = True
                    self.player.leftKeyPressed = False
                    self.player.DIRECTION = self.player.RIGHT
                elif event.key == pygame.K_SPACE:
                    self.player.spacePressed = True
                    self.player.can_move = False
                    if self.player.DIRECTION == self.player.RIGHT:
                        self.player.image = self.player.attack_right
                        oldRect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldRect.x + 15
                        self.player.rect.y = oldRect.y
                        self.player.rightKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.downKeyPressed = False
                    elif self.player.DIRECTION == self.player.LEFT:
                        self.player.image = self.player.attack_left
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.downKeyPressed = False
                        self.player.rect.x -= 30
                    elif self.player.DIRECTION == self.player.UP:
                        self.player.image = self.player.attack_up
                        self.player.rightKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.rect.y -= 30
                    elif self.player.DIRECTION == self.player.DOWN:
                        self.player.image = self.player.attack_down
                        oldRect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldRect.x
                        self.player.rect.y = oldRect.y + 15
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                    self.player.action = 'attacking'
                        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.player.upKeyPressed = False
                    if self.player.rightKeyPressed:
                        self.player.DIRECTION = self.player.RIGHT
                    elif self.player.leftKeyPressed:
                        self.player.DIRECTION = self.player.LEFT     
                elif event.key == pygame.K_s:
                    self.player.downKeyPressed = False
                    if self.player.rightKeyPressed:
                        self.player.DIRECTION = self.player.RIGHT
                    elif self.player.leftKeyPressed:
                        self.player.DIRECTION = self.player.LEFT          
                elif event.key == pygame.K_q:
                    self.player.leftKeyPressed = False
                    if self.player.upKeyPressed:
                        self.player.DIRECTION = self.player.UP
                    elif self.player.downKeyPressed:
                        self.player.DIRECTION = self.player.DOWN       
                elif event.key == pygame.K_d:
                    self.player.rightKeyPressed = False
                    if self.player.upKeyPressed:
                        self.player.DIRECTION = self.player.UP
                    elif self.player.downKeyPressed:
                        self.player.DIRECTION = self.player.DOWN   
                elif event.key == pygame.K_SPACE:
                    self.player.can_move = True
                    self.player.spacePressed = False
                    if self.player.DIRECTION == self.player.RIGHT:
                        self.player.image = self.player.right_walk[0]
                        oldRect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldRect.x - 15
                        self.player.rect.y = oldRect.y
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                    if self.player.DIRECTION == self.player.LEFT:
                        self.player.image = self.player.left_walk[0]
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                        self.player.rect.x += 30
                    if self.player.DIRECTION == self.player.UP:
                        self.player.image = self.player.up_walk[0]
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                        self.player.rect.y += 30
                    if self.player.DIRECTION == self.player.DOWN:
                        self.player.image = self.player.down_walk[0]
                        oldRect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldRect.x 
                        self.player.rect.y = oldRect.y -15
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                    self.player.action = "walking"
            
class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, DIRECTION, upKeyPressed, downKeyPressed, leftKeyPressed, rightKeyPressed, spacePressed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player/player_up1.png")
        self.attack_right = pygame.image.load("player/plate/sword/d/d5.png")
        self.attack_left = pygame.image.load("player/plate/sword/q/q5.png")
        self.attack_up = pygame.image.load("player/plate/sword/z/z5.png")
        self.attack_down = pygame.image.load("player/plate/sword/s/s5.png")
        self.right_walk = get_plate_walk_right()
        self.left_walk = get_plate_walk_left()
        self.up_walk = get_plate_walk_up()
        self.down_walk = get_plate_walk_down()
        self.ticker = 0
        self.current_frame = 0
        self.mobs = None
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
                mob_hit_list = pygame.sprite.spritecollide(self, self.mobs, False)
                wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
                for mob in mob_hit_list:
                    if self.rect.colliderect(mob):
                        if self.DIRECTION == self.UP:
                            mob.hitpoint -= 1
                        if self.DIRECTION == self.LEFT:
                            mob.hitpoint -= 1
                        if self.DIRECTION == self.RIGHT:
                            mob.hitpoint -= 1
                        if self.DIRECTION == self.DOWN:
                            mob.hitpoint -= 1
        self.ticker += 1
        if self.ticker % 8 == 0:
            self.current_frame = (self.current_frame + 1) % 2
            
class Mob(pygame.sprite.Sprite):
    def __init__(self,x,y,hitpoint, game):
        self.left1 = pygame.image.load("mob/0.png")
        self.left2 = pygame.image.load("mob/1.png")
        self.down1 = pygame.image.load("mob/2.png")
        self.down2 = pygame.image.load("mob/3.png")
        self.right1 = pygame.image.load("mob/4.png")
        self.right2 = pygame.image.load("mob/5.png")
        self.up1 = pygame.image.load("mob/6.png")
        self.up2 = pygame.image.load("mob/7.png")
        self.left_walk = [self.left1,self.left2]
        self.right_walk = [self.right1, self.right2]
        self.up_walk = [self.up1, self.up2]
        self.down_walk = [self.down1, self.down2]
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,0,48,48)
        self.image = pygame.image.load("mob/0.png")
        self.rect.x = x
        self.rect.y = y
        self.ticker = 0
        self.current_frame = 0
        self.walk_anim_frame = 0
        self.hitpoint = hitpoint
        self.x_change = 1
        self.t = 0
        self.timer = random.randint(60,180)
        self.arrow_timer = random.randint(0,120)
        self.arrow_t = 0
        self.randomDirections = ["up", "down","left","right"]
        self.randomnumber = random.randint(0,3)
        self.direction = self.randomDirections[self.randomnumber]
        self.die = [self.down1,self.down1,self.down1]
        self.walls = None
        self.doors = None
        self.game = game
        self.x_change = 1
        self.y_change = 1
        self.anim_ticker = 0
        
    def update(self):
        if self.direction == "right":
            self.image = self.right_walk[self.walk_anim_frame]
            self.rect.x += self.x_change
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.right = wall.rect.left
                self.direction = self.randomDirections[2]
            self.t += 1
            if self.arrow_t >= self.arrow_timer:
                self.game.arrows.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.arrow_t = 0
                self.arrow_timer = random.randint(60,240)
            self.arrow_t += 1
            if self.t == self.timer: 
              self.direction = self.randomDirections[random.randint(0,3)]
              self.t = 0
        elif self.direction == "left":
            self.image = self.left_walk[self.walk_anim_frame]
            self.rect.x -= self.x_change
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.left = wall.rect.right
                self.direction = self.randomDirections[3]
            self.t += 1
            self.arrow_t += 1
            if self.arrow_t >= self.arrow_timer:
                self.game.arrows.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.arrow_t = 0
                self.arrow_timer = random.randint(60,240)
            if self.t == self.timer:
                self.direction = self.randomDirections[random.randint(0,3)]
                self.t = 0
        elif self.direction == "up":
            self.image = self.up_walk[self.walk_anim_frame]
            self.rect.y -= self.y_change
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.top = wall.rect.bottom
                self.direction = self.randomDirections[1]
            self.t += 1
            self.arrow_t += 1
            if self.arrow_t >= self.arrow_timer:
                self.game.arrows.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.arrow_t = 0
                self.arrow_timer = random.randint(60,240)
            if self.t == self.timer:
                self.direction = self.randomDirections[random.randint(0,3)]
                self.t = 0
        elif self.direction == "down":
            self.image = self.down_walk[self.walk_anim_frame]
            self.rect.y += self.y_change
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.bottom = wall.rect.top
                self.direction = self.randomDirections[0]
            self.t += 1
            self.arrow_t += 1
            if self.arrow_t >= self.arrow_timer:
                self.game.arrows.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.arrow_t = 0
                self.arrow_timer = random.randint(60,240)
            if self.t == self.timer:
                self.direction = self.randomDirections[random.randint(0,3)]
                self.t = 0  
        if self.hitpoint <= 0:
            self.arrow_t = -1
            self.x_change = 0
            self.y_change = 0
            self.rect.y = self.rect.y
            self.image = self.die[self.current_frame]
            self.ticker += 1
            if self.ticker % 15 == 0:
                self.current_frame = (self.current_frame + 1) % 3
            if self.image == self.die[2]:
                self.kill()     
        self.anim_ticker += 1
        if self.anim_ticker % 10 == 0:
            self.walk_anim_frame = (self.walk_anim_frame + 1) % 2
            
class MobProjectile(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        if self.direction == "right":
            self.image = pygame.image.load("mob/fireball/2.png")
            self.image = pygame.transform.scale(self.image, (30, 10))
        elif self.direction == "left":
            self.image = pygame.image.load("mob/fireball/0.png")
            self.image = pygame.transform.scale(self.image, (30, 10))
        elif self.direction == "up":
            self.image = pygame.image.load("mob/fireball/3.png")
            self.image = pygame.transform.scale(self.image, (10, 30))
        elif self.direction == "down":
            self.image = pygame.image.load("mob/fireball/1.png")
            self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        if self.direction == "right":
            self.rect.x += 6
        elif self.direction == "left":
            self.rect.x -= 6
        elif self.direction == "up":
            self.rect.y -= 6
        elif self.direction == "down":
            self.rect.y += 6

def program_logic():
    pygame.init()
    menu()
    
score_data = decode_score()
level_list = get_level_list()
first_map(level_list)
settings = settings_logic()
gameDisplay = pygame.display.set_mode((settings.width, settings.height)) 
program_logic()