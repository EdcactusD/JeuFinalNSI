import pygame
import os

# Initialisation de Pygame
pygame.init()

# Récupérer la taille de l'écran
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Créer une fenêtre en plein écran
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Clique pour afficher les coordonnées")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Police pour afficher les numéros
font = pygame.font.Font(None, 36)

# Liste pour stocker les clics (numéro + position)
clicks = []
click_count = 0  # Numéro du clic

# Boucle principale
running = True
while running:
    bg_image = pygame.image.load(os.path.join("assets", "fonds", "reglagesessai.png"))
    screen.blit(bg_image, (0, 0))

    # Afficher les anciens clics
    for num, (x, y) in clicks:
        # Dessine un "X" rouge
        pygame.draw.line(screen, RED, (x - 10, y - 10), (x + 10, y + 10), 3)
        pygame.draw.line(screen, RED, (x - 10, y + 10), (x + 10, y - 10), 3)

        # Affiche le numéro à côté
        text_surface = font.render(str(num), True, BLACK)
        screen.blit(text_surface, (x + 15, y - 15))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Clic de souris
            click_count += 1  # Incrémente le numéro
            x, y = event.pos  # Coordonnées du clic
            clicks.append((click_count, (x, y)))  # Stocke le clic
            print(f"{click_count}: int(self.jeu.bg_width*{x}/self.jeu.bg_width), int(self.jeu.bg_height*{y}/self.jeu.bg_height)")
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Quitter avec Échap
            running = False

    pygame.display.flip()  # Met à jour l'affichage

# Quitter Pygame
pygame.quit()


