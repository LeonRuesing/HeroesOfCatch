class PacketListener:
    def on_packet_reveived(self, packet_id: int, data: list[str]):
        pass


import pygame
import os


class ProjectGlobals:
    SCREEN_RECT = pygame.rect.Rect(0, 0, 800, 800)
    FPS = 60

    IP = "localhost"
    PORT = 56021

    @staticmethod
    def load_image(image_path: str):
        return pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "..\\assets\\gfx\\") + image_path + ".png").convert_alpha()


class HandlerGlobals:
    import backend.networking
    SERVER_CONNECTION = backend.networking.ServerConnection(ProjectGlobals.IP, ProjectGlobals.PORT)

    import backend.handler
    SCREEN_HANDLER = backend.handler.ScreenHandler()
    LOGIN_HANDLER = backend.handler.LoginHandler()


class ControllerGlobals:
    import backend.controller
    LOADING_SCREEN_CONTROLLER = backend.controller.LoadingScreenController()
