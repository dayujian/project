# -*- coding:utf-8 -*-

import sys,time
import pygame

from Player import Player
from Scene import *
from Settings import *
from PopUpBox import *
from NPCs import *
from Attributes import Collidable

class GameManager:
    def __init__(self):
                    
        self.window = pygame.display.set_mode((WindowSettings.width,WindowSettings.height))
        self.name = pygame.display.set_caption(WindowSettings.name)
        self.state = GameState.MAIN_MENU
        self.clock = pygame.time.Clock()
        self.BgmPlayer = BgmPlayer()
        self.scene = StartMenu(self.window,None)
        self.Player = Player(WindowSettings.width//2,WindowSettings.height//2)
        self.NPCTalking = None
        self.time = time.time()
        self.winned = False
        self.WinTwice = False
        self.AchievementBox = AchievementBox(self.window, self.Player)
        self.scene.achievement_box = self.AchievementBox

    def game_reset(self):
        if self.state == GameState.MAIN_MENU:
            self.winned = False
            self.WinTwice = False
            self.Player = Player(WindowSettings.width//2,WindowSettings.height//2)
            self.AchievementBox = AchievementBox(self.window, self.Player)
            self.scene = StartMenu(self.window,self.AchievementBox)
            
        elif self.state == GameState.GAME_PLAY_BOSS:
            self.AchievementBox = self.scene.achievement_box
            self.scene=BossScene(self.window, self.winned)
            self.scene.achievement_box = self.AchievementBox
        else:
            self.AchievementBox = self.scene.achievement_box
            self.scene=CityScene(self.window, self.winned, self.WinTwice)
            self.scene.achievement_box = self.AchievementBox

    # Necessary game components here ↓
    def tick(self, fps):
    
        self.clock.tick(fps)

    def get_time(self):
        return time.time()-self.time

    # Scene-related update functions here ↓
    def flush_scene(self, GOTO:SceneType):
        self.AchievementBox= self.scene.achievement_box
        self.Player.rect.topleft = (WindowSettings.width//2,WindowSettings.height//2)
        if GOTO==SceneType.CITY:
            self.scene=CityScene(self.window, self.winned, self.WinTwice)
        if GOTO==SceneType.WILD:
            self.scene=WildScene(self.window, self.winned)
        if GOTO==SceneType.BOSS:
            self.scene=BossScene(self.window, self.winned)
        self.BgmPlayer.update(GOTO)
        self.scene.achievement_box = self.AchievementBox


        
    def update(self):
        self.clock.tick(30)
        try:
            if self.state == GameState.MAIN_MENU:
                self.update_main_menu(pygame.event.get())
            elif self.state == GameState.GAME_PLAY_CITY:
                self.update_city(pygame.event.get())
            elif self.state == GameState.GAME_PLAY_WILD:
                self.update_wild(pygame.event.get())
            elif self.state == GameState.GAME_PLAY_BOSS:
                self.update_boss(pygame.event.get())
            elif self.state == GameState.GAME_OVER:
                self.update_game_over(pygame.event.get())
            elif self.state == GameState.GAME_WIN:
                self.update_game_win(pygame.event.get())
            elif self.state == GameState.GAME_WIN_TWICE:
                self.update_game_win_twice(pygame.event.get())
        except SystemExit:
            sys.exit()
        except AttributeError:
            pass
        
    def update_main_menu(self,events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.flush_scene(SceneType.CITY)
                    self.state = GameState.GAME_PLAY_CITY

    def update_city(self, events):
        self.scene.event = events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GameEvent.EVENT_SWITCH_TO_BOSS:
                self.flush_scene(SceneType.BOSS)
                self.state = GameState.GAME_PLAY_BOSS
            if event.type == GameEvent.EVENT_SWITCH_TO_WILD:
                self.flush_scene(SceneType.WILD)
                self.state = GameState.GAME_PLAY_WILD
            if event.type == GameEvent.EVENT_SWITCH_TO_CITY:
                self.flush_scene(SceneType.CITY)
                self.state = GameState.GAME_PLAY_CITY
            if event.type == GameEvent.EVENT_DIED:
                self.scene = GameOver(self.window,self.Player,self.scene.achievement_box)
                self.state = GameState.GAME_OVER
            if event.type == GameEvent.EVENT_WIN_TWICE:
                self.WinTwice = True
                self.Player.talking = False
                self.scene = GameWinTwice(self.window,self.Player,self.scene.achievement_box)
                self.state = GameState.GAME_WIN_TWICE
            if event.type == GameEvent.EVENT_DIALOG:
                self.scene.trigger_dialog(self.NPCTalking)
            if event.type == GameEvent.EVENT_BATTLE:
                self.scene.trigger_battle(self.Player,self.NPCTalking)
            if event.type == GameEvent.EVENT_SHOP:
                self.scene.trigger_shop(self.Player,self.NPCTalking)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None):
                    if self.scene.achievement_box == None or self.scene.achievement_box.open == False:
                        self.Player.talking = True
                        self.scene.trigger_bag(self.Player)
                if (event.key == pygame.K_m 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None
                    and self.scene.bag == None):
                    self.Player.talking = True
                    self.scene.trigger_achievement(self.Player)
                    self.AchievementBox = self.scene.achievement_box
        ##### Your Code Here ↓ #####
        self.scene.update_camera(self.Player)
        self.Player.update()
        self.scene.npcs.update()
        ##### Your Code Here ↑ #####
        
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        self.update_collide()
        self.update_achievements()
        ##### Your Code Here ↑ #####

    def update_wild(self, events):
        self.scene.event = events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GameEvent.EVENT_SWITCH_TO_BOSS:
                self.flush_scene(SceneType.BOSS)
                self.state = GameState.GAME_PLAY_BOSS
            if event.type == GameEvent.EVENT_SWITCH_TO_WILD:
                self.flush_scene(SceneType.WILD)
                self.state = GameState.GAME_PLAY_WILD
            if event.type == GameEvent.EVENT_SWITCH_TO_CITY:
                self.flush_scene(SceneType.CITY)
                self.state = GameState.GAME_PLAY_CITY
            if event.type == GameEvent.EVENT_DIED:
                self.scene = GameOver(self.window,self.Player,self.scene.achievement_box)
                self.state = GameState.GAME_OVER
            if event.type == GameEvent.EVENT_DIALOG:
                self.scene.trigger_dialog(self.NPCTalking)
            if event.type == GameEvent.EVENT_BATTLE:
                self.scene.trigger_battle(self.Player,self.NPCTalking)
            if event.type == GameEvent.EVENT_SHOP:
                self.scene.trigger_shop(self.Player,self.NPCTalking)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None):
                    if self.scene.achievement_box == None or self.scene.achievement_box.open == False:
                        self.Player.talking = True
                        self.scene.trigger_bag(self.Player)
                if (event.key == pygame.K_m 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None
                    and self.scene.bag == None):
                    self.Player.talking = True
                    self.scene.trigger_achievement(self.Player)
                    self.AchievementBox = self.scene.achievement_box

        self.scene.update_camera(self.Player)
        self.Player.update()
        self.scene.npcs.update()

        
        # Then deal with regular updates
        self.update_collide()
        self.update_achievements()


    def update_boss(self, events):
        self.scene.event = events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == GameEvent.EVENT_SWITCH_TO_BOSS:
                self.flush_scene(SceneType.BOSS)
                self.state = GameState.GAME_PLAY_BOSS
            if event.type == GameEvent.EVENT_SWITCH_TO_WILD:
                self.flush_scene(SceneType.WILD)
                self.state = GameState.GAME_PLAY_WILD
            if event.type == GameEvent.EVENT_SWITCH_TO_CITY:
                self.flush_scene(SceneType.CITY)
                self.state = GameState.GAME_PLAY_CITY
            if event.type == GameEvent.EVENT_DIED:
                self.scene = GameOver(self.window,self.Player,self.scene.achievement_box)
                self.state = GameState.GAME_OVER
            if event.type == GameEvent.EVENT_WIN:
                self.winned = True
                self.Player.talking = False
                self.scene = GameWin(self.window,self.Player,self.scene.achievement_box)
                self.state = GameState.GAME_WIN
            if event.type == GameEvent.EVENT_DIALOG:
                self.scene.trigger_dialog(self.NPCTalking)
            if event.type == GameEvent.EVENT_BATTLE:
                self.scene.trigger_battle(self.Player, self.NPCTalking)
            if event.type == GameEvent.EVENT_SHOP:
                self.scene.trigger_shop(self.Player,self.NPCTalking)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None):
                    if self.scene.achievement_box == None or self.scene.achievement_box.open == False:
                        self.Player.talking = True
                        self.scene.trigger_bag(self.Player)
                if (event.key == pygame.K_m 
                    and self.scene.battle_box == None
                    and self.scene.shop_box == None
                    and self.scene.dialog_box == None
                    and self.scene.bag == None):
                    self.Player.talking = True
                    self.scene.trigger_achievement(self.Player)
                    self.AchievementBox = self.scene.achievement_box
            
        self.scene.update_camera(self.Player)
        self.Player.update()
        self.scene.npcs.update()
        
        # Then deal with regular updates
        self.update_collide()
        self.update_achievements()


    def update_game_over(self,events):
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = GameState.MAIN_MENU
                    self.game_reset()
    
    def update_game_win(self,events):
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = GameState.GAME_PLAY_BOSS
                    self.game_reset()

    def update_game_win_twice(self,events):
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = GameState.GAME_PLAY_CITY
                    self.game_reset()
                if event.key == pygame.K_r:
                    self.state = GameState.MAIN_MENU
                    self.game_reset()
    # Collision-relate update funtions here ↓
    def update_collide(self):
        
        if pygame.sprite.spritecollide(self.Player, self.scene.obstacles, False):
            self.Player.collidingWith["obstacle"] = True
        else:
            self.Player.collidingWith["obstacle"] = False


        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        for npc in self.scene.npcs:
            if self.scene.dialog_box == None and npc.talking:
                if npc.type == NPCType.DIALOG:
                    npc.talking = False
                    self.Player.talking = False
                    npc.reset_talkCD()
                if npc.type == NPCType.SHOP and self.scene.shop_box == None:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SHOP))
                if npc.type == NPCType.MONSTER and self.scene.battle_box == None:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_BATTLE))
            if pygame.sprite.collide_rect(npc,self.Player):
                self.Player.collidingWith["npc"] = True
                if not npc.talking: 
                    npc.rect = npc.rect.move(-npc.speed * npc.direction,0)
                if npc.can_talk and pygame.key.get_pressed()[pygame.K_RETURN] and not npc.talking:
                    npc.talking = True
                    npc.can_talk = False
                    npc.reset_talkCD()
                    self.Player.talking = True
                    self.NPCTalking = npc
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIALOG))
            
        if all(not self.Player.rect.colliderect(npc.rect) for npc in self.scene.npcs):
                self.Player.collidingWith["npc"] = False
        
            
        
        # Player -> Portals
        for portal in self.scene.portals:
            if pygame.sprite.collide_mask(portal,self.Player):
                self.Player.collidingWith["portal"] = True
                if portal.destination == SceneType.WILD:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_TO_WILD))
                if portal.destination == SceneType.CITY:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_TO_CITY))
                if portal.destination == SceneType.BOSS:
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_SWITCH_TO_BOSS))
        if all(not self.Player.rect.colliderect(portal.rect) for portal in self.scene.portals):
                self.Player.collidingWith["portal"] = False

        if self.Player.is_colliding():
                self.Player.rect = self.Player.rect.move(-self.Player.v_x, -self.Player.v_y)
        self.Player.v_x=0
        self.Player.v_y=0

    def update_achievements(self):
        if self.AchievementBox != None:
            if (self.get_time() // 60) >= 1:
                self.AchievementBox.achievement_list[0].complited = True
            count = 0
            for i in self.Player.item:    
                if str(type(i)) == "<class 'Items.Magic'>":
                    count += 1
            if count >= 2:
                self.AchievementBox.achievement_list[1].complited = True
            if self.Player.blood >= 3:
                self.AchievementBox.achievement_list[2].complited = True
            if self.winned:
                self.AchievementBox.achievement_list[3].complited = True
            if self.WinTwice:
                self.AchievementBox.achievement_list[4].complited = True
            self.scene.achievement_box = self.AchievementBox
            
    # Render-relate update functions here ↓
    def render(self):
            if self.state == GameState.MAIN_MENU:
                self.render_main_menu()
            elif self.state == GameState.GAME_PLAY_CITY:
                self.render_city()
            elif self.state == GameState.GAME_PLAY_WILD:
                self.render_wild()
            elif self.state == GameState.GAME_PLAY_BOSS:
                self.render_boss()
            elif self.state == GameState.GAME_OVER:
                self.render_game_over()
            elif self.state == GameState.GAME_WIN:
                self.render_game_win()
            elif self.state == GameState.GAME_WIN_TWICE:
                self.render_game_win_twice()

    
    def render_main_menu(self):
        
        self.scene.render()
    
    def render_city(self):
        self.scene.render(self.Player)

    def render_wild(self):
        self.scene.render(self.Player)

    def render_boss(self):
        self.scene.render(self.Player)
    
    def render_game_over(self):
        self.scene.render()

    def render_game_win(self):
        self.scene.render()
    
    def render_game_win_twice(self):
        self.scene.render()
