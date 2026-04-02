import pygame
import random
import queue
import time
import sys
import math
import tutorial
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



def findtrackundermouse(mousepos, map, hitradius=14):
    # mouse_pos is (mx, my)
    mx = mousepos[0]
    my = mousepos[1]

    # check all tracks in the map
    for t in map.trackList:
        ax = t.city1.position[0]
        ay = t.city1.position[1]
        bx = t.city2.position[0]
        by = t.city2.position[1]

        if math.hypot(mx - ax, my - ay) < 25:
            continue
        if math.hypot(mx - bx, my - by) < 25:
            continue

        # how close is the mouse to this track?
        d = pointtosegmentdistance(mx, my, ax, ay, bx, by)

        if d <= hitradius:
            return t  # this is the track we clicked

    return None  # no track under mouse

def findcityundermouse(mousepos, map, hitradius=18):
    mx, my = mousepos

    for city in map.cityList:
        cx, cy = city.position

        # distance from mouse to city center
        if math.hypot(mx - cx, my - cy) <= hitradius:
            return city

    return None

def buytrack(player, track, tracks, deck, screen, restriction = False):
    # 1. Make sure track is not already claimed
    if track.Owner is not None:
        message_log.add("Track already claimed.")
        return False

    # 2. Try to spend cards equal to the track length
    # track.color must be a number 0–8 
    numofcolor = colortonumber(track.color)

    #check if we can buy this track based on the restriction
    if restriction != False and not restriction[1] == tracks.index(track):
        return False
    
    success = player.spend(numofcolor, track.length, deck, screen)
    if not success:
        message_log.add("Not enough cards to buy this track.")
        return False

    # 3. Give ownership of the track to that player
    track.Owner = player
    player.ownedTrackList.append(track)
    player.addConnection(track.city1, track.city2)

    # 4. Score points based on the track length
    tutorial.pointsQuiz(scoreforlength(track.length))
    player.score += scoreforlength(track.length)

    if all(t.Owner is not None for t in tracks):
        player.ending = True

    if restriction != False:
        player.turns.completeactionE()
    return True

def placestation(player, city, restriction = False):
    if city.station == True:
        return False
    
    if player.stations < 1:
        return False

    if player.cars < 1:
        return False

    if restriction != False and restriction[1] != city.name:
        return False
    
    city.station = True
    city.stationowner = player
    player.stations -= 1
    player.cars -= 1

    if restriction != False:
        city.restrictedconnection = restriction[2]
        player.turns.completeactionE()
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

def choose_track_from_list(track_list, screen, city):
    background = screen.copy()

    menu_rect = pygame.Rect(0, 0, 700, 300)
    menu_rect.center = (screen.get_width() // 2, screen.get_height() // 2)

    buttons = []
    start_y = menu_rect.y + 120
    for i, t in enumerate(track_list):
        btn = pygame.Rect(menu_rect.x + 50, start_y + i*60, 600, 45)
        buttons.append(btn)

    title = smallfont.render("You placed a station. Select a track to use:", True, (0, 0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, b in enumerate(buttons):
                    if b.collidepoint(pygame.mouse.get_pos()) and city.restrictedconnection == False :
                        return track_list[i]
                    elif city.restrictedconnection[0] == track_list[i].city1.name and city.restrictedconnection[1] == track_list[i].city2.name:
                        return track_list[i]

        screen.blit(background, (0, 0))

        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (240, 240, 240), menu_rect, border_radius=10)
        pygame.draw.rect(screen, (20, 20, 20), menu_rect, 3, border_radius=10)

        screen.blit(title, (menu_rect.x + 50, menu_rect.y + 40))

        for i, b in enumerate(buttons):
            pygame.draw.rect(screen, (255, 255, 255), b, border_radius=6)
            pygame.draw.rect(screen, (0, 0, 0), b, 2, border_radius=6)

            label = smallfont.render(f"{track_list[i].city1.name} <-> {track_list[i].city2.name}",True, (0, 0, 0))
            screen.blit(label, (b.x + 12, b.y + 12))

        pygame.display.flip()


def shortest_route(map_obj, start, end):
    distances = {}
    previous = {}

    for city in map_obj.cityList:
        distances[city] = float("inf")
    distances[start] = 0

    visited = []

    while len(visited) < len(map_obj.cityList):
        current = None
        smallest_distance = float("inf")

        for city in map_obj.cityList:
            if city not in visited and distances[city] < smallest_distance:
                smallest_distance = distances[city]
                current = city

        if current is None:
            break

        visited.append(current)

        for track in map_obj.get_tracks_touching_city(current):
            if track.city1 == current:
                neighbor = track.city2
            else:
                neighbor = track.city1

            new_distance = distances[current] + track.length

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = (current, track)

    path = []
    cur = end

    while cur in previous:
        prev_city, used_track = previous[cur]
        path.append(used_track)
        cur = prev_city

    path.reverse()
    return path


def show_hints(player, map_obj):
    message_log.add("HINTS:")
    for r in player.routeCardList:
        path = shortest_route(map_obj, r.city1, r.city2)
        if not path:
            message_log.add(f"{r.city1.name} -> {r.city2.name}: no route")
        else:
            s = ", ".join(t.city1.name + "-" + t.city2.name for t in path)
            total = sum(t.length for t in path)
            message_log.add(f"• The shortest path for destination card {r.city1.name} to {r.city2.name} is using track(s) {s} with a total use of {total} cars")
    message_log.add("")