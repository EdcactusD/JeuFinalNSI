import pygame
import os 
from général.etats import Etats
#Mini jeu où une combinaison de lettres d'Etheris apparait puis disparait , le but est de s'en rappeller et de la recréer avec le clavier numérique, on prend 
#les valeurs du dictionnaire niveaux_jeux pour s'adapter au niveau et on renvoie si le joueur perd ou gagne le mini-jeu , on y reutulise les méthodes de Etats()


class Memoire_combi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        from général.etats import niveaux_jeux
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Mémoire_combi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.niveau = str(niveaux_jeux["Memoire_combi"][0])
        self.zone_reponse = pygame.Rect(int(self.jeu.bg_width / 2.8), int(self.jeu.bg_height / 1.4), int(self.jeu.bg_width / 3.5), int(self.jeu.bg_height / 12))
        self.zone_affichage = pygame.Rect(int(self.jeu.bg_width / 2.8), int(self.jeu.bg_height / 2), int(self.jeu.bg_width / 3.5), int(self.jeu.bg_height / 6))
        self.zone_noms = pygame.Rect(int(self.jeu.bg_width / 10000), int(self.jeu.bg_height / 5.1), int(self.jeu.bg_width / 10), int(self.jeu.bg_height / 1.95))
        self.font_symboles = pygame.font.Font(os.path.join("assets", "unifont-16.0.02.otf"), int(self.jeu.bg_height / 25))
        self.combi = {
            "0": ["☾ᛉ⊕♄⛧"],
            "1": ["ᚠᛏ♆ᛗ☉ᛉ"],
            "2": ["ᚦᛚᛋᛟᛞ♆♄♃☿"]
        }
        self.noms = "ᚠ   ᛒ\nᚦ   ᚲ\n☾   ᚨ\n♇   ᚹ\nᛉ   ᛋ\nᛏ   ᛚ\n⛥  ᚢ\n☉   ᛟ\n⊕   ᚱ\n☿   ♃\n♄   ♅\n⛧  ᛞ\nᛗ   ♆" #caractères affichés dans le clavier numérique à gauche#
        self.symboles_liste = self.noms.split("\n")

        self.reponse_uti = ""
        self.espacement_additionnel = 50
        self.debut_temps = pygame.time.get_ticks()  
        self.afficher_combi = True
        self.mini_jeu = "Memoire_combi"
        
        self.valide=False
        self.rect_valide=pygame.Rect(self.zone_reponse.x+self.zone_reponse.w+self.jeu.bg_width/(192*2),self.zone_reponse.y, self.zone_reponse.h, self.zone_reponse.h)
        self.redaction=True #tout le temps (pour coller au format des méthodes pour le bouton "valider")
    
    def verification(self):
        if self.reponse_uti.upper() == self.combi[self.niveau][0].upper():
          self.niveau = str(int(self.niveau) + 1) 
          self.reponse_uti = ""  
          self.debut_temps = pygame.time.get_ticks()
          self.afficher_combi = True  
        else:
          from général.etats import recommencement
          self.jeu.changer_etat(recommencement(self.__class__,self.jeu))
          print("mini-jeu perdu!")

        if self.niveau == "3":
         self.mini_jeu_fini(self.mini_jeu)
        self.valide=True
        
    def handle_events(self, event):
        super().handle_events(event)
        self.valide=False
        self.bouton_valider_detection(event, self.rect_valide)
        if event.type==pygame.MOUSEBUTTONDOWN and self.valide==True:
            self.verification()
            
        if event.type == pygame.MOUSEBUTTONDOWN and self.afficher_combi == False:
            pos = pygame.mouse.get_pos()
            for rect, symbole in self.rects_symboles:
                if rect.collidepoint(pos):
                    self.reponse_uti += symbole  #ajout d'un symbole à la suite quand on clique dessus#

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.reponse_uti = self.reponse_uti[:-1]  # Supprimer le dernier caractère

            if event.key == pygame.K_RETURN: 
              self.verification()

    def draw(self, screen):
        super().draw(screen)
        
        pygame.draw.rect(screen, "#4d3020", self.zone_reponse, border_radius=int(self.jeu.bg_height / 54))
        pygame.draw.rect(screen, "#4d3020", self.zone_affichage, border_radius=int(self.jeu.bg_height / 54))
        pygame.draw.rect(screen, "#4d3020", self.zone_noms, border_radius=int(self.jeu.bg_height / 54))

        temps_ecoule = pygame.time.get_ticks() - self.debut_temps
        if temps_ecoule >= 5000:  
         self.afficher_combi = False

        if self.afficher_combi:
            screen.blit(self.font_symboles.render(self.combi[self.niveau][0], True, "#6f553c"),(self.zone_affichage.x * 1.02, self.zone_affichage.y * 1.02))
        screen.blit(self.font_symboles.render(self.reponse_uti, True, "#ffffff"),(self.zone_reponse.x * 1.02, self.zone_reponse.y * 1.02))

        self.rects_symboles = []  # Liste pour les symboles cliquables
        ligne_height = self.font_symboles.get_height()
        espacement_horizontal = self.font_symboles.size("ᛚ")[0]  # Largeur d'un symbole, ajusté à un seul caractère
        y_offset = self.zone_noms.y  # Position verticale initiale pour la première ligne de symboles
        symboles_lignes = self.noms.split("\n")  # Chaque ligne = un élément de la liste
        for i, ligne in enumerate(symboles_lignes):
            x_offset = self.zone_noms.x  # Position horizontale de départ
            symbols = ligne.split()  # Créer une liste de symboles individuels
            for j, symbole in enumerate(symbols):
                symbole_surface = self.font_symboles.render(symbole, True, "#6f553c")
                symbole_rect = symbole_surface.get_rect()  # Créer un rectangle autour de chaque symbole
                symbole_rect.topleft = (x_offset + j * (espacement_horizontal + self.espacement_additionnel), y_offset)
                screen.blit(symbole_surface, symbole_rect.topleft)
                self.rects_symboles.append((symbole_rect, symbole))  # Ajouter le rectangle et le symbole à la liste
            y_offset += ligne_height  # Mettre à jour l'offset vertical pour la ligne suivante

        temps_ecoule = pygame.time.get_ticks() - self.debut_temps
        if self.afficher_combi:
         temps_restant = max(0, 5 - (temps_ecoule // 1000))  # Temps restant pour afficher la combinaison
         screen.blit(self.font_symboles.render(f"Temps restant : {temps_restant}s", True, "black"), 
                    (self.zone_affichage.x, self.zone_affichage.y - 40))
        
        self.bouton_valider_blit(screen, self.rect_valide)
        self.montrer_regles_aide(screen, self.last_event, "Memoire_combi")
