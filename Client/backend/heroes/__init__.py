import pygame

from backend.shared import ProjectGlobals
from backend.supers import Hero


class Rageo(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/rageo/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.idle_texture, (self.interpolation_x, self.interpolation_y))


class Digla(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/digla/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.idle_texture, (self.interpolation_x, self.interpolation_y))



class Vaaslen(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/vaaslen/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.idle_texture, (self.interpolation_x, self.interpolation_y))