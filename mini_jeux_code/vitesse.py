import pygame
import os 
from général.etats import Etats
#Le but du mini-jeu est de taper dans le temps imparti les mots qui s'affichent , il prend les valeurs du dictionnaire niveaux_jeux pour s'adapter aux niveaux
#et renvoie si le niveau est réussi ou non , on y reutulise les méthodes de Etats#

class Vitesse(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        from général.etats import niveaux_jeux
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Vitesse.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.mots = { "0": ["anticonstitutionellement"],
                         "1": ["zygomatique"],
                         "2": ["tétrathionate"] }
        self.niveau = str(niveaux_jeux["Vitesse"][0])

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
        self.mini_jeu = "Vitesse"
        
        self.valide=False
        self.rect_valide=pygame.Rect(self.zone_reponse.x+self.zone_reponse.w+self.jeu.bg_width/(192*2),self.zone_reponse.y, self.zone_reponse.h, self.zone_reponse.h)
        
    def verification(self):
        if self.reponse_uti.upper()==self.mots[self.niveau][0].upper():
            self.niveau=str(int(self.niveau)+1)
            self.reponse_uti=""
            self.mauvaise_rep=0
            self.debut_timer = pygame.time.get_ticks()
        if self.redaction and pygame.time.get_ticks() - self.debut_timer >= 5000:
                from général.etats import recommencement
                self.jeu.changer_etat(recommencement(self.__class__,self.jeu))
                print("mini-jeu perdu!")
        if self.niveau=="3" :
            self.mini_jeu_fini(self.mini_jeu)
        else:
            self.mauvaise_rep+=1
            if self.mauvaise_rep>=3:
                self.mauvaise_rep=0
                self.debut_attente=pygame.time.get_ticks()
                self.reponse_uti=""
                print("vous devez attendre 5 minutes pour soumettre de nouveau une réponse")
        self.valide=True

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
        
        self.valide=False
        self.bouton_valider_detection(event, self.rect_valide)
        if event.type==pygame.MOUSEBUTTONDOWN and self.valide==True:
            self.verification()   
        
        #si on clique sur la zone de texte il est possible de commencer à taper la réponse sinon non 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (self.zone_reponse.collidepoint(event.pos) or self.rect_valide.collidepoint(event.pos))  and self.attendre==False:
            self.redaction = True
            self.debut_timer = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos) and self.rect_valide.collidepoint(event.pos)) or self.attendre==True:
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
                self.verification()
                        
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
        
        self.bouton_valider_blit(screen, self.rect_valide)
        self.montrer_regles_aide(screen,self.last_event,"Vitesse")
