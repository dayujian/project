# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *

class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(img), 
        (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for img in GamePath.player]
        self.index = 0
        self.image = self.images[self.index]
        self.speed = PlayerSettings.playerSpeed
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fliptime = 0
        self.v_x = 0
        self.v_y = 0
        self.talking = False

        self.maxHP = PlayerSettings.playerHP
        self.HP = self.maxHP
        self.attack = PlayerSettings.playerAttack
        self.defence = PlayerSettings.playerDefence
        self.money =  PlayerSettings.playerMoney
        self.maxMP = PlayerSettings.playerMagic
        self.MP = self.maxMP
        
        self.blood = 0
        self.item = []
        self.weapon = None
        self.magic = None
        self.armor = None
    
    def attr_update(self, addCoins = 0, addHP = None, addmaxHP = 0, addAttack = 0, addDefence = 0, addMP = None, addmaxMP = 0, additem = None):
        if self.money + addCoins < 0:
            return
        if self.HP + addmaxHP <= 0:
            return
        if addHP == 0:
            return
        if addMP == 0:
            return
        if additem in self.item:
                return
        self.money += addCoins
        if addHP != None:
            self.HP += addHP
        self.HP += addmaxHP
        self.maxHP += addmaxHP
        self.attack += addAttack
        self.defence += addDefence
        self.maxMP += addmaxMP
        self.MP += addmaxMP
        if addMP != None:
            self.MP += addMP
        if additem != None : 
            self.item.append(additem)
        if addmaxHP < 0:
            self.blood += 1

    def equip(self,item):
        self.attr_update(addmaxHP = item.attr["maxHP"], addAttack = item.attr["attack"], addDefence = item.attr["defence"], addmaxMP = item.attr["maxMP"])
    
    def unequip(self,item):
        if item != None:
            self.attr_update(addmaxHP = -item.attr["maxHP"], addAttack = -item.attr["attack"], addDefence = -item.attr["defence"], addmaxMP = -item.attr["maxMP"])
    
    def achievement_complite(self,achievement):
        self.attr_update(addCoins = achievement.attr["coin"], additem = achievement.attr["item"])

    def reset_pos(self, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.rect.center = (x,y)

    def try_move(self):
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_w] and self.rect.top > 0 :
            self.rect.top -= self.speed
            self.v_y=-self.speed
        if keys[pygame.K_s] and self.rect.bottom < WindowSettings.height:
            self.rect.bottom += self.speed
            self.v_y=+self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            if self.fliptime%2==0:
                self.images=[pygame.transform.flip(image,True,False) for image in self.images]
                self.fliptime+=1
            self.rect.left -= self.speed
            self.v_x=-self.speed
        if keys[pygame.K_d] and self.rect.right < WindowSettings.width:
            if self.fliptime%2==1:
                self.images=[pygame.transform.flip(image,True,False) for image in self.images]
                self.fliptime+=1
            self.rect.right += self.speed
            self.v_x=+self.speed
        


    def update(self, width=PlayerSettings.playerWidth,height=PlayerSettings.playerHeight):
        keys=pygame.key.get_pressed()
        if not self.talking :
            self.try_move()   
                    
            keys=pygame.key.get_pressed()
            if any(key==True for key in [keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]]):
                self.index=self.index+0.5
                self.image=self.images[int(self.index)%len(GamePath.player)]
            else:
                    self.index=0
                    self.image=self.images[self.index]
        else:
            self.index=0
            self.image=self.images[self.index]
            
    def draw(self, window, dx=0, dy=0):       
        self.rect.x -= dx
        self.rect.y -= dy
        window.blit(self.image,self.rect)
