import pygame


class TextButton:
    def __init__(self, texture: pygame.Surface, rect: pygame.rect.Rect, text: str):
        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)
        self.texture = texture
        from backend.shared import ProjectGlobals
        self.hover_layer = ProjectGlobals.load_image("button_hover")
        self.hover = False
        self.rect = rect
        self.text = text

        self.pressed = False

    def render(self, screen: pygame.Surface):
        screen.blit(self.texture, self.rect)

        basic_surface = self.font.render(self.text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.center = self.rect.center

        screen.blit(basic_surface, text_rect)

        if self.hover:
            screen.blit(self.hover_layer, self.rect)

    def update(self, dt):
        pass