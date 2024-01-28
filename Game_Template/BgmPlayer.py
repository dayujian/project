import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):
        self.music=GamePath.bgm
        self.volume = 0.2
        self.index=None

    def play(self, index, loop=-1):
        pygame.mixer.music.load(self.music[index])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(loop)

    def stop(self):
        pygame.mixer.music.fadeout(1000)

    def update(self, GOTO):
        self.stop()
        if GOTO==SceneType.CITY:
            self.index=0
        if GOTO==SceneType.WILD:
            self.index=1
        if GOTO==SceneType.BOSS:
            self.index=2
        self.play(self.index)
