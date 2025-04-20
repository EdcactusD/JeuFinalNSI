import pygame
import os 
from essai3 import Etats

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
                             self.mini_jeu_fini() 
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
