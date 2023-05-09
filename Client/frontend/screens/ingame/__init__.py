from backend.shared import ProjectGlobals, HandlerGlobals


class IngameScreen:
    def __init__(self):
        self.background = ProjectGlobals.load_image("ingame_grass_background")

    def draw(self, screen, dt):
        screen.blit(self.background, (0, 0))

        for i in HandlerGlobals.INGAME_ENTITY_HANDLER.entities:
            # screen.blit(self.entities[i.hero_id], (i.x, i.y))
            i.draw(screen)
            i.update(dt)

    def update(self, dt):
        pass

    def show(self):
        pass