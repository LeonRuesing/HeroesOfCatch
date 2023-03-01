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
        image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "..\\assets\\gfx\\") + image_path + ".png").convert_alpha()
        image = pygame.transform.scale(image, ((ProjectGlobals.SCREEN_RECT.width / 1920) * image.get_rect().width,
                                       (ProjectGlobals.SCREEN_RECT.height / 1080) * image.get_rect().height))
        return image



class HandlerGlobals:
    import backend.networking
    SERVER_CONNECTION = backend.networking.ServerConnection(ProjectGlobals.IP, ProjectGlobals.PORT)

    import backend.handler
    SCREEN_HANDLER = backend.handler.ScreenHandler()
    LOGIN_HANDLER = backend.handler.LoginHandler()
    INGAME_ENTITY_HANDLER = backend.handler.IngameEntityHandler()


class ControllerGlobals:
    import backend.controller
    LOADING_SCREEN_CONTROLLER = backend.controller.LoadingScreenController()
    INGAME_SCREEN_CONTROLLER = backend.controller.IngameScreenController()
