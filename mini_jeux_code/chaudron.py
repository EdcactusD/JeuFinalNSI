import pygame
import os 
import time
from général.etats import Etats
from mini_jeux_code.mars import Mars

class Chaudron(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "chaudron.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        from général.menu_deb import Menu_debut
        menu_debut = Menu_debut(jeu)
        self.menu_debut= menu_debut
        
        #self.surface_texte= self.jeu.font.render("Créer l'élixir des mondes",True, "white")
        self.rect_creer_potion= pygame.Rect(0,0,self.jeu.bg_width//4.3,self.jeu.bg_height//15)
        self.rect_creer_potion= pygame.Rect(self.jeu.bg_width//2-self.rect_creer_potion.w//2,self.jeu.bg_height//1.2,self.rect_creer_potion.w,self.rect_creer_potion.h)
        
        self.boutons = {"creer_potion" : [self.rect_creer_potion,"#a6cbb2","white","Créer l'élixir des mondes"]
                        }
        self.boutons_ref = {bouton: [self.boutons[bouton][0].width, self.boutons[bouton][0].height] for bouton in self.boutons}

    def afficher_cinematique(self, dossier_images, fps=10):
        dossier_complet = os.path.join("assets", dossier_images)
        noms_fichiers = sorted(os.listdir(dossier_complet)) #permet de ranger toutes les images dans le bon ordre
        
        images = []
        for nom in noms_fichiers :
            image=pygame.image.load(os.path.join("assets", dossier_images,str(nom)))
            image = pygame.transform.scale(image, (self.jeu.bg_width, self.jeu.bg_height))  # redimensionne si besoin
            images.append(image)
                
        duree_frame = 1 / fps
        for frame in images:
            self.jeu.screen.blit(frame, (0, 0))
            pygame.display.flip()
            time.sleep(0.05)

    
    

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect_creer_potion.collidepoint(event.pos):
            print("lancement cinématiques : mélange puis et fée// passage au dernier mini-jeu")
            self.afficher_cinematique("animation_potion")
            self.explication_mj_final()
            #ici pour animation fée
            self.jeu.changer_etat(Mini_jeu_final(self.jeu))
    
    def draw(self,screen):
        screen.blit(self.bg_image, (0, 0))
        """pygame.draw.rect(screen, "#a6cbb2",self.rect_creer_potion, border_radius=int(self.jeu.bg_height/54)) 
        screen.blit(self.surface_texte, self.surface_texte.get_rect(center=self.rect_creer_potion.center))"""
        self.menu_debut.aggrandir_bouton(screen, self.boutons,self.boutons_ref)
        
    
        
class Mini_jeu_final(Mars):   
    def __init__(self, jeu):
        super().__init__(jeu)
        from général.etats import niveaux_jeux
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "chaudron.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.bg_height = self.jeu.bg_height
        self.bg_width = self.jeu.bg_width
        self.mini_jeu = "Chaudron"
        self.erreur = False
        self.erreur_time = 0
        
        self.niveau = str(niveaux_jeux["Chaudron"][0])
        self.niveau_max=8
        self.dico_questions = {"0" : ["Comment se nomme le monde où vous êtes bloqué ?",["Etherian","Ethos","Etheris"],"Etheris",25], #question, reponses possible, bonne reponse, chrono disponible
                               "3" : ["De combien d'îles est composé ce monde?",["1","3","4"],"3",15],
                               "2" : ["Parmis ces ingrédients, lequel n'avez vous pas récupéré?",["cheveux de Rossier","Pomme de la Discorde","Sang d'ogre"],"Sang d'ogre",10],
                               "5" : ["Quel est le seul minerais qui existe dans ce monde et que vous avez pu observer au Mont Voilé ?",["Lunarium","Solciste","Or"],"Lunarium",10],
                               "1" : ["Pour quelle raison êtes vous coincé dans ce monde?",["Coma éthylique","Mauvaise chute","Mauvaise note en NSI"],"Mauvaise chute",8],
                               "4" : ["Quelle créature magique suis-je?",["Un truc jaune","Un orbe de lumière","Une fée"],"Une fée",8],
                               "6" : ["Comment s'appelle la forêt située au milieu de ce monde?",["La forêt des âmes perdues","La forêt d'Etheris","La forêt obscure"],"La forêt des âmes perdues",7],
                               "7" : ["Les Monts d'Azur se trouvent :",["Au Sud","À l'Est","Au Nord"],"Au Nord",5],
                               "8" : ["Dans votre première traduction du langage ancien, que faisait la montagne ?",["attendre","parler","méditer"],"parler",4],
            }
        self.espace= self.jeu.bg_width//16
        self.rects_reponses = { "0" : pygame.Rect(self.espace,self.rect_reponse_y,int(self.espace*4),int(self.espace*3)), 
                                "1" : pygame.Rect(self.espace*6,self.rect_reponse_y,int(self.espace*4),int(self.espace*3)),
                                "2" : pygame.Rect(self.espace*11,self.rect_reponse_y,int(self.espace*4),int(self.espace*3)),
            }
        self.nbr_reponses_possibles=3
        self.couleur = "#a6cbb2"
        self.couleur_base = "#a6cbb2"


    def handle_events(self, event):
        Etats.handle_events(self,event) 
        #super().handle_events(event)     
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                  for cle in self.rects_reponses:
                      if self.rects_reponses[cle].collidepoint(event.pos):
                          if self.dico_questions[self.niveau][1][int(cle)]==self.dico_questions[self.niveau][2] and int(self.niveau)<self.niveau_max: #si le carré cliqué est celui qui affiche la bonne réponse
                            self.couleur=["#4c9f57", self.rects_reponses[cle]] #vert : pour montrer que c'était la bonne réponse (on associe couleur verte au bon rect)
                            self.niveau=str(int(self.niveau)+1)
                          elif self.dico_questions[self.niveau][1][int(cle)]==self.dico_questions[self.niveau][2] and int(self.niveau)>=self.niveau_max:
                             self.mini_jeu_fini(self.mini_jeu)
                             print("gagné!: Mettre animation fin")
                             self.reussite_chaudron()
                          else:
                              self.couleur=["#cf473a", self.rects_reponses[cle]] #rouge
                              print("mini-jeu perdu!")
                              self.erreur = True
                              self.erreur_time = pygame.time.get_ticks()
                              self.perte_chaudron()
                          self.chrono_debut= pygame.time.get_ticks() #on réinitialise le chrono après chaque réponse donnée
                          self.temps = pygame.time.get_ticks()
                      self.reponse_soumise=True

    def draw(self, screen):
     super().draw(screen)

     if self.erreur:
      if pygame.time.get_ticks() - self.erreur_time >= 1000:
        self.erreur = False  # Reset pour ne pas relancer
        self.perte_chaudron()
        
    