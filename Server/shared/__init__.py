from supers import *


class ServerGlobals:
    CONNECTIONS = list[ClientConnection]()
    CONNECTION_LINKS = list[UserConnectionLink]()
    PORT = 56021


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
            data += ';' + str(i) + ';' + p.username + ';' + str(p.x) + ';' + str(p.y)

        print('Tranfer', data)
        return data.encode()

    @staticmethod
    def get_character_pos_update(player_character_list: list[PlayerCharacter]):
        data = f'{3}'

        for i in range(len(player_character_list)):
            p = player_character_list[i]
            data += ';' + str(i) + ';' + str(p.x) + ';' + str(p.y)

        return data.encode()