from foundation import pygame

class Button:
    def __init__(self, image_name: str, text: str):
        self.button_id = image_name
        self.orginal_image = pygame.image.load(image_name + ".png")
        self.rect = self.orginal_image.get_rect()
        self.hovered_image = pygame.transform.scale(pygame.image.load("button_hover.png").convert_alpha(), self.rect.size)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.text = text
        self.color = (255, 255, 255)
        self.hovered = False

    def draw(self, screen: pygame.Surface):
        screen.blit(self.orginal_image, self.rect)
        if self.hovered:
            screen.blit(self.hovered_image, self.rect)

        surface = self.font.render(self.text, True, self.color)

        text_rect = surface.get_rect()
        text_rect.center = self.rect.center

        screen.blit(surface, text_rect)
