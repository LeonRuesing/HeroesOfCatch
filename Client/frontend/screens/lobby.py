from backend.shared import ProjectGlobals


class LobbyScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background").convert()
        pass

    def draw(self, screen):
        screen.fill((100, 100, 100), ProjectGlobals.SCREEN_RECT)
        pass

    def update(self):
        pass