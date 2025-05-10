import pygame
import os

class Menu_debut:
  """gère l'écran qui s'affiche pour lancer le jeu"""
  def __init__(self, jeu):
      self.jeu = jeu
      
      self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "menudebut.png"))
      self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))  
      #voir si c'est utile
      self.width_bouton, self.height_bouton, self.espace = int(self.jeu.bg_width/4.8), int(self.jeu.bg_height/9.8181), int(self.jeu.bg_height/7.2)
      self.boutons = {"Jouer" : [pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2), self.width_bouton, self.height_bouton),"#834c2c","#d9aa62","Jouer"],
                      "Lancer une nouvelle partie" : [pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2)+self.espace, self.width_bouton, self.height_bouton),"#834c2c","#d9aa62","Lancer une nouvelle partie"],
                      "Quitter" : [pygame.Rect(int(self.jeu.bg_width/2)-int(self.width_bouton/2), int(self.jeu.bg_height/2)-int(self.height_bouton/2)+self.espace*2, self.width_bouton, self.height_bouton),"#834c2c","#d9aa62","Quitter"]
          }
      self.boutons_ref = {bouton: [self.boutons[bouton][0].width, self.boutons[bouton][0].height] for bouton in self.boutons}
      self.font=self.jeu.font
      
  def handle_events(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for bouton, (position, couleur, couleur_texte,nom) in self.boutons.items():
            if position.collidepoint(event.pos) :
                if bouton == "Jouer" :
                    from général.menu import Map
                    self.jeu.changer_etat(Map(self.jeu))
                elif bouton=="Lancer une nouvelle partie" :
                    print("lancement d'une nouvelle partie")
                elif bouton=="Quitter":
                    self.jeu.running=False
            
  def aggrandir_bouton(self,screen, boutons, bouton_ref):   
     for bouton in boutons:
       if boutons[bouton][0].collidepoint(pygame.mouse.get_pos()): #on aggrandit les boutons quand la souris passe dessus
         if boutons[bouton][0].width == bouton_ref[bouton][0]: #on vérifie que le bouton n'est pas déjà aggrandi
            boutons[bouton][0]=boutons[bouton][0].inflate(int(bouton_ref[bouton][0]*0.1),int(bouton_ref[bouton][1]*0.1)) #.inflate revoie un nouveau rect avec une taille modifiée
       elif boutons[bouton][0].width != bouton_ref[bouton][0]:
            boutons[bouton][0]=boutons[bouton][0].inflate(int(-bouton_ref[bouton][0]*0.1),int(-bouton_ref[bouton][1]*0.1))
       pygame.draw.rect(screen, boutons[bouton][1], boutons[bouton][0], border_radius=int(self.jeu.bg_height/54))
       rect_texte=self.font.render(boutons[bouton][3], True, boutons[bouton][2]).get_rect()
       rect_texte.x, rect_texte.y  = boutons[bouton][0].x + (boutons[bouton][0].w- rect_texte.w)//2  ,boutons[bouton][0].y+(boutons[bouton][0].h- rect_texte.h)//2  #on ajoute la moitié des marges (donc comme si une marge que d'un coté)
       #pygame.draw.rect(screen, (255, 0, 0), rect_texte, 10)
       screen.blit(self.font.render(boutons[bouton][3], True, boutons[bouton][2]), rect_texte) #le .get_rect permet de créer un rect pour le texte
       
  def draw(self, screen):
    #screen.fill((0, 0, 0)) #pas necessaire si tout l'écran est rempli
    screen.blit(self.bg_image, (0, 0))
    self.aggrandir_bouton(screen,self.boutons,self.boutons_ref)