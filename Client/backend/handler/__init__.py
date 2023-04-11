from backend.supers import Hero


class ScreenHandler:
    def __init__(self):
        self.current_screen = 0


class LoginHandler:
    def __init__(self):
        self.username = None


class IngameEntityHandler:
    def __init__(self):
        self.entities = list[Hero]()

    def get_entity_by_id(self, id) -> Hero:
        for i in self.entities:
            if i.id == id:
                return i
        return None

