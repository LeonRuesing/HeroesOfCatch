import random
import threading
import time

from shared import DataHandler, ServerGlobals
from supers import *


class ActiveRoundHandler:
    def __init__(self, active_round: ActiveRound):
        self.running = False
        self.active_round = active_round

    def start_game(self):
        # Prepare round
        self.create_characters()

        # Send to player
        self.transfer_data_to_players(DataHandler.get_character_transfer_data(self.active_round.player_characters))

        # Start game
        self.start_game_loop()

    def create_characters(self):
        for i in self.active_round.round.users:
            player_character = PlayerCharacter(i.username, random.randint(0, 300), random.randint(0, 300), PlayerCharacter.CharacterType.HERO)
            player_character.hero_id = random.randint(0, 2)
            print(
                f'Character \'{player_character.username}\' erstellt bei x={player_character.x} y={player_character.y} cha={player_character.character_type} hero={player_character.hero_id}')
            self.active_round.player_characters.append(player_character)

    def transfer_data_to_players(self, data):
        for i in ServerGlobals.CONNECTION_LINKS:
            if self.active_round.user_present(i.username):
                DataHandler.send_to_socket(i.socket, data)

    def get_online_player_amount(self) -> int:
        players_online = 0
        for i in ServerGlobals.CONNECTION_LINKS:
            if self.active_round.user_present(i.username):
                players_online += 1
        return players_online

    def start_game_loop(self):
        self.running = True
        threading.Thread(target=self.game_loop).start()

    def update(self, delta):
        for i in self.active_round.player_characters:
            if i.movement[0]:
                i.x -= 30 * delta
            elif i.movement[1]:
                i.x += 30 * delta

            if i.movement[2]:
                i.y -= 30 * delta
            elif i.movement[3]:
                i.y += 30 * delta

            if i.x < 0:
                i.x = 960 - 150
            elif i.x > 960 - 150:
                i.x = 0

            if i.y < 0:
                i.y = 540 - 200
            elif i.y > 540 - 200:
                i.y = 0

    def game_loop(self):
        delta = 0
        last_update = 0
        while self.running:
            # Check if players are still there
            if self.get_online_player_amount() == 0:
                self.running = False
                print('[INFO] Eine Runde wurde abgebrochen.')
                return

            time.sleep(1/10)

            last_update_length = time.time() - last_update
            delta = last_update_length / (1/10)
            print(delta)
            self.update(delta)
            self.transfer_data_to_players(DataHandler.get_character_pos_update(self.active_round.player_characters))

            last_update = time.time()