import pygame
import os 
from général.etats import Etats

class Portes(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Portes.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.image_porte_bonne = pygame.image.load(os.path.join("assets", "porte_ouverte.png"))
        self.image_porte_mauvaise = pygame.image.load(os.path.join("assets", "porte_fermee.png"))
        self.image_porte_neutre = pygame.image.load(os.path.join("assets", "porte_ouverte.png"))

        largeur_porte = self.jeu.bg_width // 6
        hauteur_porte = self.jeu.bg_height // 3
        self.image_porte_bonne = pygame.transform.scale(self.image_porte_bonne, (largeur_porte, hauteur_porte))
        self.image_porte_mauvaise = pygame.transform.scale(self.image_porte_mauvaise, (largeur_porte, hauteur_porte))
        self.image_porte_neutre = pygame.transform.scale(self.image_porte_neutre, (largeur_porte, hauteur_porte))

        self.questions = [
            {"texte": "La fée est au fond d’un puits de 10 mètres\nChaque matin elle monte 3 mètres et chaque nuit descend de 2 mètres.\nCombien de jours lui faudra-t-il pour sortir du puits ?", "choix": ["10", "8", "4"], "bonne": "8"},
            {"texte": "Quelle pierre complète cette suite :\nquartz, rubis, saphir ?", "choix": ["topaze", "améthyste", "émeraude"], "bonne": "topaze"},
            {"texte": "Une barque voguant au nord de l’îlot Zéphyr possède un dessin d’étoile\nà 20 cm de l’eau sur sa coque. Si l’eau monte de 10 cm,\nquelle est la distance entre le dessin et l’eau ? ", "choix": ["20", "15", "10"], "bonne": "20"},
            {"texte": "Dans la forêt des âmes perdues\n100 esprits habitent la lisière circulaire de la forêt,\ntous ont le même discours : “je ne mens jamais mais mon voisin de gauche ment toujours”.\nCombien y-a-t’il d’esprits menteurs ?", "choix": ["100", "99", "50"], "bonne": "50"},
            {"texte": "Dans la bibliothèque du château\nune suite de lettres étranges est inscrite mais la dernière est effacée :\nU-D-T-Q-C-S-S- quelle est cette lettre ?", "choix": ["H", "S", "N"], "bonne": "H"},
        ]

        self.niveau = 0
        self.score = 0
        self.resultat = ""
        self.porte_cliquee = None
        self.mini_jeu = "Portes"
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
            self.zone_portes.append((rect, choix[i], self.image_porte_neutre))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.resultat:
            for rect, reponse, image in self.zone_portes:
                if rect.collidepoint(event.pos):
                    self.porte_cliquee = rect
                    if reponse == self.questions[self.niveau]["bonne"]:
                        self.resultat = "Bonne réponse !"
                        self.score += 1
                        pygame.time.set_timer(pygame.USEREVENT, 1000)
                        
                        
                        self.zone_portes = [(r, t, self.image_porte_bonne if t == reponse else i) for r, t, i in self.zone_portes]
                    else:
                        self.resultat = "Mauvaise réponse."
                        pygame.time.set_timer(pygame.USEREVENT, 1500)
                        
                        
                        self.zone_portes = [(r, t, self.image_porte_mauvaise if t == reponse else i) for r, t, i in self.zone_portes]

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
            from général.etats import recommencement
            self.jeu.changer_etat(recommencement(self.__class__, self.jeu))
            print("mini-jeu perdu!")

    def draw(self, screen):
        super().draw(screen)
        question = self.questions[self.niveau]["texte"] if self.niveau < len(self.questions) else ""
        self.sauter_ligne(question, self.jeu.bg_width // 4, self.jeu.bg_height // 4, 30, self.font, (255, 255, 255), screen)

        
        for rect, texte, image in self.zone_portes:
            screen.blit(image, rect)
            texte_surface = self.font.render(texte, True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=rect.center)
            screen.blit(texte_surface, texte_rect)

        if self.resultat:
            res_surface = self.font.render(self.resultat, True, (255, 255, 0))
            res_rect = res_surface.get_rect(center=(self.jeu.bg_width // 2, self.jeu.bg_height // 1.2))
            screen.blit(res_surface, res_rect)
        
        score_surface = self.font.render(f"Score : {self.score}/{len(self.questions)}", True, (255, 255, 255))
        screen.blit(score_surface, (self.jeu.bg_width - int(self.jeu.bg_width / 6), int(self.jeu.bg_height / 20)))
        
        self.montrer_regles_aide(screen, self.last_event, "Portes")
