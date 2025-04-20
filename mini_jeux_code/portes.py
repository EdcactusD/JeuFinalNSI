import pygame
import os 
from essai3 import Etats

class Portes(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Portes.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.questions = [
            {"texte": "Quelle est la capitale de la France ?", "choix": ["Lyon", "Paris", "Marseille"], "bonne": "Paris"},
            {"texte": "Combien y a-t-il de continents ?", "choix": ["5", "6", "7"], "bonne": "7"},
            {"texte": "Quel est l'élément chimique O ?", "choix": ["Or", "Oxygène", "Osmium"], "bonne": "Oxygène"},
            {"texte": "Qui a peint la Joconde ?", "choix": ["Picasso", "Léonard de Vinci", "Van Gogh"], "bonne": "Léonard de Vinci"},
            {"texte": "Combien font 8 × 7 ?", "choix": ["56", "64", "49"], "bonne": "56"},
            {"texte": "Quel est le plus grand océan ?", "choix": ["Atlantique", "Arctique", "Pacifique"], "bonne": "Pacifique"},
            {"texte": "Quelle planète est la plus proche du Soleil ?", "choix": ["Mercure", "Vénus", "Mars"], "bonne": "Mercure"},
            {"texte": "Quelle langue est parlée au Brésil ?", "choix": ["Espagnol", "Portugais", "Français"], "bonne": "Portugais"}
        ]

        self.niveau = 0
        self.score = 0
        self.resultat = ""
        self.porte_cliquee = None

        self.creer_portes()

    def creer_portes(self):
        self.zone_portes = []
        largeur_porte = self.jeu.bg_width // 6
        hauteur_porte = self.jeu.bg_height // 3
        espace = self.jeu.bg_width // 20
        start_x = (self.jeu.bg_width - (3 * largeur_porte + 2 * espace)) // 2
        y = self.jeu.bg_height // 2
        choix = self.questions[self.niveau]["choix"]

        for i in range(3):
            rect = pygame.Rect(start_x + i * (largeur_porte + espace), y, largeur_porte, hauteur_porte)
            self.zone_portes.append((rect, choix[i]))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.resultat:
            for rect, reponse in self.zone_portes:
                if rect.collidepoint(event.pos):
                    self.porte_cliquee = rect
                    if reponse == self.questions[self.niveau]["bonne"]:
                        self.resultat = "Bonne réponse !"
                        self.score += 1
                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                    else:
                        self.resultat = "Mauvaise réponse."
                        pygame.time.set_timer(pygame.USEREVENT, 1500)

        elif event.type == pygame.USEREVENT:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            self.niveau += 1
            if self.niveau < len(self.questions):
                self.resultat = ""
                self.porte_cliquee = None
                self.creer_portes()
            else:
                self.resultat = "Partie terminée ! Score: {}/{}".format(self.score, len(self.questions))
                pygame.time.set_timer(pygame.USEREVENT + 1, 3000)

        elif event.type == pygame.USEREVENT + 1:
            pygame.time.set_timer(pygame.USEREVENT + 1, 0)
            from menu import Map
            self.jeu.changer_etat(Map(self.jeu))

    def draw(self, screen):
        super().draw(screen)
        question = self.questions[self.niveau]["texte"] if self.niveau < len(self.questions) else ""
        self.sauter_ligne(question, self.jeu.bg_width // 4, self.jeu.bg_height // 4, 30, self.font, (255, 255, 255), screen)

        for rect, texte in self.zone_portes:
            couleur = (100, 50, 20)
            if self.porte_cliquee == rect and self.niveau < len(self.questions):
                couleur = (0, 200, 0) if texte == self.questions[self.niveau]["bonne"] else (200, 0, 0)
            pygame.draw.rect(screen, couleur, rect, border_radius=15)
            pygame.draw.rect(screen, (255, 255, 255), rect, 4, border_radius=15)
            texte_surface = self.font.render(texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=rect.center)
            screen.blit(texte_surface, texte_rect)

        if self.resultat:
            res_surface = self.font.render(self.resultat, True, (255, 255, 0))
            res_rect = res_surface.get_rect(center=(self.jeu.bg_width // 2, self.jeu.bg_height // 1.2))
            screen.blit(res_surface, res_rect)

        
        score_surface = self.font.render(f"Score : {self.score}/{len(self.questions)}", True, (255, 255, 255))
        screen.blit(score_surface, (self.jeu.bg_width - int(self.jeu.bg_width / 6), int(self.jeu.bg_height / 20)))
 