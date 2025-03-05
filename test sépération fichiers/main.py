import pygame
import os
import Etats

 
"""
EXPLICATIONS SUR CERTAINS POINTS ET METHODES PRATIQUE DANS LE CODE:
1. event.pos représente les coordonnées (x, y) de l'endroit où la souris a cliqué, 
obtenues dans un événement MOUSEBUTTONDOWN ou MOUSEBUTTONUP : 
collidepoint retourne un booléen suivant si la souris est dans la zone (True) ou non (False)  

2. .items()  permet d'obtenir la clé et la valeur dans un dico
"""

class Jeu:
    def __init__(self):
        pygame.init()
        
        pygame.mixer.init()  #initialise le module audio
        pygame.mixer.music.load(os.path.join("assets", "musique_jeu.mp3"))
        pygame.mixer.music.play(-1)  #joue en boucle (-1 : boucle infinie)
        pygame.mixer.music.set_volume(0.5)  # Ajuste le volume (0.0 à 1.0)

        info = pygame.display.Info()  # Récupérer les infos de l'écran
        self.bg_width = info.current_w  # Largeur de l'écran
        self.bg_height = info.current_h  # Hauteur de l'écran
        self.screen = pygame.display.set_mode((self.bg_width, self.bg_height))
        
        pygame.display.set_caption("Jeu final NSI")
        

        self.running = True
        self.etat = Menu_debut(self)  # Définition de la scène actuelle

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
                    self.running = False
                self.etat.handle_events(event)  # ICI : PAS COMPRIS : Délègue la gestion des événements à etat

            #self.etat.update() #permet d'avoir des updates différents pour chaque état
            self.etat.draw(self.screen)
            pygame.display.flip()  # Rafraîchissement de l’écran

        pygame.quit()
            
    def changer_etat(self, nouvel_etat):
        """Change l'état du jeu."""
        self.etat= nouvel_etat
         
class Menu_debut:
  """gère l'écran qui s'affiche pour lancer le jeu"""
  def __init__(self, jeu):
      self.jeu = jeu
      
      self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "menudebut.png"))
      self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))  
      self.width_bouton, self.height_bouton, self.espace = 400, 110, 150
      self.boutons = {"Jouer" : pygame.Rect(self.jeu.bg_width/2-self.width_bouton/2, self.jeu.bg_height/2-self.height_bouton/2, self.width_bouton, self.height_bouton), #permet de lancer le jeu avec la dernière sauvegarde
                      "Lancer une nouvelle partie" : pygame.Rect(self.jeu.bg_width/2-self.width_bouton/2, self.jeu.bg_height/2-self.height_bouton/2+self.espace, self.width_bouton, self.height_bouton),
                      "Quitter" : pygame.Rect(self.jeu.bg_width/2-self.width_bouton/2, self.jeu.bg_height/2-self.height_bouton/2+self.espace*2, self.width_bouton, self.height_bouton)
          }
      self.font = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), 30)
      
  def handle_events(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for bouton, position in self.boutons.items():
            if position.collidepoint(event.pos) :
                if bouton == "Jouer" :
                    self.jeu.changer_etat(Etat0(self.jeu))
                elif bouton=="Lancer une nouvelle partie" :
                    print("lancement d'une nouvelle partie")
                elif bouton=="Quitter":
                    self.jeu.running=False
            
                
      
  def draw(self, screen):
    #screen.fill((0, 0, 0)) #pas necessaire si tout l'écran est rempli
    screen.blit(self.bg_image, (0, 0))
    for bouton in self.boutons: 
      if self.boutons[bouton].collidepoint(pygame.mouse.get_pos()): #on aggrandit les boutons quand la souris passe dessus
        if self.boutons[bouton][2]==self.width_bouton : #on vérifie que le bouton n'est pas déjà aggrandi
           self.boutons[bouton]=self.boutons[bouton].inflate(40,11) #.inflate revoie un nouveau rect avec une taille modifiée
      elif self.boutons[bouton][2]!=self.width_bouton:
           self.boutons[bouton]=self.boutons[bouton].inflate(-40,-11)
      pygame.draw.rect(screen, "#834c2c", self.boutons[bouton], border_radius=20)
      screen.blit(self.font.render(bouton, True, "#d9aa62"), self.font.render(bouton, True, "#d9aa62").get_rect(center=self.boutons[bouton].center)) #le .get_rect permet de créer un rect pour le texte, le center= permet de poser le centre au milieu du rect (et non en haut à gauche)

class Etat0(Etats): 
    def __init__(self,jeu):
        super().__init__(self,jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "etat0.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.show_menu = True

    def handle_events(self, event):
        super().handle_events(event)

jeu = Jeu()
jeu.run()