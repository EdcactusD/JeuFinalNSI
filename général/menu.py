import pygame
import os 
from général.etats import Etats
from général.etats import niveaux_jeux, save_game


global volume
volume = 0.5

"""compore toutes les classes utiles pour le menu : Reglages, Inventaire et Map"""
  
class Reglages(Etats):
   """affiche une page de réglages où l'on peut gerer le son, la sauvegarde et les commandes, l'histoire du jeu son données. 
   prends en argument Etats pour garder les méthodes du handle_events, sauter_ligne, aggrandir_boutons
   renvoie les modifications apportées au son (pour ensuite les dessiner de la bonne manière)/ une nouvelle partie si la sauvegarde est réinitialisée"""
   def __init__(self,jeu):
       super().__init__(jeu)
       self.volume = self.jeu.volume
       self.bg_image = pygame.image.load(os.path.join("assets","fonds", "reglagesessai.png"))
       self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
       self.font=self.jeu.font 
       self.boutons = {"réin_SAUVEGARDE" : [pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.6), int(self.jeu.bg_width/4), int(self.jeu.bg_height/14)), (176,143,101), (143,116,81),"Réinitialiser la sauvegarde"],
                       }

       self.boutons_ref = {bouton: [self.boutons[bouton][0].width, self.boutons[bouton][0].height] for bouton in self.boutons}
       self.barre = pygame.Rect(int(self.jeu.bg_width/2.77), int(self.jeu.bg_height/3.4), int(self.jeu.bg_width/6), int(self.jeu.bg_height/15))
       self.curseur = pygame.Rect(self.barre.x + self.barre.w/2-self.barre.w/8 , self.barre.y, self.barre.w/4, self.barre.h)
       self.curseur.x = volume * (self.barre.w-self.curseur.w) + self.barre.x #pour récuperer les données du volume actuel
       self.c_mouv= False
       self.dico_commande={"menu" : ["w", int(self.jeu.bg_width/3.14),int(self.jeu.bg_height/2.05)],
                           "carte" : ["x",int(self.jeu.bg_width/2.34),int(self.jeu.bg_height/2.05)],
                           }
       self.resu_histoire= "suite à un accident vous êtes bloqué dans le monde d'Etheris,\npour en sortit il vous faut réaliser une potion et donc récuperer par les mini-jeux\nles ingrédients recquis. Arrivez à la fin de chaque niveau des mini-jeux\npour récuperer l'ingrédient et marquer le défi comme fait , vous ne pourrez plus y revenir "
       self.font_resu = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/50))
       self.font_grand = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/17))
       
   def handle_events(self, event):
     super().handle_events(event)
     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
         if self.curseur.collidepoint(event.pos):
             self.c_mouv = True
         for bouton, (position, couleur, couleur_texte,nom) in list(self.boutons.items()): #on cree une copie du dictionnaire qui est donc figée
             if position.collidepoint(event.pos) :
                if bouton=="réin_SAUVEGARDE" :
                    for key in niveaux_jeux:
                      niveaux_jeux[key][4] = False
                      save_game()
                    print("reinitialisation")
     elif event.type == pygame.MOUSEMOTION and self.c_mouv : 
         self.curseur.x = event.pos[0]  # Suit la souris
         self.curseur.clamp_ip(self.barre)  # .clamp_ip contraint un Rect pour qu'il reste entièrement à l’intérieur d’un autre Rect
         self.volume = (self.curseur.x - self.barre.x) / (self.barre.w - self.curseur.w)
         global volume
         volume = self.volume
         pygame.mixer.music.set_volume(self.volume)
     elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
         self.c_mouv = False           
       
   def draw(self, screen):
     screen.blit(self.bg_image, (0, 0))
     super().draw(screen) 
     pygame.draw.rect(screen,(176,143,101), (self.barre.x, self.barre.y, self.barre.w, self.barre.h), border_radius=int(self.barre.w/15)) #pour rect self.barre
     pygame.draw.rect(screen,(143,116,81), (self.curseur.x, self.curseur.y, self.curseur.w, self.curseur.h), border_radius=int(self.barre.w/15)) # pour curseur
     screen.blit(self.font_grand.render("Son : ", True, (6,3,3)), (int(self.jeu.bg_width/3.64), int(self.jeu.bg_height/4)))
     screen.blit(self.font_grand.render("Commandes : ", True, (6,3,3)), (int(self.jeu.bg_width/3.64), int(self.jeu.bg_height/2.5)))
     for elem in self.dico_commande:
         screen.blit(self.font.render(f"{elem} : {self.dico_commande[elem][0]}", True, (6,3,3)), (self.dico_commande[elem][1], self.dico_commande[elem][2]))
     screen.blit(self.font_grand.render("Sauvegarde : ", True, (6,3,3)), (int(self.jeu.bg_width/3.64), int(self.jeu.bg_height/1.8)))
     screen.blit(self.font_grand.render("Résumé : ", True, (6,3,3)), (int(self.jeu.bg_width/3.64), int(self.jeu.bg_height/1.4)))
     from général.menu_deb import Menu_debut
     menu_deb=Menu_debut(self.jeu)
     menu_deb.aggrandir_bouton(screen, self.boutons,self.boutons_ref )
     self.sauter_ligne(self.resu_histoire, int(self.jeu.bg_width/3.8), int(self.jeu.bg_height/1.3), 50 , self.font_resu,(6,3,3), screen)
     


#DONNEES A ENREGISTRER : position du curseur, etat du bouton on/off


class Inventaire(Etats):
    def __init__(self,jeu,):
       super().__init__(jeu)
       self.bg_image = pygame.image.load(os.path.join("assets","parchemin3.png"))
       self.image_bois = pygame.image.load(os.path.join("assets","bois.png"))
       self.image_seau_cire=pygame.transform.scale(self.image_bois, (self.jeu.bg_width, self.jeu.bg_height))
       self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
       self.show_menu = False
       self.nbr = 0

    def handle_events(self, event):
        super().handle_events(event)

    def draw(self, screen):
     screen.blit(self.image_bois, (0, 0))
     super().draw(screen)
     from général.etats import niveaux_jeux
     self.nbr = 0
     #font = pygame.font.SysFont("arial", int(self.jeu.bg_height / 36))
     font=self.jeu.font 
     checkbox_size = int(self.jeu.bg_height / 36)

     for i in niveaux_jeux:
      self.nbr += 1
    
      if self.nbr < 7:
        x = int(self.jeu.bg_width / 8)
        y = int(self.jeu.bg_height / 5) + self.nbr * int(self.jeu.bg_height / 12)
      else:
        x = int(self.jeu.bg_width * 0.58)
        y = int(self.jeu.bg_height / 5) + (self.nbr - 7) * int(self.jeu.bg_height / 12)


      rect = pygame.Rect(x, y, checkbox_size, checkbox_size)

      text = font.render((str(niveaux_jeux[i][5])), True, (0, 0, 0))
      screen.blit(text, (x + checkbox_size + 10, y))

      if niveaux_jeux[i][4] == True:
        pygame.draw.rect(screen, (0, 200, 0), rect)  
      else:
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
      
class Map(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        from mini_jeux_code.enigme_trad import Enigme
        from mini_jeux_code.mont_azur import Mont_azur #importe lui Trad et Donkey_Kong_mario
        from mini_jeux_code.chateau import Chateau #importe Pendu et Pendule
        from mini_jeux_code.memoire_combi import Memoire_combi
        from mini_jeux_code.portes import Portes
        from mini_jeux_code.tir_arc import Tir_arc
        from mini_jeux_code.vitesse import Vitesse
        from mini_jeux_code.bon_minerais import Bon_minerai
        from mini_jeux_code.eau import Eau
        from mini_jeux_code.krabi import Krabi
        from mini_jeux_code.mars import Mars
        from mini_jeux_code.chaudron import Chaudron
        
        
        self.jeu = jeu

        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "carte.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height)) #pas sûre que ce soit utile (à voir dans la super)
        self.zones_carte = { "Mont_azur" : [pygame.Rect(int(self.jeu.bg_width/2.75),int(self.jeu.bg_height/21.6),int(self.jeu.bg_width/4.71),int(self.jeu.bg_height/3.6)), Mont_azur],
        "zone_Enigme" : [pygame.Rect(int(self.jeu.bg_width/2.75),int(self.jeu.bg_height/3),int(self.jeu.bg_width/4.85),int(self.jeu.bg_height/8)), Enigme],
        "zone_Tir_arc" : [pygame.Rect(int(self.jeu.bg_width/5.657),int(self.jeu.bg_height/2.57),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/6)),Tir_arc],
        "zone_Vitesse" : [pygame.Rect(int(self.jeu.bg_width/2.06),int(self.jeu.bg_height/1.576),int(self.jeu.bg_width/7.11),int(self.jeu.bg_height/12.7058)),Vitesse],
        "zone_chateau" : [pygame.Rect(int(self.jeu.bg_width/4.658),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/3.927)),Chateau],
        "zone_Memoire_combi" : [pygame.Rect(int(self.jeu.bg_width/1.75),int(self.jeu.bg_height/2.1),int(self.jeu.bg_width/4.95),int(self.jeu.bg_height/6.8)),Memoire_combi],
        "zone_Portes" : [pygame.Rect(int(self.jeu.bg_width/3.504),int(self.jeu.bg_height/1.636),int(self.jeu.bg_width/6.6),int(self.jeu.bg_height/4)),Portes],
        "zone_Bon_minerai" : [pygame.Rect(int(self.jeu.bg_width/1.669),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/7.2)),Bon_minerai],
        "zone_Eau" : [pygame.Rect(int(self.jeu.bg_width/2.17),int(self.jeu.bg_height/1.35),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/5.4)),Eau],
        "Krabi" : [pygame.Rect(int(self.jeu.bg_width/2.6),int(self.jeu.bg_height/1.9),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/10.75)),Krabi],
        "zone_Mars" : [pygame.Rect(int(self.jeu.bg_width/1.536),int(self.jeu.bg_height/3.6),int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/6.2)),Mars],
        "zone_Chaudron" : [pygame.Rect(int(self.jeu.bg_width/1.6),int(self.jeu.bg_height/1.54),int(self.jeu.bg_width/8),int(self.jeu.bg_height/9.5)),Chaudron], }
        
        self.afficher_pop_up_bool=False
        self.afficher_pop_up_bool_chaudron=False
        self.deb_affichage_pop_up=0
        
    def handle_events(self, event):
        #pour tester la fin de jeu sans refaire tous les jeux
        """from général.etats import niveaux_jeux
        for key in niveaux_jeux:
            if key=="Chaudron":
                pass
            else:
              niveaux_jeux[key][4] = True 
        save_game()"""
        
        super().handle_events(event)  # Garde le comportement général des événements
        from général.etats import niveaux_jeux
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for zone in self.zones_carte:
                if self.zones_carte[zone][0].collidepoint(event.pos) and zone!="zone_Chaudron":
                    mini_game_key = zone if zone in niveaux_jeux else zone.replace("zone_", "")
                    if mini_game_key in niveaux_jeux and niveaux_jeux[mini_game_key][4]:
                        self.afficher_pop_up_bool = True
                        self.afficher_pop_up_bool_chaudron=False
                        self.pop_up_text = f"Vous avez déjà reçu l'objet de ce mini-jeu : {niveaux_jeux[mini_game_key][5]}\nVeuillez lancer une nouvelle partie pour recommencer"
                        self.deb_affichage_pop_up = pygame.time.get_ticks()
                    else:
                        self.jeu.changer_etat(self.zones_carte[zone][1](self.jeu))
                elif self.zones_carte[zone][0].collidepoint(event.pos) and zone=="zone_Chaudron":
                    nbr_reussi=0
                    for jeu in niveaux_jeux:
                        if niveaux_jeux[jeu][4]==True:
                            nbr_reussi+=1
                    if nbr_reussi == len(niveaux_jeux)-1: #on ne compte pas l'élixir des mondes
                       self.jeu.changer_etat(self.zones_carte["zone_Chaudron"][1](self.jeu))
                    elif nbr_reussi == len(niveaux_jeux) : #si le jeu a été fini
                       from mini_jeux_code.chaudron import Tout_gagne
                       self.jeu.changer_etat(Tout_gagne(self.jeu))
                       
                    else :
                        self.afficher_pop_up_bool_chaudron=True
                        self.afficher_pop_up_bool = False


                elif self.afficher_pop_up_bool and self.pop_up_text and self.zones_carte[zone][0].collidepoint(event.pos):
                    self.afficher_pop_up_bool = False
                    self.afficher_pop_up_bool_chaudron=False
                    from général.menu import Map
                    self.jeu.changer_etat(Map(self.jeu))
     
                
    def draw(self, screen) :
        super().draw(screen)
        if self.afficher_pop_up_bool:
            self.afficher_pop_up(screen, self.pop_up_text)
        if self.afficher_pop_up_bool_chaudron:
            self.afficher_pop_up(screen, "finissez tous les mini-jeux avant de pouvoir accéder\nà celui-ci et récuperer l'elixir des mondes")
