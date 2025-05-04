import pygame
import os


class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       self.last_event = None #va nous etre utile dans le draw des mini-jeux pour afficher regles et aide
       self.font=self.jeu.font
       self.show_menu = show_menu
       self.show_map = show_map

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

       self.map = pygame.image.load(os.path.join("assets","fonds","carte.png"))
       self.map = pygame.transform.scale(self.map, (self.jeu.bg_width, self.jeu.bg_height))
       #FAIRE UNE CLASSE A PART POUR INVENTAIRE, REGLAGES, CARTE
       
       #dico qui stocke les niveaux de jeu (0), les règles(1), les aides(2)
       self.niveaux_jeux = {"Donkey_kong_mario" :[0, " ", " ",pygame.image.load(os.path.join("assets","items", "oeuf de phoenix.png")),False],
                             "Enigme" : [0, "Entrez un mot\n(sans son déterminant)\npour répondre à l'énigme,\nsi vous répondez faux\n3 fois d'affilé,\nattendez le délais", " ",pygame.image.load(os.path.join("assets","items", "sève sagesse.png")),False],
                             "Memoire_combi" : [0, "Restituez la\ncombinaison de\nsymboles qui\napparaissent en\nappuyant sur ceux\nde la liste", " ",pygame.image.load(os.path.join("assets","items", "grain d'ambre.png")),False],
                             "Pendu" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "cheveux de Rossier.png")),False],
                             "Pendule" : [0, "Cliquez sur le\nbouton stop au\nbon moment\npour arreter\nles aiguilles", " ",pygame.image.load(os.path.join("assets","items", "poudre de perlinpimpim.png")),False],
                             "Portes" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "pomme de la discorde.png")),False],
                             "Tir_arc" :[0, "Cliquez sur l'écran pour\ntirer une flèche\nle niveau est passé\n si elle atteint la cible\nà la fin de la\ntrajectoire", "C'est à la fin de son\nmouvement que la flèche\npeut toucher la cible",pygame.image.load(os.path.join("assets","items", "Epine de Sylve.png")),False],
                             "Vitesse" : [0, "Ecrivez les mots\nles plus rapidement\n possibles en \nrespectant le délai\n des 5 secondes", " ",pygame.image.load(os.path.join("assets","items", "éclat d'obsidrune.png")),False],
                             "Bon_minerai" :[0, "Associez le bon\nnom au bon minerai", " ",pygame.image.load(os.path.join("assets","items", "pépite d'or.png")),False],
                             "Trad" : [0, "En cliquant sur les tirets\nentrez lettres à lettres\nvos propositions\nde traduction puis\nvalidez, si la lettre est\nmauvaise elle sera\nrouge", "Résolvez la\ntraduction 4\njuste après la 3",pygame.image.load(os.path.join("assets","items", "glace millénaire.png")),False],
                             "Eau" : [0, "Récupérez       \nles gouttes     \nqui tombent    \nen évitant   \nles feuilles    ", "Au plus vous    \nrécupérez     \nde gouttes    \nau plus   \nle jeu devient   \ndur",pygame.image.load(os.path.join("assets","items", "rosée du désert.png")),False],
                             "Krabi" :[0, " ", " ",pygame.image.load(os.path.join("assets","items", "pince de Kraby.png")),False],
                             "Zephyr" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "poussière du Zéphyr.png")),False],
                             "Mars" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "Sel de Mars.png")),False],
                             "Chaudron" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "Elixir des mondes.png")),False]                    
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
                     
    def handle_events_souris(self,event):
        from général.menu import Map
        self.last_event = event #pour récuperer event dans le draw pour l'appel d'une fonction
        #CLics souris             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
        # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
          if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Map(self.jeu))
          if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
              from général.menu import Inventaire
              print(self.show_menu)
              self.menu = False
              print(self.show_menu)
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
          
    def mini_jeu_fini(self, mini_jeu):
        print("mini-jeu réussi !")
        print("obtention de l'objet")

        objet = pygame.image.load(os.path.join("assets","items", "objet.png"))
        screen_width, screen_height = self.jeu.screen.get_size()
        objet = pygame.transform.scale(objet, (screen_width, screen_height))

        pygame.mixer.init()  #initialise le module audio
        pygame.mixer.music.load(os.path.join("assets", "BotW-item.mp3"))
        self.volume= pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

        prop = 0.5
        zone_affichage = pygame.Rect(
        (self.jeu.bg_width - (self.jeu.bg_width / 4)) // 2,  
        (self.jeu.bg_height - (self.jeu.bg_height / 4)) // 2.4,  
        self.jeu.bg_width // 4, 
        self.jeu.bg_height // 4 
        )
        new_width = int(self.niveaux_jeux[mini_jeu][3].get_width() * prop)
        new_height = int(self.niveaux_jeux[mini_jeu][3].get_height() * prop)
        resized_image = pygame.transform.scale(self.niveaux_jeux[mini_jeu][3], (new_width, new_height)).convert_alpha()

        self.jeu.screen.blit(objet, (0, 0))  
        self.jeu.screen.blit(resized_image,(zone_affichage.x * 1.02, zone_affichage.y * 1.02))
        pygame.display.flip()

        self.niveaux_jeux[mini_jeu][4] = True  
        pygame.time.delay(2000)

        pygame.mixer.music.load(os.path.join("assets", "musique_jeu.mp3"))
        pygame.mixer.music.play(-1)

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
    
    def Animation_debut(self):
     print("initialisation cinématique début")
     prop = 0.25
     self.objet = pygame.image.load(os.path.join("assets", "items", "objet.png"))
     self.objet = pygame.transform.scale(self.objet, (self.bg_width, self.bg_height))
     fee_width = int(self.bg_width * prop)
     fee_height = int(self.bg_width * prop)
     self.fee = pygame.image.load(os.path.join("assets", "fee.png"))
     self.fee = pygame.transform.scale(self.fee, (fee_width, fee_height))
     self.zone_reponse = pygame.Rect(int(self.bg_width / 8), int(self.bg_height / 1.4), int(self.bg_width / 2),
                                    int(self.bg_height / 12))
     self.skip_font = pygame.font.SysFont(None, int(self.bg_height * 0.035))
     self.skip_text = self.skip_font.render("Skip", True, "#FFFFFF")
     self.skip_width = self.skip_text.get_width() + 20
     self.skip_height = self.skip_text.get_height() + 10
     self.skip_button = pygame.Rect(self.bg_width - self.skip_width - 20, self.bg_height - self.skip_height - 20,
                                   self.skip_width, self.skip_height)
     self.mots = ["Bienvenue à Etheris, je suis la fée de ce monde imaginaire et je vous guiderais lors de votre aventure",
                 "Lors de votre aventure vous allez devoir compléter des mini-jeux afin de concevoir l'elixir des mondes ",
                 "Il vous permettra de vous échapper et de revenir dans votre monde, Bonne chance"]
     pygame.draw.rect(self.screen, "#4d3020", self.zone_reponse, border_radius=int(self.bg_height / 54))
     self.screen.blit(self.objet, (0, 0))
     self.screen.blit(self.fee, (0, 0))
     pygame.display.flip()
     self.temps = pygame.time.get_ticks()  
     self.durée = 2000  

     i = 0
     while i < len(self.mots):
        current_time = pygame.time.get_ticks()  
        elapsed_time = current_time - self.temps  

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.skip_button.collidepoint(event.pos):  
                    i = len(self.mots)  

        if elapsed_time >= self.durée:
            self.temps = current_time  
            self.screen.blit(self.objet, (0, 0))
            self.screen.blit(self.fee, (0, 0))
            pygame.draw.rect(self.screen, "#4d3020", self.skip_button, border_radius=8)
            self.screen.blit(self.skip_text, (self.skip_button.x + 10, self.skip_button.y + 5))
            texte = self.font.render(self.mots[i], True, "#FFFFFF")
            self.screen.blit(texte, (self.zone_reponse.x * 1.02, self.zone_reponse.y * 1.02))
            pygame.display.flip()
            i += 1  

     pygame.time.wait(1000)
     from général.menu_deb import Menu_debut
     self.etat = Menu_debut(self)
    
