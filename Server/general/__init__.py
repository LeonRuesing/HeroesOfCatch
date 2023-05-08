from shared import DataHandler, ServerGlobals
from supers import UserConnectionLink, Round, ActiveRound


class MatchmakingHandler:
    WAITING_PLAYERS = list[UserConnectionLink]()
    NEEDED_PLAYERS = 2
    @staticmethod
    def add_player(user: UserConnectionLink):
        if MatchmakingHandler.WAITING_PLAYERS.__contains__(user):
            return

        MatchmakingHandler.WAITING_PLAYERS.append(user)

        DataHandler.send_to_socket(user.socket, DataHandler.get_queue_update(len(MatchmakingHandler.WAITING_PLAYERS), MatchmakingHandler.NEEDED_PLAYERS))

        if len(MatchmakingHandler.WAITING_PLAYERS) >= MatchmakingHandler.NEEDED_PLAYERS:
            MatchmakingHandler.form_new_round()

    @staticmethod
    def remove_player(user: UserConnectionLink):
        if not MatchmakingHandler.WAITING_PLAYERS.__contains__(user):
            return

        MatchmakingHandler.WAITING_PLAYERS.remove(user)
        DataHandler.send_to_socket(user.socket, DataHandler.get_queue_leave())

    @staticmethod
    def form_new_round():
        round = Round()
        round.users = MatchmakingHandler.WAITING_PLAYERS.copy()

        active_round = ActiveRound(round)
        ServerGlobals.ACTIVE_ROUNDS.append(active_round)

        from ingame import ActiveRoundHandler
        active_round_handler = ActiveRoundHandler(active_round)
        active_round_handler.start_game()

        MatchmakingHandler.WAITING_PLAYERS.clear()