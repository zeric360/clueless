from game_board import gameBoard
from player import Player
from card import Card, Character, Weapon, Room
from game_logic import GameLogic
import random


if __name__ == "__main__":
    print("test")

    scarlett = Player(1, "Angela", "Miss Scarlett")
    mustard = Player(2, "John", "Col. Mustard")
    white = Player(3, "Jane", "Mrs. White")
    green = Player(4, "Tom", "Mr. Green")
    peacock = Player(5, "Sally", "Mrs. Peacock")
    plum = Player(6, "Bob", "Prof. Plum")
    player_objects = [scarlett, mustard, white, green, peacock, plum]
    #the game logic is initalized with all the player objects 
    
    game_logic = GameLogic(players=player_objects)
    
    #initialize all of the cards 
    character_cards = game_logic.character_cards
    weapon_cards = game_logic.weapon_cards
    room_cards = game_logic.room_cards
    
    print("printing out winning cards winning_cards")
    for card in game_logic.winning_cards:
        print(card.name, card.card_type)


    print()
    game_logic.assign_player_cards()
   
    '''
    for key in player_cards_dict:
        print(key, "is holding the following cards:")
        card = player_cards_dict[key]
        for c in card:
            print(c.name)
        print()
    '''
    suggestion_bool = True
    current_turn = 0 
    while not game_logic.gameOver:
        print("the current players in the game are: ")
        for player in player_objects:
            print(player.character)
        print("*************************************************************************")
        #current_player = game_logic.PLAYER_NAMES[current_turn]
        current_player = player_objects[current_turn]
        print(f'{current_player.character} is the current player')
        print("Would would you like to do?")
        print("1. Make a suggestion")
        print("2. Make an accusation")
        print("3. End Turn")
        action = int(input("Enter the number of the action you would like to take: "))
        if action == 1:
            print("You have chosen to make a suggestion")
            room_card = game_logic.get_room_card(suggestion_bool, current_player)  
            weapon_card = game_logic.get_weapon_card(suggestion_bool) 
            character_card = game_logic.get_character_card(suggestion_bool)  
            game_logic.process_suggestion(current_player, room_card, weapon_card, character_card)

        elif action == 2:
            print("You have chosen to make an accusation")
            room_card = game_logic.get_room_card(not suggestion_bool, current_player)  
            weapon_card = game_logic.get_weapon_card(not suggestion_bool) 
            character_card = game_logic.get_character_card(not suggestion_bool)
            game_logic.process_accusation(current_player, character_card, weapon_card, room_card)
        
        elif action == 3:
            print("Ending turn")
        
        #the number of players in the game len(player_objects). The number of players will change as players are removed from the game for making incorrect accusations
        print("printing number of players", len(player_objects))
        current_turn = (current_turn + 1) % len(player_objects)
        