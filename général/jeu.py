import pygame
import os
from général.etats import Etats

class Jeu(Etats):
    def __init__(self):
        pygame.init()
        
        logo = pygame.image.load(os.path.join("assets", "logo.png"))
        logo = pygame.transform.scale(logo, (32, 32))
        pygame.display.set_icon(logo)
        
        pygame.mixer.init()  #initialise le module audio
        pygame.mixer.music.load(os.path.join("assets", "musique_jeu.mp3"))
        pygame.mixer.music.play(-1)  #joue en boucle (-1 : boucle infinie)
        self.volume= pygame.mixer.music.set_volume(0.5)  # Ajuste le volume (0.0 à 1.0)
        

        info = pygame.display.Info()  # Récupérer les infos de l'écran
        print(f"Résolution réelle utilisée : {info.current_w}x{info.current_h}")
   
        self.bg_width = info.current_w  # Largeur de l'écran
        self.bg_height = info.current_h  # Hauteur de l'écran
        self.screen = pygame.display.set_mode((self.bg_width, self.bg_height))
        
        pygame.display.set_caption("Jeu final NSI")
        self.font = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.bg_height/36))
        pygame.mouse.set_visible(True)
        

        self.running = True
        self.Animation_debut()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    self.running = False
                self.etat.handle_events(event)
            self.etat.draw(self.screen)
            pygame.display.flip()  # Rafraîchissement de l’écran

        pygame.quit()
            
    def changer_etat(self, nouvel_etat):
        """Change l'état du jeu."""
        self.etat= nouvel_etat
   