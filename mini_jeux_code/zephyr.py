import pygame
import os 
from général.etats import Etats

class Zephyr(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Zephyr.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.mini_jeu = "Zephyr"

    def handle_events(self, event):
        super().handle_events(event)
