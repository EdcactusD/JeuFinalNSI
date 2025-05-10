import pygame
import os 
from général.etats import Etats

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
        self.reponse_uti = ""
        self.redaction=False

        self.mauvaise_rep=0

        self.niveau = str(niveaux_jeux["Bon_minerai"][0])
        self.image = None
        self.mini_jeu = "Bon_minerai"

    def handle_events(self, event):
        if self.redaction: 
            """pour qu'il soit possible d'écrire avec toutes les touches"""
            super().handle_events_souris(event)
        else:
            super().handle_events(event)  
            
        #si on clique sur la zone de texte il est possible de commencer à taper la réponse sinon non 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.zone_reponse.collidepoint(event.pos):
            self.redaction=True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not(self.zone_reponse.collidepoint(event.pos)):
            self.redaction=False
            
        if self.redaction==True and event.type == pygame.KEYDOWN:
            """Pour enlever un caractère"""
            if event.key==pygame.K_BACKSPACE: 
                self.ancienne_rep=self.reponse_uti
                self.reponse_uti=""
                for i in range(len(self.ancienne_rep)-1):
                    self.reponse_uti+=self.ancienne_rep[i]
            elif event.key == pygame.K_RETURN:
                if self.reponse_uti.upper() == self.Bon_minerai[self.niveau][0].upper():
                    self.image = self.Bon_minerai[self.niveau][1]
                    self.niveau=str(int(self.niveau)+1)
                    self.reponse_uti=""
                    self.mauvaise_rep=0
                if self.niveau == "10":
                    self.mini_jeu_fini(self.mini_jeu)
            elif len(self.reponse_uti)<=23:    
              self.reponse_uti += event.unicode  # Ajoute uniquement le caractère tapé
            else:
                print("trop long!")

    def draw(self,screen):
        super().draw(screen)
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height/54))
        pygame.draw.rect(screen, "#4d3020", self.zone_noms, border_radius=int(self.jeu.bg_height/54))
        prop = 0.5
        new_width = int(self.Bon_minerai[self.niveau][1].get_width() * prop)
        new_height = int(self.Bon_minerai[self.niveau][1].get_height() * prop)
        resized_image = pygame.transform.scale(self.Bon_minerai[self.niveau][1], (new_width, new_height)).convert_alpha() #Convert_alpha permet la transparence de l'image#
        screen.blit(resized_image,(self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))

        noms = "azurite\nvolcanium\nnetherite\nmythril\nobsidienne\némeraude\npyromithril\nlunarium\néthérium\nopale"
        noms_liste = noms.split("\n")  # Séparer les noms en une liste
        for i, nom in enumerate(noms_liste):
         screen.blit(self.font.render(nom, True, "#6f553c"),
                (self.zone_noms.x * 1.02, self.zone_noms.y * 1.02 + i * self.font.get_height())) 
        if self.redaction:
          screen.blit(self.font.render(self.reponse_uti, True, "white"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        else :
          screen.blit(self.font.render("Entrez votre réponse ici", True, "#6f553c"),(self.zone_reponse.x*1.02, self.zone_reponse.y*1.02)) #Le True est pour adoucir le bord des textes
        self.montrer_regles_aide(screen,self.last_event,"Bon_minerai")
