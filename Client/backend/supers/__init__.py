import pygame
import time

from backend.shared import ProjectGlobals


class Ability:
    def __init__(self, texture: pygame.Surface, use_time: float):
        self.texture = texture
        self.time = use_time

        self.last_used = time.time_ns()

        self.available = False


class Character:
    class Type:
        HERO = 0
        HUNTER = 1

    def __init__(self, id: int, username):
        self.id = id
        self.username = username

        self.x = 0
        self.y = 0

        self.interpolation_x = 0
        self.interpolation_y = 0
        self.orig_interpolation_speed = 5
        self.interpolation_speed = self.orig_interpolation_speed

        self.direction = 0

        self.hunted = False
        self.ability = None

    def update(self, dt):
        distance_x = self.x - self.interpolation_x

        if distance_x > 0:
            self.interpolation_x += self.interpolation_speed * dt
            self.direction = 0
        elif distance_x < 0:
            self.interpolation_x -= self.interpolation_speed * dt
            self.direction = 1

        distance_y = self.y - self.interpolation_y

        if distance_y > 0:
            self.interpolation_y += self.interpolation_speed * dt
        elif distance_y < 0:
            self.interpolation_y -= self.interpolation_speed * dt

        diff_x = abs(distance_x)
        diff_y = abs(distance_y)

        if diff_x < self.interpolation_speed * dt:
            self.interpolation_x = self.x

        if diff_y < self.interpolation_speed * dt:
            self.interpolation_y = self.y

        # Lag sync
        if diff_x > self.interpolation_speed * 10 or diff_y > self.interpolation_speed * 10:
            self.sync_pos_with_server()

    def draw(self, screen: pygame.Surface):
        pass

    def sync_pos_with_server(self):
        self.interpolation_x = self.x
        self.interpolation_y = self.y


class Hero(Character):
    def __init__(self, id: int, username):
        super().__init__(id, username)
        self.shield_texture = ProjectGlobals.load_image("effects/hero_shield")
        self.shield_texture_rect = self.shield_texture.get_rect()
        self.shield = False

    def draw(self, screen: pygame.Surface):
        if self.shield:
            self.shield_texture_rect.centerx = self.interpolation_x
            self.shield_texture_rect.centery = self.interpolation_y
            screen.blit(self.shield_texture, self.shield_texture_rect)


class Hunter(Character):
    FREEZE_IMAGES = []

    def __init__(self, id: int, username):
        super().__init__(id, username)

        for i in range(36):
            texture = ProjectGlobals.load_image(f"/effects/freeze/ice_ani_{i}")
            Hunter.FREEZE_IMAGES.append(texture)

        self.freeze_index = 0
        self.freeze = False

    def draw(self, screen: pygame.Surface):
        if self.freeze:
            screen.blit(Hunter.FREEZE_IMAGES[self.freeze_index], (self.interpolation_x, self.interpolation_y - 50))

    def update(self, dt):
        super().update(dt)
        if self.freeze:
            self.freeze_index += 1
            if self.freeze_index >= len(Hunter.FREEZE_IMAGES):
                self.freeze_index = 0
