import pygame

from backend.shared import ProjectGlobals
from backend.supers import Hero, Hunter


class Bob(Hunter):
    WALKING_SPRITES = []
    IDLE_SPRITES = []

    def __init__(self, id: int, username):
        super().__init__(id, username)

        self.interpolation_speed = 5.2

        for i in range(37):
            texture = ProjectGlobals.load_image(f"/hunter/walking/walking_{i}")
            texture = pygame.transform.scale(texture, (texture.get_width() * 3, texture.get_height() * 3))
            Bob.WALKING_SPRITES.append(texture)

        for i in range(37):
            texture = ProjectGlobals.load_image(f"/hunter/idle/idle_{i}")
            texture = pygame.transform.scale(texture, (texture.get_width() * 3, texture.get_height() * 3))
            Bob.IDLE_SPRITES.append(texture)

        self.current_walking_index = 0
        self.current_idle_index = 0
        self.walking = False

    def update(self, dt):
        if self.walking:
            self.current_walking_index += 1
            if self.current_walking_index >= len(Bob.WALKING_SPRITES):
                self.current_walking_index = 0
        else:
            self.current_idle_index += 1
            if self.current_idle_index >= len(Bob.IDLE_SPRITES):
                self.current_idle_index = 0

        self.walking = self.interpolation_x != self.x or self.interpolation_y != self.y

        super().update(dt)

    def draw(self, screen: pygame.Surface):
        if self.walking:
            texture = Bob.WALKING_SPRITES[self.current_walking_index]
        else:
            texture = Bob.IDLE_SPRITES[self.current_idle_index]

        if self.direction == 1:
            texture = pygame.transform.flip(texture, True, False)

        screen.blit(texture,
                    (self.interpolation_x - texture.get_width() / 2, self.interpolation_y - texture.get_height() / 2))
        screen.fill((255, 0, 0), (self.interpolation_x, self.interpolation_y, 2, 2))

class Rageo(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/rageo/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        texture = self.idle_texture
        if self.direction == 1:
            texture = pygame.transform.flip(texture, True, False)
        screen.blit(texture, (self.interpolation_x + texture.get_width() / 2, self.interpolation_y + texture.get_height() / 2))


class Digla(Hero):

    IDLE_SPRITES = []
    WALKING_SPRITES = []

    def __init__(self, id: int, username):
        super().__init__(id, username)

        for i in range(12):
            Digla.IDLE_SPRITES.append(ProjectGlobals.load_image(f"/heroes/digla/idle/idle_{i}"))

        for i in range(37):
            Digla.WALKING_SPRITES.append(ProjectGlobals.load_image(f"/heroes/digla/walking/walking_{i}"))

        self.current_walking_index = 0
        self.current_idle_index = 0
        self.walking = False


    def update(self, dt):
        if self.walking:
            self.current_walking_index += 1
            if self.current_walking_index >= len(Digla.WALKING_SPRITES):
                self.current_walking_index = 0
        else:
            self.current_idle_index += 1
            if self.current_idle_index >= len(Digla.IDLE_SPRITES):
                self.current_idle_index = 0

        self.walking = self.interpolation_x != self.x or self.interpolation_y != self.y

        super().update(dt)

    def draw(self, screen: pygame.Surface):
        if self.walking:
            texture = Digla.WALKING_SPRITES[self.current_walking_index]
        else:
            texture = Digla.IDLE_SPRITES[self.current_idle_index]

        if self.direction == 1:
            texture = pygame.transform.flip(texture, True, False)

        screen.blit(texture, (self.interpolation_x - texture.get_width() / 2, self.interpolation_y - texture.get_height() / 2))
        screen.fill((255, 0, 0), (self.interpolation_x, self.interpolation_y, 2, 2))



class Vaaslen(Hero):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.idle_texture = ProjectGlobals.load_image("/heroes/vaaslen/idle")

    def update(self, dt):
        super().update(dt)

    def draw(self, screen: pygame.Surface):
        texture = self.idle_texture
        if self.direction == 1:
            texture = pygame.transform.flip(texture, True, False)

        screen.blit(texture, (self.interpolation_x + texture.get_width() / 2, self.interpolation_y + texture.get_height() / 2))