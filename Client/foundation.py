import os
import pygame

import backend
import frontend.screens
from backend.handler import ScreenHandler
from frontend.screens import LoadingScreen
from frontend.screens.lobby import LobbyScreen
from frontend.screens.lobby import IngameScreen


class Game:
    def __init__(self):
        # self.shared = foundation.Globals()

        backend.shared.ProjectGlobals.SCREEN_RECT.size = (960, 540)

        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Fensterkoordinaten
        pygame.init()  # Subsysteme starten

        pygame.display.set_caption("HeroesOfCatch")
        self.screen = pygame.display.set_mode(backend.shared.ProjectGlobals.SCREEN_RECT.size)  # ,
        self.clock = pygame.time.Clock()  # Taktgeber

        backend.shared.ProjectGlobals.SCREEN_RECT.size = (self.screen.get_width(), self.screen.get_height())

        self.font = pygame.font.Font(pygame.font.get_default_font(), 14)

        self.connecting = LoadingScreen()
        self.current_screen = 0

        self.running = True  # Flagvariable

    def run(self):
        try:
            while self.running:  # Hauptprogrammschleife
                self.clock.tick(backend.shared.ProjectGlobals.FPS)  # Auf mind. 1/60s takten

                self.watch_for_events()
                self.update()
                self.draw()
        except KeyboardInterrupt:
            pygame.quit()

        backend.shared.HandlerGlobals.SERVER_CONNECTION.stop() # Serververbindung abbrechen
        pygame.quit()  # Subssysteme stoppen

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # self.button_handler.update_button_hover(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if backend.shared.HandlerGlobals.SCREEN_HANDLER.current_screen == 0:
                    self.connecting.set_to_default()
                pass
            elif event.type == pygame.KEYUP:
                backend.shared.HandlerGlobals.MOVEMENT_HANDLER.check_keyboard_input(event, 0)
            elif event.type == pygame.KEYDOWN:
                backend.shared.HandlerGlobals.MOVEMENT_HANDLER.check_keyboard_input(event, 1)

    def get_current_screen(self) -> object:
        screen_id = backend.shared.HandlerGlobals.SCREEN_HANDLER.current_screen
        if screen_id == 0:
            return self.connecting
        elif screen_id == 1:
            return LobbyScreen()
        elif screen_id == 2:
            return IngameScreen()

    def update(self):
        self.get_current_screen().update()
        pass

    def draw(self):
        self.get_current_screen().draw(self.screen)

        # Credits
        text = "HeroesOfCatch v.1.0 von Leon Rüsing"

        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centerx = backend.shared.ProjectGlobals.SCREEN_RECT.centerx
        text_rect.bottom = backend.shared.ProjectGlobals.SCREEN_RECT.bottom - 5

        self.screen.blit(basic_surface, text_rect)

        pygame.display.flip()
