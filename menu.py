import pygame
import os 
from essai3 import Etats
  
class Reglages(Etats):
   """affiche une page de réglages où l'on peut gerer le son, la sauvegarde et les commandes, l'histoire du jeu son données. 
   prends en argument Etats pour garder les méthodes du handle_events, sauter_ligne, aggrandir_boutons
   renvoie les modifications apportées au son (pour ensuite les dessiner de la bonne manière)/ une nouvelle partie si la sauvegarde est réinitialisée"""
   def __init__(self,jeu):
       from menu_deb import Menu_debut
       menu_debut = Menu_debut(jeu)
       super().__init__(jeu)
       self.menu_debut= menu_debut
       super().__init__(jeu)
       self.bg_image = pygame.image.load(os.path.join("assets","fonds", "reglagesessai.png"))
       self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
       self.font=self.jeu.font 
       self.boutons = {"ON" : [pygame.Rect(int(self.jeu.bg_width*1025/self.jeu.bg_width), int(self.jeu.bg_height*318/self.jeu.bg_height), int(self.jeu.bg_width/13), int(self.jeu.bg_height/15)), (176,143,101), (143,116,81),"ON"], 
                       "réin_SAUVEGARDE" : [pygame.Rect(int(self.jeu.bg_width*688/self.jeu.bg_width), int(self.jeu.bg_height*670/self.jeu.bg_height), int(self.jeu.bg_width/4), int(self.jeu.bg_height/14)), (176,143,101), (143,116,81),"Réinitialiser la sauvegarde"],
                       }
       self.boutons_ref = {bouton: [self.boutons[bouton][0].width, self.boutons[bouton][0].height] for bouton in self.boutons}
       self.barre = pygame.Rect(int(self.jeu.bg_width*693/self.jeu.bg_width), int(self.jeu.bg_height*318/self.jeu.bg_height), int(self.jeu.bg_width/6), self.boutons["ON"][0].h)
       self.curseur = pygame.Rect(self.barre.x + self.barre.w/2-self.barre.w/8 , self.barre.y, self.barre.w/4, self.barre.h)
       self.c_mouv= False
       self.volume = self.jeu.volume
       self.dico_commande={"menu" : ["w", int(self.jeu.bg_width*610/self.jeu.bg_width),int(self.jeu.bg_height*527/self.jeu.bg_height)],
                           "carte" : ["x",int(self.jeu.bg_width*828/self.jeu.bg_width),int(self.jeu.bg_height*527/self.jeu.bg_height)],
                           "inventaire" : ["c",int(self.jeu.bg_width*1068/self.jeu.bg_width),int(self.jeu.bg_height*527/self.jeu.bg_height)] }
       self.resu_histoire= "suite à un accident vous êtes bloqué dans le monde d'Etheris,\npour en sortit il vous faut réaliser une potion et donc récuperer par les mini-jeux\nles ingrédients recquis. Arrivez à la fin de chaque niveau des mini-jeux\npour récuperer l'ingrédient et marquer le défi comme fait , vous ne pourrez plus y revenir "
       self.font_resu = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/50))
       self.font_grand = pygame.font.Font(os.path.join("assets", "lacquer.ttf"), int(self.jeu.bg_height/17))
       
   def handle_events(self, event):
     super().handle_events(event)
     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
         if self.curseur.collidepoint(event.pos):
             self.c_mouv = True
         for bouton, (position, couleur, couleur_texte,nom) in list(self.boutons.items()): #on cree une copie du dictionnaire qui est donc figée
             if position.collidepoint(event.pos) :
                 if bouton=="ON" and self.boutons["ON"][3] == "ON" :
                     self.boutons["ON"][1], self.boutons["ON"][2],self.boutons["ON"][3]=(143,116,81), (176,143,101),"OFF"  #on change la couleur des boutons
                     pygame.mixer.music.pause()
                 elif bouton=="ON" and self.boutons["ON"][3] == "OFF" :
                     self.boutons["ON"][1], self.boutons["ON"][2], self.boutons["ON"][3]=(176,143,101), (143,116,81), "ON"
                     pygame.mixer.music.unpause()
                 elif bouton=="réin_SAUVEGARDE" :
                     print("reinitialisation")
     elif event.type == pygame.MOUSEMOTION and self.c_mouv : 
         self.curseur.x = event.pos[0]  # Suit la souris
         self.curseur.clamp_ip(self.barre)  # .clamp_ip contraint un Rect pour qu'il reste entièrement à l’intérieur d’un autre Rect
         self.volume = (self.curseur.x - self.barre.x) / (self.barre.w - self.curseur.w)
         pygame.mixer.music.set_volume(self.volume)
     elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
         self.c_mouv = False           
       
   def draw(self, screen):
     screen.blit(self.bg_image, (0, 0))
     super().draw(screen) 
     self.menu_debut.aggrandir_bouton(screen, self.boutons,self.boutons_ref)
     pygame.draw.rect(screen,(176,143,101), (self.barre.x, self.barre.y, self.barre.w, self.barre.h), border_radius=int(self.barre.w/15)) #pour rect self.barre
     pygame.draw.rect(screen,(143,116,81), (self.curseur.x, self.curseur.y, self.curseur.w, self.curseur.h), border_radius=int(self.barre.w/15)) # pour curseur
     screen.blit(self.font_grand.render("Son : ", True, (6,3,3)), (int(self.jeu.bg_width*559/self.jeu.bg_width), int(self.jeu.bg_height*240/self.jeu.bg_height)))
     screen.blit(self.font_grand.render("Commandes : ", True, (6,3,3)), (int(self.jeu.bg_width*559/self.jeu.bg_width), int(self.jeu.bg_height*424/self.jeu.bg_height)))
     for elem in self.dico_commande:
         screen.blit(self.font.render(f"{elem} : {self.dico_commande[elem][0]}", True, (6,3,3)), (self.dico_commande[elem][1], self.dico_commande[elem][2]))
     screen.blit(self.font_grand.render("Sauvegarde : ", True, (6,3,3)), (int(self.jeu.bg_width*559/self.jeu.bg_width), int(self.jeu.bg_height*590/self.jeu.bg_height)))
     screen.blit(self.font_grand.render("Résumé : ", True, (6,3,3)), (int(self.jeu.bg_width*559/self.jeu.bg_width), int(self.jeu.bg_height*765/self.jeu.bg_height)))
     self.sauter_ligne(self.resu_histoire, int(self.jeu.bg_width*521/self.jeu.bg_width), int(self.jeu.bg_height*840/self.jeu.bg_height), 50 , self.font_resu,(6,3,3), screen)
     


#DONNEES A ENREGISTRER : position du curseur, etat du bouton on/off


class Inventaire(Etats):
 pass
