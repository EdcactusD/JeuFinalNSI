import os 
import pygame
import Etats

class Reglages():
    def __init__(self):
        self.sound_enabled = True 
        self.auto_save_enabled = False  

    def toggle_sound(self):
        """Basculer le son activé et désactivé."""
        self.sound_enabled = not self.sound_enabled

    def command_info(self):
        """Fournir des informations sur les commandes."""
        return "Commandes : [Liste des commandes ici]"

    def enable_auto_save(self):
        """Activer la sauvegarde automatique."""
        self.auto_save_enabled = True

    def disable_auto_save(self):
        """Désactiver la sauvegarde automatique."""
        self.auto_save_enabled = False

    def manual_save(self):
        """Déclencher une sauvegarde manuelle."""
