from supers import *


class ServerGlobals:
    CONNECTIONS = list[ClientConnection]()
    CONNECTION_LINKS = list[UserConnectionLink]()
    PORT = 56021

    ACTIVE_ROUNDS = list[ActiveRound]()

    @staticmethod
    def get_connection_link_by_socket(client_connection: ClientConnection) -> UserConnectionLink:
        for i in ServerGlobals.CONNECTION_LINKS:
            if i.socket == client_connection.socket:
                return i

    @staticmethod
    def get_username_by_socket(socket: socket.socket) -> UserConnectionLink:
        for i in ServerGlobals.CONNECTION_LINKS:
            if i.socket == socket:
                return i

    @staticmethod
    def get_round_by_username(username: str) -> ActiveRound:
        for i in ServerGlobals.ACTIVE_ROUNDS:
            if i.user_present(username):
                return i
        return None

class DataHandler:
    def __init__(self):
        pass

    @staticmethod
    def send_to_socket(socket: socket.socket, data: bytes):
        try:
            socket.sendall(data)
        except:
            socket.close()

    @staticmethod
    def send_to_all(data: bytes):
        for connection in ServerGlobals.CONNECTIONS:
            DataHandler.send_to_socket(connection.socket, data)

    @staticmethod
    def get_character_transfer_data(player_character_list: list[PlayerCharacter]) -> bytes:
        data = f'{2}'

        for i in range(len(player_character_list)):
            p = player_character_list[i]
            data += ';' + str(i) + ';' + p.username + ';' + str(p.x) + ';' + str(p.y) + ';' + str(p.character_type)

            if p.character_type == PlayerCharacter.CharacterType.HERO:
                data += ';' + str(p.hero_id)

        print('Tranfer', data)
        return data.encode()

    @staticmethod
    def get_character_pos_update(player_character_list: list[PlayerCharacter]):
        data = f'{3}'

        for i in range(len(player_character_list)):
            p = player_character_list[i]
            data += ';' + str(i) + ';' + str(p.x) + ';' + str(p.y)

        return data.encode()