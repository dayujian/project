# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Items import *

class NPC(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y, name):
        # Initialize father classes
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        
        self.can_talk=True
        self.talking = False
        self.talkCD = 0
        self.speed = 0
        self.name = name


    def update(self):
        raise NotImplementedError

    def reset_talkCD(self):

        self.talkCD = NPCSettings.talkCD

    def draw(self, window, dx=0, dy=0):
        self.rect.x -= dx
        self.rect.y -= dy
        window.blit(self.image,self.rect)


class DialogNPC(NPC):
    def __init__(self, x, y, name, dialog):
        super().__init__(x,y,name)
        self.dialog = dialog
        if "狗子" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.npc),
                                (NPCSettings.npcWidth,NPCSettings.npcWidth))
        if "外星人" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.boss),
                                    (BossSettings.width,BossSettings.height))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed = NPCSettings.npcSpeed
        self.initialPosition = x
        self.direction = 1
        self.patrollingRange = NPCSettings.patrollingRange

        self.type=NPCType.DIALOG

    
    def update(self, ticks=0):
        if not self.talking:
            self.rect.x += self.speed * self.direction
            if abs(self.rect.center[0] - self.initialPosition) > NPCSettings.patrollingRange:
                self.direction *= -1  # 反转方向
                self.image = pygame.transform.flip(self.image, True, False)
            if self.talkCD > 0:
                self.talkCD -= 1
            if self.talkCD == 0:
                self.can_talk = True

class ShopNPC(NPC):
    def __init__(self, x, y, name, items, dialog):
        super().__init__(x, y, name)
        if "自动贩卖机" in self.name:
            self.images = [pygame.transform.scale(pygame.image.load(img), (NPCSettings.npcWidth, NPCSettings.npcHeight))
                           for img in GamePath.shop_npc]
            self.index = 0
            self.image = self.images[0]
        if "德鲁伊" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.druid), (NPCSettings.npcWidth, NPCSettings.npcHeight))
        if "魔法" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.magicmaster), (NPCSettings.npcWidth, NPCSettings.npcHeight))
        if "装备" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.weaponmaster), (NPCSettings.npcWidth, NPCSettings.npcHeight))
        self.rect=self.image.get_rect(topleft = (x, y))
        self.dialog = dialog
        self.items = items
        self.time = 0
        self.direction = 1
        
        self.type = NPCType.SHOP

    def update(self, ticks=0):
        if not self.talking:
            self.time += 1
            if (self.time // 100) % 2 == 1 and self.direction == 1 or (self.time // 100) % 2 == 0 and self.direction == -1 :
                if "自动贩卖机" in self.name:
                    self.images=[pygame.transform.flip(image,True,False) for image in self.images]
                    self.direction *= -1
                else:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.direction *= -1
            if self.talkCD > 0:
                self.talkCD -= 1
            if self.talkCD == 0:
                self.can_talk = True
            if "自动贩卖机" in self.name:
                self.index=self.index + 0.5
                self.image=self.images[int(self.index)%len(GamePath.shop_npc)]
                


class Monster(NPC):
    def __init__(self, x, y, name, dialog, HP = 31, Attack = 9, Defence = 1, Money = 15):
        super().__init__(x,y,name)
        self.HP = HP
        self.attack = Attack
        self.defence = Defence
        self.money = Money
        self.image = pygame.transform.scale(pygame.image.load(GamePath.monster),(NPCSettings.npcWidth,NPCSettings.npcHeight))
        self.path = GamePath.monster
        self.rect=self.image.get_rect(topleft=(x,y))
        self.time = 0
        self.dialog = dialog
        self.direction = 1
        self.type = NPCType.MONSTER
        self.monstertype = "enemy"
    
    def update(self):
        if not self.talking:
            self.time += 1
            if (self.time // 100) % 2 == 1 and self.direction == 1 or (self.time // 100) % 2 == 0 and self.direction == -1 :
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction *= -1


class Boss(NPC):
    def __init__(self, x, y, name, dialog, HP = 500, Attack = 30, Defence = 0, Money = 1500):
        super().__init__(x,y,name)
        self.HP = HP
        self.attack = Attack
        self.defence = Defence
        self.money = Money
        if "外星人" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.boss),(BossSettings.width,BossSettings.height))
            self.path = GamePath.boss
            self.magic = Magic("终末的圆弧",GamePath.magic[4])
        if "狗子" in self.name:
            self.image = pygame.transform.scale(pygame.image.load(GamePath.npc),(NPCSettings.npcWidth,NPCSettings.npcHeight))
            self.path = GamePath.npc
            self.magic = Magic("灭世之狐",GamePath.magic[3])
        self.rect=self.image.get_rect(topleft=(x,y))
        self.time = 0
        self.dialog = dialog
        self.direction = 1
        self.type = NPCType.MONSTER
        self.monstertype = "BOSS"
        
        

    def update(self):
        if not self.talking:
            self.time += 1
            if (self.time // 100) % 2 == 1 and self.direction == 1 or (self.time // 100) % 2 == 0 and self.direction == -1 :
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction *= -1
