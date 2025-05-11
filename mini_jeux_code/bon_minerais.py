import pygame
import os 
from général.etats import Etats

#Mini_jeu où le but est de deviner le nom du minerai affiché à l'écran , on reprend le dictionnaire niveauux_jeux et
#on renvoie la reussite ou non du joueur du mini-jeu , on reutulise les méthodes de Etats()

class Bon_minerai(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        from général.etats import niveaux_jeux
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Bon_minerai.jpeg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(niveaux_jeux["Bon_minerai"][0])
        self.Bon_minerai = { "0": ["éthérium",pygame.image.load(os.path.join("assets","Bon_minerai", "éthérium.png"))],
                         "1": ["lunarium",pygame.image.load(os.path.join("assets","Bon_minerai", "lunarium.png"))],
                         "2": ["mythril",pygame.image.load(os.path.join("assets","Bon_minerai", "mythril.png"))],
                         "3": ["netherite",pygame.image.load(os.path.join("assets","Bon_minerai", "netherite.png"))],
                         "4": ["obsidienne",pygame.image.load(os.path.join("assets","Bon_minerai", "obsidienne.png"))],
                         "5": ["opale",pygame.image.load(os.path.join("assets","Bon_minerai", "opale.png"))],
                         "6": ["pyromithril",pygame.image.load(os.path.join("assets","Bon_minerai", "pyromithril.png"))],  
                         "7": ["volcanium",pygame.image.load(os.path.join("assets","Bon_minerai", "volcanium.png"))],  
                         "8": ["azurite",pygame.image.load(os.path.join("assets","Bon_minerai", "azurite.png"))],  
                         "9": ["émeraude",pygame.image.load(os.path.join("assets","Bon_minerai", "émeraude.png"))],             
}
        self.zone_noms = pygame.Rect(int(self.jeu.bg_width/10000), int(self.jeu.bg_height/3),int(self.jeu.bg_width/10),int(self.jeu.bg_height/2))
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/3.5),int(self.jeu.bg_height/12))
        self.zone_affichage = pygame.Rect(int(self.jeu.bg_width/2.8), int(self.jeu.bg_height/6),int(self.jeu.bg_width/4),int(self.jeu.bg_height/4))
        self.zone_essais = pygame.Rect(int(self.jeu.bg_width/1.15), int(self.jeu.bg_height/1.95),int(self.jeu.bg_width/1.9),int(self.jeu.bg_height/1.95))
        self.zone_reponse_fausse = pygame.Rect(int(self.jeu.bg_width/1.3), int(self.jeu.bg_height/1.95),int(self.jeu.bg_width/1.9),int(self.jeu.bg_height/1.95))
        self.reponse_uti = ""
        self.redaction=False
        self.essais = 5
        self.total_essais = 5
        self.mauvaise_rep=0
        self.niveau = str(niveaux_jeux["Bon_minerai"][0])
        self.image = None
        self.mini_jeu = "Bon_minerai"
        self.reponse_fausse = "Réponse incorrecte"
        self.show_reponse_fausse = False
        
        self.valide=False
        self.rect_valide=pygame.Rect(self.zone_reponse.x+self.zone_reponse.w+self.jeu.bg_width/(192*2),self.zone_reponse.y, self.zone_reponse.h, self.zone_reponse.h)
        
    def verification(self):
        if self.reponse_uti.upper() == self.Bon_minerai[self.niveau][0].upper():
            self.image = self.Bon_minerai[self.niveau][1]
            self.niveau=str(int(self.niveau)+1)
            self.reponse_uti=""
            self.mauvaise_rep=0
            self.show_reponse_fausse = False
        else:
           self.essais -= 1
           self.show_reponse_fausse = True
        self.valide=True
        
        
    def handle_events(self, event):
        if self.redaction: 
            """pour qu'il soit possible d'écrire avec toutes les touches"""
            super().handle_events_souris(event)
        else:
            super().handle_events(event)  
            
        #si on clique sur la zone de texte il est possible de commencer à taper la réponse sinon non 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (self.zone_reponse.collidepoint(event.pos) or self.rect_valide.collidepoint(event.pos)):
            self.redaction=True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos) and self.rect_valide.collidepoint(event.pos)):
            self.redaction=False
            
        self.valide=False
        self.bouton_valider_detection(event, self.rect_valide)
        if event.type==pygame.MOUSEBUTTONDOWN and self.valide==True:
             self.verification()     
             
        if self.redaction==True and event.type == pygame.KEYDOWN:
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
            else:
              print("trop long!")
        if self.niveau == "10":
            self.mini_jeu_fini(self.mini_jeu)
        if self.essais <= 0:
           from général.etats import recommencement
           self.jeu.changer_etat(recommencement(self.__class__,self.jeu))
           print("mini-jeu perdu!")
           

    def draw(self,screen):
        super().draw(screen)
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        pygame.draw.rect(screen, "#4d3020", self.zone_noms, border_radius=int(self.jeu.bg_height/54))
        prop = 0.5
        new_width = int(self.Bon_minerai[self.niveau][1].get_width() * prop)
        new_height = int(self.Bon_minerai[self.niveau][1].get_height() * prop)
        resized_image = pygame.transform.scale(self.Bon_minerai[self.niveau][1], (new_width, new_height)).convert_alpha() #Convert_alpha permet la transparence de l'image#
        screen.blit(resized_image,(self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))
        self.texte_essais = self.font.render(str(self.essais) + "/" + str(self.total_essais), True, "white")
        self.position_x = self.jeu.bg_width - self.texte_essais.get_width() - 20
        self.position_y = 20
        screen.blit(self.texte_essais, (self.position_x, self.position_y))

        noms = "azurite\nvolcanium\nnetherite\nmythril\nobsidienne\némeraude\npyromithril\nlunarium\néthérium\nopale"
        noms_liste = noms.split("\n")  # Séparer les noms en une liste
        for i, nom in enumerate(noms_liste):
         screen.blit(self.font.render(nom, True, "#6f553c"),
                (self.zone_noms.x * 1.02, self.zone_noms.y * 1.02 + i * self.font.get_height())) 
        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        if self.show_reponse_fausse:
           screen.blit(self.font.render(self.reponse_fausse, True, "red"),(self.zone_reponse_fausse.x,self.zone_reponse_fausse.y))
        
        self.bouton_valider_blit(screen, self.rect_valide)      
        self.montrer_regles_aide(screen,self.last_event,"Bon_minerai")
