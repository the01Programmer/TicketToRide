CMPT 2276 Course Project - Ticket to Ride - How to Play Application change log 1- Ryder feb 18th

added basic pygame setup
set up a player class with variables for thraking the hand, wild cards, and score
set up a basic comand line based UI system should be replased with a image based one later (next milestone)
i added a function to be used to spend cards it will ask the user if they want to use wild cards if they cant afford it (and have the wilds to afford it). it returns a true false value
change log 2- Ryder mar 1st

added a train car system
added a system that will draw cards for the starting hand
change log 3- Ryder mar 2nd

made a more accurate deck system that uses a deck object to store and draw cards from.
modifyed all existing code to use the new system
added the ability to draw cards from five options during a turn with accurate restrictions.
change log 4- Ryder & 3m* mar 2nd

implemented the map showing cites and tracks (currently only visual)
updated the card display to use the same graphics system as the map since console output does't work with it
temporaly disabled the draw action as we haven't yet updated it

Martina – log 1 - March 2

1. Added a bunch of helper functions:
colortonumber, scoreforlength, buytrack, pointtosegmentdistance, and findtrackundermouse.
These let you the number correlated with a color, what the score increase is for a track, check the mouse click distance to tracks, and actually buy a track.

2. Added mouse click detection using
if event.type == pygame.MOUSEBUTTONDOWN
Now the game can tell when the player clicks on something

3. In general I made the map interactive so a player can actually click on a track and the game will detect whether the player can buy it or not
