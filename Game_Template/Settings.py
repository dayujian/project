# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Thgink Luos"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class SceneSettings:
    tileXnum = 48 # 64
    tileYnum = 27 # 36
    tileWidth = tileHeight = 40
    obstacleDensity=0.05
class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 5
    playerWidth = 60
    playerHeight = 50
    playerHP = 100
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100
    playerMagic = 10
    playerMagicAttack = 10

class NPCSettings:
    npcSpeed = 1
    npcWidth = 60
    npcHeight = 60
    patrollingRange = 70
    talkCD = 50

class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3

class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class SceneType(Enum):
    CITY = 1
    WILD = 2
    BOSS = 3

class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 + 10         # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize                 # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 3 // 4 
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 4          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 +100   
    textStartY = WindowSettings.height // 3         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 2 

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2 

    stepSize = 20
    animationCount = 15

    magicWidth = WindowSettings.width // 20
    magicHeight = WindowSettings.height // 6
    MagicCoordX = WindowSettings.width // 8 + 200
    MagicCoordY = WindowSettings.height // 2 

class ShopSettings:
    boxWidth = 800
    boxHeight = 200
    boxStartX = WindowSettings.width // 4   # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX + 10         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25    # Coordinate Y of the first line of dialog

class BagSettings:
    textSize = 56
    textStartX = ShopSettings.textStartX * 0.625
    textStartY = ShopSettings.textStartY - 200

class GamePath:
    # Window related path
    menu = r".\assets\background\menu.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"

    # player/npc related path
    npc = r".\assets\npc\npc.png"
    shop_npc=[
        r".\assets\npc\shop_npc\1.png",
        r".\assets\npc\shop_npc\2.png",
        r".\assets\npc\shop_npc\3.png",
        r".\assets\npc\shop_npc\4.png"
    ]
    player = [
        r".\assets\player\1.png", 
        r".\assets\player\1.png",
        r".\assets\player\2.png", 
        r".\assets\player\2.png", 
        r".\assets\player\3.png", 
        r".\assets\player\3.png", 
        r".\assets\player\4.png", 
        r".\assets\player\4.png", 
        # 8 frames for a single loop of animation looks much better.
    ]
    monster = r".\assets\npc\monster\1.png"
    boss = r".\assets\npc\boss.png"

    groundTiles = [
        r".\assets\tiles\ground1.png", 
        r".\assets\tiles\ground2.png", 
        r".\assets\tiles\ground3.png", 
        r".\assets\tiles\ground4.png", 
        r".\assets\tiles\ground5.png", 
        r".\assets\tiles\ground6.png", 
    ]

    cityTiles = [
        r".\assets\tiles\city1.png", 
        r".\assets\tiles\city2.png", 
        r".\assets\tiles\city3.png", 
        r".\assets\tiles\city4.png", 
        r".\assets\tiles\city5.png", 
        r".\assets\tiles\city6.png", 
    ]

    cityWall = r".\assets\tiles\cityWall.png"

    bossTiles = [
        r".\assets\tiles\boss1.png", 
        r".\assets\tiles\boss2.png", 
        r".\assets\tiles\boss3.png", 
        r".\assets\tiles\boss4.png", 
        r".\assets\tiles\boss5.png", 
        r".\assets\tiles\boss6.png", 
    ]

    bossWall = r".\assets\tiles\bossWall.png"

    portal = r".\assets\background\portal.png"

    tree = r".\assets\tiles\tree.png"

    bgm = [
        r".\assets\bgm\city.mp3",
        r".\assets\bgm\wild.mp3",
        r".\assets\bgm\boss.mp3"
    ]
    
    font = r".\assets\font\SongHuiZongShouJinJiaCuBan-2.ttf"

    magic = [
        [r".\assets\new\magic\1.png"],
        [r".\assets\new\magic\21.png",
         r".\assets\new\magic\22.png",
         r".\assets\new\magic\23.png",
         r".\assets\new\magic\24.png",
         r".\assets\new\magic\25.png",
         r".\assets\new\magic\26.png",
         r".\assets\new\magic\27.png",
         r".\assets\new\magic\28.png",
         r".\assets\new\magic\29.png",
         r".\assets\new\magic\2x.png"],
        [r".\assets\new\magic\31.png",
         r".\assets\new\magic\32.png",
         r".\assets\new\magic\33.png",
         r".\assets\new\magic\34.png",
         r".\assets\new\magic\35.png"],
        [r".\assets\new\magic\411.png",
         r".\assets\new\magic\412.png",
         r".\assets\new\magic\413.png",
         r".\assets\new\magic\414.png",
         r".\assets\new\magic\415.png",
         r".\assets\new\magic\416.png",
         r".\assets\new\magic\417.png",
         r".\assets\new\magic\418.png",
         r".\assets\new\magic\421.png",
         r".\assets\new\magic\422.png",
         r".\assets\new\magic\423.png",
         r".\assets\new\magic\424.png",
         r".\assets\new\magic\425.png",
         r".\assets\new\magic\426.png"],
        [r".\assets\new\magic\51.png",
         r".\assets\new\magic\52.png",
         r".\assets\new\magic\53.png",
         r".\assets\new\magic\54.png",
         r".\assets\new\magic\55.png",
         r".\assets\new\magic\56.png",
         r".\assets\new\magic\57.png",
         r".\assets\new\magic\58.png",             
         r".\assets\new\magic\59.png"]
    ]

    weapon = [
        r".\assets\new\weapon\1.png",
        r".\assets\new\weapon\2.png",
        r".\assets\new\weapon\3.png"
    ]

    equipment = [
        r".\assets\new\equipment\1.png",
        r".\assets\new\equipment\2.png",
        r".\assets\new\equipment\3.png"
    ]
    
    druid = r".\assets\npc\druid.png"

    deadplayer = r".\assets\player\5.png"

    gameover = r".\assets\background\gameover.jpg"

    magicmaster = r".\assets\npc\magic_master.png"

    weaponmaster = r".\assets\npc\weapon_master.png"

    gamewin = r".\assets\background\gamewin.jpg"

    gamewin2 = r".\assets\background\gamewin2.png"
class PortalSettings:
    width = 320
    height = 320
    coordX = (SceneSettings.tileXnum - 10) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_PLAY_CITY = 7
    GAME_PLAY_BOSS = 8
    GAME_WIN_TWICE = 9

class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH_TO_WILD = pygame.USEREVENT + 3
    EVENT_SWITCH_TO_CITY = pygame.USEREVENT + 4
    EVENT_SWITCH_TO_BOSS = pygame.USEREVENT + 5
    EVENT_RESTART = pygame.USEREVENT + 6
    EVENT_SHOP = pygame.USEREVENT + 7
    EVENT_DIED = pygame.USEREVENT + 8
    EVENT_WIN = pygame.USEREVENT + 9
    EVENT_WIN_TWICE = pygame.USEREVENT + 10

