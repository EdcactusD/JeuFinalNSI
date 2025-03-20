import pygame
import os

 
"""
REGLE A RESPECTER DANS LE CODE :
    ¤) pour definir des tailles d'objets faites le par une multiplication ou une division (pour que les valeurs soient toujours bien même si l'écran a une taille étrange)
    :::faire attention par exemple les rects n'accptent pas de float il faut alors caster
    
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
        

class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False, show_inventaire=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       
       self.font=self.jeu.font
       self.show_menu = show_menu
       self.show_map = show_map
       self.show_inventaire = show_inventaire

       self.bg_image = pygame.Surface((self.jeu.bg_width, self.jeu.bg_height))  # Fond par défaut (evite de planter si sous classe n'a pas de fond) // Surface crée un sorte de zone de dessin
       self.bg_image.fill((0, 0, 0))
       
       self.menu = pygame.image.load(os.path.join("assets", "menu.png"))
       self.menu_width, self.menu_height = int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/2.16) #en 1920x1080 : 100 et 500
       self.menu = pygame.transform.scale(self.menu, (self.menu_width, self.menu_height))
       self.menu_x = self.jeu.bg_width - self.menu_width - int(self.jeu.bg_width/384) #pour déclaler du bord (marge de 5 en 1920)
       self.menu_y = self.jeu.bg_height - self.menu_height - int(self.jeu.bg_height/216)
       self.zone_map_ic = pygame.Rect(self.menu_x, self.menu_y+int(self.jeu.bg_height/56.84), self.menu_width, int(self.jeu.bg_height/10.8))
       self.zone_inventaire_ic = pygame.Rect(self.menu_x, self.menu_y+int(self.jeu.bg_height/8.0597), self.menu_width, int(self.jeu.bg_height/10.8))
       self.zone_reglages_ic = pygame.Rect(self.menu_x, self.menu_y+int(self.jeu.bg_height/4.4081), self.menu_width, int(self.jeu.bg_height/10.8))
       
              
       self.inventaire = pygame.image.load(os.path.join("assets", "Test.jpg"))
       self.inventaire = pygame.transform.scale(self.inventaire, (self.jeu.bg_width, self.jeu.bg_height))

       self.map = pygame.image.load(os.path.join("assets","fonds","carte.png"))
       self.map = pygame.transform.scale(self.map, (self.jeu.bg_width, self.jeu.bg_height))
       #FAIRE UNE CLASSE A PART POUR INVENTAIRE, REGLAGES, CARTE
       
       self.niveaux_jeux = {"Mont_azur" : 0,
                            "Chateau" : 0,
                            "Donkey_kong_mario" : 0,
                            "Enigme" : 0,
                            "Memoire_combi" : 0,
                            "Pendu" : 0,
                            "Pendule" : 0,
                            "Portes" : 0,
                            "Tir_arc" : 0,
                            "Vitesse" : 0,
                            "Bon_minerai" : 0,
                            "Trad" : 0,
                            "Eau" : 0,
                            "Krabi" : 0,
                            "Zephyr" : 0,
                            "Mars" : 0,
                            "Chaudron" : 0,                    
           }
    def handle_events_keys(self,event):
        #Touches pressées
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
               self.show_menu = not self.show_menu
            if event.key == pygame.K_x: 
              self.jeu.changer_etat(Map(self.jeu))
            if event.key == pygame.K_c and self.show_menu:  
                     self.jeu.changer_etat(Inventaire(self.jeu))
                     
    def handle_events_souris(self,event):
        #CLics souris             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
        # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
          if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Map(self.jeu))
          if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Inventaire(self.jeu))
          if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Reglages(self.jeu))
              
    def handle_events(self, event):
        self.handle_events_keys(event)
        self.handle_events_souris(event)            
          
    
 
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
            
    """def update_niveau(self, mini_jeu, nouv_niveau):
        '''pour modifier le dico'''
        if int(mini_jeu) in self.niveaux_jeux :
            self.niveaux_jeux[int(mini_jeu)]=nouv_niveau # pour l'instant ne sert à rien """

         

class Menu_debut:
  """gère l'écran qui s'affiche pour lancer le jeu"""
  def __init__(self, jeu):
      self.jeu = jeu
      
      self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "menudebut.png"))
      self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))  
      self.width_bouton, self.height_bouton, self.espace = int(self.jeu.bg_width/4.8), int(self.jeu.bg_height/9.8181), int(self.jeu.bg_height/7.2)
      self.boutons = {"Jouer" : pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2), self.width_bouton, self.height_bouton), #permet de lancer le jeu avec la dernière sauvegarde
                      "Lancer une nouvelle partie" : pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2)+self.espace, self.width_bouton, self.height_bouton),
                      "Quitter" : pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2)+self.espace*2, self.width_bouton, self.height_bouton)
          }
      self.font=self.jeu.font
      
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
           self.boutons[bouton]=self.boutons[bouton].inflate(int(self.jeu.bg_width/49.5),int(self.jeu.bg_height/98.18)) #.inflate revoie un nouveau rect avec une taille modifiée
      elif self.boutons[bouton][2]!=self.width_bouton:
           self.boutons[bouton]=self.boutons[bouton].inflate(int(-self.jeu.bg_width/49.5),int(-self.jeu.bg_height/98.18))
      pygame.draw.rect(screen, "#834c2c", self.boutons[bouton], border_radius=int(self.jeu.bg_height/54))
      screen.blit(self.font.render(bouton, True, "#d9aa62"), self.font.render(bouton, True, "#d9aa62").get_rect(center=self.boutons[bouton].center)) #le .get_rect permet de créer un rect pour le texte, le center= permet de poser le centre au milieu du rect (et non en haut à gauche)
       
class Reglages(Etats):
  pass

class Inventaire(Etats):
 pass

      
class Map(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
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
            
                
class Mont_azur(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_mont_azur.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_mont_azur = {"zone_Donkey_kong_mario" : [pygame.Rect(int(self.jeu.bg_width/2.2588),int(self.jeu.bg_height/1.661),int(self.jeu.bg_width/3.2),int(self.jeu.bg_height/2.7)), Donkey_kong_mario],
                                "zone_Trad" : [pygame.Rect(int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/3.2),int(self.jeu.bg_height/1.96)),Trad]}
        
    def handle_events(self, event):
        super().handle_events(event) # Garde le comportement général des événements (utile car après on va ajouter des choses dedans)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            self.jeu.changer_etat(Map(self.jeu))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            for zone in self.zones_mont_azur:
                if self.zones_mont_azur[zone][0].collidepoint(event.pos): 
                    self.jeu.changer_etat(self.zones_mont_azur[zone][1](self.jeu))

class Chateau(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_chateau.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_chateau = {"zone_Pendu" : [pygame.Rect(int(self.jeu.bg_width/2.844),int(self.jeu.bg_height/1.4896),int(self.jeu.bg_width/4.8),int(self.jeu.bg_height/3.6)), Pendu],
                              "zone_Pendule" : [pygame.Rect(int(self.jeu.bg_width/1.92),int(self.jeu.bg_height/2.7),int(self.jeu.bg_width/3.84),int(self.jeu.bg_height/3.32)), Pendule]
                              }

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           for zone in self.zones_chateau:
               if self.zones_chateau[zone][0].collidepoint(event.pos): 
                   self.jeu.changer_etat(self.zones_chateau[zone][1](self.jeu))
           
    

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
        self.regles_ic = pygame.image.load(os.path.join("assets","aide.jpg"))
        self.regles_ic=pygame.transform.scale(self.regles_ic,(int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8)))
        self.rect_regles_ic=pygame.Rect(int(self.jeu.bg_height/120), self.jeu.bg_height - int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8))
        self.show_regles=False
        self.rect_regles=pygame.Rect(self.rect_regles_ic.x, self.rect_regles_ic.y - int(self.jeu.bg_width/19.2) ,int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8))
        
        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Enigme"])
        self.enigmes = { "0": ["On me pose sans me toucher.","question"], #dico des énigmes (énigme, réponse)
                         "1": ["Je ne suis pas vivant mais je grandi,\nJe meurs sous l’eau\nJe n’ai pas de poumons mais j’ai besoin d’air","feu"],
                         "2": ["Je peux être audible, visible ou odorante,\nmais jamais les trois à la fois \nJe peux être basse \nou haute sans jamais tomber.\nJ’évalue sans parler.\nJe suis florale ou boisée.","note"],
                         "3": ["Je suis mort et je peux hanter \nou bien je peux être ouvert \nou fermé sans être touché\net vif ou lent sans jamais bouger","esprit"],
                         "4": ["Encore une fois, on ne peut me voir,\nmais on ne peut me toucher. \nLes pauvres m’ont,\nles riches ont besoin de moi.","rien"]            
}
        
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.reponse_uti = ""
        self.redaction=False
        
        self.mauvaise_rep=0
        self.attendre = False #permet de faire attendre le joueur s'il a proposé trop de mauvaises réponses
        self.attente= 60000*5 #en milisecondes 
        self.debut_attente= -self.attente #par défaut, comme ça le if est vrai si le joueur n'a pas eu faux

    def handle_events(self, event):
        if pygame.time.get_ticks()-self.debut_attente>self.attente:
           self.attendre=False
        else : 
            self.attendre=True
        
        if self.redaction: 
            """pour qu'il soit possible d'écrire avec toutes les touches"""
            super().handle_events_souris(event)
        else:
            super().handle_events(event)  
            
        #si on clique sur la zone de texte il est possible de commencer à taper la réponse sinon non 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.zone_reponse.collidepoint(event.pos) and self.attendre==False:
            self.redaction=True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos)) or self.attendre==True:
            self.redaction=False
            
        if self.redaction==True and event.type == pygame.KEYDOWN:
            """Pour enlever un caractère"""
            if event.key==pygame.K_BACKSPACE: 
                self.ancienne_rep=self.reponse_uti
                self.reponse_uti=""
                for i in range(len(self.ancienne_rep)-1):
                    self.reponse_uti+=self.ancienne_rep[i]
            elif event.key == pygame.K_RETURN:
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau!="4" :
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau=="4" :
                    print("mini-jeu réussit !")
                    self.jeu.changer_etat(Map(self.jeu))
                    #MARQUER le jeu comme fait (impossible d'y revenir)
                else:
                    self.mauvaise_rep+=1
                    if self.mauvaise_rep>=3:
                        self.mauvaise_rep=0
                        self.debut_attente=pygame.time.get_ticks()
                        self.reponse_uti=""
                        print("vous devez attendre 5 minutes pour soumettre de nouveau une réponse")
                        
            elif len(self.reponse_uti)<=23:    
              self.reponse_uti += event.unicode  # Ajoute uniquement le caractère tapé
            else:
                print("trop long!")
                       
        if event.type == pygame.MOUSEMOTION and self.rect_regles_ic.collidepoint(event.pos):
            self.show_regles=True
        else:
            self.show_regles=False
        
        
    
    def draw(self, screen):
        super().draw(screen)
        
        screen.blit(self.regles_ic, (self.rect_regles_ic.x, self.rect_regles_ic.y))
        
        lignes= self.enigmes[self.niveau][0].split("\n") #font.render ne supporte pas \n pour le retour à la ligne, il faut le coder manuellement     
        espace = 0 #pour gérer l'espacement entre les lignes
        for ligne in lignes:
          self.texte=self.font.render(ligne, True, (123,85,57))
          screen.blit(self.texte, (int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/2.7+espace)))
          espace+=self.jeu.bg_height/23
        
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        if self.attente-(pygame.time.get_ticks()-self.debut_attente)>0: #on affiche le chronomètre tant qu'il reste du temps à attendre
          self.minutes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) // 60000  # Nombre de minutes restantes
          self.secondes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) % 60000 // 1000  # Nombre de secondes restantes

          # Format propre mm:ss (avec zéro devant si nécessaire)
          self.temps_affiche = f"{self.minutes}:{self.secondes:02d}"  #0 : complete par un 0, 2 :le nombre doit avoir 2 chiffres, d : est un entier (digit)
          screen.blit(self.font.render(self.temps_affiche, True, "white"),(0, 0))
          
        if self.show_regles:
          pygame.draw.rect(screen, "white", self.rect_regles, border_radius=int(self.jeu.bg_height/54))
          #screen.blit(self.rect_regles, (int(self.jeu.bg_height/19.2), self.jeu.bg_height - int(self.jeu.bg_height/10.8) - int(self.jeu.bg_height/10.8)))
            



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
        
class Bon_minerai(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Bon_minerai.jpeg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Trad(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Trad.jpeg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Eau(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Eau.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Krabi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Krabi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Zephyr(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Zephyr.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Mars(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Mars.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Chaudron(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Vitesse.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

jeu = Jeu()
jeu.run()


#A MARQUER DANS LES REGLAGES : pour revenir en arrière une fois l'inventaire, la carte, les réglages ouverts il est possible de réappuyer sur la touche correspondante

#Pour jeux avec entrée texte : faire un curseur qui clignote ?
#Les prints dans enigme sont à modifier en messages qui popent

#ATTENTION : pour le bon fonctionnement du jeu, quand on change d'état certaines caracteristiques doivent être conservées (genre le temps du chrono en cours, le niveau atteint)