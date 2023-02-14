import os
import pygame

# class ButtonHandler:
#   def __init__(self):
#      self.button_list = []

# def update_button_hover(self, mouseX: int, mouseY: int):
#    for button in self.button_list:
#       if button.rect.left <= mouseX <= button.rect.right and button.rect.top <= mouseY <= button.rect.bottom:
#          button.hovered = True
#     else:
#        button.hovered = False

# def update_button_click(self):
#   for button in self.button_list:
#      if button.hovered:
#         return


from networking import ServerConnection


class PacketListener:
    def on_paket_reveived(self, packet_id: int):
        pass


class ProjectGlobals:
    SCREEN_RECT = pygame.rect.Rect(0, 0, 600, 600)
    FPS = 60

    IP = "localhost"
    PORT = 56021

    SERVER_CONNECTION = ServerConnection(IP, PORT)

    #    BUTTON_HANLDER = ButtonHandler()

    @staticmethod
    def load_image(image_path: str):
        return pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "assets\\gfx\\") + image_path + ".png").convert_alpha()


class Button:
    def __init__(self, image_name: str, text: str):
        self.button_id = image_name
        self.orginal_image = pygame.image.load(image_name + ".png")
        self.rect = self.orginal_image.get_rect()
        self.hovered_image = pygame.transform.scale(pygame.image.load("button_hover.png").convert_alpha(),
                                                    self.rect.size)
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

        self.button = Button("close_button", text=None)
        self.button.rect.right = ProjectGlobals.SCREEN_RECT.right

        self.reconnect_button = Button("button_reconnect", text="Neu verbinden")
        self.reconnect_button.rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        self.reconnect_button.rect.centery = ProjectGlobals.SCREEN_RECT.centery + 100

        # mains.Main.game.button_handler.button_list.append(self.button)
        # mains.Main.game.button_list.append(self.reconnect_button)

        self.set_to_default()
        # self.set_to_error("Server konnte nicht erreicht werden!")

        ProjectGlobals.SERVER_CONNECTION.paket_listeners.append(self)

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


class IngameScreen(PacketListener):
    def __init__(self):
        self.background = ProjectGlobals.load_image("ingame_grass_background")

    def draw(self, screen: pygame.Surface):
        screen.blit(self.background, ProjectGlobals.SCREEN_RECT)

    def update(self):
        pass


class Game:
    def __init__(self):
        # self.globals = foundation.Globals()

        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Fensterkoordinaten
        pygame.init()  # Subsysteme starten

        pygame.display.set_caption("HeroesOfCatch")
        self.screen = pygame.display.set_mode(ProjectGlobals.SCREEN_RECT.size)  # , pygame.NOFRAME
        self.clock = pygame.time.Clock()  # Taktgeber

        self.font = pygame.font.Font(pygame.font.get_default_font(), 14)

        self.connecting = LoadingScreen()
        self.ingame = IngameScreen()
        self.current_screen = 0

        # self.button_handler = ButtonHandler()

        self.running = True  # Flagvariable

    def run(self):
        try:
            while self.running:  # Hauptprogrammschleife
                self.clock.tick(ProjectGlobals.FPS)  # Auf mind. 1/60s takten

                self.watch_for_events()
                self.update()
                self.draw()
        except KeyboardInterrupt:
            pygame.quit()

        ProjectGlobals.SERVER_CONNECTION.stop()
        pygame.quit()  # Subssysteme stoppen

    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # self.button_handler.update_button_hover(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                # self.button_handler.update_button_click()
                self.connecting.set_to_default()
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # if not self.connecting.error_active:
                    #   self.connecting.set_to_error("Der Verbindungsaufbau zum Server ist fehlgeschlagen!")
                    # else:
                    #   self.connecting.set_to_default()
                    pass

    def get_current_screen(self) -> object:
        if self.current_screen == 0:
            return self.connecting
        elif self.current_screen == 1:
            return self.ingame

    def update(self):
        self.get_current_screen().update()
        pass

    def draw(self):
        self.get_current_screen().draw(self.screen)

        # Credits
        text = "HeroesOfCatch v.1.0 von Leon Rüsing"

        basic_surface = self.font.render(text, True, (255, 255, 255))

        text_rect = basic_surface.get_rect()
        text_rect.centerx = ProjectGlobals.SCREEN_RECT.centerx
        text_rect.bottom = ProjectGlobals.SCREEN_RECT.bottom - 5

        self.screen.blit(basic_surface, text_rect)

        pygame.display.flip()
