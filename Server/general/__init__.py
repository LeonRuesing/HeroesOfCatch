from shared import DataHandler, ServerGlobals
from supers import UserConnectionLink, Round, ActiveRound


class MatchmakingHandler:
    WAITING_PLAYERS = list[UserConnectionLink]()
    NEEDED_PLAYERS = 3

    @staticmethod
    def add_player(user: UserConnectionLink):
        if MatchmakingHandler.WAITING_PLAYERS.__contains__(user):
            return

        MatchmakingHandler.WAITING_PLAYERS.append(user)
        print(f'[MatchmakingHandler] {user.username} nun in Warteschlange!')

        if len(MatchmakingHandler.WAITING_PLAYERS) >= MatchmakingHandler.NEEDED_PLAYERS:
            MatchmakingHandler.form_new_round()
        else:
            DataHandler.send_to_socket(user.socket, DataHandler.get_queue_enter(MatchmakingHandler.NEEDED_PLAYERS))
            MatchmakingHandler.send_info_to_all()

    @staticmethod
    def remove_player(user: UserConnectionLink):
        target_user = None
        for i in MatchmakingHandler.WAITING_PLAYERS:
            if i.username == user.username:
                target_user = i
                break

        if target_user is None:
            return

        MatchmakingHandler.WAITING_PLAYERS.remove(user)
        MatchmakingHandler.send_info_to_all()
        print(f'[MatchmakingHandler] {user.username} von Warteschlange entfernt!')
        DataHandler.send_to_socket(user.socket, DataHandler.get_queue_leave())

    @staticmethod
    def send_info_to_all():
        for i in MatchmakingHandler.WAITING_PLAYERS:
            DataHandler.send_to_socket(i.socket, DataHandler.get_queue_update(len(MatchmakingHandler.WAITING_PLAYERS)))

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
