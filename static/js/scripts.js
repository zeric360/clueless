const WEAPON_NAMES = ["Candlestick", "Dagger", "Revolver", "Lead Pipe", "Wrench", "Rope"];
const PLAYER_NAMES = ["Miss Scarlet", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"];
const ROOM_NAMES = ["Study", "Hall", "Lounge", "Dining Room", "Billiard Room", "Library", "Conservatory", "Ballroom", "Kitchen"];
const ACTION_NAMES = ["Make a Suggestion", "Make an Accusation", "Move Character", "End Turn"];
const ALL_LOCATIONS = [
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

document.addEventListener("DOMContentLoaded", () => {
    const socket = io.connect('http://' + document.domain + ':' + location.port);

    // Populate dropdowns
    function populateDropdown(dropdownId, options) {
        const dropdown = document.getElementById(dropdownId);
        options.forEach(option => {
            const optElement = document.createElement("option");
            optElement.value = option;
            optElement.textContent = option;
            dropdown.appendChild(optElement);
        });
    }

    populateDropdown("playerDropdown", PLAYER_NAMES);
    populateDropdown("weaponDropdown", WEAPON_NAMES);
    populateDropdown("roomDropdown", ROOM_NAMES);
    populateDropdown("actionDropdown", ACTION_NAMES);

    // Handle name form submission
    document.querySelector('#name-form').onsubmit = (event) => {
        event.preventDefault();
        const playerName = document.querySelector('#playerName').value;
        const characterSelection = document.querySelector('#character-selection').value;

        if (playerName.trim() !== "" && characterSelection !== "") {
            socket.emit('submit_name', {
                name: playerName,
                character: characterSelection
            });

            document.querySelector('#name-form').style.display = 'none';
            document.querySelector('#chat-section').style.display = 'block';
            //document.querySelector('#action-section').style.display = 'none';
            //document.querySelector('#dropdown-section').style.display = 'none';
        } else {
            alert("Please enter your name and select a character.");
        }
    };

    // Disable a character in the dropdown for all players when it's selected
    socket.on('disable_character', (character) => {
        const option = document.querySelector(`#character-selection option[value='${character}']`);
        if (option) {
            option.disabled = true;
        }
    });

    socket.on('already_made_suggestion', function () {
        alert(`You have already made a suggestion. Please either move you character, make an accusation or end your turn.`);
    });

    // Handle messages from the server
    socket.on('message', (msg) => {
        const logMessages = document.getElementById('log-messages');
        const newMessage = document.createElement('li');
        newMessage.textContent = msg;
        logMessages.appendChild(newMessage);

        logMessages.scrollTop = logMessages.scrollHeight;
    });

    // Handle assigned character and cards
    socket.on("assigned_character", (data) => {
        document.getElementById("character-display").innerText = `Character: ${data.character}`;
        document.getElementById("cards-display").innerText = `Cards: ${data.cards.join(", ")}`;
    });

    socket.on("start_turn", function () {
        //const selectedPlayer = document.getElementById("playerDropdown").value;
        document.querySelector('#action-section').style.display = 'block';
    });

    // notify player's whose turn it is
    socket.on("change_turn", function (turn_info) {
        const logMessages = document.getElementById('log-messages');
        const newMessage = document.createElement('li');
        if (turn_info.bool_turn) {
            newMessage.textContent = "It is your turn! Please select your action below!";
        }
        else {
            newMessage.textContent = "It is " + turn_info.current_turn + "'s turn. Please wait while they input their selection...";
        }
        logMessages.appendChild(newMessage);

        logMessages.scrollTop = logMessages.scrollHeight;
    });

    // Handle chat message submission
    document.querySelector('#send-message').onsubmit = (event) => {
        event.preventDefault();
        const userInput = document.querySelector('#myMessage').value;
        socket.send(userInput);
        document.querySelector('#myMessage').value = '';
    };

    // Handle dropdown submit button
    document.getElementById("submitButton")?.addEventListener("click", () => {
        const selectedPlayer = document.getElementById("playerDropdown")?.value;
        const selectedWeapon = document.getElementById("weaponDropdown")?.value;
        const selectedRoom = document.getElementById("roomDropdown")?.value;

        if (selectedPlayer && selectedWeapon && selectedRoom) {
            if (selectedAction === "Make a Suggestion") {
                // Handle suggestion
                socket.emit("handle_suggestion", {
                    player_sug: selectedPlayer,
                    weapon_sug: selectedWeapon,
                    room_sug: selectedRoom,
                });
            } else if (selectedAction === "Make an Accusation") {
                // Handle accusation
                socket.emit("handle_accusation", {
                    player_acc: selectedPlayer,
                    weapon_acc: selectedWeapon,
                    room_acc: selectedRoom,
                });

            } else {
                alert("Invalid action. Please select an action first using the action button.");
            }
        } else {
            alert("Please make a selection for all dropdowns.");
        }

    });

   // Handle action selection button
   document.getElementById("submitActionButton")?.addEventListener("click", () => {
    selectedAction = document.getElementById("actionDropdown").value;

    if (selectedAction === "Make a Suggestion" || selectedAction === "Make an Accusation") {
        socket.emit("action", { action: selectedAction });
    } else if (!selectedAction) {
        alert("Please select an action.");
    } else if (selectedAction === "Move Character") {
        socket.emit("action", { action: selectedAction });  //
    } else if (selectedAction === "End Turn") {
        document.querySelector('#action-section').style.display = 'none';
        document.querySelector('#dropdown-section').style.display = 'none';
        //alert("This is the action: " + selectedAction);
        socket.emit("handle_turn_end");
    }
});

    socket.on("clear_page", function () {
        document.querySelector('#card_suggestion').style.display = 'none';
        document.querySelector('#dropdown-movement-section').style.display = 'none';
    });

    socket.on("display_dropdown", function () {
        document.querySelector('#dropdown-section').style.display = 'block';
    });

    socket.on("display_movement_dropdown", function (possible_moves) {
        // Populate dropdowns
        console.log("here");
    
        function populateDropdown(dropdownId, options) {
            const dropdown = document.getElementById(dropdownId);
    
            // Clear existing options first
            dropdown.innerHTML = '';
    
            // Add new options
            options.forEach(option => {
                const optElement = document.createElement("option");
                optElement.value = option;
                optElement.textContent = option;
                dropdown.appendChild(optElement);
            });
        }
    
        populateDropdown("movementDropdown", possible_moves.moves);
        document.querySelector('#dropdown-movement-section').style.display = 'block';
    });
    

    socket.on("display_suggestion_select", function (disprove) {

        // Populate dropdowns
        function populateDropdown(dropdownId, options) {
            const dropdown = document.getElementById(dropdownId);
            options.forEach(option => {
                const optElement = document.createElement("option");
                optElement.value = option;
                optElement.textContent = option;
                dropdown.appendChild(optElement);
            });
        }

        populateDropdown("cardDropdown", disprove.disprove_cards);
        document.querySelector('#card_suggestion').style.display = 'block';

    });

    document.getElementById("submitCardButton").addEventListener("click", () => {
        const selectedCard = document.getElementById("cardDropdown").value;

        if (selectedCard == "") {
            alert("Please select an action.");
        } else {
            socket.emit('card_suggestion', {
                card: selectedCard,
            });
        }

    });

    document.getElementById("submitMovementButton").addEventListener("click", () => {
        const selectedMovement = document.getElementById("movementDropdown").value;
 
        if (selectedMovement == "") {
            alert("Please select a location.");
        } else {
            socket.emit('movement_selection', {
                location: selectedMovement,
            });
        }
 
    });

    socket.on("game_over", function (game_over_info) {
        //const selectedPlayer = document.getElementById("playerDropdown").value;
        document.querySelector('#action-section').style.display = 'none';
        document.querySelector('#dropdown-section').style.display = 'none';

        const logMessages = document.getElementById('log-messages');
        const newMessage = document.createElement('li');

        newMessage.textContent = "The game is over!";

        logMessages.appendChild(newMessage);

        logMessages.scrollTop = logMessages.scrollHeight;
        document.querySelector('#game_over').style.display = 'block';
    });

    socket.on("game_lost", function (game_over_info) {
        //const selectedPlayer = document.getElementById("playerDropdown").value;
        document.querySelector('#action-section').style.display = 'none';
        document.querySelector('#dropdown-section').style.display = 'none';
        document.querySelector('#game_over').style.display = 'block';
    });



    socket.on("disprove_card_message", function (card) {
        const logMessages = document.getElementById('log-messages');
        const newMessage = document.createElement('li');

        newMessage.textContent = card.card + " has been disproven!";

        logMessages.appendChild(newMessage);

        logMessages.scrollTop = logMessages.scrollHeight;
    });

    socket.on("move_character", function (move_character_info) {
        console.log("Received move_character_info:", move_character_info);
        
        
        const positions = {
            // Rooms
            Study: { x: 600, y: 1300 },
            Hall: { x: 900, y: 1300 },
            Lounge: { x: 1200, y: 1300 },
            Library: { x: 600, y: 1050 },
            Billiard: { x: 900, y: 1050 },
            Dining: { x: 1200, y: 1050 },
            Conservatory: { x: 600, y: 800 },
            Ballroom: { x: 900, y: 800 },
            Kitchen: { x: 1200, y: 800 },
        
            // Horizontal Hallways
            Study_Hall: { x: 750, y: 1350 },
            Hall_Lounge: { x: 1050, y: 1350 },
            Library_Billiard: { x: 750, y: 1100 },
            Billiard_Dining: { x: 1050, y: 1100 },
            Conservatory_Ballroom: { x: 750, y: 850 },
            Ballroom_Kitchen: { x: 1050, y: 850 },
        
            // Vertical Hallways
            Study_Library: { x: 675, y: 1200 },
            Hall_Billiard: { x: 975, y: 1200 },
            Lounge_Dining: { x: 1275, y: 1200 },
            Library_Conservatory: { x: 675, y: 950 },
            Billiard_Ballroom: { x: 975, y: 950 },
            Dining_Kitchen: { x: 1275, y: 950 },
        };
        
        
        
        
    
        // Extract the character name and target location
        let characterName = "";

        if (move_character_info.character_name== "Miss Scarlet"){
            characterName = "Miss_Scarlet";
        }
        if (move_character_info.character_name== "Colonel Mustard"){
            characterName = "Colonel_Mustard";
        }
        if (move_character_info.character_name== "Mrs. White"){
            characterName = "Mrs_White";
        }
        if (move_character_info.character_name== "Mr. Green"){
            characterName = "Mr_Green";
        }
        if (move_character_info.character_name== "Mrs. Peacock"){
            characterName = "Mrs_Peacock";
        }
        if (move_character_info.character_name== "Professor Plum"){
            characterName = "Professor_Plum";
        }
        
        
        
      
        const targetLocation = move_character_info.target_location;


        

        console.log("Character Name:", characterName);
        console.log("Target Location:", targetLocation);

    
        // Validate if the target location exists in the positions map
        if (!positions[targetLocation]) {
            console.error(`Target location "${targetLocation}" does not exist.`);
            return;
        }

        
    
        // Find the character element by its ID
        const characterElement = document.getElementById(characterName);
        if (!characterElement) {
            console.error(`Character "${characterName}" does not exist on the board.`);
            return;
        }
    
        // Get the target coordinates
        const targetCoordinates = positions[targetLocation];
        console.log("Target Coordinates:", targetCoordinates);

    
        // Move the character element to the new location
        
        characterElement.style.left = `${targetCoordinates.x + 150 / 2 - characterElement.offsetWidth / 2}px`; // Center horizontally
        characterElement.style.top = `${targetCoordinates.y + 150 / 2 - characterElement.offsetHeight  / 2}px`; // Center vertically
        console.log(
            `Character "${characterName}" moved to [left: ${characterElement.style.left}, top: ${characterElement.style.top}]`
        );
    });


});


