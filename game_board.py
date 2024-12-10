class gameBoard:
     #attributes
     playerIDs = [] # player IDs in current game
     player_location_dict = dict() # where each player currently is
     rooms = [ #all the rooms on the board
         "Study",  
         "Hall",
         "Lounge", 
         "Library", 
         "Billard Room", 
         "Dining Room", 
         "Conservatory", 
         "Ballroom", 
         "Kitchen"
     ] 

     hallways = [ #all the hallways on the board
          "Study_Hall",
          "Hall_Lounge",
          "Library_Billiard",
          "Billiard_Dining",
          "Conservatory_Ballroom",
          "Ballroom_Kitchen",
          "Study_Library",
          "Library_Conservatory",
          "Hall_Billiard",
          "Billiard_Ballroom",
          "Lounge_Dining",
          "Dining_Kitchen"
     ] 
     

     # methods
     def __init__(self, playerIDs):
          self.playerIDs = playerIDs
          self.player_location_dict = self.initialize_dict(self.playerIDs)

     def initialize_dict(self, playerIDs):
          player_location_dict = dict()
          #print(playerIDs)
          for player in playerIDs:
               #print(player)
               player_location_dict[player] = "Starting Position"
          #print("printing player location dict")
          #print(player_location_dict)
          return player_location_dict
     
     def update(self, playerID, loc):
          self.player_location_dict[playerID] = loc

     def print_board(self):
          for player, loc in self.player_location_dict.items():
               print(f"{player} is located in {loc}")