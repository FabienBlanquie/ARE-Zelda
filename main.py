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


###############################################################################
'''
Settings part
'''

#define settings object
class SettingsObject:
      def __init__(self, width, height):
          self.width = width
          self.height = height
          
#decode json settings in misc folder
def decode_settings():
    with open("misc/settings.json", "r") as read_file:
        settings_data = json.load(read_file)
        return settings_data

#combine the above to return the settings object
def settings_logic():
    settings_data = decode_settings()
    settings = SettingsObject(settings_data["width"],settings_data["height"])
    return settings

###############################################################################
'''
Score part
'''
        
def decode_user_json(name):
    with open(f"save/{name[0]}.json", "r") as read_file:
        user_data = json.load(read_file)
        return user_data["player"]
    
def get_data_list():
    global data_list
    data_list = []
    for user in save_list:
        data = decode_user_json(user)
        data_list.append(data)
    return data_list
        
###############################################################################
'''
User part
'''

#decode usersave json, use the user name in parameter 
def decode_save(name):
    with open(f"save/{name}.json", "r") as read_file:
        save_data = json.load(read_file)
        return save_data["player"]

#return an updated list of all the user save    
def get_save_list():
    global save_list
    name_list = os.listdir('save')
    save_list = []
    for x in name_list:
        name = x.split('.')[0]
        username = (name) 
        save_list.append([username])
    save_list.sort()
    return save_list

#create a new user json, by using the menu data in parameter.
def create_new_user(newgame_menu):
    name = get_data(newgame_menu, "username")
    data = {}
    data['player'] = []
    data['player'].append({
    'username': name,
    'current_level': level_list[0][0]
    })
    with open(f'save/{name}.json', 'w+') as f:
        json.dump(data, f)

#update(rewrite) the current user with the level name in parameter      
def update_user_next_level(level):
    data = {}
    data['player'] = []
    data['player'].append({
    'username': current_username,
    'current_level': level
    })
    with open(f'save/{current_username}.json', 'w+') as f:
        json.dump(data, f)
    
###############################################################################
'''
Level part
'''

#Decode the csv file containing the map matrix
def decode_csv(fileName):
    initial_matrix = []
    with open(fileName, "r") as file:
        for line in file :
            data = line.replace('\n', '').split(",")
            data = [int(i) for i in data]
            initial_matrix.append(data)
    file.close
    return initial_matrix

#return a list of levels from the map folder
def get_level_list():
    name_list = os.listdir('map')
    level_list = []
    for x in name_list:
        name = x.split('.')[0]
        level = (name) 
        level_list.append([level])
    level_list.sort()
    return level_list

#used to unnest the level list
def flattened_list(mylist):
    flat_list = []
    for sublist in mylist:
        for item in sublist:
            flat_list.append(item)
    return flat_list

#Select the map to play, update global current_map with the new matrix
def set_map(value):
    global current_map
    current_map = []
    global current_level
    current_level = value[0]
    filename = f"map/{value[0]}.csv"
    matrix = decode_csv(filename)
    for line in matrix:
        current_map.append(line)
        
#used  as default value to prevent crash if the user tap "Play" without using the custom map selection
def first_map(level_list):
    global current_map
    current_map = []
    global current_level
    current_level = level_list[0][0]
    filename = f"map/{level_list[0][0]}.csv"
    matrix = decode_csv(filename)
    for line in matrix:
        current_map.append(line)

#load the next file by retreving the current index position from flat_list, and incrementing. 
def next_level():
    user = decode_save(current_username)
    user_map = (user[0]["current_level"],0)
    next_map = flat_list.index(user_map[0])
    next_map = next_map + 1
    next_map2 = (flat_list[next_map],0)
    set_map(next_map2)
    update_user_next_level(flat_list[next_map])
    LoadedWorld()
    GameMain().main_loop()
    
#convert the matrix into the differents object in the game
def map_convertor(matrix, game):
    #contains the differents objects founds in the map
    object_map = []
    #contains the differents hostiles founds in the map
    mob_map = []
    row_index = 0
    value_index = 0
    #Image asset resized 
    BushImg = pygame.image.load("overworld/bush.png")
    BushImg = pygame.transform.scale(BushImg, (55, 55))
    StoneWallImg = pygame.image.load("overworld/wall.png")
    StoneWallImg = pygame.transform.scale(StoneWallImg, (55, 55))
    FireCampImg = pygame.image.load("overworld/firecamp.png")
    FireCampImg = pygame.transform.scale(FireCampImg, (55, 55))
    DoorImg = pygame.image.load("overworld/door.png")
    DoorImg = pygame.transform.scale(DoorImg, (55, 55))
    for row in matrix:
        value_index = 0
        for value in row:
            #Wall with a Bush skin
            if value == -1:
                object_map.append(Wall(value_index*55, row_index*55, BushImg))
            #Wall with a Stone wall skin
            if value == -2:
                object_map.append(Wall(value_index*55, row_index*55, StoneWallImg))
            #Wall with a firecamp skin
            if value == 1:
                object_map.append(Wall(value_index*55, row_index*55, FireCampImg))
            #wall with a door skin
            if value == 2:
                object_map.append(Wall(value_index*55, row_index*55, DoorImg))
            #Add a Skeleton mob (hostile)
            if value == 22:
                mob_map.append(Mob(value_index*55, row_index*55, 3, game))
            #add a Boss (hostile)
            if value == 55:
                mob_map.append(Boss(value_index*55, row_index*55, 50, game))
            #define player position
            if value == 0:
                player_starting_position[0] = Player(value_index*55, row_index*55,"UP",False,False,False,False,False)
            value_index = value_index + 1
        row_index = row_index + 1
    return object_map, mob_map
    
###############################################################################
'''
Menu part
'''
            
def menu():
    '''
    def containing the main menu and his submenu
    '''
    
    #score submenu
    score_menu = pygame_menu.Menu(settings.height, settings.width, 'Score', theme=pygame_menu.themes.THEME_DARK)
    for data in data_list:
        username = data[0]["username"]
        level = data[0]["current_level"]
        score_menu.add_label(f"{username} Level : {level}")
    score_menu.add_label("")
    score_menu.add_button('Back', pygame_menu.events.BACK)
    
    #settings submenu
    settings_menu = pygame_menu.Menu(settings.height, settings.width, 'Settings', theme=pygame_menu.themes.THEME_DARK)
    for attr, value in settings.__dict__.items():
        settings_menu.add_text_input(f"{attr} : ", default= value)
    settings_menu.add_label("z : up")
    settings_menu.add_label("s : down")
    settings_menu.add_label("q : left")
    settings_menu.add_label("d : right")
    settings_menu.add_label("spacebar : attack")
    settings_menu.add_label("")
    settings_menu.add_button('Back', pygame_menu.events.BACK)
    
    #custom submenu
    custom_menu = pygame_menu.Menu(settings.height, settings.width, 'Settings', theme=pygame_menu.themes.THEME_DARK)
    custom_menu.add_selector('Level Selection :', level_list, selector_id = "map")
    custom_menu.add_button('Play', custom_game, custom_menu)
    custom_menu.add_label("")
    custom_menu.add_button('Back', pygame_menu.events.BACK)

    #new game submenu
    newgame_menu = pygame_menu.Menu(settings.height, settings.width, 'Settings', theme=pygame_menu.themes.THEME_DARK)
    newgame_menu.add_text_input('Name :', default='John Doe', textinput_id = "username" )
    newgame_menu.add_button('Play', new_game, newgame_menu)
    newgame_menu.add_label("")
    newgame_menu.add_button('Back', pygame_menu.events.BACK)

    #load game submenu
    loadgame_menu = pygame_menu.Menu(settings.height, settings.width, 'Load game', theme=pygame_menu.themes.THEME_DARK)
    loadgame_menu.add_selector('User Selection :', save_list, selector_id = "save")
    loadgame_menu.add_button('Play', load_game, loadgame_menu)
    loadgame_menu.add_label("")
    loadgame_menu.add_button('Back', pygame_menu.events.BACK)
    
    #main menu
    menu = pygame_menu.Menu(settings.height, settings.width, 'Souls', theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('New Game', newgame_menu)
    menu.add_button('Load Game', loadgame_menu)
    menu.add_button('Custom Game', custom_menu)
    menu.add_button('High Score', score_menu)
    menu.add_button('Settings', settings_menu)
    menu.add_button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(gameDisplay)
  
#used to get value data from a menu
def get_data(menu, value):
    data = menu.get_input_data()
    return data[value]

#if we choose new game,we update current_username, create a new user, load the first map and start to play        
def new_game(menu):
    create_new_user(menu)
    global current_username
    current_username = get_data(menu, "username")
    first_map(level_list)
    LoadedWorld()
    GameMain().main_loop()
  
#if we choose to load a game, we update current_username, decode the associated name and load the associated map to play
def load_game(menu):
    global current_username
    current_username = get_data(menu, "save")[0]
    user = decode_save(current_username)
    #set_map need a slice, so we create one
    user_map = (user[0]["current_level"],0)
    set_map(user_map)
    LoadedWorld()
    GameMain().main_loop()

#free map selection    
def custom_game(menu):
    set_map(get_data(menu, "map"))
    LoadedWorld()
    GameMain().main_loop()
    
###############################################################################
'''
Objects used for the game
'''
#Class used for the walls
class Wall(pygame.sprite.Sprite):
    
    def __init__(self,x,y,image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#class used for the world list         
class World(object):
    wall_list = None
    def __init__(self):
        self.wall_list = pygame.sprite.Group()
        self.mobs_list = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

#used to load the world with the list and map convertor                    
class LoadedWorld(World):
    def __init__(self):
        World.__init__(self)
        walls, mobs = map_convertor(current_map, self)        
        for wall in walls:
            self.wall_list.add(wall)
        for mob in mobs:
            mob.walls = self.wall_list
            self.mobs_list.add(mob)

#main class for the game           
class GameMain():
    done = False
    def __init__(self):
        self.width, self.height = settings.width, settings.height
        self.color_red = 222
        self.color_green = 184
        self.color_blue = 135
        self.player = player_starting_position[0]     
        self.all_sprite_list = pygame.sprite.Group()
        self.all_sprite_list.add(self.player)
        self.clock = pygame.time.Clock()
        self.current_x = 0
        self.current_y = 0
        #load world
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
            self.end_of_level()
            self.current_room.projectiles.update()
            self.all_sprite_list.update()
            projectile_hit_list = self.current_room.projectiles
            for projectile in projectile_hit_list:
                    if pygame.sprite.collide_rect(self.player, projectile) and self.player.action == "attacking":
                        projectile.kill()
                    elif pygame.sprite.collide_rect(self.player, projectile) and self.player.action == "walking":
                        self.player.kill()
                    elif pygame.sprite.spritecollideany(projectile,self.player.walls):
                        projectile.kill()
    
    #draw the diffrents sprite on screen        
    def draw(self):
        self.screen.fill((self.color_red, self.color_green, self.color_blue))
        self.all_sprite_list.draw(self.screen)
        self.current_room.wall_list.draw(self.screen)
        self.current_room.projectiles.draw(self.screen)
        self.current_room.mobs_list.draw(self.screen)
        pygame.display.flip()
        
    def end_of_level(self):
        #when all the monster are killed and we haven't finished the game yet, start the next level
        if not self.current_room.mobs_list and (flat_list.index(current_level) != (len(flat_list)-1)):
            self.done = True
            next_level()
        #if we have killed all the monster and reached the last level, return to the main screen
        if not self.current_room.mobs_list and (flat_list.index(current_level) == (len(flat_list)-1)):
            self.done = True
            
    #handle player input                 
    def handle_events(self):
        for event in pygame.event.get():
            #close the game if we close the game windows
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN and self.player.can_move == True:
                if event.key == pygame.K_ESCAPE:
                    self.done = True
                    get_save_list()
                    get_data_list()
                    menu()
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
                        self.player.rect.x -= 15
                    elif self.player.DIRECTION == self.player.UP:
                        self.player.image = self.player.attack_up
                        self.player.rightKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.rect.y -= 15
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
            #action when the player keys is released            
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
                        self.player.rect.x += 15
                    if self.player.DIRECTION == self.player.UP:
                        self.player.image = self.player.up_walk[0]
                        self.player.downKeyPressed = False
                        self.player.upKeyPressed = False
                        self.player.leftKeyPressed = False
                        self.player.rightKeyPressed = False
                        self.player.rect.y += 15
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
        self.WALKRATE = 9
        self.RIGHT, self.LEFT, self.UP, self.DOWN = "right left up down".split()
        self.action = 'walking'
    
#handle player direction and input
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

#class used to define the mob attribute          
class Mob(pygame.sprite.Sprite):
    def __init__(self,x,y,hitpoint, game):
        #left animation walkcycle
        self.left1 = pygame.image.load("mob/skell/q/1.png")
        self.left2 = pygame.image.load("mob/skell/q/2.png")
        self.left_walk = [self.left1,self.left2]
        #down animation walkcycle
        self.down1 = pygame.image.load("mob/skell/s/1.png")
        self.down2 = pygame.image.load("mob/skell/s/2.png")
        self.down_walk = [self.down1, self.down2]
        #right animation walkcycle
        self.right1 = pygame.image.load("mob/skell/d/1.png")
        self.right2 = pygame.image.load("mob/skell/d/2.png")
        self.right_walk = [self.right1, self.right2]
        #up animation walkcycle
        self.up1 = pygame.image.load("mob/skell/z/1.png")
        self.up2 = pygame.image.load("mob/skell/z/2.png")
        self.up_walk = [self.up1, self.up2]

        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0,0,48,48)
        self.image = pygame.image.load("mob/skell/s/1.png")
        self.rect.x = x
        self.rect.y = y
        self.current_frame = 0
        self.walk_anim_frame = 0
        self.hitpoint = hitpoint
        self.x_change = 1
        self.t = 0
        self.timer = random.randint(60,180)
        self.projectile_timer = random.randint(0,120)
        self.projectile_t = 0
        self.randomDirections = ["up", "down","left","right"]
        self.randomnumber = random.randint(0,3)
        self.direction = self.randomDirections[self.randomnumber]
        self.walls = None
        self.doors = None
        self.game = game
        self.x_change = 1
        self.y_change = 1
        self.anim_ticker = 0
    
    #handle direction and action    
    def update(self):
        if self.direction == "right":
            self.image = self.right_walk[self.walk_anim_frame]
            self.rect.x += self.x_change
            wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
            for wall in wall_hit_list:
                self.rect.right = wall.rect.left
                self.direction = self.randomDirections[2]
            self.t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(60,240)
            self.projectile_t += 1
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(60,240)
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(60,240)
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(60,240)
            if self.t == self.timer:
                self.direction = self.randomDirections[random.randint(0,3)]
                self.t = 0  
        if self.hitpoint <= 0:
            self.kill()     
        self.anim_ticker += 1
        if self.anim_ticker % 10 == 0:
            self.walk_anim_frame = (self.walk_anim_frame + 1) % 2
 
#class used to define the mob projectile                   
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
        self.rect.x = int(x)
        self.rect.y = int(y)
        
    def update(self):
        if self.direction == "right":
            self.rect.x += 6
        elif self.direction == "left":
            self.rect.x -= 6
        elif self.direction == "up":
            self.rect.y -= 6
        elif self.direction == "down":
            self.rect.y += 6

#class used to define the boss attribute        
class Boss(pygame.sprite.Sprite):
    def __init__(self,x,y,hitpoint, game):
        #left animation walkcycle
        self.left1 = pygame.image.load("mob/boss/q/1.png")
        self.left2 = pygame.image.load("mob/boss/q/2.png")
        self.left_walk = [self.left1,self.left2]
        #down animation walkcycle
        self.down1 = pygame.image.load("mob/boss/s/1.png")
        self.down2 = pygame.image.load("mob/boss/s/2.png")
        self.down_walk = [self.down1, self.down2]
        #right animation walkcycle
        self.right1 = pygame.image.load("mob/boss/d/1.png")
        self.right2 = pygame.image.load("mob/boss/d/2.png")
        self.right_walk = [self.right1, self.right2]
        #up animation walkcycle
        self.up1 = pygame.image.load("mob/boss/z/1.png")
        self.up2 = pygame.image.load("mob/boss/z/2.png")
        self.up_walk = [self.up1, self.up2]
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mob/boss/d/1.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_frame = 0
        self.walk_anim_frame = 0
        self.hitpoint = hitpoint
        self.x_change = 1
        self.t = 0
        self.timer = random.randint(60,180)
        self.projectile_timer = random.randint(0,60)
        self.projectile_t = 0
        self.randomDirections = ["up", "down","left","right"]
        self.randomnumber = random.randint(0,3)
        self.direction = self.randomDirections[self.randomnumber]
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
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x , self.rect.y + (self.rect.y/2), self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x , self.rect.y + (self.rect.y/3), self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(30,60)
            self.projectile_t += 1
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x , self.rect.y + (self.rect.y/2), self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x , self.rect.y + (self.rect.y/3), self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(30,60)
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x + (self.rect.x/2), self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x + (self.rect.x/3), self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(30,60)
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
            self.projectile_t += 1
            if self.projectile_t >= self.projectile_timer:
                self.game.projectiles.add(MobProjectile(self.rect.x, self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x + (self.rect.x/2), self.rect.y, self.direction))
                self.game.projectiles.add(MobProjectile(self.rect.x + (self.rect.x/3), self.rect.y, self.direction))
                self.projectile_t = 0
                self.projectile_timer = random.randint(30,60)
            if self.t == self.timer:
                self.direction = self.randomDirections[random.randint(0,3)]
                self.t = 0  
        if self.hitpoint <= 0:
            self.kill()     
        self.anim_ticker += 1
        if self.anim_ticker % 10 == 0:
            self.walk_anim_frame = (self.walk_anim_frame + 1) % 2
   
###############################################################################
'''
Player Animation Walkcycle
'''
    
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

###############################################################################
'''
Program logic and global var
'''
def program_logic():
    pygame.init()
    menu()
    
#contain the list of all users saves
save_list = []
#contain user data
data_list = []
#contain current map matrix
current_map = []
#contain current level name
current_level = ""
#contain current username, with a default value to prevent crash
current_username = "John Doe"
#initial valu of the player starting position, with a default value to prevent crash
player_starting_position = [[0,0]]
   
#global level_list, contains levels name
level_list = get_level_list()
#level list un-nested
flat_list = flattened_list(level_list)
#load save for the menu
get_save_list()
#get data to display on the score menu
get_data_list()
#get inititals settings for the windows
settings = settings_logic()
gameDisplay = pygame.display.set_mode((settings.width, settings.height)) 
program_logic()
