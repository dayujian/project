# -*- coding:utf-8 -*-

import pygame
import random

from typing import *
from Settings import *
from Items import *

class DialogBox:
    def __init__(self, window, npc,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window=window
        self.npc=npc
        self.texts=npc.dialog
        self.fontSize=fontSize
        self.fontColor=fontColor
        self.text_surf_li=[]
        self.text_rect_li=[]
        self.random_num=random.randint(0,len(self.texts)-1)
        self.click_time=0
        self.bg=pygame.Surface((DialogSettings.boxWidth,
                                DialogSettings.boxHeight),pygame.SRCALPHA)
        self.bg.fill(bgColor)
    def draw(self,scene, events, keys):
        text_font=pygame.font.Font(GamePath.font,self.fontSize)
        self.window.blit(self.bg,(DialogSettings.boxStartX,DialogSettings.boxStartY))
        npc_image=self.npc.image
        npc_image=pygame.transform.scale(npc_image,(DialogSettings.npcWidth,DialogSettings.npcHeight))
        npc_rect=npc_image.get_rect(topleft=(DialogSettings.npcCoordX,DialogSettings.npcCoordY))
        self.window.blit(npc_image,npc_rect)
        name=self.npc.name
        text_serf=text_font.render(name,True,self.fontColor)
        text_rect=text_serf.get_rect()
        text_rect.topleft=(DialogSettings.textStartX, DialogSettings.textStartY- 2 * DialogSettings.textVerticalDist)
        self.window.blit(text_serf, text_rect)
        for event in events:
            if keys[pygame.K_RETURN] and event.type == pygame.KEYDOWN:
                self.click_time+=1
        for j in range(0,len(self.texts[self.random_num])):
            if j==self.click_time:
                sub_text=self.texts[self.random_num][j].split()
                time = 0
                for text in sub_text:
                    text_serf=text_font.render(text,True,self.fontColor)
                    text_rect=text_serf.get_rect()
                    text_rect.topleft=(DialogSettings.textStartX,DialogSettings.textStartY+DialogSettings.textVerticalDist*time)
                    self.text_rect_li.append(text_rect)
                    self.text_surf_li.append(text_serf)
                    time+=1
                for i in range(0,len(self.text_rect_li)):
                    self.window.blit(self.text_surf_li[i],self.text_rect_li[i])
                self.text_rect_li=[]
                self.text_surf_li=[]
        if self.click_time == len(self.texts[self.random_num]):
            scene.end_dialog()

class BattleBox:
    def __init__(self, window, player, monster, fontSize: int = BattleSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), bgColor: Tuple[int, int, int, int] = (0, 0, 0, 200)) :
                
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None, self.fontSize)

        self.bg = pygame.Surface((BattleSettings.boxWidth,
            BattleSettings.boxHeight), pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.player = player
        self.playerHP = player.HP
        self.playerMP = player.MP
        self.playerImg = pygame.transform.scale(pygame.image.load(GamePath.player[0]), 
            (BattleSettings.playerWidth, BattleSettings.playerHeight))
        
        self.playerX = BattleSettings.playerCoordX
        self.playerY = BattleSettings.playerCoordY
       
        self.monster = monster
        self.monsterHP = monster.HP
        self.monsterImg = pygame.image.load(monster.path)
        self.monsterImg = pygame.transform.scale(pygame.transform.flip((self.monsterImg),True,False),
            (BattleSettings.monsterWidth, BattleSettings.monsterHeight))
        
        self.monsterX = BattleSettings.monsterCoordX
        self.monsterY = BattleSettings.monsterCoordY
        self.MonsterCondition = []

        self.attacker = 0

        self.isPlayingAnimation = True
        self.currentAnimationCount = 0

        self.dir = 1

        self.isFinished = False

        self.random_number = None

        self.pressE = False
        self.pressQ =False

        self.bloodingNumber = [0, 0]


    def keye(self):
        if pygame.key.get_pressed()[pygame.K_e]:
            self.pressE = True
        elif pygame.key.get_pressed()[pygame.K_q]:
            self.pressQ = True



    def draw(self, Scene):
        self.window.blit(self.bg, (BattleSettings.boxStartX,
                                   BattleSettings.boxStartY))
        self.window.blit(self.playerImg, (self.playerX,
                                          self.playerY))
        self.window.blit(self.monsterImg, (self.monsterX,
                                           self.monsterY))
       
        
        text = "player HP: " + str(self.playerHP)
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.textPlayerStartX, BattleSettings.textStartY))

        text = "monster HP: " + str(self.monsterHP)
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.textMonsterStartX, BattleSettings.textStartY))

        text = "player MP: " + str(self.playerMP)
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.textPlayerStartX, BattleSettings.textStartY + BattleSettings.textVerticalDist))

        if self.MonsterCondition != []:
            text = "Monster Conditions: " + self.MonsterCondition[0]
        else:
            text = "Monster Conditions: "
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.monsterCoordX - 2 * BattleSettings.textVerticalDist,
        BattleSettings.textStartY + BattleSettings.textVerticalDist))
        for i in range(1, len(self.MonsterCondition)):
            text =self.MonsterCondition[i]
            self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.monsterCoordX + 4 * BattleSettings.textVerticalDist,
        BattleSettings.textStartY + (i+1) * BattleSettings.textVerticalDist))

        text = "Press E for Physical attack"
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.playerCoordX, BattleSettings.textStartY - BattleSettings.textVerticalDist))

        text = "Press Q for Magic Attack"
        self.window.blit(self.font.render(text, True, self.fontColor),
        (BattleSettings.monsterCoordX - 2 * BattleSettings.textVerticalDist,
          BattleSettings.textStartY - BattleSettings.textVerticalDist))

        if self.currentAnimationCount == 0:
            self.keye()

        if self.isPlayingAnimation:
            if self.pressE:
                self.pressQ = False
                damage_ability=1          
                if self.currentAnimationCount < BattleSettings.animationCount:
                    currentDir = self.dir
                else:
                    currentDir = self.dir * -1
                if self.attacker == 0:
                    self.playerX += currentDir * BattleSettings.stepSize
                    if self.player.weapon != None:
                        if self.player.weapon.name == "烈焰魔刃" and "burning" not in self.MonsterCondition:
                            self.MonsterCondition.append("burning")
                        if self.player.weapon.name == "寒霜重斧" and "frostbite" not in self.MonsterCondition:
                            self.MonsterCondition.append("frostbite")

                if self.attacker == 1 and 'paralysis' not in self.MonsterCondition:
                    if self.monster.monstertype == "enemy":
                            self.monsterX += currentDir * BattleSettings.stepSize
                    else:
                        self.monster.magic.cast_spell(self.window, BattleSettings.playerCoordX, BattleSettings.playerCoordY)

                self.currentAnimationCount += 1

                if self.currentAnimationCount == BattleSettings.animationCount * 2:
                    self.isPlayingAnimation = False
                    self.currentAnimationCount = 0

            elif self.pressQ and self.playerMP>=0:
                self.pressE = False
                if self.player.magic == None:
                    text = "You don't know how to use magic"
                    self.window.blit(self.font.render(text, True, self.fontColor),
                            (BattleSettings.textStartX, 
                            BattleSettings.textStartY - 2*BattleSettings.textVerticalDist))
                    self.pressQ = False
                elif (self.player.magic.use_time == self.player.magic.use_max_time and self.attacker == 0 
                      and self.player.magic.use_max_time != 0):
                    text = "warning : your magic has been used up"
                    self.window.blit(self.font.render(text, True, self.fontColor),
                                 (BattleSettings.textStartX-100, 
                            BattleSettings.textStartY - 2*BattleSettings.textVerticalDist))
                    self.pressQ = False
                    
                elif self.playerMP - self.player.magic.MP_used < 0:
                    text = "warning : your have no MP to use it"
                    self.window.blit(self.font.render(text, True, self.fontColor),
                                 (BattleSettings.textStartX-100, 
                            BattleSettings.textStartY - 2*BattleSettings.textVerticalDist))
                    self.pressQ = False
                else:
                    damage_ability=self.player.magic.attack
                    if self.currentAnimationCount < BattleSettings.animationCount:
                        currentDir = self.dir
                    else:
                        currentDir = self.dir * -1

                    if self.attacker == 0 :
                        self.player.magic.cast_spell(self.window)
                        if "火" in self.player.magic.name and 'blooding' not in self.MonsterCondition:
                            self.random_number = random.randint(0,1)
                            if self.random_number == 0 : 
                                self.MonsterCondition.append("blooding")
                        if "电" in self.player.magic.name and 'paralysis' not in self.MonsterCondition:
                            self.random_number = random.randint(0,1)
                            if self.random_number == 0 : 
                                self.MonsterCondition.append("paralysis")
                        if "灼热" in self.player.magic.name:
                            if 'paralysis' not in self.MonsterCondition:
                                self.MonsterCondition.append("paralysis")
                            if 'burning' not in self.MonsterCondition:
                                self.MonsterCondition.append("burning")
                    if self.attacker == 1 and 'paralysis' not in self.MonsterCondition:
                        if self.monster.monstertype == "enemy":
                            self.monsterX += currentDir * BattleSettings.stepSize
                        else:
                            self.monster.magic.cast_spell(self.window, BattleSettings.playerCoordX, BattleSettings.playerCoordY)
                    self.currentAnimationCount += 1

                    if self.currentAnimationCount == BattleSettings.animationCount * 2:
                        self.isPlayingAnimation = False
                        self.currentAnimationCount = 0
                
        if not self.isFinished and not self.isPlayingAnimation:
            if self.attacker == 0:
                if self.pressQ :
                    self.playerMP = self.playerMP - self.player.magic.MP_used
                    self.player.magic.use_time += 1
                self.monsterHP = max(0, self.monsterHP - 
                            max(0,(self.player.attack * damage_ability - self.monster.defence)))
                if self.player.weapon != None:
                    if self.player.weapon.name == "嗜血匕首":
                        self.playerHP += max(0,(self.player.attack * damage_ability - self.monster.defence))
                self.attacker = 1
                self.dir = -1
                

            else:
                if 'paralysis' not in self.MonsterCondition:
                    if self.player.armor != None:
                        if self.player.armor.name == "神圣盔甲":
                            self.random_number = random.randint(0,9)
                        else:
                            self.random_number = 1
                        if self.random_number != 0:
                            self.playerHP = max(0, self.playerHP - 
                                                max(0,(self.monster.attack - self.player.defence)))
                            if self.player.armor.name == "暴烈之甲":
                                self.monsterHP = max(0, self.monsterHP - 
                                                max(0,(self.monster.attack - self.player.defence)) // 5)
                            if self.player.armor.name == "法师之甲":
                                self.playerMP += max(0,(self.monster.attack - self.player.defence))
                    else:
                        self.playerHP = max(0, self.playerHP - 
                                                max(0,(self.monster.attack - self.player.defence)))
                if any(condition in self.MonsterCondition for condition in ["burning","frostbite"]):
                    self.monsterHP = max(0,self.monsterHP - self.monster.HP // 8)
                if 'blooding' in self.MonsterCondition:
                    self.monsterHP = max(0,self.monsterHP - self.monster.HP // 8)
                self.attacker = 0
                self.dir = 1

                new_list = []
                for i in range(0,len(self.MonsterCondition)):#移除异常
                    if self.MonsterCondition[i] in ['blooding',"burning","frostbite"]:
                        self.random_number = random.randint(0,1)
                        if self.random_number != 0:
                            if self.MonsterCondition[i] == 'blooding':
                                self.bloodingNumber[0] += 1
                                if self.bloodingNumber[0] == 3 :
                                    self.bloodingNumber[0] = 0
                                else:
                                    new_list.append(self.MonsterCondition[i])
                            else:
                                self.bloodingNumber[1] += 1
                                if self.bloodingNumber[1] == 3 :
                                    self.bloodingNumber[1] = 0
                                else:
                                    new_list.append(self.MonsterCondition[i])
                    else :
                        self.random_number = random.randint(0,1)
                        if self.random_number != 0:
                            new_list.append(self.MonsterCondition[i])
                self.MonsterCondition = new_list
                new_list = []
            
            self.isPlayingAnimation = True
            if self.pressQ:
                self.player.magic.time = 0
                self.player.magic.image = self.player.magic.images[0]
            if self.attacker == 0:
                self.pressQ = False
                self.pressE = False
            if self.monster.monstertype != "enemy":
                self.monster.magic.time = 0
                self.monster.magic.image = self.monster.magic.images[0]
            
            
                    
        
        if self.playerHP == 0 or self.monsterHP == 0:
            if self.monsterHP == 0:
                text = "You winwinwin!"
                self.window.blit(self.font.render(text, True, self.fontColor),
                        (BattleSettings.textStartX, 
                         BattleSettings.textStartY - 2*BattleSettings.textVerticalDist))
                self.monster.kill()
                self.player.HP = min(self.playerHP,self.player.maxHP)
                self.player.MP = min(self.playerMP,self.player.maxMP)
                if self.player.magic != None:
                    self.player.magic.use_time = 0
            else:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_DIED))
            self.isFinished = True
            self.isPlayingAnimation = False
            
        
        if self.isFinished and pygame.key.get_pressed()[pygame.K_RETURN]:
            self.player.talking = False
            self.player.money += self.monster.money
            if self.monster.name == "流浪外星人":
                    pygame.event.post(pygame.event.Event(GameEvent.EVENT_WIN))
            if "狗子" in self.monster.name:
                pygame.event.post(pygame.event.Event(GameEvent.EVENT_WIN_TWICE))
            self.monster.kill()
            Scene.end_battle()


class ShoppingBox:
    def __init__(self, window, npc, player,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(GamePath.font, self.fontSize)
        
        self.bg = pygame.Surface((ShopSettings.boxWidth+100, 
                                  ShopSettings.boxHeight+100),pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npc = npc
        self.npc_image = pygame.transform.scale(self.npc.image,
                (DialogSettings.npcWidth, DialogSettings.npcHeight))
        
        self.player = player
        self.items = npc.items

        self.selectedID = 0

    def buy(self):
        items = list(self.items.keys())
        try :
            cost = self.items[items[self.selectedID]].split()[1]
            value = items[self.selectedID].split()[1]
        except:
            pass
        if str(type(items[self.selectedID])) != "<class 'str'>" :
            if self.items[items[self.selectedID]].split()[0] == "Coin":
                self.player.attr_update(addCoins = int(cost),
                                         additem = items[self.selectedID])
        else:
            if items[self.selectedID].split()[0] == "Attack" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            addAttack = int(value))
            if items[self.selectedID].split()[0] == "Defence" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            addDefence = int(value))
            if items[self.selectedID].split()[0] == "HP" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            addmaxHP = int(value))
            if items[self.selectedID].split()[0] == "???" :
                if self.items[items[self.selectedID]].split()[0] == "HP":
                    self.player.attr_update(addmaxHP = int(cost))
            if items[self.selectedID].split()[0] == "Rewound" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            addHP = self.player.maxHP - self.player.HP)
            if items[self.selectedID] == "Rstore MP" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            addMP = self.player.maxMP - self.player.MP)
            if str(type(items[self.selectedID])) != "<class 'str'>" :
                if self.items[items[self.selectedID]].split()[0] == "Coin":
                    self.player.attr_update(addCoins = int(cost),
                                            additem = items[self.selectedID])



    def draw(self, scene, events, keys):
        if self.npc.talking:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_w]:
                        self.selectedID = max(0, self.selectedID - 1)
                    elif keys[pygame.K_s]:
                        self.selectedID = min(len(self.items) - 1, self.selectedID + 1)
                    elif keys[pygame.K_RETURN]:
                        if self.selectedID == len(self.items.keys()) - 1:
                            self.npc.talking = False
                            self.npc.reset_talkCD() 
                            self.player.talking = False
                            scene.end_shop()
                        else:
                            self.buy() 
            self.window.blit(self.bg, 
                (ShopSettings.boxStartX, ShopSettings.boxStartY))
            self.window.blit(self.npc_image,
                (DialogSettings.npcCoordX, DialogSettings.npcCoordY))
            
            offset = 0
            for id, item in enumerate(list(self.items.keys())):
                if str(type(item)) == "<class 'str'>":
                    if id == self.selectedID:
                        text = '-->' + item + ' ' + self.items[item]
                    else:
                        text = '      ' + item + ' ' + self.items[item]
                else:
                    if id == self.selectedID:
                        text = '-->' + item.name + ' ' + self.items[item]
                    else:
                        text = '      ' + item.name + ' ' + self.items[item]
                self.window.blit(self.font.render(text, True, self.fontColor),
                    (ShopSettings.textStartX, ShopSettings.textStartY + offset))
                offset += DialogSettings.textVerticalDist

            
            texts = ["Coins: " + str(self.player.money),
                    "HP: " + str(self.player.HP) + "/" + str(self.player.maxHP),
                    "MP: " + str(self.player.MP) + "/" + str(self.player.maxMP),
                    "Attack: " + str(self.player.attack),
                    "Defence: " + str(self.player.defence)]
        
            offset = 0
            for text in texts:
                self.window.blit(self.font.render(text, True, self.fontColor),
                    (ShopSettings.textStartX + ShopSettings.boxWidth * 3 / 4, ShopSettings.textStartY + offset))
                offset += DialogSettings.textVerticalDist

class PlayerBag:
    def __init__(self, window, player,
                 fontSize: int = 2 * DialogSettings.textSize // 3, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window=window
        self.player=player
        self.items=player.item
        self.fontSize=fontSize
        self.fontColor=fontColor
        self.bg=pygame.Surface((WindowSettings.width,
                               WindowSettings.height),pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.font=pygame.font.Font(GamePath.font,self.fontSize)
        self.selectedID = 0
        self.time = 0
    
    def equip(self, item):
        if str(type(item)) == "<class 'Items.Magic'>":
            if self.player.magic != item:
                self.player.unequip(self.player.magic)
                self.player.magic = item
                self.player.equip(item)
        elif str(type(item)) == "<class 'Items.Equipment'>":
            if self.player.armor != item:
                self.player.unequip(self.player.armor)
                self.player.armor = item
                self.player.equip(item)
        elif str(type(item)) == "<class 'Items.Weapon'>":
            if self.player.weapon != item:
                self.player.unequip(self.player.weapon)
                self.player.weapon = item
                self.player.equip(item)

    def draw(self, scene, events, keys):
        self.window.blit(self.bg, (0,0))
        for event in events:
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_w]:
                        self.selectedID = max(0, self.selectedID - 1)
                    elif keys[pygame.K_s]:
                        self.selectedID = min(len(self.items) - 1, self.selectedID + 1)
                    elif keys[pygame.K_RETURN]:
                        self.player.talking = False
                        scene.end_bag()
                    elif keys[pygame.K_a] and len(self.items) != 0:
                        self.equip(self.items[self.selectedID])
        offset = 0
        for id, item in enumerate(self.items):
            if id == self.selectedID:
                text = '-->' + item.name + str(type(item)).split(".")[-1][:-2] +"—" + item.text
                item.rect.topleft=(BagSettings.textStartX * 3, 
                        BagSettings.textStartY + offset + DialogSettings.textVerticalDist)
                self.window.blit(item.image,item.rect)
            else:
                text = '      ' + item.name
            self.window.blit(self.font.render(text, True, self.fontColor),
                        (BagSettings.textStartX, BagSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        
        texts = ["Coins: " + str(self.player.money),
                    "HP: " + str(self.player.HP) + "/" + str(self.player.maxHP),
                    "MP: " + str(self.player.MP) + "/" + str(self.player.maxMP),
                    "Attack: " + str(self.player.attack),
                    "Defence: " + str(self.player.defence),
                    "Weapon: " + str(self.player.weapon),
                    "Armor: " + str(self.player.armor),
                    "Magic: " + str(self.player.magic)]
        
        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text, True, self.fontColor),
                (10, BagSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        
        text = self.font.render("Press A to equip",
                                True, (255, 255, 255))
        textRect = text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        self.time += 1
        if self.time >= 15:
            self.window.blit(text, textRect)
            if self.time >= 15 * 2:
                self.time = 0
    
class AchievementBox:
    def __init__(self, window, player,
                 fontSize: int = 2 * DialogSettings.textSize // 3, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window=window
        self.player=player
        self.fontSize=fontSize
        self.fontColor=fontColor
        self.bg=pygame.Surface((WindowSettings.width,
                               WindowSettings.height),pygame.SRCALPHA)
        self.bg.fill(bgColor)
        self.font=pygame.font.Font(GamePath.font,self.fontSize)
        
        self.achievement_list = []
        
        self.achievement_list.append(Achievement("陪伴","在线一分钟"))
        self.achievement_list.append(Achievement("魔法大师","学会两种魔法",attr={"coin":0,"item":Magic("灼热射线",GamePath.magic[1],
                                                "造成巨额伤害使敌人麻痹并烧伤，每局限使用一次",
                                                {"maxMP":10,"attack":0,"maxHP":0,"defence":0},4,1,20)}))
        self.achievement_list.append(Achievement("献血者","在自动贩卖机处献血3次",attr={"coin":100,"item":Weapon("嗜血匕首",GamePath.weapon[1],
                                                "物理攻击回复伤害的3/4的HP，战斗中可突破HP上限",{"maxMP":0,"attack":10,"maxHP":0,"defence":0})}))
        self.achievement_list.append(Achievement("结局？","击败流浪的外星人",attr={"coin":100,"item":Equipment("法师之甲",GamePath.equipment[2],
                                                "将受到的伤害转化为MP，战斗中可突破MP上限",{"maxMP":10,"attack":0,"maxHP":0,"defence":2})}))
        self.achievement_list.append(Achievement("拥抱虚空","完成二周目",attr={"coin":10000,"item": None}))
        
        self.selectedID = 0
        self.open = False
        self.time = 0
        self.warning_text = None

    def get(self, achievement):
        if str(type(achievement)) == "<class 'Items.Achievement'>":
            if achievement.complited :
                if not achievement.got:
                    self.player.achievement_complite(achievement)
                    achievement.got = True
                    text = None
                else:
                    text = self.font.render("You Have Got the Reward",
                                True, (255, 255, 255))
            else:
                text = self.font.render("You Haven't Complited It",
                                True, (255, 255, 255))
            if text != None:
                textRect = text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 200))
                return (text,textRect)

    def draw(self, scene, events, keys):
        self.window.blit(self.bg, (0,0))
        for event in events:
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_w]:
                        self.selectedID = max(0, self.selectedID - 1)
                    elif keys[pygame.K_s]:
                        self.selectedID = min(len(self.achievement_list) - 1, self.selectedID + 1)
                    elif keys[pygame.K_RETURN]:
                        self.player.talking = False
                        scene.end_achievement()
                    elif keys[pygame.K_a]:
                        self.warning_text = self.get(self.achievement_list[self.selectedID])
        text = self.font.render("Press A to get reward",
                                True, (255, 255, 255))
        textRect = text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        
        self.time += 1
        if self.time >= 15:
            self.window.blit(text, textRect)
            if self.time >= 15 * 2:
                self.time = 0
        if self.time <= 20 and self.warning_text !=None:
            self.window.blit(self.warning_text[0],self.warning_text[1])
        else:
            self.warning_text = None
        
        offset = 0
        for id, achievement in enumerate(self.achievement_list):
            if id == self.selectedID:
                text = '-->' + achievement.name +"——" + achievement.text + "   " + str(achievement.complited)
            else:
                text = '      ' + achievement.name + "   " + str(achievement.complited)
            self.window.blit(self.font.render(text, True, self.fontColor),
                        (BagSettings.textStartX, BagSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        
        texts = ["Coins: " + str(self.player.money),
                    "HP: " + str(self.player.HP) + "/" + str(self.player.maxHP),
                    "MP: " + str(self.player.MP) + "/" + str(self.player.maxMP),
                    "Attack: " + str(self.player.attack),
                    "Defence: " + str(self.player.defence),
                    "Weapon: " + str(self.player.weapon),
                    "Armor: " + str(self.player.armor),
                    "Magic: " + str(self.player.magic)]
        
        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text, True, self.fontColor),
                (10, BagSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        
        offset = 0
        for text in self.player.item:
            self.window.blit(self.font.render(str(text) + str(type(text)).split(".")[-1][:-2], True, self.fontColor),
                (3*WindowSettings.width//4, BagSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        text = "Item: "
        self.window.blit(self.font.render(str(text), True, self.fontColor),
                (3*WindowSettings.width//4, BagSettings.textStartY - DialogSettings.textVerticalDist))
