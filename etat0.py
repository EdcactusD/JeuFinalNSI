import pygame
import os
#import random
#from menu_deb import Menu_debut
from général.etats import Etats



#Pour finir vos mini-jeux : svp utilisez la fonction  mini_jeu_fini() (ca permet de retourner à la map normalement avec les imports)
"""
REGLE A RESPECTER DANS LE CODE :
    ¤) pour definir des tailles d'objets faites le par une multiplication ou une division (pour que les valeurs soient toujours bien même si l'écran a une taille étrange)
    :::faire attention par exemple les rects n'accptent pas de float il faut alors caster
    
EXPLICATIONS SUR CERTAINS POINTS ET METHODES PRATIQUE DANS LE CODE:
1. event.pos représente les coordonnées (x, y) de l'endroit où la souris a cliqué, 
obtenues dans un événement MOUSEBUTTONDOWN ou MOUSEBUTTONUP : 
collidepoint retourne un booléen suivant si la souris est dans la zone (True) ou non (False)  

2. .items()  permet d'obtenir la clé et la valeur dans un dico
"""

     

           

class Etat0(Etats): 
    def __init__(self,jeu):
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "etat0.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.show_menu = True

    def handle_events(self, event):
        super().handle_events(event)
        



#Pour jeux avec entrée texte : faire un curseur qui clignote ?
#Les prints dans enigme sont à modifier en messages qui popent

#ATTENTION : pour le bon fonctionnement du jeu, quand on change d'état certaines caracteristiques doivent être conservées (genre le temps du chrono en cours, le niveau atteint)