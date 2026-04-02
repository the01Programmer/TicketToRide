CMPT 2276 Course Project - Ticket to Ride - How to Play Application 

change log 1- Ryder feb 18th

1. added basic pygame setup
2. set up a player class with variables for thraking the hand, wild cards, and score
3. set up a basic comand line based UI system should be replased with a image based one later (next milestone)
4. i added a function to be used to spend cards it will ask the user if they want to use wild cards if they cant afford it (and have the wilds to afford it). it returns a true false value

change log 2- Ryder mar 1st

1. added a train car system
2. added a system that will draw cards for the starting hand

change log 3- Ryder mar 2nd

1. made a more accurate deck system that uses a deck object to store and draw cards from.
2. modifyed all existing code to use the new system
3. added the ability to draw cards from five options during a turn with accurate restrictions.

change log 4- Ryder & Emmanuel mar 2nd

1. implemented the map showing cites and tracks (currently only visual)
2. updated the card display to use the same graphics system as the map since console output does't work with it
3. temporaly disabled the draw action as we haven't yet updated it

change log 5 – Martina - March 2

1. Added a bunch of helper functions:
colortonumber, scoreforlength, buytrack, pointtosegmentdistance, and findtrackundermouse.
These let you the number correlated with a color, what the score increase is for a track, check the mouse click distance to tracks, and actually buy a track.

2. Added mouse click detection using
if event.type == pygame.MOUSEBUTTONDOWN
Now the game can tell when the player clicks on something

3. In general I made the map interactive so a player can actually click on a track and the game will detect whether the player can buy it or not

change log 6- Ryder mar 2nd
1. updated the deck class to allow the user to draw cards from the map insted of the console

change log 7- Ryder mar 2nd
1. fixed issue where pile and hand ui didnt show the last card in the array
2. made the spend cards function when asking to use wild cards more user friendy by adding recognision for lowercase responses. 

change log 8 Emmanuel mar 3
1. Added routeCard class
2. added route checking functions to the player class

change log 9- Ryder mar 3nd
1. made routeCards a member variable of deck to ensure all card elements are handeled by it
2. added a system that allows the user to draw new route cards by pressing a button in the menu then with following inputs handeled in the comand line

change log 10 Emmanuel mar 3
1. added point loss on incomplete routes
2. made tweaks on route card handling for better system

change log 11 Ryder mar 4
1. added the Choicemenu class that can display and respond to choises given to the user
2. updated existing command line options to use the new system
3. in an in person meeting me and Martina decided to cut the longest route from this prototype since it requires a second player to be acuratly implemented.

change log 12 – Martina - March 4
1. Cleaned up spacing so GUI looks more organized.
2. Moved command line messages to show up on GUI instead (including adding the number of trains the user still has and what their score is).
3. Fixed drawroutes function so that when user selects a route card, it gets added to their list of routes
4. Made it so if there are less than 3 route cards available to draw, the user cannot draw any more route cards.

change log 13 – Ryder - March 4
1. fixed softlock cased by the max carts being too low to trigger the ending when unable to play
2. made the border on black cards visible

change log 14 – Ryder - March 10  
1. spread out files between (currently) 4 sepreate files main, map_classes, player_classes and utility a file for tutorial functions is planned but not implemented.
change log 14 – Ryder - March 14
1. added a basic version of the cpu that can claim ownership of a track so that other developers can start work that relies on that element of the cpu class
2. the cpu was added to player_classes as i plan for it to inheret from the base player class.
3. added a guide to adding new feture in the new file system

change log 14 – Ryder - March 15
1. updated the cpu to be able to take all current actions althoug it currently has no ai implemented so it can't use any stratagy. this implemetation would be good for a game ment to teach the user the basic controles since this cpu is incappable of being a chalange unless it gets lucky.
2. added new functions to the deck class that the cpu can use
3. updated the main file to start the cpus turn after the player makes an action

change log 15 - Martina - March 16
1. edits to map_classes.py file: 
    - edited functions draw_track_segments and drawmap to add a feature that highlights tracks that are owned by the player or the cpu using different colors (yellow for player and red for cpu)
    - added field station to City class
2. edit to player_classes.py file:
    - edited player class to include a station field
    - edited draw function to display number of stations
    - added usedTrackList field to player class
3. edits to utility.py file:
    - added a function findcityundermouse to detect whether user clicked on a city to use a station
    - added a function usestation to be able to use stations on a city
4. edits to main.py file:
    - added mouse detection for if a player clicks on a city. if they do, they will use their station unless they don't have one.
    - edited running loop so at the end of the game, it gives a player extra points if the station wasn't used 

change log 16 - Martina - March 17
1. edits to main.py
    - edited game_over code block to make exit screen look better
    - added blank lines after each line printed in message logs to make message log more readable
    - added station logic once game ends that allows player to use their station (i.e. select a track) if they have placed one down (and rechecks route completetion after that)
2. edits to map_classes.py
    - edited drawMap function to add highlighting when a station is placed on a city
    - added helper function get_tracks_touching_city to map class to return all tracks touching a city
3. edits to player_clases.py
    - edited enemy buy method so that if all tracks have been claimed, enemy.ending is true (ends game)
    - edited enemy buy method so that if track is owned, it returns false
    - fixed infinite loop in drawcard method in enemy class where it would keep trying to draw the second card forever (could happen if there are only wild cards to draw from)
    - added blank lines after each line printed in message logs to make message log more readable ()
4. edits to utility.py
    - edited buytrack method so that if all tracks have been claimed, player.ending is true (ends game)
    - added new function choose_track_from_list for a pop up that allows the player to select from tracks that they can use with the station they placed down

change log 17 – Ryder - March 18
    player classes
    - fixed issue where cpu would display a diffrent card from the one it drawed
    - fixed issue where the cpu wouldn't check the correct list when checking its completed routes
    - finished the decks cpudrawroutes as the cpus route check was disabled so i didn't see the problem
    - made the buy function able to use wild cards structured so that we could rework it to use logic to decide to use them
    main
    - added the ability to declair a winner between the user and the cpu but it currently only shows up in the text box and not the main game over screen

change log 18 - Braelyn - March 18
1. created a pop-up quiz to ask the player how many points the track is worth when they buy it

change log 19 - Martina - April 1
1. Added a button to the screen that says "Hint" (added code to main.py file to display the button)
2. When the player hits the button "Hint," the message log will display all the shortest paths that the player can take for all the destination cards they have
3. Added two new functions "shortest_route" and "show_hints" to the utility.py file


change log 20 - Ryder - Aprl 1
1. created a setplay class that stores a list of lists describing actions that the player and cpu can take
2. added child classes of the player and enemy classes that store a setplay as a variable and use it to determin their actions. the cpu does whatever is at the top of setplay while the player class restricts its options based on the top value in setplay
3. modifyed the functions in utility and draw that are responsible for some of the players actions to be restrictable by a setplay instance
4. updated deck to take a given queue and set that as it's deck value. it will shuffel its deck normaly if not given one 
5. created a new tutorial_main and small_map_classes file in preperation for making this setplay system a choseable mode 
tutorial_main holds a copy of main that uses the set play classes. it it set up to run the user through all avaliable actions as an introduction to the program's controles and the game
small_map_classes hold the smaller map so that tutorial_main can use a smaller map since that would make it easyyer

it would likely be a good idea to add messages to this main file in the future
