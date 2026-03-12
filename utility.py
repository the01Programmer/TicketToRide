import pygame
import random
import queue
import time
import sys
import math
from collections import deque
pygame.init()
font = pygame.font.SysFont('Corbel',35)
smallfont = pygame.font.SysFont('Corbel',15)
class MessageLog:
    def __init__(self, max_lines=6):
        self.max_lines = max_lines
        self.lines = []

    def add(self, text):
        if text is None:
            return
        self.lines.append(str(text))
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]

    def draw(self, surface):
        base_x, base_y = 30, 600
        for i, line in enumerate(self.lines):
            txt = smallfont.render(line, True, (0, 0, 0))
            surface.blit(txt, (base_x, base_y + i * 18))

message_log = MessageLog()

TRACK_COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "white": (255, 255, 255),
    "black": (20, 20, 20),
    "pink": (232, 158, 184),
    "yellow": (255, 255, 0),
    "orange": (255, 153, 28),
    "wild": (128, 128, 128),
}
def numbertocolor(num):
    if num == 0:
        return "red"
    if num == 1:
        return "green"
    if num == 2:
        return "blue"
    if num == 3:
        return "white"
    if num == 4:
        return "black"
    if num == 5:
        return "orange"
    if num == 6:
        return "pink"
    if num == 7:
        return "yellow"
    if num == 8:
        return "wild"
    
def colortonumber(color):
    if color == "red":
        return 0
    if color == "green":
        return 1
    if color == "blue":
        return 2
    if color == "white":
        return 3
    if color == "black":
        return 4
    if color == "orange":
        return 5
    if color == "pink":
        return 6
    if color == "yellow":
        return 7
    if color == "wild":
        return 8

def scoreforlength(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    if n == 3:
        return 4
    if n == 4:
        return 7
    if n == 5:
        return 10
    if n == 6:
        return 15


def pointtosegmentdistance(px, py, ax, ay, bx, by):
    # distance from point px,py to a line

    abx = bx - ax
    aby = by - ay
    apx = px - ax
    apy = py - ay

    # length of AB squared
    ablensq = abx * abx + aby * aby

    # if A and B are the same point, measure to A
    if ablensq == 0:
        dx = px - ax
        dy = py - ay
        return math.hypot(dx, dy)

     # compute projection factor (with limited range)
    t = (apx * abx + apy * aby) / ablensq
    if t < 0:
        t = 0
    if t > 1:
        t = 1

    # closest point on AB
    cx = ax + t * abx
    cy = ay + t * aby

    dx = px - cx
    dy = py - cy

    return math.hypot(dx, dy)



def findtrackundermouse(mousepos, map, hitradius=18):
    # mouse_pos is (mx, my)
    mx = mousepos[0]
    my = mousepos[1]

    # check all tracks in the map
    for t in map.trackList:
        ax = t.city1.position[0]
        ay = t.city1.position[1]
        bx = t.city2.position[0]
        by = t.city2.position[1]

        # how close is the mouse to this track?
        d = pointtosegmentdistance(mx, my, ax, ay, bx, by)

        if d <= hitradius:
            return t  # this is the track we clicked

    return None  # no track under mouse


def buytrack(player, track, deck, screen):
    # 1. Make sure track is not already claimed
    if track.Owner is not None:
        message_log.add("Track already claimed.")
        return False

    # 2. Try to spend cards equal to the track length
    # track.color must be a number 0–8 
    numofcolor = colortonumber(track.color)
    
    success = player.spend(numofcolor, track.length, deck,screen)
    if not success:
        message_log.add("Not enough cards to buy this track.")
        return False

    # 3. Give ownership of the track to that player
    track.Owner = player
    player.ownedTrackList.append(track)
    player.addConnection(track.city1, track.city2)

    # 4. Score points based on the track length
    player.score += scoreforlength(track.length)

    return True

class Choicemenu:
    def __init__(self,Owner,options = ["true","false"], text = "choice"):
        self.text = smallfont.render(text , True , (0,0,0))
        self.Owner = Owner
        self.options = options
        self.buttons = []
        for i in range(len(self.options)):
            self.buttons.append(pygame.Rect(30+(120*i),500,100,40))
    def buttoncheck(self):
        for i in range(len(self.options)):
            if self.buttons[i].collidepoint(pygame.mouse.get_pos()):
                self.Owner.awns = self.options[i]

    def draw(self,screen):
        for i in range(len(self.options)):
            pygame.draw.rect(screen,(0,0,0),(30+(120*i),500,100,40),border_radius=3)
            text = font.render(f"{self.options[i]}" , True , (255,255,255))
            screen.blit(text,(50+(120*i),500))
            screen.blit(self.text,(50,450))