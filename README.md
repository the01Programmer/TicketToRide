Martina – log 1 - March 2

1. Added a bunch of helper functions:
colortonumber, scoreforlength, buytrack, pointtosegmentdistance, and findtrackundermouse.
These let you the number correlated with a color, what the score increase is for a track, check the mouse click distance to tracks, and actually buy a track.

2. Added mouse click detection using
if event.type == pygame.MOUSEBUTTONDOWN
Now the game can tell when the player clicks on something

3. In general I made the map interactive so a player can actually click on a track and the game will detect whether the player can buy it or not
