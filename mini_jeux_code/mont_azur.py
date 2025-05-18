import pygame
import os 
from général.etats import Etats
import random

"""contient la classe Mont-azur et un des mini-jeu qu'elle permet d'acceder (le plateformer) car Trad est avec Enigme pour leur ressemblance au nievau du code (héritage)"""

class Mont_azur(Etats): 
    def __init__(self,jeu):
        from mini_jeux_code.enigme_trad import Trad
        super().__init__(jeu)
        self.bg_image = pygame.image.load(os.path.join("assets","fonds", "plan_mont_azur.png"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))
        self.zones_mont_azur = {"zone_Donkey_kong_mario" : [pygame.Rect(int(self.jeu.bg_width/2.2588),int(self.jeu.bg_height/1.661),int(self.jeu.bg_width/3.2),int(self.jeu.bg_height/2.7)), Donkey_kong_mario],
                                "zone_Trad" : [pygame.Rect(int(self.jeu.bg_width/6.4),int(self.jeu.bg_height/10.8),int(self.jeu.bg_width/3.2),int(self.jeu.bg_height/1.96)),Trad]}
        self.afficher_pop_up_bool = False
        self.pop_up_text = ""
        
    def handle_events(self, event):
        super().handle_events(event) # Garde le comportement général des événements (utile car après on va ajouter des choses dedans)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            from général.menu import Map
            self.jeu.changer_etat(Map(self.jeu)) 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.afficher_pop_up_bool:
                self.afficher_pop_up_bool = False
            else:
                from général.etats import niveaux_jeux
                for zone in self.zones_mont_azur:
                    if self.zones_mont_azur[zone][0].collidepoint(event.pos):
                        mini_game_key = zone.replace("zone_", "")
                        if mini_game_key in niveaux_jeux and niveaux_jeux[mini_game_key][4]:
                            self.pop_up_text = f"Vous avez déjà reçu l'objet de ce mini-jeu : {niveaux_jeux[mini_game_key][5]}\nVeuillez lancer une nouvelle partie pour recommencer"
                            self.afficher_pop_up_bool = True
                        else:
                            self.jeu.changer_etat(self.zones_mont_azur[zone][1](self.jeu))
        
    def draw(self, screen):
        super().draw(screen)
        if self.afficher_pop_up_bool:
            self.afficher_pop_up(screen, self.pop_up_text)

class Donkey_kong_mario(Etats):
    FPS = 60
    W_P, H_P = 38, 50
    W_B, H_B = 26, 26
    W_LAD = 22
    VX_P = 4
    VY_SAUT = -8
    GRAV_P = 0.6

    VX_B = 4
    GRAV_B = 5
    BARIL_MIN_MS, BARIL_MAX_MS = 1500, 1800

    PLATS = [
        (0.86, .94, (0.47, 0.53)),
        (0.68, 1.00, (0.77, 0.83)),
        (0.50, .94, (0.22, 0.28)),
        (0.32, 1.00, (0.54, 0.60)),
        (0.14, .94, (0.74, 0.80))
    ]

    def __init__(self, jeu):
        super().__init__(jeu)
        self.mini_jeu, self.fichier = "Donkey_kong_mario", "mont_azur"

        self.bg_image = pygame.image.load(os.path.join("assets", "fonds", "Donkey_kong_mario.jpg"))
        self.bg_image = pygame.transform.scale(self.bg_image, (self.jeu.bg_width, self.jeu.bg_height))

        self.img_player = pygame.image.load(os.path.join("assets", "player_platformer.png")).convert_alpha()
        self.img_barrel = pygame.image.load(os.path.join("assets", "projectile_platformer.png")).convert_alpha()
        self.img_platform = pygame.image.load(os.path.join("assets", "sol_platformer.png")).convert_alpha()
        self.img_ladder = pygame.image.load(os.path.join("assets", "echelle_platformer.png")).convert_alpha()
        self.img_win_zone = pygame.image.load(os.path.join("assets", "arrivee_platformer.png")).convert_alpha()
        self.img_thrower = pygame.image.load(os.path.join("assets", "mechant_platformer.png")).convert_alpha()

        y0 = int(self.jeu.bg_height * self.PLATS[0][0]) - self.H_P
        x0 = 40
        self.player = pygame.Rect(x0, y0, self.W_P, self.H_P)
        self.vx = self.vy = 0
        self.on_ground = self.on_ladder = False

        self.player_facing_right = True  
        self.barils = []
        for etg in range(1, len(self.PLATS) - 1):
            y = int(self.jeu.bg_height * self.PLATS[etg][0]) - self.H_B
            dir0 = -1 if etg % 2 == 0 else 1
            x = 0 if dir0 == 1 else self.jeu.bg_width - self.W_B
            self.barils.append({"rect": pygame.Rect(x, y, self.W_B, self.H_B),
                                "etage": etg,
                                "chute": False,
                                "dir": dir0})
        self._plan_next_spawn()

        pygame.time.set_timer(pygame.USEREVENT + 2, int(1000 / self.FPS))

        self._build_ladders()

        win_y = int(self.jeu.bg_height * 0.03)
        win_w = self.jeu.bg_width//19.2
        win_h = self.jeu.bg_height//8.5
        self.win_zone = pygame.Rect(int(self.jeu.bg_width * 0.05), win_y, win_w, win_h)

        throw_x = int(self.jeu.bg_width * 0.78) + 40
        self.thrower = pygame.Rect(throw_x, self.win_zone.bottom, self.W_P, self.H_P)
        self.thrower = pygame.Rect(throw_x, self.thrower.y-self.thrower.h, self.W_P, self.H_P)

    def _build_ladders(self):
        self.ladders = []
        h_ladder = int(self.jeu.bg_height * (self.PLATS[0][0] - self.PLATS[1][0]))

        x1 = int(self.jeu.bg_width * 0.65)
        y_bot = int(self.jeu.bg_height * self.PLATS[0][0])
        self.ladders.append(pygame.Rect(x1, y_bot - h_ladder, self.W_LAD, h_ladder))

        left, right = int(self.jeu.bg_width * 0.10), int(self.jeu.bg_width * 0.80)
        for i in range(1, len(self.PLATS) - 1):
            y_bot = int(self.jeu.bg_height * self.PLATS[i][0])
            y_top = int(self.jeu.bg_height * self.PLATS[i + 1][0])
            h = y_bot - y_top
            x = left if i % 2 == 1 else right
            self.ladders.append(pygame.Rect(x, y_top, self.W_LAD, h))

    def _plan_next_spawn(self):
        delay = random.randint(self.BARIL_MIN_MS, self.BARIL_MAX_MS)
        pygame.time.set_timer(pygame.USEREVENT + 1, delay, True)

    def _update_player(self, keys):
        self.on_ladder = any(self.player.colliderect(l) for l in self.ladders)
        if self.on_ladder:
            self.vy = 0
            if keys[pygame.K_UP]:
                self.vy = -self.VX_P
            if keys[pygame.K_DOWN]:
                self.vy = self.VX_P
        else:
            self.vy += self.GRAV_P

        self.vx = (-self.VX_P if keys[pygame.K_LEFT] else
                   self.VX_P if keys[pygame.K_RIGHT] else 0)

        
        if self.vx > 0:
            self.player_facing_right = True
        elif self.vx < 0:
            self.player_facing_right = False

        if keys[pygame.K_SPACE] and self.on_ground and not self.on_ladder:
            self.vy = self.VY_SAUT

        self.player.x += self.vx
        self.player.y += self.vy

        self.on_ground = False
        if not self.on_ladder:
            for idx, (y_ratio, w_ratio, trou) in enumerate(self.PLATS):
                plat_y = int(self.jeu.bg_height * y_ratio)
                plat_full = pygame.Rect(0, plat_y, int(self.jeu.bg_width * w_ratio), 8)
                gau, dro = int(self.jeu.bg_width * trou[0]), int(self.jeu.bg_width * trou[1])
                segs = [pygame.Rect(0, plat_y, gau, 8),
                        pygame.Rect(dro, plat_y, plat_full.w - dro, 8)]
                for seg in segs:
                    if self.vy >= 0 and self.player.colliderect(seg):
                        self.player.bottom, self.vy, self.on_ground = seg.top, 0, True
                        break

        self.player.clamp_ip(self.jeu.screen.get_rect())
        bas_y = int(self.jeu.bg_height * self.PLATS[0][0]) + 10
        if self.player.top > bas_y:
            from général.etats import recommencement
            self.jeu.changer_etat(recommencement(Donkey_kong_mario, self.jeu))

    def _update_barils(self):
        for b in self.barils:
            if b["chute"]:
                b["rect"].y += self.GRAV_B
                nxt = b["etage"] - 1
                if nxt >= 0:
                    y_nxt = int(self.jeu.bg_height * self.PLATS[nxt][0]) - self.H_B
                    if b["rect"].y >= y_nxt:
                        b["rect"].y, b["etage"], b["chute"] = y_nxt, nxt, False
                        b["dir"] *= -1
            else:
                b["rect"].x += self.VX_B * b["dir"]
                plat_w = int(self.jeu.bg_width * self.PLATS[b["etage"]][1])
                if (b["dir"] == 1 and b["rect"].right >= plat_w) or \
                   (b["dir"] == -1 and b["rect"].left <= 0):
                    b["chute"] = True

        self.barils = [b for b in self.barils if b["rect"].top < self.jeu.bg_height]

    def handle_events(self, event):
        super().handle_events(event)
        if event.type == pygame.USEREVENT + 1:
            r = pygame.Rect(self.thrower.left - self.W_B, self.thrower.y, self.W_B, self.H_B)
            self.barils.append({"rect": r,
                                "etage": len(self.PLATS) - 1,
                                "chute": False,
                                "dir": -1})
            self._plan_next_spawn()
        if event.type == pygame.USEREVENT + 2:
            k = pygame.key.get_pressed()
            self._update_player(k)
            self._update_barils()
            self._check_collisions()

    def _check_collisions(self):
        if any(self.player.colliderect(b["rect"]) for b in self.barils):
            from général.etats import recommencement
            self.jeu.changer_etat(recommencement(Donkey_kong_mario, self.jeu))
        if self.player.colliderect(self.win_zone):
            self.mini_jeu_fini(self.mini_jeu)

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0)) #on ne peut pas importer le draw d'etats car sinon les plateformes se blitent sur le menu
        for y_ratio, w_ratio, trou in self.PLATS:
            y = int(self.jeu.bg_height * y_ratio)
            plat_w = int(self.jeu.bg_width * w_ratio)
            gau = int(self.jeu.bg_width * trou[0])
            dro = int(self.jeu.bg_width * trou[1])
            left_rect = pygame.Rect(0, y, gau, self.img_platform.get_height())
            screen.blit(pygame.transform.scale(self.img_platform, (left_rect.w, left_rect.h)), left_rect)
            right_rect = pygame.Rect(dro, y, plat_w - dro, self.img_platform.get_height())
            screen.blit(pygame.transform.scale(self.img_platform, (right_rect.w, right_rect.h)), right_rect)

        for lad in self.ladders:
            img = pygame.transform.scale(self.img_ladder, (lad.w, lad.h))
            screen.blit(img, lad)

        screen.blit(pygame.transform.scale(self.img_win_zone, (self.win_zone.w, self.win_zone.h)), self.win_zone)


        thrower_img = pygame.transform.flip(self.img_thrower, True, False)
        thrower_img = pygame.transform.scale(thrower_img, (self.thrower.w, self.thrower.h))
        screen.blit(thrower_img, self.thrower)

        player_img = self.img_player
        if not self.player_facing_right:
            player_img = pygame.transform.flip(self.img_player, True, False)
        player_img = pygame.transform.scale(player_img, (self.player.w, self.player.h))
        screen.blit(player_img, self.player)

        for b in self.barils:
            img = pygame.transform.scale(self.img_barrel, (b["rect"].w, b["rect"].h))
            screen.blit(img, b["rect"])
        
        if self.show_menu: #suite du draw de etats
            screen.blit(self.menu, (self.menu_x, self.menu_y))
        if not self.show_menu : 
            screen.blit(self.menu_rond_ic, (self.rect_menu_rond.x, self.rect_menu_rond.y))
        self.montrer_regles_aide(screen,self.last_event,"Donkey_kong_mario")
        
        
