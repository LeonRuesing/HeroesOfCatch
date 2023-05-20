import os

import pygame

import backend
from backend.shared import ProjectGlobals
from frontend.screens.loading import LoadingScreen
from frontend.screens.lobby import LobbyScreen
from frontend.screens.ingame import IngameScreen
from frontend.screens.lobby.matchmaking import MatchmakingScreen
from frontend.screens.round_result import RoundResultScreen


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
        self.lobby = LobbyScreen()
        self.ingame = IngameScreen()
        self.matchmaking = MatchmakingScreen()
        self.round_result = RoundResultScreen()

        self.last_updated = 0

        ProjectGlobals.RUNNING = True

    def run(self):
        try:
            while ProjectGlobals.RUNNING:  # Hauptprogrammschleife
                delta = self.clock.tick(ProjectGlobals.FPS) / (1000 / ProjectGlobals.FPS)  # Auf mind. 1/60s takten

                self.watch_for_events()
                self.update(delta)
                self.draw(delta)
        except KeyboardInterrupt:
            pygame.quit()

        backend.shared.HandlerGlobals.SERVER_CONNECTION.stop() # Serververbindung abbrechen
        pygame.quit()  # Subssysteme stoppen

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ProjectGlobals.RUNNING = False
            elif event.type == pygame.MOUSEMOTION:
                # self.button_handler.update_button_hover(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                backend.shared.HandlerGlobals.BUTTON_HANDLER.update_hover(pygame.mouse.get_pos())
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen() == 0:
                    self.connecting.set_to_default()
                backend.shared.HandlerGlobals.BUTTON_HANDLER.update_press()
                pass
            elif event.type == pygame.KEYUP:
                if backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen() == 2:
                    backend.shared.HandlerGlobals.MOVEMENT_HANDLER.check_keyboard_input(event, 0)
            elif event.type == pygame.KEYDOWN:
                if backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen() == 2:
                    backend.shared.HandlerGlobals.MOVEMENT_HANDLER.check_keyboard_input(event, 1)

    def get_current_screen(self) -> object:
        screen_id = backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen()

        if screen_id == 0:
            return self.connecting
        elif screen_id == 1:
            return self.lobby
        elif screen_id == 2:
            return self.ingame
        elif screen_id == 3:
            return self.matchmaking
        elif screen_id == 4:
            return self.round_result

    def update(self, dt):
        self.get_current_screen().update(dt)

        switched = backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen() != self.last_updated
        if switched:
            self.get_current_screen().show()
            self.last_updated = backend.shared.HandlerGlobals.SCREEN_HANDLER.get_screen()

        pass

    def draw(self, dt):
        self.get_current_screen().draw(self.screen, dt)

        # Credits
        text = "HeroesOfCatch v.1.0 von Leon Rüsing | " + str(round(self.clock.get_fps())) + " FPS"
        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centerx = backend.shared.ProjectGlobals.SCREEN_RECT.centerx
        text_rect.bottom = backend.shared.ProjectGlobals.SCREEN_RECT.bottom - 5

        #self.screen.blit(basic_surface, text_rect)

        pygame.display.flip()
