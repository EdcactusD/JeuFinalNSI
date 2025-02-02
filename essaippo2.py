import pygame
import os


"""
EXPLICATIONS SUR CERTAINS POINTS ET METHODES PRATIQUE DANS LE CODE:
1. event.pos représente les coordonnées (x, y) de l'endroit où la souris a cliqué, 
obtenues dans un événement MOUSEBUTTONDOWN ou MOUSEBUTTONUP : 
collidepoint retourne un booléen suivant si la souris est dans la zone (True) ou non (False)   
"""

class Jeu:
    def __init__(self):
        pygame.init()
        
        self.bg_width, self.bg_height = 1000,1000
        self.screen = pygame.display.set_mode((self.bg_width, self.bg_height))
    
        pygame.display.set_caption("Jeu final NSI")
        

        self.running = True
        self.etat = Etat0(self)  # Définition de la scène actuelle

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.etat.handle_events(event)  # ICI : PAS COMPRIS : Délègue la gestion des événements à etat

            self.etat.update() #CEST QUOI CA?
            self.etat.draw(self.screen)
            pygame.display.flip()  # Rafraîchissement de l’écran

        pygame.quit()
    
    def changer_etat(self, nouvel_etat):
        """Change l'état du jeu."""
        self.etat= nouvel_etat
        
class Etats: #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self,jeu):
        self.jeu = jeu  # Référence à l'objet Jeu pour changer d'état et interagir directement avec lui
    
    def handle_events(self, event):
       """Gère les événements clavier/souris."""      
       pass
   
    def update(self):
        """Met à jour les éléments de la scène."""
        pass

    def draw(self, screen):
        """Affiche la scène sur l'écran."""
        pass

class Etat0(Etats):
    def __init__(self,jeu):
       super().__init__(jeu)
       self.show_menu = False
       self.show_map = False
       self.show_inventaire = False

       self.assets_dir = os.path.join(os.path.dirname(__file__), "assets")
       self.bg_image = pygame.image.load(os.path.join(self.assets_dir, "etat0.jpg"))
       self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_height, self.jeu.bg_width))

       self.menu = pygame.image.load(os.path.join(self.assets_dir, "AL1 POPN.png"))
       self.menu_width, self.menu_height = 100, 500
       self.menu_x = self.jeu.bg_height - self.menu_width  
       self.menu_y = self.jeu.bg_width - self.menu_height
       self.menu = pygame.transform.scale(self.menu, (self.menu_x, self.menu_y))
       
       self.map = pygame.image.load(os.path.join(self.assets_dir, "carte.jpg"))
       self.inventaire = pygame.image.load(os.path.join(self.assets_dir, "Test.jpg"))
       self.inventaire = pygame.transform.scale(self.inventaire, (self.jeu.bg_height, self.jeu.bg_width))

       self.zone_carte = pygame.Rect(8, 8, self.jeu.bg_width, self.jeu.bg_height)  #j'ai mis des trucs au pif
       
    def handle_events(self, event):
          #Touches pressées
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_w:
                 self.show_menu = not self.show_menu
              if event.key == pygame.K_x:
                 self.show_map = not self.show_map
                 if self.show_map:
                     self.show_menu = False
              if event.key == pygame.K_c and self.show_menu:
                   if self.show_inventaire:  
                       self.show_inventaire = False
                   elif self.show_menu:  
                       self.show_inventaire = True
                       
          #CLics souris             
          if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
          # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
            if self.show_map and self.zone_carte.collidepoint(event.pos):  
              # Si on clique sur une zone de la carte, on change d'état
              self.jeu.changer_etat(Enigme(self.jeu))  
              print(event.pos)  # Affiche la position du clic pour debug
              print("Zone cliquée dans la carte !")
    
 
    def update(self):
        pass  # JSPPPPP Ajoute ici la mise à jour des éléments si nécessaire

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Efface l’écran avec du noir avant d’afficher les images
        screen.blit(self.bg_image, (0, 0))
        if self.show_map:
            screen.blit(self.map, (0, 0))
        if self.show_menu and not self.show_map:
            screen.blit(self.menu, (self.menu_x, self.menu_y))
        if self.show_inventaire:
            screen.blit(self.inventaire, (0, 0))

class Enigme(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.assets_dir = os.path.join(os.path.dirname(__file__), "assets") #BANCAL : de remettre ici mais bon c'est un détail à changer
        self.bg_image = pygame.image.load(os.path.join(self.assets_dir, "enigme.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_height, self.jeu.bg_width))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Retour au menu principal
                self.jeu.changer_etat(Etat0(self.jeu))

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        
jeu = Jeu()
jeu.run()

#A FAIRE : gerer un meilleur affichage de la map etc. 