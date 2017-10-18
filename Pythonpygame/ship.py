import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        super(Ship, self).__init__()

        #Load the ship image
        self.image = pygame.image.load("Untitled1-1.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        #make ship at the bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        #Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """to update ship's postition based n movement flags"""
        #Update ship's center value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.centerx += 1
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx -= 1
            self.center -= self.settings.ship_speed_factor
        #update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
