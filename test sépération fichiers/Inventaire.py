import os
import pygame
import Etats

class Inventaire():
    def __init__(self):
        self.ingredients_images = {
            "cheveux de Rossier": "assets/items/cheveux de Rossier.jpg",
            "éclat d'obsidrune": "assets/items/éclat d'obsidrune.jpg",
            "Elixir des mondes": "assets/items/Elixir des mondes.jpg",
            "Epine de Sylve": "assets/items/Epine de Sylve.jpg",
            "glace millénaire": "assets/items/glace millénaire.jpg",
            "grain d'ambre": "assets/items/grain d'ambre.jpg",
            "oeuf de phoenix": "assets/items/oeuf de phoenix.jpg",
            "pépite d'or": "assets/items/pépite d'or.jpg",
            "pince de Kraby": "assets/items/pince de Kraby.png",
            "pomme de la discorde": "assets/items/pomme de la discorde.jpg",
            "poudre de perlinpimpim": "assets/items/poudre de perlinpimpim.jpg",
            "poussière du Zéphyr": "assets/items/poussière du Zéphyr.jpg",
            "rosée du désert": "assets/items/rosée du désert.jpg",
            "Sel de Mars": "assets/items/Sel de Mars.jpg",
            "sève sagesse": "assets/items/sève sagesse.jpg"
        }
        self.owned_ingredients = {
            "cheveux de Rossier": False,
            "éclat d'obsidrune": False,
            "Elixir des mondes": False,
            "Epine de Sylve": False,
            "glace millénaire": False,
            "grain d'ambre": False,
            "oeuf de phoenix": False,
            "pépite d'or": False,
            "pince de Kraby": False,
            "pomme de la discorde": False,
            "poudre de perlinpimpim": False,
            "poussière du Zéphyr": False,
            "rosée du désert": False,
            "Sel de Mars": False,
            "sève sagesse": False
        }

    def set_ingredient_state(self, ingredient, owned):
        if ingredient in self.owned_ingredients:
            self.owned_ingredients[ingredient] = owned

    def display_inventory(self, screen):
        x_position = 100
        y_position = 100
        for ingredient, image_path in self.ingredients_images.items():
            if not self.owned_ingredients[ingredient]:
                image = pygame.image.load(image_path)
                gray_image = pygame.transform.threshold(image, image, (200, 200, 200), (255, 255, 255), (0, 0, 0), 1)
                screen.blit(gray_image, (x_position, y_position))
            else:
                image = pygame.image.load(image_path)
                x_position = 100
                y_position = 100
                screen.blit(image, (x_position, y_position))
