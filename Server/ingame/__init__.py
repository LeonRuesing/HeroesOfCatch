import random
import threading
import time

from shared import DataHandler, ServerGlobals
from supers import *


class ActiveRound:
    def __init__(self, round: Round):
        self.round = round
        self.running = False
        self.player_characters = list[PlayerCharacter]()

    def start_game(self):
        # Prepare round
        self.create_characters()

        # Send to player
        self.transfer_data_to_players(DataHandler.get_character_transfer_data(self.player_characters))

        # Start game
        self.start_game_loop()

    def create_characters(self):
        for i in self.round.users:
            player_character = PlayerCharacter(i.username, random.randint(0, 300), random.randint(0, 300))
            print(
                f'Character \'{player_character.username}\' erstellt bei x={player_character.x} y={player_character.y}')
            self.player_characters.append(player_character)

    def transfer_data_to_players(self, data):
        for i in ServerGlobals.CONNECTION_LINKS:
            if self.user_present(i.username):
                DataHandler.send_to_socket(i.socket, data)

    def start_game_loop(self):
        self.running = True
        threading.Thread(target=self.game_loop).start()

    def game_loop(self):
        while self.running:
            for i in self.player_characters:
                i.x += 0.5
                i.y += 0
            time.sleep(0.010)
            self.transfer_data_to_players(DataHandler.get_character_pos_update(self.player_characters))

    def user_present(self, username):
        for i in self.round.users:
            #print(i.username, username)
            if username == i.username:
                return True
            #print('False')
        return False
