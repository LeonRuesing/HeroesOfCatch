import threading
from foundation import ProjectGlobals
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

    def draw(self, screen):
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

        self.background = ProjectGlobals.load_image("lobby_background")
        self.stateTextBackground = ProjectGlobals.load_image("lobby_state_text_background")
        self.stateTextBackground = pygame.transform.scale(self.stateTextBackground, (500, 100))
        self.loading_points_animation = LoadingPointAnimation(200)

        self.error_active = False
        self.error_message = None

        self.loading_state = None

        self.loading_cirlce = LoadingCircle()
        self.loading_cirlce.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.loading_cirlce.rect.centery = ProjectGlobals.SCREEN_RECT.centery

        #self.button = utils.Button("close_button", text=None)
        #self.button.rect.right = ProjectGlobals.SCREEN_RECT.right

        #self.reconnect_button = utils.Button("button_reconnect", text="Neu verbinden")
        #self.reconnect_button.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        #self.reconnect_button.rect.centery = ProjectGlobals.SCREEN_RECT.centery + 75

        #mains.Main.game.button_handler.button_list.append(self.button)
        #mains.Main.game.button_list.append(self.reconnect_button)

        self.set_to_default()
        # self.set_to_error("Server konnte nicht erreicht werden!")

    def connect(self):
        self.loading_state = "Stelle Verbindung mit Server her"
        connected, error = ProjectGlobals.SERVER_CONNECTION.connect()
        self.loading_state = "Verbunden, warte auf Austausch"
        threading.Thread(target=ProjectGlobals.SERVER_CONNECTION.listen).start()

        if not connected:
            self.set_to_error("Der Verbindungsaufbau zum Server schlug fehl!")
        else:
            self.loading_state = ""

    def set_to_default(self):
        self.error_active = False
        threading.Thread(target=self.connect).start()

    def set_to_error(self, error: str):
        self.error_message = error
        self.error_active = True

    def update(self):
        self.loading_points_animation.check_if_next_step()
        pass

    def draw(self, screen: pygame.Surface):
        # screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        screen.fill(color=(0, 0, 0), rect=ProjectGlobals.SCREEN_RECT)

        if not self.error_active:
            basic_surface = self.font.render(self.loading_state + ' ...', True, (255, 255, 255))
            headline_surface = self.font.render(self.loading_state + ' ' + self.loading_points_animation.get_current_step(), True,
                                                (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 100

            screen.blit(headline_surface, text_rect)

            self.loading_cirlce.draw(screen)
        else:
            rect = self.stateTextBackground.get_rect()
            rect.center = ProjectGlobals.SCREEN_RECT.center
            # screen.blit(self.stateTextBackground, rect)

            # Headline
            text = "Etwas ist schiefgelaufen!"

            basic_surface = self.headline_font.render(text, True, (200, 0, 0))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery - 10

            screen.blit(basic_surface, text_rect)

            # Error text
            text = self.error_message
            basic_surface = self.font.render(text, True, (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 10

            screen.blit(basic_surface, text_rect)

            self.reconnect_button.draw(screen)

        self.button.draw(screen)


class LobbyScreen:
    def __init__(self):
        self.background = pygame.image.load("lobby_background.png").convert()
        pass

    def draw(self, screen):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)
