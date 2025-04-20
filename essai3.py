import pygame
import os
import time
import random
import math
from math import sqrt

from menu_deb import Menu_debut


 
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
       
       #dico qui stocke les niveaux de jeu (0), les règles(1), les aides (2)
       self.niveaux_jeux = {"Mont_azur" : [0, " ", " "],
                             "Chateau" : [0, " ", " "],
                             "Donkey_kong_mario" :[0, " ", " "],
                             "Enigme" : [0, "Entrez un mot\n(sans son déterminant)\npour répondre à l'énigme,\nsi vous répondez faux\n3 fois d'affilé,\nattendez le délais", " "],
                             "Memoire_combi" : [0, "Restituez la\ncombinaison de\nsymboles qui\napparaissent en\nappuyant sur ceux\nde la liste", " "],
                             "Pendu" : [0, " ", " "],
                             "Pendule" : [0, "Cliquez sur le\nbouton stop au\nbon moment\npour arreter\nles aiguilles", " "],
                             "Portes" : [0, " ", " "],
                             "Tir_arc" :[0, "Cliquez sur l'écran pour\ntirer une flèche\nle niveau est passé\n si elle atteint la cible\nà la fin de la\ntrajectoire", "C'est à la fin de son\nmouvement que la flèche\npeut toucher la cible"],
                             "Vitesse" : [0, "Ecrivez les mots\nles plus rapidement\n possibles en \nrespectant le délai\n des 5 secondes", " "],
                             "Bon_minerai" :[0, "Associez le bon\n nom au bon minerai", " "],
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
        from menu import Map
        #Touches pressées
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
               self.show_menu = not self.show_menu
            if event.key == pygame.K_x: 
              self.jeu.changer_etat(Map(self.jeu))
            if event.key == pygame.K_c:  
                     from menu import Inventaire # Import retardé pour éviter les boucles circulaires
                     self.jeu.changer_etat(Inventaire(self.jeu))
                     
    def handle_events_souris(self,event):
        from menu import Map
        self.last_event = event #pour récuperer event dans le draw pour l'appel d'une fonction
        #CLics souris             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
        # Vérifiez si la zone est cliquée uniquement lorsque la carte est ouverte
          if self.show_menu and self.zone_map_ic.collidepoint(event.pos):
              self.jeu.changer_etat(Map(self.jeu))
          if self.show_menu and self.zone_inventaire_ic.collidepoint(event.pos):
              from menu import Inventaire # Import retardé pour éviter les boucles circulaires
              self.jeu.changer_etat(Inventaire(self.jeu))
          if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
              from menu import Reglages # Import retardé pour éviter les boucles circulaires
              self.jeu.changer_etat(Reglages(self.jeu))
              
    def handle_events(self, event):
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
    """Mini-jeu qui affiche des énigmes, le joueur doit y répondre en les tapant dans une zone de texte
    réutilise les méthodes d'Etats() et prend notamment les valeurs dans son dico self.niveaux_jeux pour adapter au bon niveau
    renvoie le nouveau niveau atteind/si le jeu est fini"""
    def __init__(self, jeu):
        super().__init__(jeu)
        
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "enigme2.png"))
        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Enigme"][0])
        self.enigmes = { "0": ["On me pose sans me toucher.","question"], #dico des énigmes (énigme, réponse)
                         "1": ["Je ne suis pas vivant mais je grandi,\nJe meurs sous l’eau\nJe n’ai pas de poumons mais j’ai besoin d’air","feu"],
                         "2": ["Je peux être audible, visible ou odorante,\nmais jamais les trois à la fois \nJe peux être basse \nou haute sans jamais tomber.\nJ’évalue sans parler.\nJe suis florale ou boisée.","note"],
                         "3": ["Je suis mort et je peux hanter \nou bien je peux être ouvert \nou fermé sans être touché\net vif ou lent sans jamais bouger","esprit"],
                         "4": ["Encore une fois, on ne peut me voir,\nmais on ne peut me toucher. \nLes pauvres m’ont,\nles riches ont besoin de moi.","rien"]            
}
        self.dernier_niveau="4"
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.reponse_uti = ""
        self.redaction=False
        self.lenmax = 23 #permet d'éviter de sortir de la zone de texte
        
        self.mauvaise_rep=0
        self.attendre = False #permet de faire attendre le joueur s'il a proposé trop de mauvaises réponses
        self.attente= 60000*1 #en milisecondes 
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
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau!=self.dernier_niveau :
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau==self.dernier_niveau :
                    print("mini-jeu réussit !")
                    self.jeu.changer_etat(Map(self.jeu))
                    #MARQUER le jeu comme fait (impossible d'y revenir)
                else:
                    self.mauvaise_rep+=1
                    if self.mauvaise_rep>3:
                        self.mauvaise_rep=0
                        self.debut_attente=pygame.time.get_ticks()
                        self.reponse_uti=""
                        print("vous devez attendre 1 minutes pour soumettre de nouveau une réponse")
                        
            elif len(self.reponse_uti)<=self.lenmax:    
              self.reponse_uti += event.unicode  # Ajoute uniquement le caractère tapé
            else:
                print("trop long!")
        
    
    def draw(self, screen):
        super().draw(screen)
        
        #récupéré dans la super classe
        self.sauter_ligne(self.enigmes[self.niveau][0], int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/2.7),23,self.font,(123,85,57), screen)
        
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
          screen.blit(self.font.render(self.temps_affiche, True, "#4d3020"),(int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/3.8)))
          

        self.montrer_regles_aide(screen, self.last_event, "Enigme")
        


class Memoire_combi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Mémoire_combi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Memoire_combi"][0])
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width / 2.8), int(self.jeu.bg_height / 1.4), int(self.jeu.bg_width / 3.5), int(self.jeu.bg_height / 12))
        self.zone_affichage = pygame.Rect(int(self.jeu.bg_width / 2.8), int(self.jeu.bg_height / 2), int(self.jeu.bg_width / 3.5), int(self.jeu.bg_height / 6))
        self.zone_noms = pygame.Rect(int(self.jeu.bg_width / 10000), int(self.jeu.bg_height / 5.1), int(self.jeu.bg_width / 10), int(self.jeu.bg_height / 1.95))
        self.font_symboles = pygame.font.Font(os.path.join("assets", "unifont-16.0.02.otf"), int(self.jeu.bg_height / 25))
        self.combi = {
            "0": ["☾ᛉ⊕♄⛧"],
            "1": ["ᚠᛏ♆ᛗ☉ᛉ"],
            "2": ["ᚦᛚᛋᛟᛞ♆♄♃☿"]
        }
        self.noms = "ᚠ   ᛒ\nᚦ   ᚲ\n☾   ᚨ\n♇   ᚹ\nᛉ   ᛋ\nᛏ   ᛚ\n⛥  ᚢ\n☉   ᛟ\n⊕   ᚱ\n☿   ♃\n♄   ♅\n⛧  ᛞ\nᛗ   ♆"
        self.symboles_liste = self.noms.split("\n")

        self.reponse_uti = ""
        self.espacement_additionnel = 50
        self.debut_temps = pygame.time.get_ticks()  
        self.afficher_combi = True

    def handle_events(self, event):
        super().handle_events(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.afficher_combi == False:
            pos = pygame.mouse.get_pos()
            for rect, symbole in self.rects_symboles:
                if rect.collidepoint(pos):
                    self.reponse_uti += symbole 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.reponse_uti = self.reponse_uti[:-1]  # Supprimer le dernier caractère

            if event.key == pygame.K_RETURN: 
              if self.reponse_uti.upper() == self.combi[self.niveau][0].upper():
                self.niveau = str(int(self.niveau) + 1) 
                self.reponse_uti = ""  
                self.debut_temps = pygame.time.get_ticks()
                self.afficher_combi = True  
              else:
               self.jeu.changer_etat(Map(self.jeu))
               print("Mini-jeu perdu")
               return

              if self.niveau == "3":
               print("Mini-jeu réussi!")
               self.jeu.changer_etat(Map(self.jeu))
               return

    def draw(self, screen):
        super().draw(screen)
        self.montrer_regles_aide(screen, self.last_event, "Memoire_combi")
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height / 54))
        pygame.draw.rect(screen, "#4d3020", self.zone_affichage, border_radius=int(self.jeu.bg_height / 54))
        pygame.draw.rect(screen, "#4d3020", self.zone_noms, border_radius=int(self.jeu.bg_height / 54))

        temps_ecoule = pygame.time.get_ticks() - self.debut_temps
        if temps_ecoule >= 5000:  
         self.afficher_combi = False

        if self.afficher_combi:
            screen.blit(self.font_symboles.render(self.combi[self.niveau][0], True, "#6f553c"),(self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))
        screen.blit(self.font_symboles.render(self.reponse_uti, True, "#ffffff"),(self.zone_reponse.x * 1.02, self.zone_reponse.y * 1.02))

        self.rects_symboles = []  # Liste pour les symboles cliquables
        ligne_height = self.font_symboles.get_height()
        espacement_horizontal = self.font_symboles.size("ᛚ")[0]  # Largeur d'un symbole, ajusté à un seul caractère
        y_offset = self.zone_noms.y  # Position verticale initiale pour la première ligne de symboles
        symboles_lignes = self.noms.split("\n")  # Chaque ligne = un élément de la liste
        for i, ligne in enumerate(symboles_lignes):
            x_offset = self.zone_noms.x  # Position horizontale de départ
            symbols = ligne.split()  # Créer une liste de symboles individuels
            for j, symbole in enumerate(symbols):
                symbole_surface = self.font_symboles.render(symbole, True, "#6f553c")
                symbole_rect = symbole_surface.get_rect()  # Créer un rectangle autour de chaque symbole
                symbole_rect.topleft = (x_offset + j * (espacement_horizontal + self.espacement_additionnel), y_offset)
                screen.blit(symbole_surface, symbole_rect.topleft)
                self.rects_symboles.append((symbole_rect, symbole))  # Ajouter le rectangle et le symbole à la liste
            y_offset += ligne_height  # Mettre à jour l'offset vertical pour la ligne suivante

        temps_ecoule = pygame.time.get_ticks() - self.debut_temps
        if self.afficher_combi:
         temps_restant = max(0, 5 - (temps_ecoule // 1000))  # Temps restant pour afficher la combinaison
         screen.blit(self.font_symboles.render(f"Temps restant : {temps_restant}s", True, "black"), 
                    (self.zone_affichage.x, self.zone_affichage.y - 40))


        
        
class Pendu(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendu.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.words_easy = ["chat", "chien", "pomme", "maison", "voiture"]
        self.words_medium = ["ordinateur", "python", "programmation", "hangman", "jeu"]
        self.words_hard = ["développement", "intelligence", "algorithmique", "complexité", "optimisation"]

        self.difficulty_levels = {
            "Easy": self.words_easy,
            "Medium": self.words_medium,
            "Hard": self.words_hard
        }

        self.difficulty = "Medium"
        self.word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        self.win = False
        self.input_active = False
        self.message = ""
        self.letter_input = ""
        self.font_large = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/20))
        self.font_medium = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/30))
        self.font_small = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/40))

        self.completed_difficulties = {"Easy": False, "Medium": False, "Hard": False}
        self.reward_given = False

        self.start_new_game()

        self.buttons = {
            "Easy": pygame.Rect(int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Medium": pygame.Rect(int(self.jeu.bg_width*0.22), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Hard": pygame.Rect(int(self.jeu.bg_width*0.34), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Restart": pygame.Rect(int(self.jeu.bg_width*0.8), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05))
        }

    def start_new_game(self):
        import random
        self.word = random.choice(self.difficulty_levels[self.difficulty]).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.win = False
        self.message = ""
        self.letter_input = ""
        self.input_active = True

    def handle_events(self, event):
        super().handle_events(event)
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons["Restart"].collidepoint(event.pos):
                    self.start_new_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    if key in ["Easy", "Medium", "Hard"]:
                        self.difficulty = key
                        self.start_new_game()
                    elif key == "Restart":
                        self.start_new_game()
                    return

        if event.type == pygame.KEYDOWN and self.input_active and not self.game_over:
            if event.key == pygame.K_BACKSPACE:
                self.letter_input = ""
            elif event.key == pygame.K_RETURN:
                if len(self.letter_input) == 1 and self.letter_input.isalpha():
                    letter = self.letter_input.upper()
                    if letter in self.guessed_letters:
                        self.message = f"Lettre '{letter}' déjà proposée."
                    else:
                        self.guessed_letters.add(letter)
                        if letter not in self.word:
                            self.wrong_guesses += 1
                            if self.wrong_guesses >= self.max_wrong_guesses:
                                self.game_over = True
                                self.win = False
                                self.message = f"Perdu ! Le mot était : {self.word}"
                        else:
                            if all(l in self.guessed_letters for l in self.word):
                                self.game_over = True
                                self.win = True
                                self.message = "Bravo ! Vous avez gagné !"
                                self.completed_difficulties[self.difficulty] = True
                                if all(self.completed_difficulties.values()) and not self.reward_given:
                                    self.reward_given = True
                                    self.message = "Félicitations ! Vous avez obtenu l'objet : cheveux de rossier"
                    self.letter_input = ""
                else:
                    self.message = "Entrez une seule lettre valide."
                    self.letter_input = ""
            else:
                if len(self.letter_input) == 0 and event.unicode.isalpha():
                    self.letter_input = event.unicode.upper()

    def draw_hangman(self, screen):
        base_x = int(self.jeu.bg_width * 0.7)
        base_y = int(self.jeu.bg_height * 0.8)
        line_color = (139, 69, 19)

        pygame.draw.line(screen, line_color, (base_x - 100, base_y), (base_x + 100, base_y), 8)
        pygame.draw.line(screen, line_color, (base_x - 50, base_y), (base_x - 50, base_y - 300), 8)
        pygame.draw.line(screen, line_color, (base_x - 50, base_y - 300), (base_x + 50, base_y - 300), 8)
        pygame.draw.line(screen, line_color, (base_x + 50, base_y - 300), (base_x + 50, base_y - 250), 8)

        if self.wrong_guesses > 0:
            pygame.draw.circle(screen, (0, 0, 0), (base_x + 50, base_y - 230), 20, 3)
        if self.wrong_guesses > 1:
            pygame.draw.line(screen, (0, 0, 0), (base_x + 50, base_y - 210), (base_x + 50, base_y - 150), 3)
        if self.wrong_guesses > 2:
            pygame.draw.line(screen, (0, 0, 0), (base_x + 50, base_y - 200), (base_x + 20, base_y - 170), 3)
        if self.wrong_guesses > 3:
            pygame.draw.line(screen, (0, 0, 0), (base_x + 50, base_y - 200), (base_x + 80, base_y - 170), 3)
        if self.wrong_guesses > 4:
            pygame.draw.line(screen, (0, 0, 0), (base_x + 50, base_y - 150), (base_x + 20, base_y - 110), 3)
        if self.wrong_guesses > 5:
            pygame.draw.line(screen, (0, 0, 0), (base_x + 50, base_y - 150), (base_x + 80, base_y - 110), 3)

    def draw_word(self, screen):
        display_word = ""
        for letter in self.word:
            display_word += letter + " " if letter in self.guessed_letters else "_ "
        text_surface = self.font_large.render(display_word.strip(), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.jeu.bg_width * 0.35, self.jeu.bg_height * 0.5))
        screen.blit(text_surface, text_rect)

    def draw_guessed_letters(self, screen):
        guessed = "Lettres proposées: " + " ".join(sorted(self.guessed_letters))
        text_surface = self.font_medium.render(guessed, True, (255, 255, 255))
        screen.blit(text_surface, (int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.7)))

    def draw_input_box(self, screen):
        input_box = pygame.Rect(int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.6), int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.05))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_text = self.font_medium.render(self.letter_input, True, (255, 255, 255))
        screen.blit(input_text, (input_box.x + 5, input_box.y + 5))
        prompt_text = self.font_small.render("Tapez une lettre et appuyez sur Entrée", True, (255, 255, 255))
        screen.blit(prompt_text, (input_box.x, input_box.y - 25))

    def draw_buttons(self, screen):
        for key, rect in self.buttons.items():
            color = (100, 100, 100)
            if key == self.difficulty:
                color = (200, 200, 50)
            pygame.draw.rect(screen, color, rect)
            text_surface = self.font_small.render(key, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def draw_message(self, screen):
        if self.message:
            message_surface = self.font_medium.render(self.message, True, (255, 0, 0))
            message_rect = message_surface.get_rect(center=(self.jeu.bg_width * 0.5, self.jeu.bg_height * 0.85))
            screen.blit(message_surface, message_rect)

    def draw(self, screen):
        super().draw(screen)

        overlay = pygame.Surface((self.jeu.bg_width, self.jeu.bg_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        titre = self.font_large.render("PENDU", True, (255, 255, 255))
        screen.blit(titre, (self.jeu.bg_width // 2 - titre.get_width() // 2, int(self.jeu.bg_height * 0.05)))

        self.draw_word(screen)
        self.draw_guessed_letters(screen)
        self.draw_input_box(screen)
        self.draw_buttons(screen)
        self.draw_hangman(screen)
        self.draw_message(screen)

        bar_width = int(self.jeu.bg_width * 0.6)
        bar_height = int(self.jeu.bg_height * 0.02)
        bar_x = (self.jeu.bg_width - bar_width) // 2
        bar_y = int(self.jeu.bg_height * 0.9)

        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        if self.wrong_guesses > 0:
            filled_width = bar_width * (self.wrong_guesses / self.max_wrong_guesses)
            pygame.draw.rect(screen, (200, 60, 60), (bar_x, bar_y, filled_width, bar_height), border_radius=10)

        

class Pendule(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendule.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zone_bouton = pygame.Rect(int(self.jeu.bg_width/2.1), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/11),int(self.jeu.bg_height/16))
        self.zone_angle = pygame.Rect(int(self.jeu.bg_width/3), int(self.jeu.bg_height/5),int(self.jeu.bg_width/2.8),int(self.jeu.bg_height/16))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gris = (112, 128, 144)
        self.brown = (139, 69, 19)
        self.center = (self.menu_width // 0.1, self.menu_height // 1)
        self.radius = 200
        self.angle = 0
        self.target_angle = random.choice([i * 30 for i in range(12)])
        self.objectif = [self.target_angle,self.target_angle+30]
        self.visee = "Arretez l'horloge entre " + str(self.objectif[0] // 30) +  "heures et " + str(self.objectif[1] // 30) + "heures"
        self.action = True
        print(self.target_angle)

    def handle_events(self, event):
        super().handle_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.zone_bouton.collidepoint(event.pos):
            self.action = False
            angle = self.angle
            print(angle)
            print(self.objectif)

            if self.objectif[0] <= self.angle <= self.objectif[1]:
             print("mini-jeu réussi!")
             self.jeu.changer_etat(Map(self.jeu))
            else:
             print("mini-jeu perdu!")
             self.jeu.changer_etat(Map(self.jeu))

    
    def draw(self, screen):
        super().draw(screen)
        if self.action == True:
          self.angle = (self.angle + 10) % 360

        pygame.draw.rect(screen,self.brown,self.zone_bouton,border_radius=int(self.jeu.bg_height / 5))
        screen.blit(self.font.render("   Stop", True, self.white),(self.zone_bouton.x*1.02, self.zone_bouton.y*1.02)) #Le True est pour adoucir le bord des textes

        pygame.draw.rect(screen,self.brown,self.zone_angle,border_radius=int(self.jeu.bg_height / 5))
        screen.blit(self.font.render(self.visee , True, self.white),(self.zone_angle.x*1.02, self.zone_angle.y*1.02))
    
        pygame.draw.circle(screen, self.brown, self.center, self.radius)
        pygame.draw.circle(screen, self.black, self.center, self.radius, 5)
        for i in range(12):
         x = self.center[0] + math.cos(math.radians(i * 30 - 90)) * (self.radius - 20)
         y = self.center[1] + math.sin(math.radians(i * 30 - 90)) * (self.radius - 20)
         pygame.draw.circle(screen, self.black, (int(x), int(y)), 5)

        aiguille_length = self.radius - 20
        end_x = self.center[0] + math.cos(math.radians(self.angle - 90)) * aiguille_length
        end_y = self.center[1] + math.sin(math.radians(self.angle - 90)) * aiguille_length
        pygame.draw.line(screen, self.gris, self.center, (end_x, end_y), width = 5)

        self.montrer_regles_aide(screen,self.last_event,"Pendule")



class Portes(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Portes.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.questions = [
            {"texte": "Quelle est la capitale de la France ?", "choix": ["Lyon", "Paris", "Marseille"], "bonne": "Paris"},
            {"texte": "Combien y a-t-il de continents ?", "choix": ["5", "6", "7"], "bonne": "7"},
            {"texte": "Quel est l'élément chimique O ?", "choix": ["Or", "Oxygène", "Osmium"], "bonne": "Oxygène"},
            {"texte": "Qui a peint la Joconde ?", "choix": ["Picasso", "Léonard de Vinci", "Van Gogh"], "bonne": "Léonard de Vinci"},
            {"texte": "Combien font 8 × 7 ?", "choix": ["56", "64", "49"], "bonne": "56"},
            {"texte": "Quel est le plus grand océan ?", "choix": ["Atlantique", "Arctique", "Pacifique"], "bonne": "Pacifique"},
            {"texte": "Quelle planète est la plus proche du Soleil ?", "choix": ["Mercure", "Vénus", "Mars"], "bonne": "Mercure"},
            {"texte": "Quelle langue est parlée au Brésil ?", "choix": ["Espagnol", "Portugais", "Français"], "bonne": "Portugais"}
        ]

        self.niveau = 0
        self.score = 0
        self.resultat = ""
        self.porte_cliquee = None

        self.creer_portes()

    def creer_portes(self):
        self.zone_portes = []
        largeur_porte = self.jeu.bg_width // 6
        hauteur_porte = self.jeu.bg_height // 3
        espace = self.jeu.bg_width // 20
        start_x = (self.jeu.bg_width - (3 * largeur_porte + 2 * espace)) // 2
        y = self.jeu.bg_height // 2
        choix = self.questions[self.niveau]["choix"]

        for i in range(3):
            rect = pygame.Rect(start_x + i * (largeur_porte + espace), y, largeur_porte, hauteur_porte)
            self.zone_portes.append((rect, choix[i]))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.resultat:
            for rect, reponse in self.zone_portes:
                if rect.collidepoint(event.pos):
                    self.porte_cliquee = rect
                    if reponse == self.questions[self.niveau]["bonne"]:
                        self.resultat = "Bonne réponse !"
                        self.score += 1
                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                    else:
                        self.resultat = "Mauvaise réponse."
                        pygame.time.set_timer(pygame.USEREVENT, 1500)

        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            self.niveau += 1
            if self.niveau < len(self.questions):
                self.resultat = ""
                self.porte_cliquee = None
                self.creer_portes()
            else:
                self.resultat = "Partie terminée ! Score: {}/{}".format(self.score, len(self.questions))
                pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

        elif event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            self.jeu.changer_etat(Map(self.jeu))

    def draw(self, screen):
        super().draw(screen)
        question = self.questions[self.niveau]["texte"] if self.niveau < len(self.questions) else ""
        self.sauter_ligne(question, self.jeu.bg_width // 4, self.jeu.bg_height // 4, 30, self.font, (255, 255, 255), screen)

        for rect, texte in self.zone_portes:
            couleur = (100, 50, 20)
            if self.porte_cliquee == rect and self.niveau < len(self.questions):
                couleur = (0, 200, 0) if texte == self.questions[self.niveau]["bonne"] else (200, 0, 0)
            pygame.draw.rect(screen, couleur, rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), rect, 4, border_radius=15)
            texte_surface = self.font.render(texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=rect.center)
            screen.blit(texte_surface, texte_rect)

        if self.resultat:
            res_surface = self.font.render(self.resultat, True, (255, 255, 0))
            res_rect = res_surface.get_rect(center=(self.jeu.bg_width // 2, self.jeu.bg_height // 1.2))
            screen.blit(res_surface, res_rect)

        
        score_surface = self.font.render(f"Score : {self.score}/{len(self.questions)}", True, (255, 255, 255))
        screen.blit(score_surface, (self.jeu.bg_width - int(self.jeu.bg_width / 6), int(self.jeu.bg_height / 20)))
        

class Tir_arc(Etats):
    """Mini-jeu qui affiche une cible sur laquelle le joueur doit tirer un flèche (c'est la fin de la trajectoire de cette dernière qui permet de passer d'un niveau à l'autre)
     réutilise les méthodes d'Etats() et prend notamment les valeurs dans son dico self.niveaux_jeux pour adapter au bon niveau
     renvoie le nouveau niveau atteind/si le jeu est fini"""
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Tir_arc.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.curseur_img= pygame.image.load(os.path.join("assets", "viseur.png"))
        self.curseur_img = pygame.transform.scale(self.curseur_img, (self.jeu.bg_width/11, self.jeu.bg_width/11 )) #on fait que par rapport à width car on veut un carré
        self.fleche_img=pygame.image.load(os.path.join("assets", "fleche.png"))
        self.fleche_img_wh =self.jeu.bg_width/15
        self.fleche_img = pygame.transform.scale(self.fleche_img, (self.fleche_img_wh, self.fleche_img_wh))
        
        self.cible_img = pygame.image.load(os.path.join("assets", "cible.png"))
        
        self.niveau = str(self.niveaux_jeux["Tir_arc"][0])
        self.niveau_increment = False #permet d'incrementer 1 fois par bon tir le niveau
        
        self.dico_niveaux = { "0" : { "cible_taille" : self.jeu.bg_width//4},
                              "1" : { "cible_taille" : self.jeu.bg_width//6},
                              "2" : { "cible_taille" : self.jeu.bg_width//6,  "vitesse_cible" : 0.75},
                              "3" : { "cible_taille" : self.jeu.bg_width//6,  "vitesse_cible" : 1.25},
                              "4" : { "cible_taille" : self.jeu.bg_width//6,  "vitesse_cible" : 1.8}
            }
        
        #pour les niveaux 2 et 4, où la cible va bouger
        self.cible_pos_bouge = self.jeu.bg_width//2-self.dico_niveaux["2"]["cible_taille"]//2 #on prend la taille de niv.2, qui est la même pour niv.4
        
        self.direction= 1 #1 pour vers la gauche, -1 pour vers la droite
        self.distance_cible_max=200

        self.en_tir= True
        self.en_vol=False
         
        self.tir_x = 0 #position finale de la fleche une fois tout le mouvement effectué, mise à 0 pour eviter les bugs (car cible ne sera jamais à 0;0 donc pas de problemes et ce sont des valeurs de coordonées possibles donc pas de modifiactions dans la logique du code)
        self.tir_y = 0
        self.vitesse = 15 #represente la vitesse de la fleche a parcourir la trajectoire
        
        self.hauteur = 300
        self.longueur = 210
        

    def cible_attributs(self, niveau):
        """les attributs de la cible bougent en fonction des niveaux, cette fonction va renvoyer les bons attributs pour chaque niveau"""
        self.cible_taille = self.dico_niveaux[self.niveau]["cible_taille"]
        self.cible_pos = (self.jeu.bg_width//2-self.cible_taille//2,self.jeu.bg_height//2-self.cible_taille//2)
        self.cible_img = pygame.transform.scale(self.cible_img, (self.cible_taille, self.cible_taille )) #l'image de base est un carré

        if niveau=="2" or niveau=="3" or niveau=="4": 
            self.rond_cible = { "centre" : (self.cible_pos_bouge + self.cible_taille//2 , self.cible_pos[1] + self.cible_taille//2), #car sur l'image le centre de la cible est le centre de l'image
                                "rayon" : self.cible_taille//6 , 
                }
        else:

          self.rond_cible = { "centre" : (self.cible_pos[0] + self.cible_taille//2 , self.cible_pos[1] + self.cible_taille//2), #car sur l'image le centre de la cible est le centre de l'image
                              "rayon" : self.cible_taille//6 , 
              }
        return self.cible_taille,self.cible_pos, self.cible_img,self.rond_cible

    def handle_events(self, event):
        self.cible_taille,self.cible_pos, self.cible_img,self.rond_cible=self.cible_attributs(self.niveau)
        super().handle_events(event)
        #le get_rect crée un rect pour le menu, le topleft le positionne au bon endroit (à partir du haut gauche comme dans le reste du programme) sinon il va en (0,0)
    
        if (event.type == pygame.MOUSEMOTION and self.menu.get_rect(topleft=(self.menu_x, self.menu_y)).collidepoint(event.pos) and self.show_menu) or (event.type == pygame.MOUSEMOTION and self.rect_regles_ic.collidepoint(event.pos)) or (event.type == pygame.MOUSEMOTION and self.rect_aide_ic.collidepoint(event.pos)) or not isinstance(self.jeu.etat, Tir_arc): #on vérifie que self.jeu.etat est un objet de type Tir_arc (autrement dit si on n'est plus dans la phase de mini-jeu du tir à l'arc, on réaffiche la souris)
            self.en_tir= False
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.mouse.set_visible(True)
        else :
            self.en_tir = True
            pygame.mouse.set_visible(False) #car on va afficher une image pour remplacer le curseur (viseur) 
        
        self.x_souris, self.y_souris = pygame.mouse.get_pos() #on le met dans handle_events pour qu'il change bien à chaque fois
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.en_tir and not self.en_vol: #on verfie si on peut lancer une fleche
           self.deb_temps_en_vol = time.time()
           self.en_vol=True
           self.niveau_increment=False 
            #enregistre le moment du début du mouvement
           self.tir_x_base,self.tir_y_base=self.x_souris, self.y_souris
           #on déduis les coordonées de alpha et beta
           self.alpha = self.longueur/2 #alpha est la longeur/2 car alpha est la coordonée en x du sommet, axe de symétrie de la parabole // on definit les caractéristiques de notre trajectoire
           self.beta= self.hauteur
           self.a = -self.beta/(self.alpha**2) #on trouve a tel que les points sont sur la parabole

        
        #self.tir_x est calculé dand le draw pour une meilleure fluidité     
        self.distance_cible_fleche= sqrt((self.rond_cible["centre"][0]-self.tir_x)**2 + (self.rond_cible["centre"][1]-self.tir_y)**2) #théroème de Pythagore
        if self.distance_cible_fleche<= self.rond_cible["rayon"] and self.tir_x_base-self.tir_x>self.longueur/2:  #on vérifie qu'on est assez avancé dans la trajectoire (éviter qu'on puisse juste viser directement sur al cible)
              if not self.niveau_increment and self.niveau!="4":
                  self.niveau=str(int(self.niveau)+1)
                  self.niveau_increment=True
              if not self.niveau_increment and self.niveau=="4": #le mini-jeu est fini
                 self.jeu.changer_etat(Map(self.jeu))
                 pygame.mouse.set_visible(True)
    
    def draw(self, screen):
        self.cible_taille,self.cible_pos, self.cible_img,self.rond_cible=self.cible_attributs(self.niveau)
        super().draw(screen)
        if self.niveau=="2" or self.niveau=="3" or self.niveau=="4": 
            if abs(self.cible_pos[0]-self.cible_pos_bouge) >= self.distance_cible_max: #on recupere la valeur absolue (donc la longueur qui spéare les deux éléments)
                self.direction*=-1
            self.cible_pos_bouge+=self.dico_niveaux[self.niveau]["vitesse_cible"]*self.direction
            screen.blit(self.cible_img, (self.cible_pos_bouge, self.cible_pos[1]))
        else:
          screen.blit(self.cible_img, self.cible_pos)
          
        if self.en_tir:
            souris_pos = pygame.mouse.get_pos()
            screen.blit(self.curseur_img, (souris_pos[0] - self.curseur_img.get_width() // 2, #on blit pour que le centre de l'image soit blit où il y a le curseur (si on ne divise pas par 2 ce sera le coin gauche au niveau du curseur)
                                           souris_pos[1] - self.curseur_img.get_height() // 2)) 
        if self.en_vol:
            self.temps_passe_en_vol = time.time() - self.deb_temps_en_vol
            
            self.tir_x = self.tir_x_base - self.vitesse* self.temps_passe_en_vol*10
            self.tir_y =self.tir_y_base - self.a*(((self.tir_x_base-self.tir_x)-self.alpha)**2)-self.beta #on a calculé l'image dans le repere d'origine (tir_x_base;tir_y_base) donc on ajoute tir_y_base pour que la position soit bonne + on change le signe du trinôme pour que les branches soient vers le haut

            # Vérifier si la distance entre le point de départ et le point actuel dépasse un certain seuil
            if self.tir_x_base - self.tir_x >= self.longueur:
                self.en_vol = False  # Arrêter le mouvement lorsque la distance est atteinte
            
            screen.blit(self.fleche_img, (self.tir_x-self.fleche_img_wh//2, self.tir_y-self.fleche_img_wh//2)) #on blit l'image à partir de son centre (si on enleve rien c'est au coin supérieur gauche)

        #pygame.draw.circle(screen, (0,255,0), self.rond_cible["centre"], self.rond_cible["rayon"]) #pour dessiner la zone de touche (tests)
        
        self.montrer_regles_aide(screen, self.last_event, "Tir_arc")

        

class Vitesse(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Vitesse.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.mots = { "0": ["anticonstitutionellement"],
                         "1": ["zygomatique"],
                         "2": ["tétrathionate"] }
        self.niveau = str(self.niveaux_jeux["Vitesse"][0])

        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.zone_affichage = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/2),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/6))
        self.redaction = False

        self.reponse_uti = ""
        self.mauvaise_rep=0

        self.attendre = False #permet de faire attendre le joueur s'il a proposé trop de mauvaises réponses
        self.attente= 60000*5 #en milisecondes 
        self.debut_attente= -self.attente #par défaut, comme ça le if est vrai si le joueur n'a pas eu faux
        self.timer = False
        self.timer = 1000*5
        self.debut_timer = self.timer

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
            self.redaction = True
            self.debut_timer = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos)) or self.attendre==True:
            self.redaction=False
            
        if self.redaction==True and event.type == pygame.KEYDOWN:
            if self.reponse_uti == "":  # Premier caractère tapé
               self.debut_timer = pygame.time.get_ticks()  # On lance le timer
            """Pour enlever un caractère"""
            if event.key==pygame.K_BACKSPACE: 
                self.ancienne_rep=self.reponse_uti
                self.reponse_uti=""
                for i in range(len(self.ancienne_rep)-1):
                    self.reponse_uti+=self.ancienne_rep[i]

            elif event.key == pygame.K_RETURN:
                if self.reponse_uti.upper()==self.mots[self.niveau][0].upper():
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                    self.debut_timer = pygame.time.get_ticks()
                if self.redaction and pygame.time.get_ticks() - self.debut_timer >= 5000:
                        self.jeu.changer_etat(Map(self.jeu))
                        print("mini-jeu perdu!")
                        return
                if self.niveau=="3" :
                    print("mini-jeu réussi !")
                    self.jeu.changer_etat(Map(self.jeu))
                    return
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

                       
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        pygame.draw.rect(screen, "#4d3020", self.zone_affichage, border_radius=int(self.jeu.bg_height/54))
        screen.blit(self.font.render(self.mots[self.niveau][0], True, "#6f553c"), (self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))

        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
          temps_restant = max(0, 5 - (pygame.time.get_ticks() - self.debut_timer) // 1000)
          screen.blit(self.font.render(f"Temps restant : {temps_restant}s", True, "red"), (self.zone_affichage.x, self.zone_affichage.y - 40))
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        if self.attente-(pygame.time.get_ticks()-self.debut_attente)>0: #on affiche le chronomètre tant qu'il reste du temps à attendre
          self.minutes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) // 60000  # Nombre de minutes restantes
          self.secondes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) % 60000 // 1000  # Nombre de secondes restantes

          # Format propre mm:ss (avec zéro devant si nécessaire)
          self.temps_affiche = f"{self.minutes}:{self.secondes:02d}"  #0 : complete par un 0, 2 :le nombre doit avoir 2 chiffres, d : est un entier (digit)
          screen.blit(self.font.render(self.temps_affiche, True, "white"),(0, 0))
        
        self.montrer_regles_aide(screen,self.last_event,"Vitesse")

class Bon_minerai(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Bon_minerai.jpeg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Bon_minerai"][0])
        self.Bon_minerai = { "0": ["éthérium",pygame.image.load(os.path.join("assets","Bon_minerai", "éthérium.png"))],
                         "1": ["lunarium",pygame.image.load(os.path.join("assets","Bon_minerai", "lunarium.png"))],
                         "2": ["mythril",pygame.image.load(os.path.join("assets","Bon_minerai", "mythril.png"))],
                         "3": ["netherite",pygame.image.load(os.path.join("assets","Bon_minerai", "netherite.png"))],
                         "4": ["obsidienne",pygame.image.load(os.path.join("assets","Bon_minerai", "obsidienne.png"))],
                         "5": ["opale",pygame.image.load(os.path.join("assets","Bon_minerai", "opale.png"))],
                         "6": ["pyromithril",pygame.image.load(os.path.join("assets","Bon_minerai", "pyromithril.png"))],  
                         "7": ["volcanium",pygame.image.load(os.path.join("assets","Bon_minerai", "volcanium.png"))],  
                         "8": ["azurite",pygame.image.load(os.path.join("assets","Bon_minerai", "azurite.png"))],  
                         "9": ["émeraude",pygame.image.load(os.path.join("assets","Bon_minerai", "émeraude.png"))],             
}
        self.zone_noms = pygame.Rect(int(self.jeu.bg_width/10000), int(self.jeu.bg_height/3),int(self.jeu.bg_width/10),int(self.jeu.bg_height/2))
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.zone_affichage = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/6),int(self.jeu.bg_width/4),int(self.jeu.bg_height/4))
        self.reponse_uti = ""
        self.redaction=False

        self.mauvaise_rep=0

        self.niveau = str(self.niveaux_jeux["Bon_minerai"][0])
        self.image = None

    def handle_events(self, event):
        if self.redaction: 
            """pour qu'il soit possible d'écrire avec toutes les touches"""
            super().handle_events_souris(event)
        else:
            super().handle_events(event)  
            
        #si on clique sur la zone de texte il est possible de commencer à taper la réponse sinon non 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.zone_reponse.collidepoint(event.pos):
            self.redaction=True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos)):
            self.redaction=False
            
        if self.redaction==True and event.type == pygame.KEYDOWN:
            """Pour enlever un caractère"""
            if event.key==pygame.K_BACKSPACE: 
                self.ancienne_rep=self.reponse_uti
                self.reponse_uti=""
                for i in range(len(self.ancienne_rep)-1):
                    self.reponse_uti+=self.ancienne_rep[i]
            elif event.key == pygame.K_RETURN:
                if self.reponse_uti.upper() == self.Bon_minerai[self.niveau][0].upper():
                    self.image = self.Bon_minerai[self.niveau][1]
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                if self.niveau == "10":
                    print("mini-jeu réussi !")
                    self.jeu.changer_etat(Map(self.jeu))
                    #MARQUER le jeu comme fait (impossible d'y revenir)
            elif len(self.reponse_uti)<=23:    
              self.reponse_uti += event.unicode  # Ajoute uniquement le caractère tapé
            else:
                print("trop long!")

    def draw(self,screen):
        super().draw(screen)
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        pygame.draw.rect(screen, "#4d3020", self.zone_noms, border_radius=int(self.jeu.bg_height/54))
        prop = 0.5
        new_width = int(self.Bon_minerai[self.niveau][1].get_width() * prop)
        new_height = int(self.Bon_minerai[self.niveau][1].get_height() * prop)
        resized_image = pygame.transform.scale(self.Bon_minerai[self.niveau][1], (new_width, new_height)).convert_alpha() #Convert_alpha permet la transparence de l'image#
        screen.blit(resized_image,(self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))

        noms = "azurite\nvolcanium\nnetherite\nmythril\nobsidienne\némeraude\npyromithril\nlunarium\néthérium\nopale"
        noms_liste = noms.split("\n")  # Séparer les noms en une liste
        for i, nom in enumerate(noms_liste):
         screen.blit(self.font.render(nom, True, "#6f553c"),
                (self.zone_noms.x * 1.02, self.zone_noms.y * 1.02 + i * self.font.get_height())) 
        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        self.montrer_regles_aide(screen,self.last_event,"Pendule")

class Trad(Enigme):
    """Mini-jeu qui affiche des traductions, le joueur doit les résoudre grâce à un énnoncé et un historique qui s'affichent
     réutilise les méthodes d'Enigme() (et donc aussi d'Etats), ce qui permet de garder tout ce qui est saisie de texte
     renvoie le nouveau niveau atteind/si le jeu est fini"""
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Trad.jpeg"))
        self.zone_reponse = pygame.Rect(0, int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2-self.zone_reponse.w/2),self.zone_reponse.y ,self.zone_reponse.w,self.zone_reponse.h) #on redefini les x pour que la zone soit centrée
        self.mauvaises_lettres_id=[]
        
        self.font_symboles = pygame.font.Font(os.path.join("assets", "unifont-16.0.02.otf"), int(self.jeu.bg_height/25)) #sinon les symboles ne sont pas supportés par la police actuelle
        self.font_symboles_petit = pygame.font.Font(os.path.join("assets", "unifont-16.0.02.otf"), int(self.jeu.bg_height/40))
        self.niveau = str(self.niveaux_jeux["Trad"][0])
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.enigmes = {   "0": ["ᛚᚠ ⛥☉ᚢ♃ᚠ♇ᚢ☾ ᛟᚠᚱᛚ☾","la montagne parle", "sachant que le mot 'montagne' est présent dans la phrase,\ntraduire mot par mot :"], #dico des traductions(on reprend nom engime pour garder le mem fonctionnement que dans la super clsse) (traduction à effectuer, réponse, énoncé)
                         "1": ["ᛚ☾ ♅☾ᚢ♃ ⛥♄ᚱ⛥♄ᚱ☾ ᚲ☾☿ ⛥☉♃☿ ☉♄ᛒᛚᛉ☽☿","le vent murmure des mots oubliés", "sachant que le 'e' et le 'é' se ressemblent,\nle 'o' et le 'b' sont proche de notre alphabet\net que la dernière lettre est un 's', traduire :"],
                         "2": ["ᛚ☾☿ ᛚ☽♇☾ᚢᚲ☾☿ ᚲᛉ☿☾ᚢ♃ ⊕♄☾ ᛚ☾☿ ᚠᚢᚦᛉ☾ᚢ☿ ☉ᛒ☿☾ᚱ♅☾ᚢ♃ ☾ᚢᚦ☉ᚱ☾ ᚲ☾ᛟ♄ᛉ☿ ᛚ☾☿ ☿☉⛥⛥☾♃☿","les légendes disent que les anciens observent encore depuis les sommets", "avec les traductions trouvées précédemment,\ntraduire :"],
                         "3": ["ᛚ☾☿ ⛥☉ᚢ♃☿ ☿☉ᚢ♃ ☿☾ᚦᚱ☾♃☿","les monts sont secrets", "à l’aide de vos connaissances sur la langue d’Etheris\nacquises grâce aux traductions précédentes,\ntraduire :"],
                         }
        self.dernier_niveau="3"
        self.tirets="" #va afficher les endroits où une lettre doit être tapée (ex : __ ___ pour le mont)
        self.tirets_defini = False #permet de savoir si on a déjà défini les tirets ou pas (pour le faire qu'une seule fois par traduction)
        self.taille_texte = 0 #va permettre de centrer les tirrets
        self.font_tirets = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/34)) #on aggrandit
        self.lenmax= 85

        
    def handle_events(self, event):
        self.mauvaises_lettres_id #ATTENTION : ou les reinitialiser??? 
        if self.redaction==True and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.mauvaises_lettres_id=[]
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() :
                    self.tirets_defini=False
                    self.tirets=""
                    self.taille_texte=0
                else :
                    if len(self.reponse_uti)>len(self.enigmes[self.niveau][1]):
                        for i in range(len(self.enigmes[self.niveau][1]),len(self.reponse_uti)):
                            self.mauvaises_lettres_id.append(i)               
                    else: 
                      for i in range(len(self.reponse_uti)):
                        if self.reponse_uti[i]!=self.enigmes[self.niveau][1][i]:
                          self.mauvaises_lettres_id.append(i)
        
        super().handle_events(event)
            

        
    def draw(self,screen):
        Etats.draw(self,screen)
        self.montrer_regles_aide(screen,self.last_event,"Trad")
        
        self.texte_rect=self.font_symboles.render(self.enigmes[self.niveau][0], True, (255, 255, 255))
        self.texte_rect = self.texte_rect.get_rect() #on récupere les dimensions du texte pour ensuite bien centrer l'affichage
        
        self.sauter_ligne(self.enigmes[self.niveau][0], int(self.jeu.bg_width/2 - self.texte_rect.w/2), int(self.jeu.bg_height/2.7),self.jeu.bg_height/47,self.font_symboles,"#4d3020", screen)

        self.sauter_ligne(self.enigmes[self.niveau][2], int(self.jeu.bg_width*680/self.jeu.bg_width), 0, self.jeu.bg_height/47, self.font,"#6f553c", screen)
        
        #gestion des tirets
        self.espacement= self.jeu.bg_width/72
        self.taille_tiret = self.font_tirets.size("_") #on récupere la taille d'un tiret
        self.taille_espace = self.font_tirets.size(" ")
        if not self.tirets_defini:
            for elem in self.enigmes[self.niveau][0]:
              if elem==" ":
                self.tirets+=" "
              else:
                self.tirets+="_"
              self.taille_texte+=self.espacement
              self.tirets_defini=True
        self.tiret_milieu= int(self.jeu.bg_width/2 - self.taille_texte/2)
        self.zone_reponse = pygame.Rect(int(self.tiret_milieu), int(self.jeu.bg_height/1.5), int(self.taille_texte), int(self.taille_tiret[1]*2)) #pour coller au format de la super classe, sinon le handle event est défini sur celui de la super classe !
    
        for i in range(len(self.tirets)):
            """permet de centrer les lettres sur les tirets"""
            self.espacement_x = self.tiret_milieu + i * self.espacement
            screen.blit(self.font_tirets.render(self.tirets[i], True, "black"),(int(self.espacement_x), self.zone_reponse.y))
            if self.redaction and len(self.reponse_uti)>i:   #on vérifie que l'indice i existe pour self.reponse_uti
              if i in self.mauvaises_lettres_id:
                 screen.blit(self.font_tirets.render(self.reponse_uti[i], True, "red"),(int(self.espacement_x), self.zone_reponse.y)) 
              else:
                  screen.blit(self.font_tirets.render(self.reponse_uti[i], True, "#4d3020"),(int(self.espacement_x), self.zone_reponse.y))
        if self.redaction and len(self.reponse_uti)>len(self.tirets):
            self.reponse_uti="" #si on dépasse la zone, la réponse se réinitialise
            
        #on affiche l'historique:
        screen.blit(self.font.render("historique :", True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005))
        if self.niveau!=self.dernier_niveau:
          for i in range(int(self.niveau)):
           screen.blit(self.font_symboles_petit.render(self.enigmes[str(i)][0] + " = " + self.enigmes[str(i)][1], True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005+(i+1)*self.jeu.bg_height*0.04))
        else: 
            screen.blit(self.font_symboles_petit.render("--disparu--", True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005+self.jeu.bg_height*0.04))
        
        if self.attente-(pygame.time.get_ticks()-self.debut_attente)>0: #on affiche le chronomètre tant qu'il reste du temps à attendre
          self.minutes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) // 60000  # Nombre de minutes restantes
          self.secondes = (self.attente - (pygame.time.get_ticks() - self.debut_attente)) % 60000 // 1000  # Nombre de secondes restantes

          # Format propre mm:ss (avec zéro devant si nécessaire)
          self.temps_affiche = f"{self.minutes}:{self.secondes:02d}"  #0 : complete par un 0, 2 :le nombre doit avoir 2 chiffres, d : est un entier (digit)
          screen.blit(self.font.render(self.temps_affiche, True, "#4d3020"),(int(self.jeu.bg_width/2 - self.texte_rect.w/2), int(self.jeu.bg_height/2.4)))

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
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Krabi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.vocab = {
            "orage": "O",
            "brume": "B",
            "lumière": "L",
            "frisson": "F",
            "aube": "A"
        }

        self.secret = "BLOAF"
        self.reponse = ""
        self.input_active = False
        self.message = ""

        self.mots_dynamiques = []
        for mot, lettre in self.vocab.items():
            surf = self.jeu.font.render(mot, True, (255, 255, 255))
            x = random.randint(0, self.jeu.bg_width - surf.get_width())
            y = random.randint(0, self.jeu.bg_height - surf.get_height() - int(self.jeu.bg_height * 0.2))
            dx = random.uniform(-0.7, 0.7)
            dy = random.uniform(-0.5, 0.5)
            self.mots_dynamiques.append({
                "mot": mot,
                "lettre": lettre,
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "cliqué": False,
                "alpha": 0,
                "brillance_sens": 1
            })

        self.zone_input = pygame.Rect(int(self.jeu.bg_width * 0.3), int(self.jeu.bg_height * 0.85), int(self.jeu.bg_width * 0.4), int(self.jeu.bg_height * 0.07))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for item in self.mots_dynamiques:
                if not item["cliqué"]:
                    mot_surf = self.jeu.font.render(item["mot"], True, (255, 255, 255))
                    rect = mot_surf.get_rect(topleft=(item["x"], item["y"]))
                    if rect.collidepoint(mx, my):
                        item["cliqué"] = True
                        item["dx"] *= 0.1
                        item["dy"] *= 0.1
                        item["alpha"] = 0
                        item["brillance_sens"] = 1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.input_active = self.zone_input.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                if self.reponse.upper() == self.secret:
                    self.message = "✨ Succès ! ✨"
                else:
                    self.message = "Mot incorrect"
            elif event.key == pygame.K_BACKSPACE:
                self.reponse = self.reponse[:-1]
            elif len(self.reponse) < len(self.secret):
                self.reponse += event.unicode.upper()

    def draw(self, screen):
        super().draw(screen)

        lettres_revelees = []

        for item in self.mots_dynamiques:
            item["x"] += item["dx"]
            item["y"] += item["dy"]

            if item["x"] <= 0 or item["x"] >= self.jeu.bg_width - 150:
                item["dx"] *= -1
            if item["y"] <= 0 or item["y"] >= self.jeu.bg_height - 200:
                item["dy"] *= -1

            if item["cliqué"]:
                if item["alpha"] < 200:
                    item["alpha"] = min(255, item["alpha"] + 10)
                else:
                    item["alpha"] += item["brillance_sens"] * 2
                    if item["alpha"] > 255:
                        item["alpha"] = 255
                        item["brillance_sens"] = -1
                    elif item["alpha"] < 200:
                        item["alpha"] = 200
                        item["brillance_sens"] = 1

                surface = self.jeu.font.render(item["lettre"], True, (0, 255, 100))
                faded = surface.copy()
                faded.set_alpha(int(item["alpha"]))
                screen.blit(faded, (item["x"], item["y"]))
                lettres_revelees.append(item["lettre"])
            else:
                surface = self.jeu.font.render(item["mot"], True, (255, 255, 255))
                screen.blit(surface, (item["x"], item["y"]))

        lettres_surface = self.jeu.font.render(" ".join(lettres_revelees), True, (0, 255, 100))
        screen.blit(lettres_surface, (int(self.jeu.bg_width * 0.05), int(self.jeu.bg_height * 0.8)))

        pygame.draw.rect(screen, (255, 255, 255), self.zone_input, border_radius=10, width=2)
        input_surface = self.jeu.font.render(self.reponse, True, (255, 255, 255))
        screen.blit(input_surface, (self.zone_input.x + 10, self.zone_input.y + 10))

        if self.message:
            msg_surface = self.jeu.font.render(self.message, True, (255, 215, 0))
            screen.blit(msg_surface, (self.zone_input.x, self.zone_input.y - 40))


class Zephyr(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Zephyr.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

class Mars(Etats):
    """Mini-jeu qui affiche 4 propositions possible à des questions de culture générale, le joueur doit cliquer sur la bonne pour augmenter de niveau
     réutilise les méthodes d'Etats() et prend notamment les valeurs dans son dico self.niveaux_jeux pour adapter au bon niveau
     renvoie le nouveau niveau atteind/si le jeu est fini"""
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Mars.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Mars"][0])
        self.niveau_max=9
        self.dico_questions = {"0" : ["Combien y a t’il de 0 dans un million ?",["3","6","9","10"],"6",25], #question, reponses possible, bonne reponse, chrono disponible
                               "1" : ["Quelle est la planète la plus proche du Soleil dans le monde que vous connaissez ?",["Vénus","Terre","Mars","Mercure"],"Mercure",15],
                               "2" : ["Quel est l’élément chimique dont le symbole est Au ?",["L'or","L'argent","L'oxygène","L'aluminium"],"L'or",10],
                               "3" : ["Dans le monde duquel vous provenez, quelle est la planète gazeuse la plus volumineuse du système solaire ?",["Saturne","Jupiter","Uranus","Neptune"],"Jupiter",10],
                               "4" : ["De quelle couleur est le cobalt sous sa forme pure ?",["Gris","Rouge","Bleu","Vert"],"Gris",8],
                               "5" : ["Dans une taverne vous commandez de l’hydromel, que buvez-vous ?",["Une bière","Un vin","Alcool à base de miel","Mêle macéré"],"Alcool à base de miel",8],
                               "6" : ["Si une pierre précieuse absorbe toutes les couleurs sauf le bleu, de quelle couleur apparaît-elle ?",["Bleue","Magenta","Rouge","Jaune"],"Bleue",7],
                               "7" : ["Quel est le quatrième état de la matière, avec solide, liquide et gazeux ? ",["Plasma","Liquoreux","Pâteux","Hydrogénique"],"Plasma",5],
                               "8" : ["Quelle est la température d'ébullition de l’eau ?",["94","-100","212","543"],"212",5],
                               "9" : ["Quel est le pays du monde d’où vous venez qui possède le plus grand nombre de fuseaux horaires ?",["La Chine","La France","La Russie","Les Etats-Unis"],"La France",3],
            }
        self.espace= self.jeu.bg_width//17
        self.rect_reponse_y = int(self.jeu.bg_height*387/self.jeu.bg_height)
        self.rects_reponses = { "0" : pygame.Rect(self.espace,self.rect_reponse_y,int(self.espace*3),int(self.espace*3)), 
                                "1" : pygame.Rect(self.espace*5,self.rect_reponse_y,int(self.espace*3),int(self.espace*3)),
                                "2" : pygame.Rect(self.espace*9,self.rect_reponse_y,int(self.espace*3),int(self.espace*3)),
                                "3" : pygame.Rect(self.espace*13,self.rect_reponse_y,int(self.espace*3),int(self.espace*3))
            }
        
        self.couleur = "#facf79" #jaune, la couleur des carrés où sont les réponses
        self.chrono_debut= pygame.time.get_ticks()
        self.temps_ecoule = False
        self.chrono_tmps_passe = 0
        self.temps=0 #valeur arbitraire
        self.deja_clignote_temps_depasse = False
        
        
    def handle_events(self, event):
        super().handle_events(event)     
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                  for cle in self.rects_reponses:
                      if self.rects_reponses[cle].collidepoint(event.pos):
                          if self.dico_questions[self.niveau][1][int(cle)]==self.dico_questions[self.niveau][2] and int(self.niveau)<self.niveau_max: #si le carré cliqué est celui qui affiche la bonne réponse
                            self.couleur=["#4c9f57", self.rects_reponses[cle]] #vert : pour montrer que c'était la bonne réponse (on associe couleur verte au bon rect)
                            self.niveau=str(int(self.niveau)+1)
                          elif self.dico_questions[self.niveau][1][int(cle)]==self.dico_questions[self.niveau][2] and int(self.niveau)>=self.niveau_max:
                             print("mini-jeu réussit !")
                             self.jeu.changer_etat(Map(self.jeu)) 
                          else:
                              self.couleur=["#cf473a", self.rects_reponses[cle]] #rouge
                              self.niveau="0" #le joueur recommence
                          self.chrono_debut= pygame.time.get_ticks() #on réinitialise le chrono après chaque réponse donnée
                          self.temps = pygame.time.get_ticks()            
    
    def draw(self, screen):
        super().draw(screen)
        self.montrer_regles_aide(screen,self.last_event,"Mars")
        self.texte_rect=self.font.render(self.dico_questions[self.niveau][0], True, (255, 255, 255))
        self.texte_rect = self.texte_rect.get_rect()
        self.sauter_ligne(self.dico_questions[self.niveau][0], int(self.jeu.bg_width/2-self.texte_rect.w/2), int(self.jeu.bg_height*84/self.jeu.bg_height),23,self.font,"white", screen)
  
        self.temps_actuel=pygame.time.get_ticks() 
        for cle in self.rects_reponses:
              if self.rects_reponses[cle]==self.couleur[1] and self.temps_actuel-self.temps<100: #on affiche la couleur différente seulement pendant un certain temps
                  pygame.draw.rect(screen, self.couleur[0], self.rects_reponses[cle],  border_radius=self.jeu.bg_height//80)
              else:
                  pygame.draw.rect(screen, "#facf79", self.rects_reponses[cle],  border_radius=self.jeu.bg_height//80)
        
        #ici chrono : on met la condition ici car dans le handle_event(), il faudrait qu'il y ait un évenement avant que le changement soit remarqué
        self.chrono_tmps_passe = pygame.time.get_ticks()
        self.temps_actu=pygame.time.get_ticks()
        if self.dico_questions[self.niveau][3]-((self.chrono_tmps_passe-self.chrono_debut)//1000) <= 0 : #le temps est en mili-secondes donc conversion    
           if not self.deja_clignote_temps_depasse:
               self.temps = pygame.time.get_ticks()
               self.deja_clignote_temps_depasse=True
           self.temps_ecoule = True       
           self.niveau="0"
        self.temps_actuel=pygame.time.get_ticks()
        if self.temps_actuel-self.temps<100 and self.temps_ecoule:
            #self.temps_ecoule = True
            for cle in self.rects_reponses:
                pygame.draw.rect(screen, "#cf473a", self.rects_reponses[cle],  border_radius=self.jeu.bg_height//80) #rouge
        else:
            self.temps_ecoule = False
            self.deja_clignote_temps_depasse=False

          
        

        for i in range(4): #car il y a 4 réponses possibles
          self.taille_reponse=self.font.size(self.dico_questions[self.niveau][1][i])
          screen.blit(self.font.render(self.dico_questions[self.niveau][1][i], True, "white"),(self.rects_reponses[str(i)].x+self.rects_reponses[str(i)].w//2-self.taille_reponse[0]//2, self.rects_reponses[str(i)].y+self.rects_reponses[str(i)].h//2-self.taille_reponse[1]//2)) #on centre au milieu des carrés
        
        self.chrono_tmps_passe = pygame.time.get_ticks()
        screen.blit(self.font.render(str(self.dico_questions[self.niveau][3]-((self.chrono_tmps_passe-self.chrono_debut)//1000)), True, "#4d3020"),(int(self.jeu.bg_width/2-self.texte_rect.w/2), int(self.jeu.bg_height*127/self.jeu.bg_height)))
        
        

class Chaudron(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Vitesse.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

    def handle_events(self, event):
        super().handle_events(event)

jeu = Jeu()

menu_debut = Menu_debut(jeu)

jeu.run()


#A MARQUER DANS LES REGLAGES : pour revenir en arrière une fois l'inventaire, la carte, les réglages ouverts il est possible de réappuyer sur la touche correspondante

#Pour jeux avec entrée texte : faire un curseur qui clignote ?
#Les prints dans enigme sont à modifier en messages qui popent

#ATTENTION : pour le bon fonctionnement du jeu, quand on change d'état certaines caracteristiques doivent être conservées (genre le temps du chrono en cours, le niveau atteint)