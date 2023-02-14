from backend.shared import *


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


import threading


class LoadingScreen(PacketListener):
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

        self.loading_state = ""

        self.loading_cirlce = LoadingCircle()
        self.loading_cirlce.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.loading_cirlce.rect.centery = ProjectGlobals.SCREEN_RECT.centery

        self.set_to_default()

        #ProjectGlobals.SERVER_CONNECTION.paket_listeners.append(self)

    def connect(self):
        try:
            self.loading_state = "Stelle Verbindung mit Server her"
            connected, error = ProjectGlobals.SERVER_CONNECTION.connect()

            if not connected:
                return

            self.loading_state = "Verbunden, warte auf Austausch"
            threading.Thread(target=ProjectGlobals.SERVER_CONNECTION.listen).start()
        except:
            self.set_to_error("Bei der Verbindung zum Server ist ein Problem aufgetreten")

    # Override
    def on_paket_reveived(self, packet_id: int):
        if packet_id == 0:
            ProjectGlobals.SERVER_CONNECTION.state = "Kommunikation mit Server erfolgreich, Anmelden..."
            pass

    def set_to_default(self):
        threading.Thread(target=self.connect).start()

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

        if not ProjectGlobals.SERVER_CONNECTION.error:
            basic_surface = self.font.render(ProjectGlobals.SERVER_CONNECTION.state, True, (255, 255, 255))
            # headline_surface = self.font.render(text, True,
            # (255, 255, 255))

            text_rect = basic_surface.get_rect()
            text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
            text_rect.centery = ProjectGlobals.SCREEN_RECT.centery + 100

            screen.blit(basic_surface, text_rect)

            self.loading_cirlce.draw(screen)
        else:
            error_icon_rect = self.error_icon.get_rect()
            error_icon_rect.center = ProjectGlobals.SCREEN_RECT.center

            screen.blit(self.error_icon, error_icon_rect)

            text = ProjectGlobals.SERVER_CONNECTION.state
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

            # self.reconnect_button.draw(screen)

        # self.button.draw(screen)
