class Card:
    def __init__(self, name, card_type):
        self.name = name 
        self.card_type = card_type #character, weapon, room
        

class Character(Card):
    def __init__(self, name):
        super().__init__(name, "character")
    
class Weapon(Card):
    def __init__(self, name):
        super().__init__(name, "weapon")


class Room(Card):
    def __init__(self, name):
        super().__init__(name, "room")

