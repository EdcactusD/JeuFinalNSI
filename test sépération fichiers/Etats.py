import os
import pygame
import Map
import Inventaire
import Reglages

class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False, show_inventaire=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       
       self.show_menu = show_menu
       self.show_map = show_map
       self.show_inventaire = show_inventaire

       self.bg_image = pygame.Surface((self.jeu.bg_width, self.jeu.bg_height))  # Fond par défaut (evite de planter si sous classe n'a pas de fond) // Surface crée un sorte de zone de dessin
       self.bg_image.fill((0, 0, 0))
       
       self.menu = pygame.image.load(os.path.join("assets", "menu.png"))
       self.menu_width, self.menu_height = 100, 500
       self.menu = pygame.transform.scale(self.menu, (self.menu_width, self.menu_height))
       self.menu_x = self.jeu.bg_width - self.menu_width - 5 #pour décaler du bord 
       self.menu_y = self.jeu.bg_height - self.menu_height - 5
       self.zone_map_ic = pygame.Rect(self.menu_x, self.menu_y+19, self.menu_width, 100)
       self.zone_inventaire_ic = pygame.Rect(self.menu_x, self.menu_y+134, self.menu_width, 100)
       self.zone_reglages_ic = pygame.Rect(self.menu_x, self.menu_y+245, self.menu_width, 100)
       
              
       self.inventaire = pygame.image.load(os.path.join("assets", "Test.jpg"))
       self.inventaire = pygame.transform.scale(self.inventaire, (self.jeu.bg_width, self.jeu.bg_height))

       self.map = pygame.image.load(os.path.join("assets","fonds","carte.png"))
       self.map = pygame.transform.scale(self.map, (self.jeu.bg_width, self.jeu.bg_height))
       self.zone_carte = pygame.Rect(0, 0, self.jeu.bg_width, self.jeu.bg_height)  #j'ai mis des trucs au pif (ON GERTE CA DE LA)
       #FAIRE UNE CLASSE A PART POUR INVENTAIRE, REGLAGES, CARTE

    def changer_etat(self, nouvel_etat):
        """Change l'état du jeu."""
        self.etat= nouvel_etat
       
    def handle_events(self, event):
          #Touches pressées
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_w:
                 self.show_menu = not self.show_menu
              if event.key == pygame.K_x: 
                self.jeu.changer_etat(Map(self.jeu))
              if event.key == pygame.K_c and self.show_menu:  
                       self.jeu.changer_etat(Inventaire(self.jeu))
                       
          #CLics souris             
          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
          # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
           print(event.pos)
           print("Zone cliquée dans la carte !")
           if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
                self.jeu.changer_etat(Map(self.jeu))
           if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
                self.jeu.changer_etat(Inventaire(self.jeu))
           if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
                self.jeu.changer_etat(Reglages(self.jeu))
    
 
    """def update(self):
        pass  # permet de gerer independament les updates de chaque mini-jeu"""

    def draw(self, screen):
        #screen.fill((0, 0, 0))  # Efface l’écran avec du noir avant d’afficher les images (pas necessaire si tout l'écran est rempli et non transaparent)
        screen.blit(self.bg_image, (0, 0))

        if self.show_menu:
            screen.blit(self.menu, (self.menu_x, self.menu_y))
            #Tests pour voir les rect. 
            #pygame.draw.rect(screen, (255, 0, 0), self.zone_map_ic, 2)  # Contour rouge pour tester
            #pygame.draw.rect(screen, (0, 255, 0), self.zone_inventaire_ic, 2)
            #pygame.draw.rect(screen, (0, 0, 255), self.zone_reglages_ic, 2)



