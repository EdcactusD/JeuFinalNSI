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
        self.goutte_actuelle,self.feuille_actuelle= 0,0 #permet de savoir quand l'élément doit tomber
        self.nbr_gouttes_recup = 0
        self.objectif_gouttes = 20
        self.transition_niveau = False
        self.fin_pause , self.debut_pause,self.pause,self.temps_ecoule_en_pause=0, 0,False, 0
        
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
        self.feuille_rect_dico={} #nombre (ID) : rect, bool
        
        self.goutte = pygame.image.load(os.path.join("assets", "goutte.png"))
        self.goutte_wh = self.jeu.bg_width//15
        self.goutte = pygame.transform.scale(self.goutte, (self.goutte_wh, self.goutte_wh))
        self.goutte_rect=pygame.Rect(100,100,self.goutte_wh,self.goutte_wh)
        self.goutte_rect_dico={}
        
        
        self.debut_descente = pygame.time.get_ticks() #en milisecondes
        
        self.mini_jeu = "Eau"

        

    def handle_events(self, event):
        super().handle_events(event)
        
    def enlever_elem_dico(self,dico):
         """permet d'optimiser le jeu en limitant la taille des dictionnaires : lorsque l'éléement est sorti de l'écran il est supprimé"""
         cles_a_supprimer = []
         for elem in dico:
           if dico[elem]["rect"].y >= self.jeu.bg_height:
             cles_a_supprimer.append(elem)
 
         for cle in cles_a_supprimer:
            del dico[cle]
            for elem in dico:
             if dico[elem]["rect"].y>=self.jeu.bg_height:
                del dico[elem] 
    
    def gerer_elem_tombent(self,screen,elem,niveau):
        if elem=="goutte":
            increment=self.goutte_actuelle
            nbr_recup=self.nbr_gouttes_recup
            image=self.goutte
            dimensions=self.goutte_wh
            place_temps_dans_dico=0
            dico = self.goutte_rect_dico
            
            
        elif elem=="feuille":
            increment=self.feuille_actuelle
            nbr_recup=self.nbr_gouttes_recup #on parle aussi en gouttes (mais à cause des feuilles cette fois-ci leur nombre peut baisser)
            image= self.feuille
            dimensions=self.feuille_wh
            place_temps_dans_dico=1
            dico = self.feuille_rect_dico
        
        self.temps_actuel = pygame.time.get_ticks() - self.temps_ecoule_en_pause
        #print("fin",self.temps_actuel) 
        #print("temps en pause", self.temps_ecoule_en_pause)
        if (self.temps_actuel - self.debut_descente)/1000 >= increment*self.nivs[niveau][place_temps_dans_dico] : #on regarde si les temps écoulé correspond au moment auquel l'elem doit tomber
          random_x= random.randint(0,self.jeu.bg_width-dimensions)  
          dico={str(increment) : {"rect" : pygame.Rect(random_x,0,dimensions,dimensions),
                        "naissance" : self.temps_actuel,
                        "bool" : False}}

          increment+=1

        for truc in dico:
            if dico[truc]["bool"]=="déja":
                continue #on ne traite rien si la goutte a déja été récupérée
            dico[truc]["rect"].y = self.nivs[niveau][2] * (self.temps_actuel-dico[truc]["naissance"]) #v=d/t d'où d = v*t
            
            portion_seau = pygame.Rect(self.seau_rect.x, self.seau_rect.y, self.seau_rect.w, self.seau_rect.h//3)
            #pygame.draw.rect(screen, (255, 0, 0), portion_seau, 10)
            if dico[truc]["rect"].colliderect(portion_seau):
              dico[truc]["bool"]=True
            if dico[truc]["bool"]: 
                #on ne blit pas (comme ca il y a l'impression que l'element est rentré dans le seau) 
                if elem=="goutte":
                    nbr_recup+=1
                elif elem=="feuille":
                    if nbr_recup-2>=0:
                     nbr_recup-=2
                    else: #on évite que le joueur ai trop de déficit possible 
                        nbr_recup=0
                dico[truc]["bool"]="déja" #évite qu'on repasse dans la condition pour un même élément
            else : 
               screen.blit(image, (dico[truc]["rect"].x, dico[truc]["rect"].y))
        return increment,dico,nbr_recup


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
            self.enlever_elem_dico(self.feuille_rect_dico)


            if len(self.feuille_rect_dico)==0 :
                self.goutte_actuelle=0
                self.goutte_rect_dico={}
                
                self.feuille_actuelle=0
                self.feuille_rect_dico={}
                self.transition_niveau=False
                self.temps_ecoule_en_pause=0
            
        
        self.mouse_pos_x = pygame.mouse.get_pos()[0]
        if self.mouse_pos_x+self.seau_w//2>=self.menu_x and self.show_menu==True: # pour éviter que le seau soit blit sur le menu : on met en "pause"
            self.debut_pause = pygame.time.get_ticks()
            police = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/4))
            texte = police.render("En pause", True, "#623f37")
            screen.blit(texte,(self.jeu.bg_width//2 - texte.get_size()[0]//2 , self.jeu.bg_height//2 - texte.get_size()[1]//2, texte.get_size()[0], texte.get_size()[1]))
            self.pause=True
            #print("debut", self.temps_actuel)
        elif self.pause:
            self.pause=False
            self.fin_pause=pygame.time.get_ticks()
            self.temps_ecoule_en_pause += (self.fin_pause - self.debut_pause)*100 #conversion
            
        else:
          #self.temps_pause = pygame.time.get_ticks() #on le "réinitialise"
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
            self.goutte_actuelle, self.goutte_rect_dico,self.nbr_gouttes_recup = self.gerer_elem_tombent(screen,"goutte",self.niveau)
            self.feuille_actuelle,self.feuille_rect_dico,self.nbr_gouttes_recup = self.gerer_elem_tombent(screen,"feuille",self.niveau)
            #optimisation pour éviter d'avoir un dico trop grand :
            self.enlever_elem_dico(self.feuille_rect_dico)
            self.enlever_elem_dico(self.goutte_rect_dico)
          
          else: #on le fait que pour les feuilles car dans tous les cas la goutte n'est plus visible quand on change de niveau (puisqu'elle a été récupérée)
              #reprend une grande partie de la fin de la fonction mais avec quelques modifications (donc pas possible de la réutiliser)
              self.temps_actuel = pygame.time.get_ticks()
              cles_a_supprimer = []
              for truc in self.feuille_rect_dico:
                  if self.feuille_rect_dico[truc]["bool"] == "déja":
                      cles_a_supprimer.append(truc)
                      continue  # on passe à l'élément suivant
                  self.feuille_rect_dico[truc]["rect"].y = self.nivs[self.niveau][2] * (self.temps_actuel - self.feuille_rect_dico[truc]["naissance"])
                  
                  portion_seau = pygame.Rect(self.seau_rect.x, self.seau_rect.y, self.seau_rect.w, self.seau_rect.h // 3)
                  
                  if self.feuille_rect_dico[truc]["rect"].colliderect(portion_seau):
                      self.feuille_rect_dico[truc]["bool"] = True
                  
                  if self.feuille_rect_dico[truc]["bool"]:
                      if self.nbr_gouttes_recup - 2 >= 0:
                          self.nbr_gouttes_recup -= 2
                      else:
                          self.nbr_gouttes_recup = 0
                      self.feuille_rect_dico[truc]["bool"] = "déja"
                  else:
                      screen.blit(self.feuille, (self.feuille_rect_dico[truc]["rect"].x, self.feuille_rect_dico[truc]["rect"].y))
              for cle in cles_a_supprimer:
                  del self.feuille_rect_dico[cle] 
        
        
            
        #screen.blit(self.goutte, (self.goutte_rect.x, self.goutte_rect.y))
        
        self.taille_nbr_gouttes=self.font.size(str(self.nbr_gouttes_recup)+"/"+str(self.objectif_gouttes))
        screen.blit(self.font.render(str(self.nbr_gouttes_recup)+"/"+str(self.objectif_gouttes), True, "#4d3020"),(self.jeu.bg_width-self.taille_nbr_gouttes[0], 0))
        #pygame.draw.rect(screen, (255, 0, 0), self.feuille_rect, 10)
        #pygame.draw.rect(screen, (0, 255, 0), self.seau_rect, 10)
        
        
            
        self.montrer_regles_aide(screen, self.last_event, "Eau")