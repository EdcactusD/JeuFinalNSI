import os
import pygame
from Donkey_kong_mario import Donkey_kong_mario
from main import Etats
from Trad import Trad

class Mont_azur(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_mont_azur.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_mont_azur = {"zone_Donkey_kong_mario" : [pygame.Rect(850,650,600,400), Donkey_kong_mario],
                                "zone_Trad" : [pygame.Rect(300,100,600,550),Trad]
                                }
        
    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           for zone in self.zones_chateau:
               if self.zones_chateau[zone][0].collidepoint(event.pos): 
                   self.jeu.changer_etat(self.zones_chateau[zone][1](self.jeu))

