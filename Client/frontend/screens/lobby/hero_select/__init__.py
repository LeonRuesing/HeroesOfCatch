import pygame

from backend.shared import ProjectGlobals, HandlerGlobals
from frontend.supers import TextButton


class HeroSelectScreen:

    def __init__(self):
        self.background = ProjectGlobals.load_image("lobby_background")

        self.font = pygame.font.Font(pygame.font.get_default_font(), 28)
        self.sub_font = pygame.font.Font(pygame.font.get_default_font(), 16)

        texture = ProjectGlobals.load_image("navigation_button_right")
        texture = pygame.transform.flip(texture, True, False)
        self.navigation_left_button_rect = texture.get_rect()
        self.navigation_left_button_rect.left = ProjectGlobals.SCREEN_RECT.left + 50
        self.navigation_left_button_rect.centery = ProjectGlobals.SCREEN_RECT.centery
        self.navigation_left_button = TextButton(texture, self.navigation_left_button_rect, '')

        texture = ProjectGlobals.load_image("navigation_button_right")
        self.navigation_right_button_rect = texture.get_rect()
        self.navigation_right_button_rect.right = ProjectGlobals.SCREEN_RECT.right - 50
        self.navigation_right_button_rect.centery = ProjectGlobals.SCREEN_RECT.centery
        self.navigation_right_button = TextButton(texture, self.navigation_right_button_rect, '')

        texture = ProjectGlobals.load_image("button_green")
        self.select_button_rect = texture.get_rect()
        self.select_button_rect.bottom = ProjectGlobals.SCREEN_RECT.bottom - 25
        self.select_button_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.select_button = TextButton(texture, self.select_button_rect, "Auswählen")

        self.selected_id = 1

    def draw(self, screen, dt):
        screen.blit(self.background, (0, 0))

        current_hero = HandlerGlobals.HERO_HANDLER.build_hero(self.selected_id, -1, None)
        current_hero.x = ProjectGlobals.SCREEN_RECT.width / 2
        current_hero.y = ProjectGlobals.SCREEN_RECT.height / 2
        current_hero.sync_pos_with_server()

        hero_name = current_hero.__class__.__name__

        font_surface = self.font.render(hero_name, True, (255, 255, 255))

        font_rect = font_surface.get_rect()
        font_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        font_rect.top = ProjectGlobals.SCREEN_RECT.top + 50

        screen.blit(font_surface, font_rect)

        if current_hero.description is not None:
            font_surface = self.sub_font.render('Beschreibung: ' + current_hero.description, True, (255, 255, 255))

            font_rect = font_surface.get_rect()
            font_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            font_rect.top = ProjectGlobals.SCREEN_RECT.top + 90

            screen.blit(font_surface, font_rect)

        current_hero.draw(screen)

        self.select_button.render(screen)
        self.navigation_left_button.render(screen)
        self.navigation_right_button.render(screen)

    def update(self, dt):
        self.select_button.update(dt)
        self.navigation_left_button.update(dt)
        self.navigation_right_button.update(dt)

        if self.select_button.pressed:
            HandlerGlobals.HERO_HANDLER.selected_hero = self.selected_id
            HandlerGlobals.SCREEN_HANDLER.set_screen(1)
            self.select_button.pressed = False

        if self.navigation_left_button.pressed:
            self.navigate_left()
            self.navigation_left_button.pressed = False

        if self.navigation_right_button.pressed:
            self.navigate_right()
            self.navigation_right_button.pressed = False

    def show(self):
        HandlerGlobals.BUTTON_HANDLER.active_buttons.clear()
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.select_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.navigation_left_button)
        HandlerGlobals.BUTTON_HANDLER.active_buttons.append(self.navigation_right_button)

    def navigate_left(self):
        self.selected_id -= 1

        if self.selected_id < 0:
            self.selected_id = len(HandlerGlobals.HERO_HANDLER.heroes) - 1

    def navigate_right(self):
        self.selected_id += 1

        if self.selected_id > len(HandlerGlobals.HERO_HANDLER.heroes) - 1:
            self.selected_id = 0