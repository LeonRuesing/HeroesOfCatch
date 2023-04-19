import socket


class DisconnectListener:
    def on_disconnect(self, client_connection: object):
        pass


class ClientConnection:
    def __init__(self, client_socket: socket.socket, client_ip: str, disconnect_listener: DisconnectListener):
        self.socket = client_socket
        self.client_ip = client_ip
        self.disconnect_listener = disconnect_listener


class UserConnectionLink:
    def __init__(self, socket: socket.socket, username: str):
        self.socket = socket
        self.username = username


class PlayerCharacter:

    class CharacterType:
        HERO = 0
        HUNTER = 1

    def __init__(self, username, x, y, character_type):
        self.username = username
        self.x = x
        self.y = y
        self.hero_id = 0
        self.character_type = character_type
        self.movement = [0, 0, 0, 0]

class Round:
    def __init__(self):
        self.users: list[UserConnectionLink] = []


class ActiveRound:
    def __init__(self, round: Round):
        self.round = round
        self.running = False
        self.player_characters = list[PlayerCharacter]()

    def user_present(self, username):
        for i in self.round.users:
            if username == i.username:
                return True
        return False

    def update_movement_for_user(self, username, movement):
        character = self.get_character_by_username(username)
        if character is not None:
            character.movement = movement

    def get_character_by_username(self, username):
        for i in self.player_characters:
            if i.username == username:
                return i
        return None
