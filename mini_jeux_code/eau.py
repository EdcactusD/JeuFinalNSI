import pygame
import os
import random
from général.etats import Etats

#POUR LA SAUVEGARDE : ne pas mettre le niveau dans le dico des niveaux, mais garder en mémoire le nombre de gouttes! 
class Eau(Etats):
    """Mini-jeu qui avec des gouttes et des feuilles tombent du haut de l’écran, le joueur doit récupérer les gouttes (avec le seau) en vue de faire monter leur nombre récupéré et finir le mini-jeu. S’il récupère des feuilles, le compteur descend de 2.
     réutilise les méthodes d'Etats() et prend notamment les valeurs dans son dico self.niveaux_jeux pour adapter au bon nombre de gouttes déjà récupérées
     renvoie le nouveau nombre de gouttes/si le jeu est fini"""
    def __init__(self, jeu):
        super().__init__(jeu)
        #initialisations :
        self.mouse_pos_x = 0 
        self.goutte_actuelle,self.feuille_actuelle= 0,0 #permet d'identifier la goutte
        self.nbr_gouttes_recup = 0
        self.objectif_gouttes = 20
        self.transition_niveau = False
        
        self.niveau=str(self.niveaux_jeux["Eau"][0])
        self.nivs = {"0": [2,1.6,0.75], #temps entre les gouttes, temps entre les feuilles, vitesse maximum
                     "1": [2,1.5,0.9],
                     "2": [2,1.5,1.2],
                     "3": [2,1.4,1.4],
                     "4": [2,1.2,2],
                     "5": [2,1.1,2.3]}
        
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Eau.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.seau = pygame.image.load(os.path.join("assets", "seau.png"))
        self.seau_w = self.jeu.bg_width//7
        self.seau = pygame.transform.scale(self.seau, (self.seau_w, self.seau_w)) #car l'image de base est un carré
        self.seau_rect = pygame.Rect(self.mouse_pos_x, self.rect_regles_ic.y-self.seau_w,self.seau_w,self.seau_w)
        
        self.feuille = pygame.image.load(os.path.join("assets", "feuille.png"))
        self.feuille_wh = self.jeu.bg_width//15
        self.feuille = pygame.transform.scale(self.feuille, (self.feuille_wh, self.feuille_wh))
        self.feuille_rect=pygame.Rect(0,0,self.feuille_wh, self.feuille_wh )
        self.feuille_rect_liste=[]
        
        self.goutte = pygame.image.load(os.path.join("assets", "goutte.png"))
        self.goutte_wh = self.jeu.bg_width//15
        self.goutte = pygame.transform.scale(self.goutte, (self.goutte_wh, self.goutte_wh))
        self.goutte_rect=pygame.Rect(100,100,self.goutte_wh,self.goutte_wh)
        self.goutte_rect_liste=[]
        
        
        self.debut_descente = pygame.time.get_ticks() #en milisecondes
        
        self.liste_elem_bool_recup_goutte,self.liste_elem_bool_recup_feuille=[],[]
        self.mini_jeu = "Eau"

        

    def handle_events(self, event):
        super().handle_events(event)
    
    def gerer_elem_tombent(self,screen,elem,niveau):
        if elem=="goutte":
            increment=self.goutte_actuelle
            liste=self.goutte_rect_liste
            booleens=self.liste_elem_bool_recup_goutte
            nbr_recup=self.nbr_gouttes_recup
            image=self.goutte
            dimensions=self.goutte_wh
            place_temps_dans_dico=0
            
        elif elem=="feuille":
            increment=self.feuille_actuelle
            liste=self.feuille_rect_liste
            booleens=self.liste_elem_bool_recup_feuille
            nbr_recup=self.nbr_gouttes_recup #on parle aussi en gouttes (mais à cause des feuilles cette fois-ci leur nombre peut baisser)
            image= self.feuille
            dimensions=self.feuille_wh
            place_temps_dans_dico=1
        
        self.temps_actuel = pygame.time.get_ticks()
        if (self.temps_actuel - self.debut_descente)/1000 >= increment*self.nivs[niveau][place_temps_dans_dico] : #on regarde si les temps écoulé correspond au moment auquel l'elem doit tomber
          random_x= random.randint(0,self.jeu.bg_width-dimensions)  
          liste.append({"rect" : pygame.Rect(random_x,0,dimensions,dimensions),
                                         "naissance" : self.temps_actuel})
          booleens.append(False)   
          increment+=1
        
        for i in range(len(liste)):
            if booleens[i]=="déja":
                continue #on ne traite rien si la goutte a déja été récupérée
            liste[i]["rect"].y = self.nivs[niveau][2] * (self.temps_actuel-liste[i]["naissance"]) #v=d/t d'où d = v*t
            
            portion_seau = pygame.Rect(self.seau_rect.x, self.seau_rect.y, self.seau_rect.w, self.seau_rect.h//3)
            #pygame.draw.rect(screen, (255, 0, 0), portion_seau, 10)
            if liste[i]["rect"].colliderect(portion_seau):
               booleens[i]=True
            if booleens[i]: 
                #on ne blit pas (comme ca il y a l'impression que l'element est rentré dans le seau) 
                if elem=="goutte":
                    nbr_recup+=1
                elif elem=="feuille":
                    if nbr_recup-2>=0:
                     nbr_recup-=2
                    else: #on évite que le joueur ai trop de déficit possible 
                        nbr_recup=0
                booleens[i]="déja" #évite qu'on repasse dans la condition pour un même élément
            else : 
               screen.blit(image, (liste[i]["rect"].x, liste[i]["rect"].y))
        return increment,liste,booleens,nbr_recup


    def draw(self, screen): #on va gérer dans le draw les changements de niveaux (en plus de l'affichage) car ils faut qu'ils soient aussi possible quand il n'y a pas d'event détecté        
        super().draw(screen)
        
        ancien_niveau = self.niveau
        #changements de niveaux
        if self.nbr_gouttes_recup>=self.objectif_gouttes:
            self.mini_jeu_fini(self.mini_jeu)
        if self.nbr_gouttes_recup<=4:
            self.niveau="1"
        elif self.nbr_gouttes_recup>4 and self.nbr_gouttes_recup<=8:
            self.niveau="2"
        elif self.nbr_gouttes_recup>8 and self.nbr_gouttes_recup<=12:
            self.niveau="3"
        elif self.nbr_gouttes_recup>12 and self.nbr_gouttes_recup<=17:
            self.niveau="4"
        else:
            self.niveau="5"
        
        
        if self.niveau != ancien_niveau: #si le niveau change : on réinitialise tout (1. pour éviter de trop longues liste, 2. pour éviter les problèmes liés au changement brutal de vitesse)

          self.debut_descente = pygame.time.get_ticks()
          self.transition_niveau = True
        
        if self.transition_niveau:
            i=0 #permet de parcourir en même temps une autre liste
            for elem in self.feuille_rect_liste:
                if elem["rect"].y>=self.jeu.bg_height:
                    self.feuille_rect_liste.remove(elem)
                    self.liste_elem_bool_recup_feuille.remove(self.liste_elem_bool_recup_feuille[i])

            if len(self.feuille_rect_liste)==0 :
                self.goutte_actuelle=0
                self.goutte_rect_liste=[]
                self.liste_elem_bool_recup_goutte=[]
                
                self.feuille_actuelle=0
                self.feuille_rect_liste=[]
                self.liste_elem_bool_recup_feuille=[]
                self.transition_niveau=False
            i+=1
        
        self.mouse_pos_x = pygame.mouse.get_pos()[0]
        if self.mouse_pos_x+self.seau_w//2>=self.menu_x and self.show_menu==True: # pour éviter que le seau soit blit sur le menu
            pass
        else:
          if self.mouse_pos_x < self.jeu.bg_width : #pour éviter que le seau sorte de l'écran (étant donné que l'image est blit à partir de son coin gauche)
             screen.blit(self.seau, (self.mouse_pos_x-self.seau_w//2, self.seau_rect.y)) #pour que le seau s'affiche au-dessus des icones
             self.seau_rect = pygame.Rect(self.mouse_pos_x-self.seau_w//2, self.rect_regles_ic.y-self.seau_w,self.seau_w,self.seau_w)
          else : 
              screen.blit(self.seau, (self.jeu.bg_width - self.seau_w//2,self.seau_rect.y))
              self.seau_rect = pygame.Rect(self.jeu.bg_width - self.seau_w//2, self.rect_regles_ic.y-self.seau_w,self.seau_w,self.seau_w)
           
        
        #self.feuille_rect=pygame.Rect(0,0,self.feuille_wh, self.feuille_wh )
        #self.goutte_rect=pygame.Rect(100,100,self.goutte_wh,self.goutte_wh)
        
        #pygame.draw.rect(screen, (255, 0, 0), self.goutte_rect, 10)

        if not self.transition_niveau: #permet d'afficher les dernieres feuilles présentes à l'écran le temps qu'elles en sortent. 
          self.goutte_actuelle,self.goutte_rect_liste,self.liste_elem_bool_recup_goutte,self.nbr_gouttes_recup = self.gerer_elem_tombent(screen,"goutte",self.niveau)
          self.feuille_actuelle,self.feuille_rect_liste,self.liste_elem_bool_recup_feuille,self.nbr_gouttes_recup = self.gerer_elem_tombent(screen,"feuille",self.niveau)
        
        else: #on le fait que pour les feuilles car dans tous les cas la goutte n'est plus visible quand on change de niveau (puisqu'elle a été récupérée)
            #reprend une grande partie de la fin de la fonction mais avec quelques modifications (donc pas possible de la réutiliser)
            self.temps_actuel = pygame.time.get_ticks()
            for i in range(len(self.feuille_rect_liste)):
                if self.liste_elem_bool_recup_feuille[i]=="déja":
                    self.feuille_rect_liste.remove(self.feuille_rect_liste[i])
                    self.liste_elem_bool_recup_feuille.remove(self.liste_elem_bool_recup_feuille[i])
                    continue #on ne traite rien si la goutte a déja été récupérée
                self.feuille_rect_liste[i]["rect"].y = self.nivs[str(int(self.niveau)-1)][2] * (self.temps_actuel-self.feuille_rect_liste[i]["naissance"]) 
                portion_seau = pygame.Rect(self.seau_rect.x, self.seau_rect.y, self.seau_rect.w, self.seau_rect.h//3)
                
                if self.feuille_rect_liste[i]["rect"].colliderect(portion_seau):
                   self.liste_elem_bool_recup_feuille[i]=True
                
                if self.liste_elem_bool_recup_feuille[i]: 
                    #on ne blit pas (comme ca il y a l'impression que l'element est rentré dans le seau) 
                  if self.nbr_gouttes_recup-2>=0:
                    self.nbr_gouttes_recup-=2
                  else: #on évite que le joueur ai trop de déficit possible 
                    self.nbr_gouttes_recup=0
                  self.liste_elem_bool_recup_feuille[i]="déja" #évite qu'on repasse dans la condition pour un même élément
                
                else : 
                   screen.blit(self.feuille, (self.feuille_rect_liste[i]["rect"].x, self.feuille_rect_liste[i]["rect"].y))
        
        #screen.blit(self.goutte, (self.goutte_rect.x, self.goutte_rect.y))
        
        self.taille_nbr_gouttes=self.font.size(str(self.nbr_gouttes_recup)+"/"+str(self.objectif_gouttes))
        screen.blit(self.font.render(str(self.nbr_gouttes_recup)+"/"+str(self.objectif_gouttes), True, "#4d3020"),(self.jeu.bg_width-self.taille_nbr_gouttes[0], 0))
        #pygame.draw.rect(screen, (255, 0, 0), self.feuille_rect, 10)
        #pygame.draw.rect(screen, (0, 255, 0), self.seau_rect, 10)
        
            
            
        self.montrer_regles_aide(screen, self.last_event, "Eau")