class Hero:
    def __init__(self, id: int, username):
        self.id = id
        self.username = username

        self.x = 0
        self.y = 0

        self.interpolation_x = 0
        self.interpolation_y = 0

        self.speed = 5

        self.hero_id = 0

    def update(self, dt):
        diff_x = self.x - self.interpolation_x

        if diff_x > 0:
            self.interpolation_x += self.speed * dt
        elif diff_x < 0:
            self.interpolation_x -= self.speed * dt

        diff_y = self.y - self.interpolation_y

        if diff_y > 0:
            self.interpolation_y += self.speed * dt
        elif diff_y < 0:
            self.interpolation_y -= self.speed * dt

        if abs(diff_x) < self.speed * dt:
            self.interpolation_x = self.x

        if abs(diff_y) < self.speed * dt:
            self.interpolation_y = self.y

