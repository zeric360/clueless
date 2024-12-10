# Player Class
class Player:
    def __init__(self, player_id, name, character):
        self.player_id = player_id      # Unique Player ID
        self.name = name                # Name of Player
        self.character = character      # Character assigned to Player
        self.position = "starting position"            # Position on the board of Player
        self.active = True              # Is the player still in the game
        self.cards = []                 # Cards player is holding
    
    def request_move(self, position):
        # Request to move to a new position 
        self.position = position

    def make_suggestion(self, suggestion):
        # Make a suggestion when it is the player's turn
        pass
    
    def make_accusation(self, accusation):
        # Make an accusation when it is the plater's turn
        pass