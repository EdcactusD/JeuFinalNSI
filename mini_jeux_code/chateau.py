import pygame
import os 
import math
import random
from général.etats import Etats

"""contient la classe Chateau et les mini-jeux auxuels elle permet d'acceder le Pendu et la Pendule """

class Chateau(Etats):
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_chateau.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_chateau = {"zone_Pendu" : [pygame.Rect(int(self.jeu.bg_width/2.844),int(self.jeu.bg_height/1.4896),int(self.jeu.bg_width/4.8),int(self.jeu.bg_height/3.6)), Pendu],
                              "zone_Pendule" : [pygame.Rect(int(self.jeu.bg_width/1.92),int(self.jeu.bg_height/2.7),int(self.jeu.bg_width/3.84),int(self.jeu.bg_height/3.32)), Pendule]
                              }

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
           for zone in self.zones_chateau:
               if self.zones_chateau[zone][0].collidepoint(event.pos): 
                   self.jeu.changer_etat(self.zones_chateau[zone][1](self.jeu))
                   
class Pendu(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendu.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.words_easy = ["chat", "chien", "pomme", "maison", "voiture"]
        self.words_medium = ["ordinateur", "python", "programmation", "hangman", "jeu"]
        self.words_hard = ["développement", "intelligence", "algorithmique", "complexité", "optimisation"]

        self.difficulty_levels = {
            "Easy": self.words_easy,
            "Medium": self.words_medium,
            "Hard": self.words_hard
        }

        self.difficulty = "Easy"
        self.word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_over = False
        self.win = False
        self.input_active = False
        self.message = ""
        self.letter_input = ""
        self.font_large = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/20))
        self.font_medium = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/30))
        self.font_small = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/40))

        self.completed_difficulties = {"Easy": False, "Medium": False, "Hard": False}
        self.reward_given = False
        
        
        self.attendre = False
        self.attente = 10000  
        self.debut_attente = -self.attente

        self.start_new_game()

        self.buttons = {
            "Easy": pygame.Rect(int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Medium": pygame.Rect(int(self.jeu.bg_width*0.22), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Hard": pygame.Rect(int(self.jeu.bg_width*0.34), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05)),
            "Restart": pygame.Rect(int(self.jeu.bg_width*0.8), int(self.jeu.bg_height*0.1), int(self.jeu.bg_width*0.1), int(self.jeu.bg_height*0.05))
        }

        self.mini_jeu = "Pendu"
        self.fichier =  "chateau"  

    def start_new_game(self):
        import random
        self.word = random.choice(self.difficulty_levels[self.difficulty]).upper()
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.game_over = False
        self.win = False
        self.message = ""
        self.letter_input = ""
        self.input_active = True

    def handle_events(self, event):
        
        super().handle_events_souris(event)
        
       
        if self.attendre:
            if pygame.time.get_ticks() - self.debut_attente > self.attente:
                self.attendre = False
        
        if self.game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.buttons["Restart"].collidepoint(event.pos):
                    self.start_new_game()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for key, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    if key in ["Easy", "Medium", "Hard"]:
                        self.difficulty = key
                        self.start_new_game()
                    elif key == "Restart":
                        self.start_new_game()
                    return

        if event.type == pygame.KEYDOWN and self.input_active and not self.game_over and not self.attendre:
            if event.key == pygame.K_BACKSPACE:
                self.letter_input = ""
            elif event.key == pygame.K_RETURN:
                if len(self.letter_input) == 1 and self.letter_input.isalpha():
                    letter = self.letter_input.upper()
                    if letter in self.guessed_letters:
                        self.message = f"Lettre '{letter}' déjà proposée."
                    else:
                        self.guessed_letters.add(letter)
                        if letter not in self.word:
                            self.wrong_guesses += 1
                            if self.wrong_guesses >= self.max_wrong_guesses:
                                self.game_over = True
                                self.win = False
                                self.message = f"Perdu ! Le mot était : {self.word}"
                                self.debut_attente = pygame.time.get_ticks()
                                self.attendre = True
                        else:
                            if all(l in self.guessed_letters for l in self.word):
                                self.game_over = True
                                self.win = True
                                self.message = "Bravo ! Vous avez gagné !"
                                self.completed_difficulties[self.difficulty] = True
                                if all(self.completed_difficulties.values()) and not self.reward_given:
                                    self.reward_given = True
                                    self.message = "Félicitations ! Vous avez obtenu l'objet : cheveux de rossier"
                                    self.mini_jeu_fini(self.mini_jeu)
                    self.letter_input = ""
                else:
                    self.message = "Entrez une seule lettre valide."
                    self.letter_input = ""
            else:
                if len(self.letter_input) == 0 and event.unicode.isalpha():
                    self.letter_input = event.unicode.upper()

    def draw_hangman(self, screen):
        base_x = int(self.jeu.bg_width * 0.7)
        base_y = int(self.jeu.bg_height * 0.8)
        line_color = (139, 69, 19)
        
       
        pygame.draw.rect(screen, (60, 60, 60, 180), (base_x - 120, base_y - 320, 250, 340))

       
        pygame.draw.line(screen, line_color, (base_x - 100, base_y), (base_x + 100, base_y), 8)
        pygame.draw.line(screen, line_color, (base_x - 50, base_y), (base_x - 50, base_y - 300), 8)
        pygame.draw.line(screen, line_color, (base_x - 50, base_y - 300), (base_x + 50, base_y - 300), 8)
        pygame.draw.line(screen, line_color, (base_x + 50, base_y - 300), (base_x + 50, base_y - 250), 8)

       
        person_color = (230, 230, 230)  
        stroke_width = 4  

        if self.wrong_guesses > 0:
            pygame.draw.circle(screen, person_color, (base_x + 50, base_y - 230), 20, stroke_width)
        if self.wrong_guesses > 1:
            pygame.draw.line(screen, person_color, (base_x + 50, base_y - 210), (base_x + 50, base_y - 150), stroke_width)
        if self.wrong_guesses > 2:
            pygame.draw.line(screen, person_color, (base_x + 50, base_y - 200), (base_x + 20, base_y - 170), stroke_width)
        if self.wrong_guesses > 3:
            pygame.draw.line(screen, person_color, (base_x + 50, base_y - 200), (base_x + 80, base_y - 170), stroke_width)
        if self.wrong_guesses > 4:
            pygame.draw.line(screen, person_color, (base_x + 50, base_y - 150), (base_x + 20, base_y - 110), stroke_width)
        if self.wrong_guesses > 5:
            pygame.draw.line(screen, person_color, (base_x + 50, base_y - 150), (base_x + 80, base_y - 110), stroke_width)

    def draw_word(self, screen):
        display_word = ""
        for letter in self.word:
            display_word += letter + " " if letter in self.guessed_letters else "_ "
        text_surface = self.font_large.render(display_word.strip(), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.jeu.bg_width * 0.35, self.jeu.bg_height * 0.5))
        screen.blit(text_surface, text_rect)

    def draw_guessed_letters(self, screen):
        guessed = "Lettres proposées: " + " ".join(sorted(self.guessed_letters))
        text_surface = self.font_medium.render(guessed, True, (255, 255, 255))
        screen.blit(text_surface, (int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.7)))

    def draw_input_box(self, screen):
        input_box = pygame.Rect(int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.6), int(self.jeu.bg_width * 0.1), int(self.jeu.bg_height * 0.05))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        input_text = self.font_medium.render(self.letter_input, True, (255, 255, 255))
        screen.blit(input_text, (input_box.x + 5, input_box.y + 5))
        prompt_text = self.font_small.render("Tapez une lettre et appuyez sur Entrée", True, (255, 255, 255))
        screen.blit(prompt_text, (input_box.x, input_box.y - 25))

    def draw_buttons(self, screen):
        for key, rect in self.buttons.items():
            color = (100, 100, 100)
            if key == self.difficulty:
                color = (200, 200, 50)
            pygame.draw.rect(screen, color, rect)
            text_surface = self.font_small.render(key, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

    def draw_message(self, screen):
        if self.message:
            message_surface = self.font_medium.render(self.message, True, (255, 0, 0))
            message_rect = message_surface.get_rect(center=(self.jeu.bg_width * 0.5, self.jeu.bg_height * 0.85))
            screen.blit(message_surface, message_rect)

    def draw(self, screen):
        super().draw(screen)

        overlay = pygame.Surface((self.jeu.bg_width, self.jeu.bg_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        titre = self.font_large.render("PENDU", True, (255, 255, 255))
        screen.blit(titre, (self.jeu.bg_width // 2 - titre.get_width() // 2, int(self.jeu.bg_height * 0.05)))

        self.draw_word(screen)
        self.draw_guessed_letters(screen)
        self.draw_input_box(screen)
        self.draw_buttons(screen)
        self.draw_hangman(screen)
        self.draw_message(screen)

        bar_width = int(self.jeu.bg_width * 0.6)
        bar_height = int(self.jeu.bg_height * 0.02)
        bar_x = (self.jeu.bg_width - bar_width) // 2
        bar_y = int(self.jeu.bg_height * 0.9)

        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        if self.wrong_guesses > 0:
            filled_width = bar_width * (self.wrong_guesses / self.max_wrong_guesses)
            pygame.draw.rect(screen, (200, 60, 60), (bar_x, bar_y, filled_width, bar_height), border_radius=10)
        
        
        if self.attendre:
            temps_restant = max(0, (self.attente - (pygame.time.get_ticks() - self.debut_attente)) // 1000)
            attente_text = self.font_medium.render(f"Veuillez attendre {temps_restant} secondes...", True, (255, 0, 0))
            attente_rect = attente_text.get_rect(center=(self.jeu.bg_width * 0.5, self.jeu.bg_height * 0.3))
            screen.blit(attente_text, attente_rect)
        
        self.montrer_regles_aide(screen, self.last_event, "Pendu")

#Mini-jeu où le but est d'arrêter la pendule au bon moment , on y reprend le dictionnaire niveaux_jeux pour gérer les niveaux
#On renvoie la reussité du mini-jeu par le joueur et on réutulise les methodes de Etats()

class Pendule(Etats):
    def __init__(self, jeu):
        super().__init__(jeu)
        from général.etats import niveaux_jeux
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "Pendule.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zone_bouton = pygame.Rect(int(self.jeu.bg_width/2.1), int(self.jeu.bg_height/1.4),int(self.jeu.bg_width/11),int(self.jeu.bg_height/16))
        self.zone_angle = pygame.Rect(int(self.jeu.bg_width/3), int(self.jeu.bg_height/5),int(self.jeu.bg_width/2.8),int(self.jeu.bg_height/16))

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gris = (112, 128, 144)
        self.brown = (139, 69, 19)
        self.center = (self.menu_width // 0.1, self.menu_height // 1)
        self.radius = 200
        self.angle = 0
        self.target_angle = random.choice([i * 30 for i in range(12)]) #on prned une valeur random dans une liste aléatoire
        self.objectif = [self.target_angle,self.target_angle+30] #l'objectif est donc de cette angle + 30
        self.visee = "Arretez l'horloge entre " + str(self.objectif[0] // 30) +  "heures et " + str(self.objectif[1] // 30) + "heures"
        self.action = True
        self.mini_jeu = "Pendule"
        self.etapes = [0,1,2,3]
        self.niveau = str(niveaux_jeux["Pendule"][0])
        self.vitesse = 10
        print(self.target_angle)

    def handle_events(self, event):
        super().handle_events(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if self.zone_bouton.collidepoint(event.pos):
            if self.objectif[0] <= self.angle <= self.objectif[1]:
             self.niveau=str(int(self.niveau)+1)
             self.vitesse += 5
             angle = self.angle
             print(angle)
             print(self.objectif)
             self.target_angle = random.choice([i * 30 for i in range(12)])
             self.objectif = [self.target_angle,self.target_angle+30]
             self.visee = "Arretez l'horloge entre " + str(self.objectif[0] // 30) +  "heures et " + str(self.objectif[1] // 30) + "heures"
            else:
             print("mini-jeu perdu!")
             from général.etats import recommencement
             self.jeu.changer_etat(recommencement(self.__class__,self.jeu))
        if self.niveau=="3":
            self.mini_jeu_fini(self.mini_jeu)
  
            

    
    def draw(self, screen):
        super().draw(screen)
        if self.action == True:
          self.angle = (self.angle + self.vitesse) % 360

        pygame.draw.rect(screen,self.brown,self.zone_bouton,border_radius=int(self.jeu.bg_height / 5))
        screen.blit(self.font.render("   Stop", True, self.white),(self.zone_bouton.x*1.02, self.zone_bouton.y*1.02)) #Le True est pour adoucir le bord des textes

        pygame.draw.rect(screen,self.brown,self.zone_angle,border_radius=int(self.jeu.bg_height / 5))
        screen.blit(self.font.render(self.visee , True, self.white),(self.zone_angle.x*1.02, self.zone_angle.y*1.02))
    
        pygame.draw.circle(screen, self.brown, self.center, self.radius)
        pygame.draw.circle(screen, self.black, self.center, self.radius, 5)
        for i in range(12):
         x = self.center[0] + math.cos(math.radians(i * 30 - 90)) * (self.radius - 20)
         y = self.center[1] + math.sin(math.radians(i * 30 - 90)) * (self.radius - 20)
         pygame.draw.circle(screen, self.black, (int(x), int(y)), 5)

        aiguille_length = self.radius - 20
        end_x = self.center[0] + math.cos(math.radians(self.angle - 90)) * aiguille_length
        end_y = self.center[1] + math.sin(math.radians(self.angle - 90)) * aiguille_length
        pygame.draw.line(screen, self.gris, self.center, (end_x, end_y), width = 5)

        self.montrer_regles_aide(screen,self.last_event,"Pendule")

