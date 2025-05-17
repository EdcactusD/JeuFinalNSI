import pygame
import os
import json

#dico qui stocke les niveaux de jeu (0), les règles(1), les aides(2) , les images(3), la reussite du mini-jeu(4) , le nom de l'item(5)
global niveaux_jeux
niveaux_jeux = {"Donkey_kong_mario" :[0, " ", " ",pygame.image.load(os.path.join("assets","items", "oeuf de phoenix.png")),False,"œuf de phénix"],
                "Enigme" : [0, "Entrez un mot\n(sans son déterminant)\npour répondre à l'énigme,\nsi vous répondez faux\n3 fois d'affilé,\nattendez le délais", " ",pygame.image.load(os.path.join("assets","items", "sève sagesse.png")),False,"Sève de Sagesse"],
                "Memoire_combi" : [0, "Restituez la\ncombinaison de\nsymboles qui\napparaissent en\nappuyant sur ceux\nde la liste", "Evidemment, vous ne\npouvez entrer\nvotre réponse que\nlorsque la\ncombinaison a \ndisparue",pygame.image.load(os.path.join("assets","items", "grain d'ambre.png")),False,"grains d’ambre"],
                "Pendu" : [0, "Proposez des lettres\npour restituer le\nmot                                                            ", "Non, probablement que\nZ n'est pas\nla meilleure\nlettre à tester",pygame.image.load(os.path.join("assets","items", "cheveux de Rossier.png")),False,"cheveux de Rossier"],
                "Pendule" : [0, "Cliquez sur le\nbouton stop au\nbon moment\npour arreter\nles aiguilles", "Il y a toujours\ndes places en\ncours de CP\nsi besoin...",pygame.image.load(os.path.join("assets","items", "poudre de perlinpimpim.png")),False,"poudre de perlimpinpin"],
                "Portes" : [0, "Résolvez l'énigme\nen choisissant la\nbonne porte                                   ", "Il va falloir\nfaire chauffer\nles deux neurones\nqui se battent \nen duel là haut...",pygame.image.load(os.path.join("assets","items", "pomme de la discorde.png")),False,"Pomme de la Discorde"],
                "Tir_arc" :[0, "Cliquez sur l'écran pour\ntirer une flèche\nle niveau est passé\n si elle atteint la cible\nà la fin de la\ntrajectoire", "C'est à la fin de son\nmouvement que la flèche\npeut toucher la cible",pygame.image.load(os.path.join("assets","items", "Epine de Sylve.png")),False,"Épine de Sylve"],
                "Vitesse" : [0, "Ecrivez les mots\nles plus rapidement\npossibles en \nrespectant le délai\ndes 5 secondes", "Là je peux pas\ntrop t'aider\nfaut juste\nsavoir écrire",pygame.image.load(os.path.join("assets","items", "éclat d'obsidrune.png")),False,"Eclat d’obsidrune"],
                "Bon_minerai" :[0, "Associez le bon        \nnom au bon \nminerai                                  ", "Parfois c'est \nlogique",pygame.image.load(os.path.join("assets","items", "pépite d'or.png")),False,"pépite d'or"],
                "Trad" : [0, "En cliquant sur les tirets\nentrez lettres à lettres\nvos propositions\nde traduction puis\nvalidez, si la lettre est\nmauvaise elle sera\nrouge", "Résolvez la\ntraduction 4\njuste après la 3",pygame.image.load(os.path.join("assets","items", "glace millénaire.png")),False,"glace millénaire"],
                "Eau" : [0, "Récupérez       \nles gouttes     \nqui tombent    \nen évitant   \nles feuilles    ", "Au plus vous    \nrécupérez     \nde gouttes    \nau plus   \nle jeu devient   \ndur",pygame.image.load(os.path.join("assets","items", "rosée du désert.png")),False,"Rosée du désert"],
                "Krabi" :[0, "Appuyez sur\nles mots pour\nréveller des\nlettres\npuis remettez les\ndans le bon ordre", "Si vous avez\ndu temps à\nperdre vous\npouvez faire\ntoutes les\ncombinaisons\npossibles",pygame.image.load(os.path.join("assets","items", "pince de Kraby.png")),False,"pince de Kraby"],
                "Mars" : [0, "Appuyez sur la\ncase contenant\nla bonne réponse\nrecommencez si\nvous avez faux", "Pour le plus\ndur, tout\nest question\nd'unité",pygame.image.load(os.path.join("assets","items", "Sel de Mars.png")),False,"Sel de Mars"],
                "Chaudron" : [0, " ", " ",pygame.image.load(os.path.join("assets","items", "Elixir des mondes.png")),False,"Elixir des mondes"]}

SAVE_FILE = os.path.join(os.path.dirname(__file__), "save_data.json")

def save_game():
    data = {key: niveaux_jeux[key][4] for key in niveaux_jeux}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        for key in data:
            if key in niveaux_jeux:
                niveaux_jeux[key][4] = data[key]


class Etats(): #SUPERCLASSE : la classe qui gère tous les etats du jeu
    def __init__(self, jeu, show_menu=False, show_map=False): #on récupère les éléments essentiels et on met des valeurs par défaut pour éviter les problèmes
       self.jeu = jeu
       self.last_event = None #va nous etre utile dans le draw des mini-jeux pour afficher regles et aide
       self.font=self.jeu.font
       self.show_menu = show_menu
       self.show_map = show_map
       self.volume = self.jeu.volume
       self.volume = 0.5

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
       
       self.menu_rond_ic = pygame.image.load(os.path.join("assets","menu_rond.png"))
       self.menu_rond_ic=pygame.transform.scale(self.menu_rond_ic,(int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8)))
       self.rect_menu_rond = pygame.Rect(int(self.jeu.bg_width -  self.menu_rond_ic.get_width() -10), int(self.jeu.bg_height -self.menu_rond_ic.get_height()-10),int(self.menu_rond_ic.get_width()), int(self.menu_rond_ic.get_height()))

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
             
             self.font_petit = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_width/(len(niveaux_jeux[nom_mini_jeu][1])/1.2)))
             if self.show_regles:
               self.font_petit = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_width/(len(niveaux_jeux[nom_mini_jeu][1])/1.2)))
               pygame.draw.rect(screen, "white", self.rect_regles, border_radius=int(self.jeu.bg_height/54))
               self.sauter_ligne(niveaux_jeux[nom_mini_jeu][1], self.rect_regles.x+10, self.rect_regles.y,45,self.font_petit,(123,85,57), screen)
             if self.show_aide:
                 pygame.draw.rect(screen, "white", self.rect_aide, border_radius=int(self.jeu.bg_height/54))
                 self.sauter_ligne(niveaux_jeux[nom_mini_jeu][2], self.rect_aide.x+10, self.rect_aide.y,45,self.font_petit,(123,85,57), screen)
 
        
        
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
              print(self.show_menu)
              self.show_menu = False
              print(self.show_menu)
              pygame.display.flip()
              from général.menu import Inventaire
              self.jeu.changer_etat(Inventaire(self.jeu))
          if self.show_menu and self.zone_reglages_ic.collidepoint(event.pos):
              from général.menu import Reglages # Import retardé pour éviter les boucles circulaires
              self.jeu.changer_etat(Reglages(self.jeu))
          if not self.show_menu and self.rect_menu_rond.collidepoint(event.pos):
                self.show_menu=True
                
                
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

        prop = 0.5
        zone_affichage = pygame.Rect(
        (self.jeu.bg_width - (self.jeu.bg_width / 4)) // 2,  
        (self.jeu.bg_height - (self.jeu.bg_height / 4)) // 2.4,  
        self.jeu.bg_width // 4, 
        self.jeu.bg_height // 4 
        )
        new_width = int(niveaux_jeux[mini_jeu][3].get_width() * prop)
        new_height = int(niveaux_jeux[mini_jeu][3].get_height() * prop)
        resized_image = pygame.transform.scale(niveaux_jeux[mini_jeu][3], (new_width, new_height)).convert_alpha()

        self.jeu.screen.blit(objet, (0, 0))  
        self.jeu.screen.blit(resized_image,(zone_affichage.x * 1.02, zone_affichage.y * 1.02))

        niveaux_jeux[mini_jeu][4] = True 
        save_game()
        
        pygame.display.flip()
        from général.menu import volume
        print(volume)
        if volume != 0:
         pygame.mixer.init()
         pygame.mixer.music.load(os.path.join("assets", "BotW-item.mp3"))
         self.volume= pygame.mixer.music.set_volume(volume)
         pygame.mixer.music.play()

        pygame.time.delay(2000)
        
        if volume != 0:
         pygame.mixer.music.load(os.path.join("assets", "musique_jeu.mp3"))
         pygame.mixer.music.set_volume(volume)
         pygame.mixer.music.play(-1)

        from général.menu import Map
        self.jeu.changer_etat(Map(self.jeu))
        #MARQUER le jeu comme fait (impossible d'y revenir)

    def mini_jeu_perdu(self, screen, attente, debut_attente,position):
        if attente-(pygame.time.get_ticks()-debut_attente)>0: #on affiche le chronomètre tant qu'il reste du temps à attendre
          self.minutes = (attente - (pygame.time.get_ticks() - debut_attente)) // 60000  # Nombre de minutes restantes
          self.secondes = (attente - (pygame.time.get_ticks() - debut_attente)) % 60000 // 1000  # Nombre de secondes restantes

          # Format propre mm:ss (avec zéro devant si nécessaire)
          self.temps_affiche = f"{self.minutes}:{self.secondes:02d}"  #0 : complete par un 0, 2 :le nombre doit avoir 2 chiffres, d : est un entier (digit)
          screen.blit(self.font.render(self.temps_affiche, True, "#4d3020"),(position))

          texte="Vous avez fait trop de mauvaises propositions\nattendez pour pouvoir soumettre une nouvelle réponse"
          pixel_10_dans_ref = int(self.jeu.bg_width/192)
          lignes = texte.split("\n")
          largeur_max = max([self.font.size(ligne)[0] for ligne in lignes])
          ratio = pixel_10_dans_ref*3
          hauteur_totale = len(lignes) * (self.jeu.bg_height / ratio)  # même valeur que l'espace ratio pour le blit
          texte_dimensions = (largeur_max+10, int(hauteur_totale)+pixel_10_dans_ref)
          popup = pygame.Rect(self.rect_menu_rond.x - texte_dimensions[0] - pixel_10_dans_ref , self.jeu.bg_height- texte_dimensions[1]-pixel_10_dans_ref ,int(texte_dimensions[0]),int(texte_dimensions[1]))
          
          pygame.draw.rect(screen, "white", popup, border_radius=15)
          self.sauter_ligne(texte, popup.x+pixel_10_dans_ref//2, popup.y+pixel_10_dans_ref//2, ratio, self.font,(123,85,57), screen)
          #screen.blit(self.font.render(texte, True, "#4d3020"),(popup.x+5, popup.y+5))
 
    
 #les 2 premières méthodes permettent (ensemble) d'afficher un bouton pour valider une saisie
    def bouton_valider_detection(self, event, rect):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and rect.collidepoint(event.pos) and self.redaction:
            self.valide = True
        if self.redaction==True and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.valide = True
    def bouton_valider_blit(self, screen, rect):
        pygame.draw.rect(screen, "#7ace77", rect, border_radius=int(self.jeu.bg_height/54))
        texte = pygame.font.SysFont("arial", int(rect.height * 0.6)).render("→", True, "#50844e")
        screen.blit(texte, texte.get_rect(center=rect.center))
        #va permettre d'afficher qu'une séléction a été effectuée :
        if self.valide==True:
           self.deb_temps=pygame.time.get_ticks()
        if hasattr(self, "deb_temps") and pygame.time.get_ticks()-self.deb_temps<900 and self.redaction: #hasattr(self, "deb_temps") permet de vérifier que self.deb_temps existe (pour éviter les bugs)
           rect_validerr= pygame.Rect(rect.x, int(rect.y+ rect.h+self.jeu.bg_height/(108*2)), rect.w,rect.h//3)
           pygame.draw.rect(screen, "#7ace77",rect_validerr, border_radius=int(self.jeu.bg_height/54))
           font= pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/70))
           texte=font.render("soumis !", True, "#50844e" )
           screen.blit(texte, texte.get_rect(center=rect_validerr.center))

    def afficher_pop_up(self,screen, texte):
        """permet d'afficher un message sur l'écran"""
        pixel_10_dans_ref = int(self.jeu.bg_width/192)
        lignes = texte.split("\n")
        largeur_max = max([self.font.size(ligne)[0] for ligne in lignes])
        ratio = pixel_10_dans_ref*3
        hauteur_totale = len(lignes) * (self.jeu.bg_height / ratio)  # même valeur que l'espace ratio pour le blit
        texte_dimensions = (largeur_max+10, int(hauteur_totale)+pixel_10_dans_ref)
        popup = pygame.Rect(self.rect_menu_rond.x - texte_dimensions[0] - pixel_10_dans_ref , self.jeu.bg_height- texte_dimensions[1]-pixel_10_dans_ref ,int(texte_dimensions[0]),int(texte_dimensions[1]))
        
        pygame.draw.rect(screen, "white", popup, border_radius=15)
        self.sauter_ligne(texte, popup.x+pixel_10_dans_ref//2, popup.y+pixel_10_dans_ref//2, ratio, self.font,(123,85,57), screen)
    
    def draw(self, screen):
        #screen.fill((0, 0, 0))  # Efface l’écran avec du noir avant d’afficher les images (pas necessaire si tout l'écran est rempli et non transaparent)
        screen.blit(self.bg_image, (0, 0))
        
        if self.show_menu:
            screen.blit(self.menu, (self.menu_x, self.menu_y))
            #Tests pour voir les rect. 
            #pygame.draw.rect(screen, (255, 0, 0), self.zone_map_ic, 2)  # Contour rouge pour tester
            #pygame.draw.rect(screen, (0, 255, 0), self.zone_inventaire_ic, 2)
            #pygame.draw.rect(screen, (0, 0, 255), self.zone_reglages_ic, 2)
        if not self.show_menu : 
            screen.blit(self.menu_rond_ic, (self.rect_menu_rond.x, self.rect_menu_rond.y))
        
    
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
     self.durée = 3000  

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
     
    def reussite_chaudron(self):
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
     self.mots = ["Bien joué , jeune aventurier , vous avez réussi à créer l'elixir des mondes",
                 "Avant de retourner dans votre monde je vais vous montrer le grand trésor d'Etheris",
                 "Celui-ci est rare et peu ont pu l'observer, profitez de ce moment"]
     self.tresor = {"images":[pygame.image.load(os.path.join("assets","tresor", "R1.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R2.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R3.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R4.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R5.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R6.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R7.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R8.jpg")),
                    pygame.image.load(os.path.join("assets","tresor", "R9.jpg"))]}
     pygame.draw.rect(self.screen, "#4d3020", self.zone_reponse, border_radius=int(self.bg_height / 54))
     self.screen.blit(self.objet, (0, 0))
     self.screen.blit(self.fee, (0, 0))
     pygame.display.flip()
     self.temps = pygame.time.get_ticks()  
     self.durée = 3000 

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

     for image in self.tresor["images"]:
       self.objet = pygame.transform.scale(image, (self.bg_width, self.bg_height))
       self.screen.blit(self.objet, (0, 0))
       pygame.display.flip()
       pygame.time.wait(3000)
    
     pygame.time.wait(1000)
     from général.menu_deb import Menu_debut
     self.etat = Menu_debut(self)

    def perte_chaudron(self):
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
     self.mots = ["Vous avez failli lors de l'épreuve , Aventurier, ceci va vous paraitre hardu",
                 "Vous avez perdu l'ensemble de vos ingrédients , vous devez les retrouver",
                 "ainsi vous devez recommencer chaque mini-jeu que Ethéris vous permet de faire, bonne chance"]
     pygame.draw.rect(self.screen, "#4d3020", self.zone_reponse, border_radius=int(self.bg_height / 54))
     self.screen.blit(self.objet, (0, 0))
     self.screen.blit(self.fee, (0, 0))
     pygame.display.flip()
     self.temps = pygame.time.get_ticks()  
     self.durée = 3000

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

     for jeu in niveaux_jeux:
      niveaux_jeux[jeu][4] = False
    
     pygame.time.wait(1000)
     from général.menu import Map
     self.jeu.changer_etat(Map(self.jeu))

class recommencement(Etats):
    def __init__(self, mini_jeu_cls, jeu):
        super().__init__(jeu)  
        self.mini_jeu_cls = mini_jeu_cls
        self.white = (255, 255, 255)
        self.brown = (139, 69, 19)
        self.red = (255, 0, 0)
        self.zone_bouton = pygame.Rect(int(self.jeu.bg_width / 2.3),int(self.jeu.bg_height / 1.4),int(self.jeu.bg_width / 9),int(self.jeu.bg_height / 16))
        self.zone_message = pygame.Rect(int(self.jeu.bg_width / 3.3),int(self.jeu.bg_height / 5),int(self.jeu.bg_width / 3.5),int(self.jeu.bg_height / 7))
        self.font_perdu = pygame.font.Font(os.path.join("assets", "lacquer.ttf"),int(self.jeu.bg_height / 15))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.zone_bouton.collidepoint(event.pos):
                self.jeu.changer_etat(self.mini_jeu_cls(self.jeu))  

    def draw(self, screen):
        super().draw(screen)
        screen.fill((0, 0, 0))  
        pygame.draw.rect(screen, self.brown, self.zone_bouton, border_radius=int(self.jeu.bg_height / 5))
        screen.blit(self.font.render("Recommencer", True, self.white),(self.zone_bouton.x * 1.02, self.zone_bouton.y * 1.02))
        screen.blit(self.font_perdu.render("Vous avez perdu !", True, self.red),(self.zone_message.x * 1.02, self.zone_message.y * 1.02))

      
    
      
   
   



    
