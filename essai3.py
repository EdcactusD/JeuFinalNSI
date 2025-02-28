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
       self.menu_x = self.jeu.bg_width - self.menu_width - 5 #pour déclaler du bord 
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
       
    def handle_events(self, event):
          #Touches pressées
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_w:
                 self.show_menu = not self.show_menu
                 if self.show_map:
                     self.show_menu = False
              if event.key == pygame.K_x:
                 self.show_map = not self.show_map     
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
              self.jeu.changer_etat(Map(self.jeu))  
            if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
                self.show_map = not self.show_map
                if self.show_map:
                    self.show_menu = False
            if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
                pass
            if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
                pass
    
 
    """def update(self):
        pass  # permet de gerer independament les upadates de chaque mini-jeu"""

    def draw(self, screen):
        #screen.fill((0, 0, 0))  # Efface l’écran avec du noir avant d’afficher les images (pas necessaire si tout l'écran est rempli et non transaparent)
        screen.blit(self.bg_image, (0, 0))
        if self.show_map:
            screen.blit(self.map, (0, 0))
        if self.show_menu and not self.show_map:
            screen.blit(self.menu, (self.menu_x, self.menu_y))
            #Tests pour voir les rect. 
            #pygame.draw.rect(screen, (255, 0, 0), self.zone_map_ic, 2)  # Contour rouge pour tester
            #pygame.draw.rect(screen, (0, 255, 0), self.zone_inventaire_ic, 2)
            #pygame.draw.rect(screen, (0, 0, 255), self.zone_reglages_ic, 2)


        if self.show_inventaire and not self.show_map:
            screen.blit(self.inventaire, (0, 0))          

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
       
      
class Map(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "carte.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_carte = { "Mont_azur" : [pygame.Rect(720,50,420,300), Mont_azur(self.jeu)],
        "zone_enigme" : [pygame.Rect(700,360,400,135), Enigme(self.jeu)],
        "zone_Tir_arc" : [pygame.Rect(350,420,300,180),Tir_arc(self.jeu)],
        "zone_Vitesse" : [pygame.Rect(930,685,270,85),Vitesse(self.jeu)],
        "zone_chateau" : [pygame.Rect(425,100,300,275),Chateau(self.jeu)],
        "zone_Memoire_combi" : [pygame.Rect(1100,500,400,150),Memoire_combi(self.jeu)],
        "zone_Portes" : [pygame.Rect(565,660,300,270),Portes(self.jeu)]
            }
        
    def handle_events(self, event):
        super().handle_events(event)  # Garde le comportement général des événements
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.jeu.changer_etat(Map(self.jeu)) #de base ça changeait pour Etat0 mais pour l'héritage c'est mieux comme ça (et aussi pas trop logique de pouvoir revenir à Etat0)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for zone in self.zones_carte:
                if self.zones_carte[zone][0].collidepoint(event.pos): 
                    self.jeu.changer_etat(self.zones_carte[zone][1])
    
    """def draw(self, screen) :
        super().draw(screen)
        for zone in  self.zones_carte:
            pygame.draw.rect(screen, (255, 0, 0), self.zones_carte[zone][0], 10)
            pygame.display.update()""" #pour tester les zones d'affichage
                
class Mont_azur(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_mont_azur.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_mont_azur = {"zone_Donkey_kong_mario" : [pygame.Rect(850,650,600,400), Donkey_kong_mario(self.jeu)]
                                }
        
    def handle_events(self, event):
        super().handle_events(event) # Garde le comportement général des événements (utile car après on va ajouter des choses dedans)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.jeu.changer_etat(Map(self.jeu))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            for zone in self.zones_mont_azur:
                if self.zones_mont_azur[zone][0].collidepoint(event.pos): 
                    self.jeu.changer_etat(self.zones_mont_azur[zone][1])

class Chateau(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_chateau.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_chateau = {"zone_Pendu" : [pygame.Rect(675,725,400,300), Pendu(self.jeu)],
                              "zone_Pendule" : [pygame.Rect(1000,400,500,325), Pendule(self.jeu)]
                              }

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           for zone in self.zones_chateau:
               if self.zones_chateau[zone][0].collidepoint(event.pos): 
                   self.jeu.changer_etat(self.zones_chateau[zone][1])
           
    

class Donkey_kong_mario(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Donkey_kong_mario.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)


class Etat0(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "etat0.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.show_menu = True

    def handle_events(self, event):
        super().handle_events(event)
        


class Enigme(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "enigme2.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        


class Memoire_combi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Mémoire_combi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        
class Pendu(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendu.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        

class Pendule(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendule.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        

class Portes(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Portes.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        

class Tir_arc(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Tir_arc.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        

class Vitesse(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Vitesse.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)  
        


jeu = Jeu()
jeu.run()


#LA ZONE POUR LE CHATEAU EST BOF!

#A MARQUER DANS LES REGLAGES : pour revenir en arrière une fois l'inventaire, la carte, les réglages ouverts il est possible de réappuyer sur la touche correspondante


#ATTENTION : les touches permettent de revenir sur le lieu d'avant (peut-etre problemes plus-tard)