import pygame
import os

 
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
        print(f"Résolution réelle utilisée : {info.current_w}x{info.current_h}")
   
        self.bg_width = info.current_w  # Largeur de l'écran
        self.bg_height = info.current_h  # Hauteur de l'écran
        self.screen = pygame.display.set_mode((self.bg_width, self.bg_height))
        
        pygame.display.set_caption("Jeu final NSI")
        self.font = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.bg_height/36))
        

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
                    self.jeu.changer_etat(Map(self.jeu))
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

class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False, show_inventaire=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       
       self.show_menu = show_menu
       self.show_map = show_map
       self.show_inventaire = show_inventaire
       
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

class Map(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        from Mont_azur import Mont_azur 
        from Enigme import Enigme
        from Tir_arc import Tir_arc
        from Vitesse import Vitesse
        from Chateau import Pendu, Pendule,Chateau 
        from Memoire_combi import Memoire_combi
        from Portes import Portes
        from Bon_minerai import Bon_minerai
        from Eau import Eau
        from Krabi import Krabi
        from Zephyr import Zephyr
        from Mars import Mars
        from Chaudron import Chaudron
        
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "carte.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height)) #pas sûre que ce soit utile (à voir dans la super)
        self.zones_carte = { "Mont_azur" : [pygame.Rect(int(self.jeu.bg_width/2.75),int(self.jeu.bg_height/21.6),int(self.jeu.bg_width/4.71),int(self.jeu.bg_height/3.6)), Mont_azur],
        "zone_enigme" : [pygame.Rect(int(self.jeu.bg_width/2.75),int(self.jeu.bg_height/3),int(self.jeu.bg_width/4.85),int(self.jeu.bg_height/8)), Enigme],
        "zone_Tir_arc" : [pygame.Rect(int(self.jeu.bg_width/5.657),int(self.jeu.bg_height/2.57),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/6)),Tir_arc],
        "zone_Vitesse" : [pygame.Rect(int(self.jeu.bg_width/2.06),int(self.jeu.bg_height/1.576),int(self.jeu.bg_width/7.11),int(self.jeu.bg_height/12.7058)),Vitesse],
        "zone_chateau" : [pygame.Rect(int(self.jeu.bg_width/4.658),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/3.927)),Chateau],
        "zone_Memoire_combi" : [pygame.Rect(int(self.jeu.bg_width/1.75),int(self.jeu.bg_height/2.1),int(self.jeu.bg_width/4.95),int(self.jeu.bg_height/6.8)),Memoire_combi],
        "zone_Portes" : [pygame.Rect(int(self.jeu.bg_width/3.504),int(self.jeu.bg_height/1.636),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/4)),Portes],
        "zone_Bon_minerai" : [pygame.Rect(int(self.jeu.bg_width/1.669),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/7.2)),Bon_minerai],
        "zone_Eau" : [pygame.Rect(int(self.jeu.bg_width/2.17),int(self.jeu.bg_height/1.35),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/5.4)),Eau],
        "Krabi" : [pygame.Rect(int(self.jeu.bg_width/2.6),int(self.jeu.bg_height/1.9),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/10.75)),Krabi],
        "zone_Zephyr" : [pygame.Rect(int(self.jeu.bg_width/1.5),int(self.jeu.bg_height/1.27),int(self.jeu.bg_width/6.3),int(self.jeu.bg_height/9.81)),Zephyr],
        "zone_Mars" : [pygame.Rect(int(self.jeu.bg_width/1.536),int(self.jeu.bg_height/3.6),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/6.2)),Mars],
        "zone_Chaudron" : [pygame.Rect(int(self.jeu.bg_width/1.6),int(self.jeu.bg_height/1.54),int(self.jeu.bg_width/8),int(self.jeu.bg_height/9.5)),Chaudron], }
        
        
    def handle_events(self, event):
        super().handle_events(event)  # Garde le comportement général des événements
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for zone in self.zones_carte:
                if self.zones_carte[zone][0].collidepoint(event.pos): 
                    self.jeu.changer_etat(self.zones_carte[zone][1](self.jeu))
    
    """def draw(self, screen) :
        super().draw(screen)
        for zone in  self.zones_carte:
            pygame.draw.rect(screen, (255, 0, 0), self.zones_carte[zone][0], 10)
        pygame.display.flip() #pour tester les zones"""
    


class Inventaire(Etats):
 pass

class Reglages(Etats):
  pass

jeu = Jeu()
jeu.run()