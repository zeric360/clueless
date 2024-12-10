from game_board import gameBoard
from player import Player
from card import Card, Character, Weapon, Room
import random
from flask_socketio import SocketIO, send, emit

# Game Logic Class
class GameLogic:
    #constants for the game
    WEAPON_NAMES = ["Candlestick", "Dagger", "Revolver", "Lead Pipe", "Wrench", "Rope"]
    PLAYER_NAMES = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    ROOM_NAMES = ["Study", "Hall", "Lounge", "Dining Room", "Billiard Room", "Library", "Conservatory", "Ballroom", "Kitchen"]
    
    
    def __init__(self, players):
        # Initialize cards as lists of Card objects
        self.character_cards = [Character(name) for name in GameLogic.PLAYER_NAMES]
        self.weapon_cards = [Weapon(name) for name in GameLogic.WEAPON_NAMES]
        self.room_cards = [Room(name) for name in GameLogic.ROOM_NAMES]

        self.character_cards_all = [Character(name) for name in GameLogic.PLAYER_NAMES]
        self.weapon_cards_all = [Weapon(name) for name in GameLogic.WEAPON_NAMES]
        self.room_cards_all = [Room(name) for name in GameLogic.ROOM_NAMES]

        #[character, weapon, room]
        self.winning_cards = self.pick_winning_cards()

        self.players = players
        
        # Initialize game state variables
        self.currentPlayer = 0
        self.gameOver = False
        self.winner = None
        self.losers = []

        
        
        #self.player_hands = self.deal_cards_to_players(6)  # Example with 6 players


        #self.pick_winning_cards()
        #self.assign_players_cards()

    def pick_winning_cards(self):
        """Selects one winning card each from characters, weapons, and rooms and removes them from the lists."""
        
        character_win = random.choice(self.character_cards)
        self.character_cards.remove(character_win)

        weapon_win = random.choice(self.weapon_cards)
        self.weapon_cards.remove(weapon_win)

        room_win = random.choice(self.room_cards)
        self.room_cards.remove(room_win)
        
        return [character_win, weapon_win, room_win]
        
       
    def assign_player_cards(self):
        # assign remaining cards to players
        all_remaining_cards = self.character_cards + self.weapon_cards + self.room_cards
        random.shuffle(all_remaining_cards)
        # Initialize each player's hand
        cards_per_player = 3  # Number of cards each player should receive

        # Iterate over each player and randomy assign them 3 cards
        for i, (player_id, player) in enumerate(self.players.items()):
            start_index = i * cards_per_player
            end_index = start_index + cards_per_player
            player.cards = all_remaining_cards[start_index:end_index]

        # Debug output to check card assignment
        
        #for player in self.players:
            #print(f"{player.character}'s cards: {[card.name for card in player.cards]}")



    def process_suggestion(self, player_card, weapon_card, room_card, cur_player):
        #self.process_movement(suggestedPlayer, location) # Move player into suggestion room
        #self.board.move_weapon(weapon, location)# Move the weapon into the suggestion room, I think this has to get covered in the game_board class

        print('Entered processing...')
        print(player_card.name)
        print(weapon_card.name)
        print(room_card.name)
        print(cur_player)
        
        for player in self.players.values():
            if player.name != cur_player.name:
                disprove_cards = self.disprove_cycle(player, room_card, weapon_card, player_card)   # Starts asking players to disprove the suggestion if they can
                if not disprove_cards:
                    # tell user they cannot disprove suggestion
                    print('cannot disprove suggestion')
                    
                else:
                    print('give user option to select cards...')
                    disprove = {
                        "disprove_cards" : disprove_cards
                    }
                    emit('display_suggestion_select', disprove, to=player.player_id)

    def process_accusation(self, accuser, who, what, where):
        # processes the accusation from player class
        #[character, weapon, room]
        
        winning_character = self.winning_cards[0].name
        winning_weapon = self.winning_cards[1].name
        winning_room = self.winning_cards[2].name

        if (who == winning_character and what == winning_weapon and where == winning_room):
            self.gameOver = True
            self.winner = accuser.character
            print(self.winner + " has won the game!")
            print("The winning cards are: ")
            for card in self.winning_cards:
                print(card.name, card.card_type)

        else:
            #if player makes an incorrect accusation, they are removed from the game
            print("Your accusation was incorrect, you have lost.") # This is a method to print something only for one specific client at a time, this needs to be implemented in the client class I believe
            accuser.active = False
            print(accuser.character, "has been removed from the game.")

            #print("The winning cards are:")
            #for card in self.winning_cards:
                #print(card.name, card.card_type)


    def disprove_cycle(self, player, location, weapon, character):
        # print out the suggestion

        #print("{} just made a suggestion. They suggested {} in the {} with a {} commited the murder".format(suggestor.character, character, location, weapon))

        disprove_cards = []
        for card in player.cards:
            if card.name == location.name or card.name == weapon.name or card.name == character.name:
                print(f"{player.character} can disprove the suggestion with the {card.card_type}: {card.name}!")
                disprove_cards.append(card.name)
        
        return disprove_cards


    def check_users_cards(self, player):
        #returns true if the player actually does not have cards they can use to disprove
        #returns false if the player could disprove
        return False

    def process_movement(self, player, new_position):
        # movement class validates the move and sends to game logic to process it for the server this just needs to send it to the game board class
        pass

    def get_room_card(self, suggestion_bool, player):
        if suggestion_bool:
            print("Please choose the room for your suggestion...")
        else:
            print("Please choose the room for your accusation...")
        # print all the weapon cards


        for i, room in enumerate(self.ROOM_NAMES):
            print("{}) {}".format(i+1, room))
        
        # ask player to select one
        room_num = int(input())
        room_card = self.ROOM_NAMES[room_num-1]
        
        #room_card = self.room_cards[int(room_num)-1]
        #player.request_move(room_card.name)
        #player.position = room_card.name

        return room_card

    def get_weapon_card(self, suggestion_bool):
        if suggestion_bool:
            print("Please choose the weapon for your suggestion...")
        else:
            print("Please choose the weapon for your accusation...")
        # print all the weapon cards

        for i, weapon in enumerate(self.WEAPON_NAMES):
            print("{}) {}".format(i+1, weapon))
        
        # ask player to select one
        weapon_num = int(input())
        weapon_card = self.WEAPON_NAMES[weapon_num-1] 
        return weapon_card


    def get_character_card(self, suggestion_bool):
        if suggestion_bool:
            print("Please choose the character for your suggestion...")
        else:
            print("Please choose the character for your accusation...")
        # print all the character cards

        for i, player in enumerate(self.PLAYER_NAMES):
            print("{}) {}".format(i+1, player))
        
        # ask player to select one
        char_num = int(input())
        char_card = self.PLAYER_NAMES[char_num-1]
        return char_card

    def get_player_card(self, card):
        print(f"card: {card}")
        for char_card in self.character_cards_all:
            #print(f"char card: {char_card.name}")
            if card == char_card.name:
                return char_card

    def get_weapon_card(self, card):
        #print(f"card: {card}")
        for weapon_card in self.weapon_cards_all:
            #print(f"weapon: {weapon_card.name}")
            if card == weapon_card.name:
                print(f"weapon: {weapon_card.name}")
                return weapon_card

    def get_room_card(self, card):
        print(f"card: {card}")
        for room_card in self.room_cards_all:
            #print(f"room_card: {room_card.name}")
            if card == room_card.name:
                return room_card
