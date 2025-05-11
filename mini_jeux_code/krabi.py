import pygame
import os
import random
from général.etats import Etats

class Krabi(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Krabi.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.levels = [
            {
                "vocab": {
                    "eau": "E",
                    "montagne": "M",
                    "terre": "T",
                    "soleil": "S",
                    "pluie": "P"
                },
                "secret": "TEMPS"
            },
            {
                "vocab": {
                    "vent": "E",
                    "pluie": "P",
                    "neige": "N",
                    "soleil": "S",
                    "nuit": "U"
                },
                "secret": "PNEUS"
            },
            {
                "vocab": {
                    "bleu": "B",
                    "terre": "T",
                    "eau": "E",
                    "air": "A",
                    "limon": "L"
                },
                "secret": "TABLE"
            }
        ]

        self.current_level = 0
        self.finished = False
        self.load_level(self.current_level)

        self.input_active = False
        self.message = ""

        self.zone_input = pygame.Rect(int(self.jeu.bg_width * 0.3), int(self.jeu.bg_height * 0.85), int(self.jeu.bg_width * 0.4), int(self.jeu.bg_height * 0.07))
        self.mini_jeu = "Krabi"


    def load_level(self, level_index):
        level = self.levels[level_index]
        self.vocab = level["vocab"]
        self.secret = level["secret"]
        self.reponse = ""
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

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if not self.finished:
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
            self.input_active = self.zone_input.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.input_active:
            if not self.finished:
                if event.key == pygame.K_RETURN:
                    if self.reponse.upper() == self.secret:
                        self.message = "Succès !"
                        self.advance_level()
                    else:
                        self.message = "Mot incorrect"
                elif event.key == pygame.K_BACKSPACE:
                    self.reponse = self.reponse[:-1]
                elif len(self.reponse) < len(self.secret):
                    self.reponse += event.unicode.upper()

    def advance_level(self):
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.finished = True
            self.reponse = ""
        else:
            self.load_level(self.current_level)

    def draw(self, screen):
        super().draw(screen)

        progress = min((self.current_level) / len(self.levels), 1)
        bar_width = int(progress * self.jeu.bg_width)
        bar_height = 20
        bar_x = 0
        bar_y = 10

        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, self.jeu.bg_width, bar_height), border_radius=10)

        color_start = (0, 200, 0)
        color_end = (0, 255, 100)
        gradient_surface = pygame.Surface((bar_width, bar_height))
        for i in range(bar_width):
            r = color_start[0] + (color_end[0] - color_start[0]) * i // bar_width
            g = color_start[1] + (color_end[1] - color_start[1]) * i // bar_width
            b = color_start[2] + (color_end[2] - color_start[2]) * i // bar_width
            pygame.draw.line(gradient_surface, (r, g, b), (i, 0), (i, bar_height))
        gradient_surface.set_alpha(220)
        screen.blit(gradient_surface, (bar_x, bar_y))

        brillance_x = (pygame.time.get_ticks() // 5) % self.jeu.bg_width
        brillance_width = 80
        brillance_rect = pygame.Rect(brillance_x, bar_y, brillance_width, bar_height)
        brillance_surface = pygame.Surface((brillance_width, bar_height), pygame.SRCALPHA)
        pygame.draw.rect(brillance_surface, (255, 255, 255, 70), brillance_surface.get_rect())
        screen.blit(brillance_surface, brillance_rect)

        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, self.jeu.bg_width, bar_height), width=2, border_radius=10)

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

        if self.finished:
            fin_surface = self.jeu.font.render("🎉 Tous les niveaux terminés ! 🎉", True, (255, 215, 0))
            screen.blit(fin_surface, (self.zone_input.x - 30, self.zone_input.y - 80))
        elif self.message:
            msg_surface = self.jeu.font.render(self.message, True, (255, 215, 0))
            screen.blit(msg_surface, (self.zone_input.x, self.zone_input.y - 40))
            
        self.montrer_regles_aide(screen, self.last_event, "Krabi")
