import pygame
import random
import queue
import time
import sys
import math
import utility; print('Import successful')
import player_classes
from collections import deque

class Track:
    def __init__(self, color, length, wildReq, city1, city2):
        self.Owner = None
        self.User = None
        self.color = color
        self.length = length
        self.wildReq = wildReq
        self.city1 = city1
        self.city2 = city2
    def beClaimed(self, player):
        self.Owner = player
    
class City:
    def __init__(self, name, x, y):
        self.name = name
        self.station = False
        self.adjacent = [] # use to give the player an adjacency list for detecting connections
        self.position = (x, y)
    def addAdjacent(self, cities):
        for i in cities:
            self.adjacent.append(i)

class Map:
    def __init__(self, routeList):
        self.routeList = routeList
        self.trackList, self.cityList = self.setUpTracks()
    def setUpTracks(self):
        trackList = []
        cityList = []
        #set up default tracks manually
        a = City("A", 100, 120)
        b = City("B", 100, 320)
        c = City("C", 400, 320)
        d = City("D", 300, 100)

        a.addAdjacent([b,c,d])
        b.addAdjacent([a,c])
        c.addAdjacent([a,b])
        d.addAdjacent([a])

        cityList.append(a)
        cityList.append(b)
        cityList.append(c)
        cityList.append(d)

        self.routeList.append(self.createRouteCard(b, d, 10))
        self.routeList.append(self.createRouteCard(c, d, 25))
        self.routeList.append(self.createRouteCard(a, d, 20))
        self.routeList.append(self.createRouteCard(a, c, 15))
        
        t1 = Track("red", 4, 0, a, b)
        t2 = Track("blue", 6, 0, a, c)
        t3 = Track("green", 5, 0, b, c)
        t4 = Track("white", 3, 0, a, d)

        trackList.append(t1)
        trackList.append(t2)
        trackList.append(t3)
        trackList.append(t4)

        return trackList, cityList
    def createRouteCard(self, city1, city2, points):
        newCard = RouteCard(city1, city2, points)
        return newCard
    def draw_track_segments(self, surface, start_pos, end_pos, length, color, highlight_color=None, highlight_thickness=6):
        # 1. Calculate the distance and angle between cities
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # 2. Dimensions of each train car rectangle
        rect_width = (distance / length) * 0.8  # 80% of segment space for gap
        rect_height = 15 

        for i in range(length):
            # Calculate center point for each segment
            # We offset by 0.5 to center the segments between cities
            fraction = (i + 0.5) / length
            center_x = start_pos[0] + dx * fraction
            center_y = start_pos[1] + dy * fraction

            # 4. Rotate
            rect_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surf, color, (0, 0, rect_width, rect_height), border_radius=3)
            pygame.draw.rect(rect_surf, (0, 0, 0), (0, 0, rect_width, rect_height), 2, border_radius=3) # Outline

            rotated_surf = pygame.transform.rotate(rect_surf, -math.degrees(angle))
            rect_center = rotated_surf.get_rect(center=(center_x, center_y))

            # 5. highlight if applicable
            if highlight_color:
                glow_surf = pygame.Surface((rect_width + highlight_thickness, rect_height + highlight_thickness), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, highlight_color, (0, 0, rect_width + highlight_thickness, rect_height + highlight_thickness), border_radius=5)
                rotated_glow = pygame.transform.rotate(glow_surf, -math.degrees(angle))
                glow_rect = rotated_glow.get_rect(center=(center_x, center_y))
                surface.blit(rotated_glow, glow_rect)

            # 6. blit
            surface.blit(rotated_surf, rect_center)
    def drawMap(self, surface):
        for t in self.trackList:
            start = t.city1.position
            end = t.city2.position
            color = utility.TRACK_COLORS.get(t.color)
        
            highlight = None

            if isinstance(t.Owner, player_classes.player):
                highlight = (255, 255, 150, 180)

            if isinstance(t.Owner, player_classes.enemy):
                highlight = (255, 80, 80, 180)
    
            self.draw_track_segments(surface, start, end, t.length, color, highlight_color=highlight)

        for c in self.cityList:
            pygame.draw.circle(surface, (50, 50, 50), c.position, 15) 
            pygame.draw.circle(surface, (255, 215, 0), c.position, 12)
            text_surf = utility.font.render(c.name, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(c.position[0], c.position[1] - 25))
            surface.blit(text_surf, text_rect)

class RouteCard:
    def __init__(self, city1, city2, points):
        self.city1 = city1
        self.city2 = city2
        self.points = points
        self.completed = False
    def drawRouteCard(self, surface,x,y):
        if self.completed:
            text_surf = utility.font.render(self.city1.name + " to " + self.city2.name + " Points: " + str(self.points) + " Completed", True, (0, 0, 0))
        else:
            text_surf = utility.font.render(self.city1.name + " to " + self.city2.name + " Points: " + str(self.points), True, (0, 0, 0))
        text_rect = text_surf.get_rect(midright=(surface.get_width() - 20, y))
        surface.blit(text_surf, text_rect)