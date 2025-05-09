import pygame
import os 
from général.etats import Etats

"""Contient les mini-jeux enigme et traduction (car ils marchent avec un certain nombre de points en commun)"""

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
                         "1": ["On dit que je meurs sous l'eau\net que j'ai besoin d'air\npourtant je ne suis pas vivant\net je n'ai pas de poumons.","feu"],
                         "2": ["Je peux être audible, visible ou odorante,\nmais jamais les trois à la fois \nJe peux être basse \nou haute sans jamais tomber.\nJ’évalue sans parler.\nJe suis florale ou boisée.","note"],
                         "3": ["Je suis mort et je peux hanter \nou bien je peux être ouvert \nou fermé sans être touché\net vif ou lent sans jamais bouger","esprit"],
                         "4": ["Les pauvres m’ont,\nles riches ont besoin de moi.","rien"]            
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
        self.mini_jeu = "Enigme"
        
        self.case_en_cour_de_modif=None #utile pour trad (on ne s'en occuppe pas ici)
        
    def handle_events_ecrire(self,event):
        if self.redaction==True and event.type == pygame.KEYDOWN:
            if event.key==pygame.K_BACKSPACE: #Pour enlever un caractère
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
                    self.mini_jeu_fini(self.mini_jeu)
                else:
                    self.mauvaise_rep+=1
                    if self.mauvaise_rep>3:
                        self.mauvaise_rep=0
                        self.debut_attente=pygame.time.get_ticks()
                        self.reponse_uti=""
                        print("vous devez attendre 1 minutes pour soumettre de nouveau une réponse")
                        
            elif len(self.reponse_uti)<=self.lenmax and self.case_en_cour_de_modif==None:    
              self.reponse_uti += event.unicode  # Ajoute uniquement le caractère tapé
            else:
                print("trop long!")
        
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
        self.handle_events_ecrire(event)
    
    def draw(self, screen):
        super().draw(screen)
        
        #récupéré dans la super classe
        self.sauter_ligne(self.enigmes[self.niveau][0], int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/2.7),23,self.font,(123,85,57), screen)
        
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes

        self.montrer_regles_aide(screen, self.last_event, "Enigme")
        self.mini_jeu_perdu(screen, self.attente, self.debut_attente,(int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/3.8)))
        
        
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
        self.enigmes = {   "0": ["ᛚᚠ ⛥☉ᚢ♃ᚠ♇ᚢ☾ ᛟᚠᚱᛚ☾","lamontagneparle", "sachant que le mot 'montagne' est présent dans la phrase,\ntraduire mot par mot :", [],"la montagne parle"], #dico des traductions(on reprend nom engime pour garder le meme fonctionnement que dans la super clsse) (traduction à effectuer, réponse, énoncé, liste des rects pour les tirets, réponse pour l'historique)
                         "1": ["ᛚ☾ ♅☾ᚢ♃ ⛥♄ᚱ⛥♄ᚱ☾ ᚲ☾☿ ⛥☉♃☿ ☉♄ᛒᛚᛉ☽☿","leventmurmuredesmotsoubliés", "sachant que le 'e' et le 'é' se ressemblent,\nle 'o' et le 'b' sont proche de notre alphabet\net que la dernière lettre est un 's', traduire :", [],"le vent murmure des mots oubliés"],
                         "2": ["ᛚ☾☿ ᛚ☽♇☾ᚢᚲ☾☿ ᚲᛉ☿☾ᚢ♃ ⊕♄☾ ᛚ☾☿ ᚠᚢᚦᛉ☾ᚢ☿ ☉ᛒ☿☾ᚱ♅☾ᚢ♃ ☾ᚢᚦ☉ᚱ☾ ᚲ☾ᛟ♄ᛉ☿ ᛚ☾☿ ☿☉⛥⛥☾♃☿","leslégendesdisentquelesanciensobserventencoredepuislessommets", "avec les traductions trouvées précédemment,\ntraduire :", [],"les légendes disent que les anciens observent encore depuis les sommets"],
                         "3": ["ᛚ☾☿ ⛥☉ᚢ♃☿ ☿☉ᚢ♃ ☿☾ᚦᚱ☾♃☿","lesmontssontsecrets", "à l’aide de vos connaissances sur la langue d’Etheris\nacquises grâce aux traductions précédentes,\ntraduire :", [],"les monts sont secrets"],
                         }
        self.dernier_niveau="3"
        self.tirets="" #va afficher les endroits où une lettre doit être tapée (ex : __ ___ pour le mont)
        self.tirets_defini = False #permet de savoir si on a déjà défini les tirets ou pas (pour le faire qu'une seule fois par traduction)
        self.tiret_milieu=0
        self.taille_texte = 0 #va permettre de centrer les tirrets
        self.font_tirets = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/34)) #on aggrandit
        self.lenmax= 85
        self.mini_jeu = "Trad"
        
        self.case_en_cour_de_modif=None
        self.reponse_uti = [" " for i in range(len(self.enigmes[self.niveau][0]))]
        self.nbr_tirets=0

        
    def handle_events_ecrire(self,event):
        if self.redaction == True and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
          for i in range(len(self.enigmes[self.niveau][3])):
            if self.enigmes[self.niveau][3][i].collidepoint(event.pos):
               self.case_en_cour_de_modif=i
               
        if self.redaction==True and event.type == pygame.KEYDOWN:
            if event.key==pygame.K_BACKSPACE: #Pour enlever un caractère
                if self.case_en_cour_de_modif!=None:
                    if self.case_en_cour_de_modif>0:
                        self.case_en_cour_de_modif-=1
                    self.reponse_uti[self.case_en_cour_de_modif] = " "
                    if self.case_en_cour_de_modif in self.mauvaises_lettres_id:
                        self.mauvaises_lettres_id.remove(self.case_en_cour_de_modif)
                        
                    
                
                
            elif event.key == pygame.K_RETURN:
                self.mauvaises_lettres_id=[]
                for i in range(len(self.enigmes[self.niveau][1])):
                   if self.reponse_uti[i].upper()!=self.enigmes[self.niveau][1][i].upper():
                      self.mauvaises_lettres_id.append(i)
                      if self.mauvaise_rep>3:
                        self.mauvaise_rep=0
                        self.debut_attente=pygame.time.get_ticks()
                if len(self.mauvaises_lettres_id)!=0:
                    self.mauvaise_rep+=1
                if len(self.mauvaises_lettres_id)==0 and self.niveau!=self.dernier_niveau :
                    self.mauvaises_lettres_id=[]
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti = [" " for i in range(len(self.enigmes[self.niveau][0]))]
                    self.mauvaise_rep=0
                    self.nbr_tirets=0
                    self.case_en_cour_de_modif=None
                    self.tirets_defini=False
                    self.tirets=""
                    self.taille_texte=0
                    
                elif len(self.mauvaises_lettres_id)==0 and self.niveau==self.dernier_niveau: 
                    self.mini_jeu_fini(self.mini_jeu)
                
                        
            if self.case_en_cour_de_modif!=None:
                if event.key != pygame.K_RETURN and event.key != pygame.K_BACKSPACE:
                  self.reponse_uti[self.case_en_cour_de_modif] = event.unicode
                  if self.case_en_cour_de_modif<self.nbr_tirets : #si on est pas sur la dernière case, on passe à la suivante pour plus de fluidité
                     self.case_en_cour_de_modif+=1
                
        
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
                self.nbr_tirets+=1
              self.taille_texte+=self.espacement
              self.tirets_defini=True
              
            for i in range(len(self.tirets)):
                self.tiret_milieu= int(self.jeu.bg_width/2 - self.taille_texte/2)
                self.espacement_x = self.tiret_milieu + i * self.espacement
                self.zone_reponse = pygame.Rect(int(self.tiret_milieu), int(self.jeu.bg_height/1.5), int(self.taille_texte), int(self.taille_tiret[1]*2)) #pour coller au format de la super classe, sinon le handle event est défini sur celui de la super classe !
                if self.tirets[i]!=" ":   
                  #ATTENTION : que pour la taille des tirets 
                  self.enigmes[self.niveau][3].append(pygame.Rect(int(self.espacement_x), self.zone_reponse.y,self.taille_tiret[0],self.taille_tiret[1]))
                  
                
                
        for i in range(len(self.tirets)):
            """permet de centrer les lettres sur les tirets"""
            self.tiret_milieu= int(self.jeu.bg_width/2 - self.taille_texte/2)
            self.zone_reponse = pygame.Rect(int(self.tiret_milieu), int(self.jeu.bg_height/1.5), int(self.taille_texte), int(self.taille_tiret[1]*2)) #pour coller au format de la super classe, sinon le handle event est défini sur celui de la super classe !
            
            self.espacement_x = self.tiret_milieu + i * self.espacement
            screen.blit(self.font_tirets.render(self.tirets[i], True, "black"),(int(self.espacement_x), self.zone_reponse.y))
        for i in range(self.nbr_tirets):    
            if self.redaction and len(self.reponse_uti)>i:   #on vérifie que l'indice i existe pour self.reponse_uti
              if i in self.mauvaises_lettres_id:
                 screen.blit(self.font_tirets.render(self.reponse_uti[i], True, "red"),(self.enigmes[self.niveau][3][i].x, self.enigmes[self.niveau][3][i].y)) 
              else:
                  screen.blit(self.font_tirets.render(self.reponse_uti[i], True, "#4d3020"),(self.enigmes[self.niveau][3][i].x, self.enigmes[self.niveau][3][i].y))
            #pygame.draw.rect(screen, "red", self.enigmes[self.niveau][3][i], 10)
    
            
        #on affiche l'historique:
        screen.blit(self.font.render("historique :", True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005))
        if self.niveau!=self.dernier_niveau:
          for i in range(int(self.niveau)):
           screen.blit(self.font_symboles_petit.render(self.enigmes[str(i)][0] + " = " + self.enigmes[str(i)][4], True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005+(i+1)*self.jeu.bg_height*0.04))
        else: 
            screen.blit(self.font_symboles_petit.render("--disparu--", True, "#6f553c"),(0+self.jeu.bg_width*0.005, 0+self.jeu.bg_height*0.005+self.jeu.bg_height*0.04))
        
        self.mini_jeu_perdu(screen, self.attente, self.debut_attente,(int(self.jeu.bg_width/2 - self.texte_rect.w/2), int(self.jeu.bg_height/2.4)))