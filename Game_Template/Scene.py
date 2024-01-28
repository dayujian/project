# -*- coding:utf-8 -*-

import pygame
import random

from enum import Enum
from Settings import *
from NPCs import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *
from Tile import *
from Attributes import Collidable
from Items import *

class Scene():
    def __init__(self, window, win):
        
        self.type = None

        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.cameraX=0
        self.cameraY=0
        self.map_height=WindowSettings.height * WindowSettings.outdoorScale
        self.map_width=WindowSettings.width * WindowSettings.outdoorScale

        
        self.camerax_li=[0]
        self.cameray_li=[0]
        self.delta_cx=0
        self.delta_cy=0

        self.battle_box = None
        self.dialog_box = None
        self.shop_box = None
        self.bag = None
        self.achievement_box = None

        self.map=None
        self.event = None
        self.is_win = win


    
    def trigger_dialog(self, npc):
        self.dialog_box = DialogBox(self.window, npc)

    def end_dialog(self):
        self.dialog_box = None

    def trigger_battle(self, player, monster):
        self.battle_box = BattleBox(self.window, player, monster)

    def end_battle(self):
        self.battle_box = None

    def trigger_shop(self, player, npc):
        self.shop_box = ShoppingBox(self.window, npc, player)

    def end_shop(self):
        self.shop_box = None

    def trigger_bag(self,player):
        self.bag = PlayerBag(self.window,player)

    def end_bag(self):
        self.bag = None

    def trigger_achievement(self, player):
        if self.achievement_box == None:
            self.achievement_box = AchievementBox(self.window, player)
        else:
            self.achievement_box.open = True

    def end_achievement(self):
        self.achievement_box.open = False
    
    def fix_with_bg(self,object):
        object.rect.x -= self.delta_cx
        object.rect.y -= self.delta_cy
        try:
            object.initialPosition -= self.delta_cx
        except:
            pass

    def update_camera(self, player):
        if player.rect.x > WindowSettings.width / 4 * 3:
            self.cameraX += player.speed 
            if self.cameraX >= self.map_width - WindowSettings.width:
                self.cameraX = self.map_width - WindowSettings.width  
        elif player.rect.x < WindowSettings.width / 4 :
            self.cameraX -= player.speed 
            if self.cameraX <= 0:
                self.cameraX = 0

        if player.rect.y > WindowSettings.height / 4 * 3:
            self.cameraY += player.speed 
            if self.cameraY >= self.map_height-WindowSettings.height:
                self.cameraY = self.map_height-WindowSettings.height 
        elif player.rect.y < WindowSettings.height / 4 :
            self.cameraY -= player.speed 
            if self.cameraY <= 0:
                self.cameraY = 0
        self.camerax_li.append(self.cameraX)
        self.cameray_li.append(self.cameraY)
        self.delta_cx=self.camerax_li[-1]-self.camerax_li[-2]
        self.delta_cy=self.cameray_li[-1]-self.cameray_li[-2]
        
        
        

    def render(self, player):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                                 (SceneSettings.tileWidth * i-self.cameraX, 
                                SceneSettings.tileHeight * j-self.cameraY))
        for obstacle in self.obstacles:
            self.fix_with_bg(obstacle)
        for npc in self.npcs:
            self.fix_with_bg(npc)
        for portal in self.portals:
            self.fix_with_bg(portal)
        self.fix_with_bg(player)
        self.obstacles.draw(self.window)
        player.draw(self.window)
        self.npcs.draw(self.window)
        self.portals.draw(self.window)
        if self.dialog_box != None:
            self.dialog_box.draw(self, self.event, pygame.key.get_pressed())
        if self.shop_box != None:
            self.shop_box.draw(self, self.event, pygame.key.get_pressed())
        if self.battle_box != None:
            self.battle_box.draw(self)
        if self.bag != None:
            self.bag.draw(self, self.event, pygame.key.get_pressed())
        if self.achievement_box != None and self.achievement_box.open == True:
            self.achievement_box.draw(self, self.event, pygame.key.get_pressed())

class StartMenu():
    def __init__(self,window,achievement):
        
        
        self.window = window
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))
        
        self.font = pygame.font.Font(None, DialogSettings.textSize)
        self.text = self.font.render("Press ENTER to start",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        self.time = 0
        self.achievement_box = achievement
        


    def render(self):
        
        self.window.blit(self.bg, (0, 0))
        self.time += 1
        if self.time >= 15:
            self.window.blit(self.text, self.textRect)
            if self.time >= 15 * 2:
                self.time = 0

class GameOver:
    def __init__(self, window, player, achievement) -> None:
        self.window = window
        self.bg = pygame.transform.scale(pygame.image.load(GamePath.gameover)
                                         ,(WindowSettings.width, WindowSettings.height))
        self.font = pygame.font.Font(None, DialogSettings.textSize)
        self.text = self.font.render("Press ENTER to restart",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        self.time = 0
        self.score = player.maxHP*7+(player.attack+player.defence)**3+player.money
        self.scoretext = self.font.render(f"Your Score is :{self.score}",
                                True, (255, 255, 255))
        self.scoretextRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 150))
        self.image = pygame.transform.scale(pygame.image.load(GamePath.deadplayer),
                                            (NPCSettings.npcWidth * 4,NPCSettings.npcHeight * 4))
        self.rect = self.image.get_rect(center=(WindowSettings.width //2, WindowSettings.height //4))
        
        self.achievement_box = achievement
    
    def render(self):
        
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.scoretext,self.scoretextRect)
        self.window.blit(self.image,self.rect)
        self.time += 1
        if self.time >= 15:
            self.window.blit(self.text, self.textRect)
            if self.time >= 15 * 2:
                self.time = 0
    
class GameWin:
    def __init__(self, window, player, achievement) -> None:
        self.window = window
        self.bg = pygame.transform.scale(pygame.image.load(GamePath.gamewin)
                                         ,(WindowSettings.width, WindowSettings.height))
        self.font = pygame.font.Font(None, DialogSettings.textSize)
        self.text = self.font.render("Press ENTER to start twice",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2 + 50, 
                                WindowSettings.height - 50))
        self.time = 0
        self.score = player.maxHP*7+(player.attack+player.defence)**3+player.money
        self.scoretext = self.font.render(f"Your Score is :{self.score}",
                                True, (255, 255, 255))
        self.scoretextRect = self.text.get_rect(center=(WindowSettings.width // 2 + 50, 
                                WindowSettings.height - 150))
        
        self.achievement_box = achievement
    
    def render(self):
        
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.scoretext,self.scoretextRect)
        self.time += 1
        if self.time >= 15:
            self.window.blit(self.text, self.textRect)
            if self.time >= 15 * 2:
                self.time = 0

class GameWinTwice:
    def __init__(self, window, player, achievement) -> None:
        self.window = window
        self.bg = pygame.transform.scale(pygame.image.load(GamePath.gamewin2)
                                         ,(WindowSettings.width, WindowSettings.height))
        self.font = pygame.font.Font(None, DialogSettings.textSize)
        self.text = self.font.render("Press ENTER to continue or Press R to reset your game completely",
                                True, (0, 0, 0))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2 + 50, 
                                WindowSettings.height - 50))
        self.time = 0
        self.score = player.maxHP*7+(player.attack+player.defence)**3+player.money
        self.scoretext = self.font.render(f"Your Score is :{self.score}",
                                True, (0, 0, 0))
        self.scoretextRect = self.text.get_rect(center=(WindowSettings.width // 2 + 50, 
                                WindowSettings.height - 150))
        
        self.achievement_box = achievement
    
    def render(self):
        
        self.window.blit(self.bg, (0, 0))
        self.window.blit(self.scoretext,self.scoretextRect)
        self.time += 1
        if self.time >= 15:
            self.window.blit(self.text, self.textRect)
            if self.time >= 15 * 2:
                self.time = 0

class CityScene(Scene):
    def __init__(self, window, win,win_twice):
        super().__init__(window=window,win=win)
        self.win_twice = win_twice
        self.gen_CITY()
        self.type = SceneType.CITY

    def gen_city_map(self):
        images = [pygame.image.load(path).convert() 
              for path in GamePath.cityTiles]
        images = [pygame.transform.scale(image, 
        (SceneSettings.tileWidth, SceneSettings.tileHeight))
        for image in images]

        mapObj = []
        for i in range(SceneSettings.tileXnum):
            tmp = []
            for j in range(SceneSettings.tileYnum):
                tmp.append(images[random.randint(0, len(images) - 1)])
            mapObj.append(tmp)

        return mapObj
    def gen_city_obstacle(self):
        image = pygame.image.load(GamePath.cityWall)

        for i in [0,1,2,SceneSettings.tileXnum-2,SceneSettings.tileXnum-1,SceneSettings.tileXnum-3]:
            for j in range(0,SceneSettings.tileYnum):
                    self.obstacles.add(Tile(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        for j in [0,1,2,SceneSettings.tileYnum-2,SceneSettings.tileYnum-1,SceneSettings.tileYnum-3]:
            for i in range(3,SceneSettings.tileXnum-3):
                    self.obstacles.add(Tile(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    def gen_CITY(self):

        self.map=self.gen_city_map()
        self.gen_city_obstacle()
        if not self.is_win:
            self.npcs.add(DialogNPC(WindowSettings.width//3,WindowSettings.height//4,"智慧的狗子",[['汪',"汪？","汪！！！"],["汪","喵？"]]))
        elif not self.win_twice:
            self.npcs.add(Boss(WindowSettings.width//3,WindowSettings.height//4,"银河舰队首领狗子",[["被你发现了吗？",
                                                                                "我早就知道你会发现 懒惰的开发者不会编写一个无用的npc"]],1000,20,10,500))
        else:
            self.npcs.add(Boss(WindowSettings.width//3,WindowSettings.height//4,"游戏重置工具人狗子",[["二周目通关了很无聊吧",
                                                                                "我存在的意义是让你可以重新开始游 戏"]],500,30,10,500))
        self.npcs.add(ShopNPC(WindowSettings.width//3,2 * WindowSettings.height//4,"会说话的自动贩卖机",{"Attack +1": "Coin -15", "Defence +1": "Coin -15",
             "HP +1": "Coin -15", "???": "HP -5", "Exit": ""}, [["快来买东西"]]))
        self.npcs.add(ShopNPC(WindowSettings.width* 2/3,2 * WindowSettings.height//4,"魔法导师",
                              {Magic("电之哀伤",GamePath.magic[2],"造成2倍伤害,概率使敌人麻痹",{"maxMP":5,"attack":0,"maxHP":0,"defence":0},2):"Coin -45",
                               Magic("火之高兴",GamePath.magic[0],"造成1.5倍伤害，概率烧伤敌人",{"maxMP":10,"attack":0,"maxHP":0,"defence":0},1.5,MP_used=3):"Coin -35","Exit": ""}, 
                               [["只有金钱才能换来魔力"]]))
        self.npcs.add(ShopNPC(WindowSettings.width* 4/5,3 * WindowSettings.height//4,"装备大师",{Weapon("烈焰魔刃",GamePath.weapon[2],"造成火焰伤害",{"maxMP":0,"attack":3,"maxHP":0,"defence":0}):"Coin -45",
                                                                        Weapon("寒霜重斧",GamePath.weapon[0],"造成冰霜伤害",{"maxMP":0,"attack":5,"maxHP":0,"defence":0}):"Coin -55",
                                                                        Equipment("暴烈之甲",GamePath.equipment[0],"反弹20%的伤害",{"maxMP":0,"attack":0,"maxHP":3,"defence":2}):"Coin -45",
                                                                        Equipment("神圣盔甲",GamePath.equipment[1],"10%概率免疫敌方伤害",{"maxMP":0,"attack":0,"maxHP":5,"defence":5}):"Coin -85","Exit": ""}, 
                                                                        [["当你凝视装备时，金钱也凝视着你"]]))
        self.portals.add(Portal(SceneType.WILD))

class WildScene(Scene):
    def __init__(self, window, win):
        super().__init__(window=window,win=win)
        
        self.gen_WILD()
        self.type=SceneType.WILD


    def gen_wild_map(self):

        images = [pygame.image.load(path).convert() 
              for path in GamePath.groundTiles]
        images = [pygame.transform.scale(image, 
        (SceneSettings.tileWidth, SceneSettings.tileHeight))
        for image in images]

        mapObj = []
        for i in range(SceneSettings.tileXnum):
            tmp = []
            for j in range(SceneSettings.tileYnum):
                tmp.append(images[random.randint(0, len(images) - 1)])
            mapObj.append(tmp)

        return mapObj

    def gen_wild_obstacle(self):
        image = pygame.image.load(GamePath.tree)

        midX = WindowSettings.width // 2
        midY = WindowSettings.height // 2

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                if random.random() < SceneSettings.obstacleDensity and \
                    ((i*SceneSettings.tileWidth not in range(midX - 200, midX + 200))\
                    or (j*SceneSettings.tileHeight not in range(midY - 200, midY + 200))):
                    self.obstacles.add(Tile(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))         
    def gen_monsters(self, num=10):
        midX = WindowSettings.width // 2
        midY = WindowSettings.height // 2
        while len(self.npcs.sprites()) < num:
            x = random.randint(0, SceneSettings.tileXnum - 1)
            y = random.randint(0, SceneSettings.tileYnum)
            monster = Monster( x * SceneSettings.tileWidth,
                               y * SceneSettings.tileHeight, "流浪武士",
                              [["拿你试试刀吧"]])
            if x*SceneSettings.tileWidth in range (midX - 200, midX + 200) or y*SceneSettings.tileHeight in range  (midY - 200, midY + 200):
                pass
            else:
                if ( not pygame.sprite.spritecollide(monster, self.portals, False)
                    and not pygame.sprite.spritecollide(monster, self.npcs, False)
                ):
                          self.npcs.add(monster)
    def gen_WILD(self):
        
        self.map=self.gen_wild_map()
        self.gen_wild_obstacle()
        
        self.portals.add(Portal(SceneType.BOSS))
        self.portals.add(Portal(SceneType.CITY,PortalSettings.coordX - WindowSettings.width // 4))
        self.npcs.add(ShopNPC(WindowSettings.width//3,2 * WindowSettings.height//4,
                              "战场德鲁伊",{"Rewound": "Coin -15","Rstore MP": "Coin -15","Exit": ""},[["自然在忽悠着你"]]))
        self.gen_monsters()
        pygame.sprite.groupcollide(self.portals,self.obstacles,False,True)
        pygame.sprite.groupcollide(self.npcs,self.obstacles,False,True)

    


class BossScene(Scene):
    def __init__(self, window, win):
        super().__init__(window=window,win=win)
        self.gen_BOSS()
        self.type = SceneType.BOSS

    def gen_boss_obstacle(self):
        image = pygame.image.load(GamePath.bossWall)

        for i in [0,1,2,SceneSettings.tileXnum-2,SceneSettings.tileXnum-1,SceneSettings.tileXnum-3]:
            for j in range(0,SceneSettings.tileYnum):
                    self.obstacles.add(Tile(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        for j in [0,1,2,SceneSettings.tileYnum-2,SceneSettings.tileYnum-1,SceneSettings.tileYnum-3]:
            for i in range(3,SceneSettings.tileXnum-3):
                    self.obstacles.add(Tile(image, 
                    SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

    def gen_boss_map(self):
        images = [pygame.image.load(path).convert() 
            for path in GamePath.bossTiles]
        images = [pygame.transform.scale(image, 
        (SceneSettings.tileWidth, SceneSettings.tileHeight))
            for image in images]

        mapObj = []
        for i in range(SceneSettings.tileXnum):
            tmp = []
            for j in range(SceneSettings.tileYnum):
                tmp.append(images[random.randint(0, len(images) - 1)])
            mapObj.append(tmp)

        return mapObj

    def gen_BOSS(self):
        self.map=self.gen_boss_map()
        self.gen_boss_obstacle()
        if not self.is_win:
            self.npcs.add(Boss(BossSettings.coordX,BossSettings.coordY,"流浪外星人",[["愚蠢的人类 毁灭吧"]]))
        else:
            self.npcs.add(DialogNPC(BossSettings.coordX + WindowSettings.width // 4,BossSettings.coordY,"流浪外星人",[["狗子骗了你 我才是这个星球的居民",
                                                                                "他们为了资源 要破坏这个星球",
                                                                                "我的家园也被他们摧毁",
                                                                                "这是我用最后的力量 帮你打开的传送门",
                                                                                "你一定要帮我复仇啊"]]))
            self.portals.add(Portal(SceneType.WILD,WindowSettings.width // 4))
            
