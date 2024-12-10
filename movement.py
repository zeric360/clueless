## Movement Class
import game_board
from game_board import gameBoard
from player import Player
from game_logic import GameLogic

class Movement:
    def __init__(self):
        self.ALL_LOCATIONS = [
            "Study",
            "Hall",
            "Lounge",
            "Library",
            "Billiard",
            "Dining",
            "Conservatory",
            "Ballroom",
            "Kitchen",
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
    
    # Check if two locations are adjacent
    def is_adjacent(self, position, target_position):
        if position in target_position or target_position in position:
            print("Valid move")
            print(f"Moving from {position} to new location: {target_position}")
            return True 
        if position == target_position:
            return False
        else:
            print("Not adjacent") 
            return False 

    # Check if a secret passage exists between two rooms
    def is_secret_passage(self, current_location, target_location):
        target = ""
        match current_location:
            case "Study":
                target = "Kitchen"        
            case "Kitchen": 
                target = "Study"
            case "Lounge":
                target = "Conservatory"
            case "Conservatory":
                target = "Lounge"
        return target_location == target

    # Check if a hallway is unoccupied
    def is_hallway_unoccupied(self, player_dict, target_position):
        print ("is_hallway_unoccupied has been called")
        print("player dictionary: ")
        print(player_dict)
        print("room being checked, target_position : "+ target_position)
        if "_" in target_position:
            print("if statement satisfied")
            for key,value in player_dict.items():
                
                if target_position == value.position:
                    print(target_position + " is occupied by ")
                    return False 
            #print(i.position)
            
       
        return True 

    # Validate player movement
    def validate_player_movement(self, player_dict, cur_player):
        possible_moves = []
        print(f"Validating movement for player: {cur_player}")
        print(player_dict)
        # Logic to validate player movement
        for i in self.ALL_LOCATIONS:
            if (self.is_adjacent(cur_player.position, i) and self.is_hallway_unoccupied(player_dict, i)) or self.is_secret_passage(cur_player.position, i):
                possible_moves.append(i)



        # possible_moves = self.ALL_LOCATIONS  # Example logic, replace with actual checks
        return possible_moves
