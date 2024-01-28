import pygame
import Map
from random import randint

from enum import Enum
from Settings import *
from NPC import *
from Portal import *

class Scene():
    def __init__(self, window):
        self.type = None

        self.map = None
        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()

        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height

        self.shoppingBox = None

    def render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                                 (SceneSettings.tileWidth * i, 
                                SceneSettings.tileHeight * j))
                
        self.obstacles.draw(self.window)
        self.npcs.draw(self.window)
        self.portals.draw(self.window)
        
class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.CITY
        self.map = Map.gen_city_map()
        self.obstacles = Map.gen_obstacles()

        self.npcs.add(NPC(self.width // 3, self.height // 3))
        self.portals.add(Portal(self.width // 3 * 2, self.height // 3 * 2))


class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.type = SceneType.WILD
        self.map = Map.gen_wild_map()
        self.obstacles = Map.gen_obstacles()

        self.portals.add(Portal(self.width // 3, self.height // 3))

class MainMenuScene(Scene):
    def __init__(self, window):
        super().__init__(window)
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, 
                (WindowSettings.width, WindowSettings.height))
        
        self.font = pygame.font.Font(None, MenuSettings.textSize)
        self.text = self.font.render("Press ENTER to start",
                                True, (255, 255, 255))
        self.textRect = self.text.get_rect(center=(WindowSettings.width // 2, 
                                WindowSettings.height - 50))
        
        self.blinkTimer = 0
        
    def render(self):
        self.window.blit(self.bg, (0, 0))
        
        self.blinkTimer += 1
        if self.blinkTimer >= MenuSettings.blinkInterval:
            self.window.blit(self.text, self.textRect)
            if self.blinkTimer >= MenuSettings.blinkInterval * 2:
                self.blinkTimer = 0



