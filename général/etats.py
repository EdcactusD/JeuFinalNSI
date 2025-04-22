import pygame
import os


class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False, show_inventaire=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       self.last_event = None #va nous etre utile dans le draw des mini-jeux pour afficher regles et aide
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
       
       #dico qui stocke les niveaux de jeu (0), les règles(1), les aides(2)
       self.niveaux_jeux = {"Donkey_kong_mario" :[0, " ", " "],
                             "Enigme" : [0, "Entrez un mot\n(sans son déterminant)\npour répondre à l'énigme,\nsi vous répondez faux\n3 fois d'affilé,\nattendez le délais", " "],
                             "Memoire_combi" : [0, "Restituez la\ncombinaison de\nsymboles qui\napparaissent en\nappuyant sur ceux\nde la liste", " "],
                             "Pendu" : [0, " ", " "],
                             "Pendule" : [0, "Cliquez sur le\nbouton stop au\nbon moment\npour arreter\nles aiguilles", " "],
                             "Portes" : [0, " ", " "],
                             "Tir_arc" :[0, "Cliquez sur l'écran pour\ntirer une flèche\nle niveau est passé\n si elle atteint la cible\nà la fin de la\ntrajectoire", "C'est à la fin de son\nmouvement que la flèche\npeut toucher la cible"],
                             "Vitesse" : [0, "Ecrivez les mots\nles plus rapidement\n possibles en \nrespectant le délai\n des 5 secondes", " "],
                             "Bon_minerai" :[0, "Associez le bon\nnom au bon minerai", " "],
                             "Trad" : [0, "En cliquant sur les tirets\nentrez lettres à lettres\nvos propositions\nde traduction puis\nvalidez, si la lettre est\nmauvaise elle sera\nrouge", "Résolvez la\ntraduction 4\njuste après la 3"],
                             "Eau" : [0, " ", " "],
                             "Krabi" :[0, " ", " "],
                             "Zephyr" : [0, " ", " "],
                             "Mars" : [0, " ", " "],
                             "Chaudron" : [0, " ", " "]                    
            }
       
       #pour les icones de regles et aide dans les mini-jeux
       self.regles_ic = pygame.image.load(os.path.join("assets","regles.png"))
       self.regles_ic=pygame.transform.scale(self.regles_ic,(int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8)))
       self.rect_regles_ic=pygame.Rect(int(self.jeu.bg_height/120), self.jeu.bg_height - int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/20), int(self.jeu.bg_height/10.8))
       self.show_regles=False
       self.rect_regles=pygame.Rect(self.rect_regles_ic.x, self.rect_regles_ic.y - int(self.jeu.bg_height/5) ,int(self.jeu.bg_width/7.5), int(self.jeu.bg_height/5))
 
       self.aide_ic = pygame.image.load(os.path.join("assets","aide.png"))
       self.aide_ic=pygame.transform.scale(self.aide_ic,(int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8)))
       self.rect_aide_ic=pygame.Rect(int(self.jeu.bg_width/18), self.jeu.bg_height - int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8))
       self.show_aide=False
       self.rect_aide=pygame.Rect(self.rect_aide_ic.x, self.rect_aide_ic.y - int(self.jeu.bg_height/5) ,int(self.jeu.bg_width/7.5), int(self.jeu.bg_height/5))
    
    def montrer_regles_aide(self, screen,event, nom_mini_jeu):
         if event != None :
             if event.type == pygame.MOUSEMOTION and self.rect_regles_ic.collidepoint(event.pos):
                 self.show_regles=True
             else:
                 self.show_regles=False
             if event.type == pygame.MOUSEMOTION and self.rect_aide_ic.collidepoint(event.pos):
                 self.show_aide=True
             else:
                 self.show_aide=False
 
             screen.blit(self.regles_ic, (self.rect_regles_ic.x, self.rect_regles_ic.y))
             screen.blit(self.aide_ic, (self.rect_aide_ic.x, self.rect_aide_ic.y)) 
             
             self.font_petit = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_width/(len(self.niveaux_jeux[nom_mini_jeu][1])/1.2)))
             if self.show_regles:
               self.font_petit = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_width/(len(self.niveaux_jeux[nom_mini_jeu][1])/1.2)))
               pygame.draw.rect(screen, "white", self.rect_regles, border_radius=int(self.jeu.bg_height/54))
               self.sauter_ligne(self.niveaux_jeux[nom_mini_jeu][1], self.rect_regles.x+10, self.rect_regles.y,45,self.font_petit,(123,85,57), screen)
             if self.show_aide:
                 pygame.draw.rect(screen, "white", self.rect_aide, border_radius=int(self.jeu.bg_height/54))
                 self.sauter_ligne(self.niveaux_jeux[nom_mini_jeu][2], self.rect_aide.x+10, self.rect_aide.y,45,self.font_petit,(123,85,57), screen)
 
        
        
    def handle_events_keys(self,event):
        from général.menu import Map
        #Touches pressées
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
               self.show_menu = not self.show_menu
            if event.key == pygame.K_x: 
              self.jeu.changer_etat(Map(self.jeu))
            if event.key == pygame.K_c:  
                     from général.menu import Inventaire # Import retardé pour éviter les boucles circulaires
                     self.jeu.changer_etat(Inventaire(self.jeu))
                     
    def handle_events_souris(self,event):
        from général.menu import Map
        self.last_event = event #pour récuperer event dans le draw pour l'appel d'une fonction
        #CLics souris             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
        # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
          if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Map(self.jeu))
          if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
              from général.menu import Inventaire # Import retardé pour éviter les boucles circulaires
              self.jeu.changer_etat(Inventaire(self.jeu))
          if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
              from général.menu import Reglages # Import retardé pour éviter les boucles circulaires
              self.jeu.changer_etat(Reglages(self.jeu))
              
    def handle_events(self, event): #dans certains jeu d'entrée de texte il peut être utile de désactiver un temps les raccoucis, c'est pourquoi les deux fonctions sont séparées
        self.handle_events_keys(event)
        self.handle_events_souris(event)            
     
    def sauter_ligne(self, recuperer_texte, pos_x, pos_y, espace_ratio, font,couleur, screen):
        """permet de sauter des lignes avec les font.render"""
        lignes= recuperer_texte.split("\n") #font.render ne supporte pas \n pour le retour à la ligne, il faut le coder manuellement     
        espace = 0 #pour gérer l'espacement entre les lignes
        for ligne in lignes:
          self.texte=font.render(ligne, True, couleur)
          screen.blit(self.texte, (pos_x, pos_y+espace))
          espace+=self.jeu.bg_height/espace_ratio
          
    def mini_jeu_fini(self):
        print("mini-jeu réussit !")
        from général.menu import Map
        self.jeu.changer_etat(Map(self.jeu))
        #MARQUER le jeu comme fait (impossible d'y revenir)

 
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
