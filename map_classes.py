import pygame
import random
import queue
import time
import sys
import math
import utility; print('Import successful')
from player_classes import player, enemy
from collections import deque
from collections import defaultdict

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
        # --- 1. Northern & Western Europe ---
        edinburgh = City("Edinburgh", 200, 120)
        london = City("London", 230, 220)
        dieppe = City("Dieppe", 240, 290)
        brest = City("Brest", 170, 330)
        paris = City("Paris", 300, 310)
        bruxelles = City("Bruxelles", 330, 240)
        amsterdam = City("Amsterdam", 310, 200)
        essen = City("Essen", 410, 200)
        frankfurt = City("Frankfurt", 410, 260)
        berlin = City("Berlin", 520, 190)
        danzig = City("Danzig", 640, 150)
        copenhagen = City("Kobenhavn", 490, 120)
        stockholm = City("Stockholm", 590, 70)

        # --- 2. Central Europe ---
        munchen = City("Munchen", 490, 300)
        zurich = City("Zurich", 410, 350)
        wien = City("Wien", 590, 300)
        warszawa = City("Warszawa", 660, 200)
        wilno = City("Wilno", 750, 190)
        budapest = City("Budapest", 640, 340)

        # --- 3. Southern Europe & Mediterranean ---
        madrid = City("Madrid", 180, 470)
        lisboa = City("Lisboa", 80, 520)
        cadiz = City("Cadiz", 140, 580)
        barcelona = City("Barcelona", 250, 510)
        pamplona = City("Pamplona", 230, 420)
        marseille = City("Marseille", 370, 460)
        venezia = City("Venezia", 480, 390)
        roma = City("Roma", 490, 480)
        brindisi = City("Brindisi", 580, 510)
        palermo = City("Palermo", 520, 580)
        athens = City("Athina", 700, 530)

        # --- 4. Eastern Europe & Balkans ---
        petrograd = City("Petrograd", 880, 70)
        riga = City("Riga", 730, 110)
        moskva = City("Moskva", 940, 190)
        smolensk = City("Smolensk", 880, 220)
        kyiv = City("Kyiv", 770, 260)
        kharkov = City("Kharkov", 910, 300)
        rostov = City("Rostov", 940, 370)
        sochi = City("Sochi", 950, 450)
        sevastopol = City("Sevastopol", 860, 400)
        bucuresti = City("Bucuresti", 740, 370)
        sofia = City("Sofia", 740, 470)
        sarajevo = City("Sarajevo", 640, 440)
        zagrab = City("Zagrab", 550, 380)
        constantinople = City("Constantinople", 820, 480)
        angora = City("Angora", 850, 560)
        erzurum = City("Erzurum", 970, 530)
        smyrna = City("Smyrna", 760, 580)

        cityList.extend([
            edinburgh, london, dieppe, brest, paris, bruxelles, amsterdam, essen, frankfurt, berlin, danzig,
            munchen, zurich, wien, warszawa, wilno, budapest,
            madrid, lisboa, cadiz, barcelona, pamplona, marseille, venezia, roma, brindisi, palermo, athens,
            petrograd, riga, moskva, smolensk, kyiv, kharkov, rostov, sochi, sevastopol, bucuresti, sofia, 
            sarajevo, zagrab, constantinople, angora, erzurum, smyrna, copenhagen, stockholm
        ])

        self.routeList.append(self.createRouteCard(edinburgh, constantinople, 21)) # Long Route
        self.routeList.append(self.createRouteCard(berlin, roma, 9))
        self.routeList.append(self.createRouteCard(paris, wien, 8))
        self.routeList.append(self.createRouteCard(amsterdam, budapest, 13))

        raw_tracks = [
            # Western / UK
            (edinburgh, london, "orange", 4, True),
            (edinburgh, london, "black", 4, True),
            (london, amsterdam, "wild", 2, False),
            (london, dieppe, "wild", 2, True),
            (london, dieppe, "wild", 2, True),
            (dieppe, brest, "orange", 2, False),
            (dieppe, paris, "pink", 1, False),
            (dieppe, bruxelles, "green", 2, False),
            (brest, paris, "black", 3, False),
            (brest, pamplona, "pink", 4, False),
            (paris, bruxelles, "yellow", 2, True),
            (paris, bruxelles, "red", 2, True),
            (paris, frankfurt, "white", 3, True),
            (paris, frankfurt, "orange", 3, True),
            (paris, zurich, "wild", 3, False),
            (paris, marseille, "wild", 4, False),
            (paris, pamplona, "blue", 4, False),
            (paris, pamplona, "green", 4, False),

            # Central / Northern
            (amsterdam, bruxelles, "black", 1, False),
            (amsterdam, essen, "yellow", 3, False),
            (amsterdam, frankfurt, "white", 2, False),
            (bruxelles, frankfurt, "blue", 2, False),
            (essen, berlin, "blue", 2, False),
            (essen, frankfurt, "green", 2, False),
            (frankfurt, berlin, "black", 3, True),
            (frankfurt, berlin, "red", 3, True),
            (frankfurt, munchen, "pink", 2, False),
            (berlin, danzig, "wild", 4, False),
            (berlin, warszawa, "pink", 4, True),
            (berlin, warszawa, "yellow", 4, True),
            (berlin, wien, "green", 3, False),
            (munchen, zurich, "yellow", 2, False),
            (munchen, venezia, "blue", 2, False),
            (munchen, wien, "orange", 3, False),
            (wien, warszawa, "blue", 4, False),
            (copenhagen, essen, "wild", 3, False),
            (copenhagen, essen, "wild", 3, False),
            (copenhagen, stockholm, "yellow", 3, False),
            (copenhagen, stockholm, "white", 3, False),
            (stockholm, petrograd, "wild", 8, False),

            # Southern / Iberian
            (lisboa, cadiz, "blue", 2, False),
            (lisboa, madrid, "pink", 3, False),
            (madrid, cadiz, "orange", 3, False),
            (madrid, pamplona, "black", 3, True),
            (madrid, pamplona, "white", 3, True),
            (madrid, barcelona, "yellow", 2, False),
            (pamplona, barcelona, "wild", 2, False),
            (pamplona, marseille, "red", 4, False),
            (barcelona, marseille, "wild", 4, False),
            (marseille, roma, "wild", 4, False),
            (marseille, zurich, "pink", 2, False),
            (roma, venezia, "black", 2, False),
            (roma, brindisi, "white", 2, False),
            (roma, palermo, "wild", 4, False),
            (palermo, brindisi, "wild", 3, False),
            (venezia, zagrab, "wild", 2, False),
            (venezia, zurich, "green", 2, False),

            # Eastern / Balkans
            (danzig, riga, "black", 3, False),
            (riga, wilno, "green", 4, False),
            (riga, petrograd, "wild", 4, False),
            (petrograd, wilno, "blue", 4, False),
            (petrograd, moskva, "white", 4, False),
            (wilno, warszawa, "red", 3, False),
            (wilno, kyiv, "wild", 2, False),
            (wilno, smolensk, "yellow", 3, False),
            (warszawa, kyiv, "wild", 4, False),
            (warszawa, wien, "blue", 4, False),
            (warszawa, danzig, "wild", 2, False),
            (wien, budapest, "white", 1, True),
            (wien, budapest, "red", 1, True),
            (wien, zagrab, "wild", 2, False),
            (budapest, zagrab, "orange", 2, False),
            (budapest, sarajevo, "pink", 3, False),
            (budapest, kyiv, "wild", 6, False),
            (kyiv, smolensk, "red", 3, False),
            (kyiv, kharkov, "wild", 4, False),
            (kyiv, bucuresti, "wild", 4, False),
            (kharkov, moskva, "wild", 4, False),
            (smolensk, moskva, "orange", 2, False),
            (kharkov, rostov, "green", 2, False),
            (kharkov, kyiv, "wild", 4, False),
            (rostov, sevastopol, "wild", 4, False),
            (rostov, sochi, "wild", 2, False),
            (bucuresti, budapest, "wild", 4, False),
            (bucuresti, sevastopol, "white", 4, False),
            (bucuresti, constantinople, "yellow", 3, False),
            (bucuresti, sofia, "wild", 2, False),
            (sarajevo, zagrab, "red", 3, False),
            (sarajevo, sofia, "wild", 2, False),
            (sarajevo, athens, "green", 4, False),
            (athens, sofia, "pink", 3, False),
            (athens, smyrna, "wild", 2, False),
            (athens, brindisi, "wild", 4, False),
            (constantinople, sevastopol, "wild", 4, False),
            (constantinople, sofia, "blue", 3, False),
            (constantinople, smyrna, "wild", 2, False),
            (constantinople, angora, "wild", 2, False),
            (smyrna, angora, "orange", 3, False),
            (smyrna, palermo, "wild", 6, False),
            (angora, erzurum, "black", 3, False),
            (erzurum, sochi, "red", 3, False),
            (sevastopol, sochi, "wild", 2, False),
            (sevastopol, erzurum, "wild", 4, False)
        ]

        # Batch process the data into your Track objects
        trackList = []
        for c1, c2, color, length, is_double in raw_tracks:
            # Create the track object
            new_track = Track(color, length, 0, c1, c2)
            trackList.append(new_track)
            
            # 2. Update Adjacency (The Graph)
            # We only add the neighbor if it's not already in the list
            # This prevents double-routes from breaking BFS/Dijkstra logic
            if c2 not in c1.adjacent:
                c1.addAdjacent([c2])
            if c1 not in c2.adjacent:
                c2.addAdjacent([c1])

        return trackList, cityList
    def createRouteCard(self, city1, city2, points):
        newCard = RouteCard(city1, city2, points)
        return newCard
    def draw_track_segments(self, surface, start_pos, end_pos, length, color, track_index=0, total_tracks=1, highlight_color=None, highlight_thickness=8):
        # 1. Calculate the distance and angle between cities
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # --- OFFSET CALCULATION ---
        perp_angle = angle + math.pi / 2
        track_spacing = 15 
        total_offset_width = (total_tracks - 1) * track_spacing
        offset_start = -total_offset_width / 2
        current_offset = offset_start + (track_index * track_spacing)
        offset_x = math.cos(perp_angle) * current_offset
        offset_y = math.sin(perp_angle) * current_offset

        # 2. Dimensions of each train car rectangle
        rect_width = (distance / length) * 0.8  # 80% of segment space for gap
        rect_height = 10 

        for i in range(length):
            # Calculate center point for each segment
            # We offset by 0.5 to center the segments between cities
            fraction = (i + 0.5) / length
            base_center_x = start_pos[0] + dx * fraction
            base_center_y = start_pos[1] + dy * fraction

            center_x = base_center_x + offset_x
            center_y = base_center_y + offset_y

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
        # 1. Group tracks by their city connections
        connection_groups = defaultdict(list)
        for t in self.trackList:
            connection_id = frozenset([t.city1.name, t.city2.name])
            connection_groups[connection_id].append(t)

        # 2. Draw grouped tracks with side-by-side logic
        for group in connection_groups.values():
            total_tracks = len(group)
            for index, t in enumerate(group):
                start = t.city1.position
                end = t.city2.position
                color = utility.TRACK_COLORS.get(t.color)

                highlight = None

                if isinstance(t.Owner, player):
                    highlight = (255, 255, 150, 180)

                elif isinstance(t.Owner, enemy):
                    highlight = (255, 80, 80, 180)
                
                # Pass the index and total count to your updated draw_track_segments
                self.draw_track_segments(
                    surface, start, end, t.length, color, 
                    track_index=index, 
                    total_tracks=total_tracks,
                    highlight_color=highlight
                )
        
        for c in self.cityList:
            pygame.draw.circle(surface, (50, 50, 50), c.position, 12) 
            pygame.draw.circle(surface, (255, 215, 0), c.position, 9)
            text_surf = utility.smallfontBold.render(c.name, True, (255, 255, 255))
            text_rect = text_surf.get_rect(midright=(c.position[0] - 0 + 2, c.position[1] - 20 + 2))
            surface.blit(text_surf, text_rect)
            text_surf = utility.smallfontBold.render(c.name, True, (0, 0, 0))
            text_rect = text_surf.get_rect(midright=(c.position[0] - 0, c.position[1] - 20))
            surface.blit(text_surf, text_rect)
            
    
    def get_tracks_touching_city(self, city):
        return [t for t in self.trackList if t.city1 == city or t.city2 == city]


class RouteCard:
    def __init__(self, city1, city2, points):
        self.city1 = city1
        self.city2 = city2
        self.points = points
        self.completed = False
    def drawRouteCard(self, surface, x, y):
        # Line 1: City Names
        city_text = f"{self.city1.name} to {self.city2.name}"
        city_surf = utility.mediumFontBold.render(city_text, True, (0, 0, 0))
        
        # Line 2: Points and Status
        status = " (Completed)" if self.completed else ""
        points_text = f"Points: {self.points}{status}"
        points_surf = utility.mediumFont.render(points_text, True, (0, 0, 0))

        # Position Line 1 slightly above the original center 'y'
        city_rect = city_surf.get_rect(midright=(surface.get_width() - 20, y - 12))
        
        # Position Line 2 slightly below the original center 'y'
        points_rect = points_surf.get_rect(midright=(surface.get_width() - 20, y + 12))

        # Draw both lines
        surface.blit(city_surf, city_rect)
        surface.blit(points_surf, points_rect)