import pygame
import os 
import time
from math import sqrt
from général.etats import Etats

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
        self.mini_jeu = "Tir_arc"
        
        self.afficher_croix = False
        self.position_croix = (0, 0)
        self.temps_croix = 0
        self.image_croix = pygame.image.load(os.path.join("assets", "croix.png"))
        self.image_croix = pygame.transform.scale(self.image_croix, (50, 50))

        

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
                  self.croix_ratio = ((self.tir_x - self.rond_cible["centre"][0]) / self.rond_cible["rayon"], (self.tir_y - self.rond_cible["centre"][1]) / self.rond_cible["rayon"])
                  self.temps_croix = pygame.time.get_ticks()     # moment du contact
                  self.afficher_croix = True
              if not self.niveau_increment and self.niveau=="4": #le mini-jeu est fini
                 self.mini_jeu_fini(self.mini_jeu)
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
            self.tir_y =self.tir_y_base - self.a*(((self.tir_x_base-self.tir_x)-self.alpha)**2)-self.beta #on a calculé l'image dans le repere d'origine (tir_x_base;tir_y_base) donc on ajoute tir_y_base pour que la position soit bonne + on change le signe du trinôme pour que les branches soient vers le bas

            # Vérifier si la distance entre le point de départ et le point actuel dépasse un certain seuil
            if self.tir_x_base - self.tir_x >= self.longueur:
                self.en_vol = False  # Arrêter le mouvement lorsque la distance est atteinte
            
           #pour faire tourner la flèche
            distance_x = abs(self.tir_x - self.tir_x_base)
            t = distance_x / self.longueur  # de 0 à 1
            self.angle = 180 * t  # de 0° à 180° donc flèche orientée vers le bas
            self.fleche_img_tourne = pygame.transform.rotozoom(self.fleche_img, self.angle, 1)
            self.rect_img_tourne =  self.fleche_img_tourne.get_rect(center=(self.tir_x, self.tir_y)) #permet d'être toujours au même endroit même si le coin supérieur gauche change
            screen.blit( self.fleche_img_tourne, self.rect_img_tourne)
            
            #screen.blit(self.fleche_img, (self.tir_x-self.fleche_img_wh//2, self.tir_y-self.fleche_img_wh//2)) #on blit l'image à partir de son centre (si on enleve rien c'est au coin supérieur gauche)

        #pygame.draw.circle(screen, (0,255,0), self.rond_cible["centre"], self.rond_cible["rayon"]) #pour dessiner la zone de touche (tests)
        
        if self.afficher_croix:
            if pygame.time.get_ticks() - self.temps_croix < 500:  
               x = self.rond_cible["centre"][0] + self.croix_ratio[0] * self.rond_cible["rayon"]
               y = self.rond_cible["centre"][1] + self.croix_ratio[1] * self.rond_cible["rayon"]
               screen.blit(self.image_croix, (x - self.image_croix.get_width() // 2, y - self.image_croix.get_height() // 2))

            else:
                self.afficher_croix = False  # on arrête d'afficher

        
        self.montrer_regles_aide(screen, self.last_event, "Tir_arc")