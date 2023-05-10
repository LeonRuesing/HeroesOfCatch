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
        hunter_player = random.randint(0, len(self.active_round.round.users) - 1)
        for i in range(len(self.active_round.round.users)):
            character_type = PlayerCharacter.CharacterType.HERO

            if hunter_player == i:
                character_type = PlayerCharacter.CharacterType.HUNTER

            i = self.active_round.round.users[i]
            player_character = PlayerCharacter(i.username, random.randint(0, 300), random.randint(0, 300), character_type)
            #player_character.hero_id = random.randint(0, 1)
            player_character.hero_id = 0
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

    def freeze_hunter(self):
        for i in self.active_round.player_characters:
            if i.character_type == PlayerCharacter.CharacterType.HUNTER:
                i.current_effect = Effect('Freeze', 4)
                i.effective_speed = 1.5
                i.end_of_effect = time.time_ns() + (4 * 1_000_000_000) # 4Sec.
                self.transfer_data_to_players(DataHandler.get_freeze_hunter(i))

    def unfreeze_hunter(self):
        for i in self.active_round.player_characters:
            if i.character_type == PlayerCharacter.CharacterType.HUNTER:
                i.effective_speed = i.speed

    def hunt_hero(self, character: PlayerCharacter):
        character.hunted = True
        self.transfer_data_to_players(DataHandler.get_hero_hunt(character, self.active_round.player_characters))
        print(f'Hunted {character.username}')

    def clear_effect(self, character: PlayerCharacter):
        character.clear_effect()
        self.transfer_data_to_players(DataHandler.get_effect_clear(character, self.active_round.player_characters))

    def update(self, delta):
        for i in self.active_round.player_characters:

            if i.hunted:
                continue

            if i.ability_requested:
                if i.character_type == PlayerCharacter.CharacterType.HERO:
                    if i.hero_id == 0:
                        self.freeze_hunter()
                        i.ability_requested = False
                if i.character_type == PlayerCharacter.CharacterType.HUNTER:
                    hunt_range = 50
                    for y in self.active_round.player_characters:
                        if y.character_type == PlayerCharacter.CharacterType.HERO and not y.hunted:
                            if i != y:
                                if abs(i.x - y.x) <= hunt_range and abs(i.y - y.y) <= hunt_range:
                                    self.hunt_hero(y)
                    i.ability_requested = False

            if i.current_effect is not None:
                if i.current_effect.effect_done():
                    self.clear_effect(i)
                    print('Effect cleared')


            speed = i.effective_speed

            if i.movement[0]:
                i.x -= speed * delta
            elif i.movement[1]:
                i.x += speed * delta

            if i.movement[2]:
                i.y -= speed * delta
            elif i.movement[3]:
                i.y += speed * delta

            if i.x < 0:
                i.x = 960
            elif i.x > 960:
                i.x = 0

            if i.y < 0:
                i.y = 540
            elif i.y > 540:
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

            time.sleep(1/60)

            last_update_length = time.time() - last_update
            delta = last_update_length / (1/60)
            self.update(delta)
            self.transfer_data_to_players(DataHandler.get_character_pos_update(self.active_round.player_characters))

            last_update = time.time()
