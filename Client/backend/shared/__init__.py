import pygame
import os

import backend.networking


class PacketListener:
    def on_paket_reveived(self, packet_id: int):
        pass


class ProjectGlobals:
    SCREEN_RECT = pygame.rect.Rect(0, 0, 600, 600)
    FPS = 60

    IP = "localhost"
    PORT = 56021

    @staticmethod
    def load_image(image_path: str):
        return pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                              "..\\assets\\gfx\\") + image_path + ".png").convert_alpha()


class HandlerGlobals:
    SERVER_CONNECTION = backend.networking.ServerConnection(ProjectGlobals.IP, ProjectGlobals.PORT)
