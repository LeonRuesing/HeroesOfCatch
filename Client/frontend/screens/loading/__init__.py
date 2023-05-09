import threading
from backend.shared import ControllerGlobals, ProjectGlobals
from backend.shared import HandlerGlobals
from foundation import pygame

class LoadingCircle:
    def __init__(self):
        self.loading_cirlce = ProjectGlobals.load_image("loading_circle")
        self.loading_cirlce = pygame.transform.scale(self.loading_cirlce, (100, 100))
        self.image = self.loading_cirlce
        self.rect = self.loading_cirlce.get_rect()
        self.angle = 0

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.loading_cirlce, self.angle)

        rect = self.image.get_rect()
        rect.center = self.rect.center
        self.rect = rect

    def draw(self, screen, dt):
        self.angle += 4
        self.rotate_image()

        screen.blit(self.image, self.rect)


class LoadingPointAnimation():
    def __init__(self, time: int):
        self.start_time = pygame.time.get_ticks()
        self.time = time
        self.loading_points_index = 0

    def get_current_step(self) -> str:
        points = ""
        for i in range(self.loading_points_index):
            points += "."
        return points

    def check_if_next_step(self):
        now = pygame.time.get_ticks() - self.start_time

        if now >= self.time:
            self.loading_points_index += 1
            self.start_time = pygame.time.get_ticks()

            if self.loading_points_index > 3:
                self.loading_points_index = 0


class LoadingScreen:
    def __init__(self):
        self.small_font = pygame.font.Font(pygame.font.get_default_font(), 8)
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.headline_font = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.background = pygame.transform.scale(ProjectGlobals.load_image("lobby_background"),
                                                 ProjectGlobals.SCREEN_RECT.size)
        self.error_icon = ProjectGlobals.load_image("error_icon")
        self.stateTextBackground = ProjectGlobals.load_image("lobby_state_text_background")
        self.stateTextBackground = pygame.transform.scale(self.stateTextBackground, (500, 100))

        self.error_active = False
        self.error_message = None

        self.loading_cirlce = LoadingCircle()
        self.loading_cirlce.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.loading_cirlce.rect.centery = ProjectGlobals.SCREEN_RECT.centery

        # mains.Main.game.button_handler.button_list.append(self.button)
        # mains.Main.game.button_list.append(self.reconnect_button)

        self.set_to_default()
        # self.set_to_error("Server konnte nicht erreicht werden!")

    def set_to_default(self):
        threading.Thread(target=ControllerGlobals.LOADING_SCREEN_CONTROLLER.connect).start()

    def update(self, dt):
        pass

    def draw(self, screen: pygame.Surface, dt):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        if not HandlerGlobals.SERVER_CONNECTION.error:
            basic_surface = self.font.render(HandlerGlobals.SERVER_CONNECTION.state, True, (255, 255, 255))
            # headline_surface = self.font.render(text, True,
            # (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 100

            screen.blit(basic_surface, text_rect)

            self.loading_cirlce.draw(screen, dt)
        else:
            error_icon_rect = self.error_icon.get_rect()
            error_icon_rect.center = ProjectGlobals.SCREEN_RECT.center

            screen.blit(self.error_icon, error_icon_rect)

            text = HandlerGlobals.SERVER_CONNECTION.state
            basic_surface = self.font.render(text, True, (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 50

            screen.blit(basic_surface, text_rect)

            text = "Klicken Sie auf den Bildschirm, um neu zu verbinden!"
            basic_surface = self.font.render(text, True, (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 70

            screen.blit(basic_surface, text_rect)

    def show(self):
        pass
