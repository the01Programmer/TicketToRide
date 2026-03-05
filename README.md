CMPT 2276 Course Project - Ticket to Ride - How to Play Application change log 1- Ryder feb 18th

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
