# -*- coding:utf-8 -*-

from Settings import *

import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, GOTO:SceneType,x=PortalSettings.coordX, y=PortalSettings.coordY):
        super().__init__()
        
        self.image=pygame.transform.scale(pygame.image.load(GamePath.portal).convert_alpha(),
                                          (PortalSettings.width,PortalSettings.height))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.destination=GOTO
        self.mask=pygame.mask.from_surface(self.image)

    def draw(self, window, dx=0, dy=0):
        self.rect.x -= dx
        self.rect.y -= dy
        window.blit(self.image,self.rect)
