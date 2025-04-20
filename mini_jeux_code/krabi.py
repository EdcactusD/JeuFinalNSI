import pygame
import os 
import random 
from essai3 import Etats

class Krabi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Krabi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.vocab = {
            "orage": "O",
            "brume": "B",
            "lumière": "L",
            "frisson": "F",
            "aube": "A"
        }

        self.secret = "BLOAF"
        self.reponse = ""
        self.input_active = False
        self.message = ""

        self.mots_dynamiques = []
        for mot, lettre in self.vocab.items():
            surf = self.jeu.font.render(mot, True, (255, 255, 255))
            x = random.randint(0, self.jeu.bg_width - surf.get_width())
            y = random.randint(0, self.jeu.bg_height - surf.get_height() - int(self.jeu.bg_height * 0.2))
            dx = random.uniform(-0.7, 0.7)
            dy = random.uniform(-0.5, 0.5)
            self.mots_dynamiques.append({
                "mot": mot,
                "lettre": lettre,
                "x": x,
                "y": y,
                "dx": dx,
                "dy": dy,
                "cliqué": False,
                "alpha": 0,
                "brillance_sens": 1
            })

        self.zone_input = pygame.Rect(int(self.jeu.bg_width * 0.3), int(self.jeu.bg_height * 0.85), int(self.jeu.bg_width * 0.4), int(self.jeu.bg_height * 0.07))

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for item in self.mots_dynamiques:
                if not item["cliqué"]:
                    mot_surf = self.jeu.font.render(item["mot"], True, (255, 255, 255))
                    rect = mot_surf.get_rect(topleft=(item["x"], item["y"]))
                    if rect.collidepoint(mx, my):
                        item["cliqué"] = True
                        item["dx"] *= 0.1
                        item["dy"] *= 0.1
                        item["alpha"] = 0
                        item["brillance_sens"] = 1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.input_active = self.zone_input.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                if self.reponse.upper() == self.secret:
                    self.message = "✨ Succès ! ✨"
                else:
                    self.message = "Mot incorrect"
            elif event.key == pygame.K_BACKSPACE:
                self.reponse = self.reponse[:-1]
            elif len(self.reponse) < len(self.secret):
                self.reponse += event.unicode.upper()

    def draw(self, screen):
        super().draw(screen)

        lettres_revelees = []

        for item in self.mots_dynamiques:
            item["x"] += item["dx"]
            item["y"] += item["dy"]

            if item["x"] <= 0 or item["x"] >= self.jeu.bg_width - 150:
                item["dx"] *= -1
            if item["y"] <= 0 or item["y"] >= self.jeu.bg_height - 200:
                item["dy"] *= -1

            if item["cliqué"]:
                if item["alpha"] < 200:
                    item["alpha"] = min(255, item["alpha"] + 10)
                else:
                    item["alpha"] += item["brillance_sens"] * 2
                    if item["alpha"] > 255:
                        item["alpha"] = 255
                        item["brillance_sens"] = -1
                    elif item["alpha"] < 200:
                        item["alpha"] = 200
                        item["brillance_sens"] = 1

                surface = self.jeu.font.render(item["lettre"], True, (0, 255, 100))
                faded = surface.copy()
                faded.set_alpha(int(item["alpha"]))
                screen.blit(faded, (item["x"], item["y"]))
                lettres_revelees.append(item["lettre"])
            else:
                surface = self.jeu.font.render(item["mot"], True, (255, 255, 255))
                screen.blit(surface, (item["x"], item["y"]))

        lettres_surface = self.jeu.font.render(" ".join(lettres_revelees), True, (0, 255, 100))
        screen.blit(lettres_surface, (int(self.jeu.bg_width * 0.05), int(self.jeu.bg_height * 0.8)))

        pygame.draw.rect(screen, (255, 255, 255), self.zone_input, border_radius=10, width=2)
        input_surface = self.jeu.font.render(self.reponse, True, (255, 255, 255))
        screen.blit(input_surface, (self.zone_input.x + 10, self.zone_input.y + 10))

        if self.message:
            msg_surface = self.jeu.font.render(self.message, True, (255, 215, 0))
            screen.blit(msg_surface, (self.zone_input.x, self.zone_input.y - 40))
