from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from player import Player 
from card import Card
from game_board import gameBoard
from gui import Gui
from game_logic import GameLogic
from movement import Movement



app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Dictionary to store connected clients with their names
player_dict = {}
player_order_join = [] # list with order of client id's
global has_suggested
has_suggested = False 
global has_moved
has_moved = False
MAX_PLAYERS = 6
turn_count = 0
#player_obj_list = []
selected_characters = set()
#client_list = [] 
# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')


# Handle player joining with their name
@socketio.on('submit_name')
def handle_player_joined(data):
    client_id = request.sid  # Get the session ID of the connecting client
    player_name = data['name']  # Get the player's name from the client data
    #character = "Scarlet"
    character = data['character']
    
    if character not in selected_characters:
        selected_characters.add(character)

        emit('disable_character', character, broadcast=True)
        send(f"{player_name} has joined the game and selected {character}", broadcast=True)
    else:
        send(f"{player_name} has selected a character that has already been chosen. Please select another character.", to=client_id)
    
    print()
    print(f"Player {player_name} with ID {client_id} connected and selected {character}. to play as.")
    send(f"Welcome, {player_name}!", to=client_id)  # Send a private welcome message to the player
    # Broadcasts to all players that a new player has joined
    
   
    #instantiating player object for each client that connects to the server 
    new_player = Player(client_id, player_name, character)
    player_dict[client_id] = new_player 
    player_order_join.append(client_id)
    #player_dict[character] = new_player 
    #player_obj_list.append(new_player)
    #once the max number of players is reached, the game will start
    if len(player_dict) == MAX_PLAYERS:
        send("Maximum players reached. Starting the game of Clue!", broadcast=True)
        handle_start_game()

@socketio.on('start_game_event')
def handle_start_game():
    send("Starting the game of Clue!", broadcast=True)
    #randomly pick winning character, room, and weapon
    global game_logic 
    game_logic = GameLogic(players=player_dict)
    

    #initialize all of the cards 
    character_cards = game_logic.character_cards
    weapon_cards = game_logic.weapon_cards
    room_cards = game_logic.room_cards
    
    #randomly initializes the 3 winning cards 
    print()
    print("******************************************************")
    print("For testing purposes printing out winning cards: ")
    for card in game_logic.winning_cards:
        print(card.name, card.card_type)
    print("******************************************************")
    print()
    
    #randomly assigns each player 3 cards
    game_logic.assign_player_cards()
    for player_id, player in player_dict.items():
        print(f"{player.character}'s cards: {[card.name for card in player.cards]}")
    print()
   
    for player_id, player in player_dict.items():
        assigned_info = {
            "character": player.character,
            "cards": [card.name for card in player.cards]
        }
        emit("assigned_character", assigned_info, to=player_id)

    #initialize each players position on the board
    for player_id, player in player_dict.items():
        if player.character == "Miss Scarlet":
            player.position = "Hall_Lounge"
        elif player.character == "Colonel Mustard":
            player.position = "Lounge_Dining"
        elif player.character == "Mrs. White":
            player.position = "Ballroom_Kitchen"
        elif player.character == "Mr. Green":
            player.position = "Conservatory_Ballroom"
        elif player.character == "Mrs. Peacock":
            player.position = "Library_Conservatory"
        elif player.character == "Professor Plum":
            player.position = "Study_Library"
    whose_turn()

def whose_turn():
    global cur_player
    global player_ids
   
    cur_player = player_dict[player_order_join[turn_count % MAX_PLAYERS]]
    if cur_player.active == False:
        offset = 0
        while(cur_player.active == False):
            offset += 1
            cur_player = player_dict[player_order_join[(turn_count % MAX_PLAYERS) + offset]]
    
    broadcast_turn(cur_player)

def broadcast_turn(cur_player):
    print(f"It's currently {cur_player.character}'s turn")
    for id, player in player_dict.items():
        if player.character == cur_player.character:
            turn_info = {'current_turn': cur_player.character, 'bool_turn':True}
            emit('change_turn', turn_info, to=id)
        else:
            turn_info = {'current_turn': cur_player.character, 'bool_turn':False}
            emit('change_turn', turn_info, to=id)
    handle_turn(cur_player)

def handle_turn(cur_player):
    # display menus for person whose turn it is
    print(f"Starting {cur_player.character}'s turn")
    emit('start_turn', to=cur_player.player_id)

@socketio.on('action')
def action_response(action_input):
    print("test test test")
    print(f"This is the action input: {action_input['action']}")
    action = action_input['action']
    suggestion_bool = True
    #current_turn = 0
    #total_turn_count = 0
    #player_ids = list(player_dict.keys())  # List of player IDs to maintain turn order
    global has_suggested
    global has_moved
    has_accused = False
    movement = Movement()
    bool_flag = False
   
    #while True:
    if action == "Make a Suggestion":
        if has_suggested:
            #print("You have already made a suggestion this turn.")
            emit('already_made_suggestion')
        else:
            has_suggested = True
            print("You have chosen to make a suggestion.")
            emit("display_dropdown", to=cur_player.player_id)
            #break
    elif action == "Make an Accusation":
        print("test")
        if has_accused:
            print("You have already made an accusation this turn.")
            emit('already_made_accusation')
        else:
            print("You have chosen to make an accusation.")
            emit("display_dropdown", to=cur_player.player_id)
            #break
    elif action == "Move Character":
        if has_moved:
            print("You have already moved your character...")
            emit("already_moved_character", to=cur_player.player_id)
        else:
            print("You have chosen to move your character.")
            movement = Movement()
            list_of_possible_moves = []
            list_of_possible_moves.clear()
            print("player dict in server passing to movement here:  ")
            print(player_dict)
            list_of_possible_moves = movement.validate_player_movement(player_dict, cur_player)
            print(list_of_possible_moves)
            possible_moves = {"moves": list_of_possible_moves}
            emit("display_movement_dropdown", possible_moves, to=cur_player.player_id)
    elif action == "End Turn":
        print("Ending turn.")
        #break


@socketio.on('handle_suggestion')
def handle_suggestion(suggestions):
     # get cards
    character = cur_player.character
    player_sug = suggestions['player_sug']
    weapon_sug = suggestions['weapon_sug']
    room_sug = suggestions['room_sug']
    print()
    print(f"player: {player_sug}")
    print(f"weapon: {weapon_sug}")
    print(f"room: {room_sug}")
    print()
    # need to convert cards to actual card
    # need to convert cards to actual card
    player_card = game_logic.get_player_card(player_sug)
    weapon_card = game_logic.get_weapon_card(weapon_sug)
    room_card = game_logic.get_room_card(room_sug)
    print(type(player_card))

     # need to change process suggestion function
    send("{} just made a suggestion. They suggested {} in the {} with a {} commited the murder".format(character, player_sug, room_sug, weapon_sug), broadcast=True)
    game_logic.process_suggestion(player_card, weapon_card, room_card, cur_player)    

@socketio.on('handle_accusation')
def handle_accusation(accusations):
    # get cards
    player_acc = accusations['player_acc']
    weapon_acc = accusations['weapon_acc']
    room_acc = accusations['room_acc']
    print(f"Current player: {cur_player.character}")
    print(f"player: {player_acc}")
    print(f"weapon: {weapon_acc}")
    print(f"room: {room_acc}")
    print()

    game_logic.process_accusation(cur_player, player_acc, weapon_acc, room_acc)
    if game_logic.gameOver == True:
        send(f"{cur_player.character} has correctly accused {player_acc} in the {room_acc} with the {weapon_acc}", broadcast=True)
        send(f"{cur_player.character} has won the game!", broadcast=True)
        game_over_info = {"game_over": True}
        emit('game_over', game_over_info, broadcast=True)
    else:
        send(f"{cur_player.character} has incorrectly accused {player_acc} in the {room_acc} with the {weapon_acc}", broadcast=True)
        cur_player.active = False
        print(player_dict, "before removing character")
        #removes player from game
        print("player dict before removing player", player_dict)
        #player_dict.pop(cur_player.player_id)
        #print("player dict after removing player", player_dict)
        #print(player_dict, "after removing character")
        send(f"{cur_player.character} is removed from the game.", broadcast=True)

        game_lost_info = {"game_lost": True}
        emit('game_lost', game_lost_info, to=cur_player.player_id)
        handle_turn_end()

        if len(player_dict) == 1:
            send(f"{cur_player.character} is the only play left in the game. Game over!", broadcast=True)

@socketio.on('movement_selection')
def handle_movement(location):
    loc = location['location']
    global cur_player
    move_character_info = {"character_name": cur_player.character, "target_location": loc}
    print(f"This is the location:  {loc}")
    print(f"current character at turn:  {cur_player.character}")
    
    
    emit("move_character", move_character_info, broadcast=True)


    # still need to invoke movement.py to validate moves
    print("old position is: " + cur_player.position)
    cur_player.position = loc # update location after move decided my player at their turn 
    print("New position is: " + cur_player.position)
    



@socketio.on('handle_turn_end')
def handle_turn_end():
    global turn_count
    global has_suggested
    global has_moved
    has_moved = False
    has_suggested = False 
    print()
    print("We are in the handle_turn_end function")
    print("printing turn_count", turn_count)
    turn_count += 1
    print("printing turn_count", turn_count)
    emit('clear_page', broadcast=True)
    whose_turn()

@socketio.on('card_suggestion')
def handle_card_suggestion(card):
    print(card['card'])
    card_name = card['card']
    card_selected = {
        'card': card_name
    }
    emit('disprove_card_message', card_selected, to=cur_player.player_id)
            

# Handle player disconnecting
@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid  # Get the session ID of the disconnecting client
    if client_id in player_dict:
        player_name = player_dict[client_id].name
        del player_dict[client_id]
        print(f"Player {player_name} with ID {client_id} disconnected.")
        # Optionally, broadcast to all players that the player has left
        send(f"{player_name} has left the game.", broadcast=True)
        print(player_dict)



@socketio.on('message')
def handle_message(msg):
    client_id = request.sid  # Get the sender's session ID
    if client_id in player_dict:
        player_name = player_dict[client_id].name  # Retrieve the player's name
        print(f"Received message from {player_name}: {msg}")
        # Broadcast the message to all connected clients
        send(f"{player_name}: {msg}", broadcast=True)

    
    

if __name__ == '__main__':
    socketio.run(app, debug=True)
    
    