import pygame


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
        self.interpolation_speed = 5

        self.direction = 0

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


class Hunter(Character):
    def __init__(self, id: int, username):
        super().__init__(id, username)
