import pygame
import os
from main import Etats

class Enigme(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "enigme2.png"))
        self.regles_ic = pygame.image.load(os.path.join("assets","aide.jpg"))
        self.regles_ic=pygame.transform.scale(self.regles_ic,(int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8)))
        self.rect_regles_ic=pygame.Rect(int(self.jeu.bg_height/120), self.jeu.bg_height - int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8))
        self.show_regles=False
        self.rect_regles=pygame.Rect(self.rect_regles_ic.x, self.rect_regles_ic.y - int(self.jeu.bg_width/19.2) ,int(self.jeu.bg_width/19.2), int(self.jeu.bg_height/10.8))
        
        
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(self.niveaux_jeux["Enigme"])
        self.enigmes = { "0": ["On me pose sans me toucher.","question"], #dico des énigmes (énigme, réponse)
                         "1": ["Je ne suis pas vivant mais je grandi,\nJe meurs sous l’eau\nJe n’ai pas de poumons mais j’ai besoin d’air","feu"],
                         "2": ["Je peux être audible, visible ou odorante,\nmais jamais les trois à la fois \nJe peux être basse \nou haute sans jamais tomber.\nJ’évalue sans parler.\nJe suis florale ou boisée.","note"],
                         "3": ["Je suis mort et je peux hanter \nou bien je peux être ouvert \nou fermé sans être touché\net vif ou lent sans jamais bouger","esprit"],
                         "4": ["Encore une fois, on ne peut me voir,\nmais on ne peut me toucher. \nLes pauvres m’ont,\nles riches ont besoin de moi.","rien"]            
}
        
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.reponse_uti = ""
        self.redaction=False
        
        self.mauvaise_rep=0
        self.attendre = False #permet de faire attendre le joueur s'il a proposé trop de mauvaises réponses
        self.attente= 60000*5 #en milisecondes 
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
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau!="4" :
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                if self.reponse_uti.upper()==self.enigmes[self.niveau][1].upper() and self.niveau=="4" :
                    print("mini-jeu réussit !")
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
            else:
                print("trop long!")
                       
        if event.type == pygame.MOUSEMOTION and self.rect_regles_ic.collidepoint(event.pos):
            self.show_regles=True
        else:
            self.show_regles=False
        
        
    
    def draw(self, screen):
        super().draw(screen)
        
        screen.blit(self.regles_ic, (self.rect_regles_ic.x, self.rect_regles_ic.y))
        
        lignes= self.enigmes[self.niveau][0].split("\n") #font.render ne supporte pas \n pour le retour à la ligne, il faut le coder manuellement     
        espace = 0 #pour gérer l'espacement entre les lignes
        for ligne in lignes:
          self.texte=self.font.render(ligne, True, (123,85,57))
          screen.blit(self.texte, (int(self.jeu.bg_width/2.9), int(self.jeu.bg_height/2.7+espace)))
          espace+=self.jeu.bg_height/23
        
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
          screen.blit(self.font.render(self.temps_affiche, True, "white"),(0, 0))
          
        if self.show_regles:
          pygame.draw.rect(screen, "white", self.rect_regles, border_radius=int(self.jeu.bg_height/54))
          #screen.blit(self.rect_regles, (int(self.jeu.bg_height/19.2), self.jeu.bg_height - int(self.jeu.bg_height/10.8) - int(self.jeu.bg_height/10.8)))