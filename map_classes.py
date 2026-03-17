import pygame
import random
import queue
import time
import sys
import math
import utility; print('Import successful')
from collections import deque
from collections import defaultdict

class Track:
    def __init__(self, color, length, wildReq, city1, city2):
        self.Owner = None
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
        edinburgh = City("Edinburgh", 200, 100)
        london = City("London", 200, 210)
        dieppe = City("Dieppe", 210, 290)
        brest = City("Brest", 130, 330)
        paris = City("Paris", 270, 310)
        bruxelles = City("Bruxelles", 310, 230)
        amsterdam = City("Amsterdam", 340, 190)
        essen = City("Essen", 400, 180)
        frankfurt = City("Frankfurt", 400, 250)
        berlin = City("Berlin", 520, 170)
        danzig = City("Danzig", 600, 130)

        # --- 2. Central Europe ---
        munchen = City("Munchen", 480, 300)
        zurich = City("Zurich", 390, 350)
        wien = City("Wien", 600, 300)
        warszawa = City("Warszawa", 670, 180)
        wilno = City("Wilno", 770, 130)
        budapest = City("Budapest", 650, 340)
        praha = City("Praha", 550, 250)

        # --- 3. Southern Europe & Mediterranean ---
        madrid = City("Madrid", 140, 490)
        lisboa = City("Lisboa", 110, 550)
        cadiz = City("Cadiz", 140, 610)
        barcelona = City("Barcelona", 220, 530)
        pamplona = City("Pamplona", 190, 430)
        marseille = City("Marseille", 300, 470)
        nice = City("Nice", 360, 450)
        venezia = City("Venezia", 470, 400)
        roma = City("Roma", 480, 500)
        brindisi = City("Brindisi", 580, 530)
        palermo = City("Palermo", 520, 610)
        athens = City("Athina", 720, 600)

        # --- 4. Eastern Europe & Balkans ---
        petrograd = City("Petrograd", 860, 80)
        riga = City("Riga", 730, 90)
        moskva = City("Moskva", 880, 170)
        smolensk = City("Smolensk", 820, 210)
        kyiv = City("Kyiv", 800, 290)
        kharkov = City("Kharkov", 880, 300)
        rostov = City("Rostov", 880, 400)
        sochi = City("Sochi", 870, 460)
        sevastopol = City("Sevastopol", 800, 420)
        bucuresti = City("Bucuresti", 760, 370)
        sofia = City("Sofia", 710, 450)
        sarajevo = City("Sarajevo", 600, 430)
        zagrab = City("Zagrab", 550, 390)
        constantinople = City("Constantinople", 850, 520)
        angora = City("Angora", 880, 580)
        erzurum = City("Erzurum", 890, 630)
        smyrna = City("Smyrna", 780, 610)

        # --- 1. Western Europe & British Isles ---
        edinburgh.addAdjacent([london])
        london.addAdjacent([edinburgh, dieppe, amsterdam])
        dieppe.addAdjacent([london, brest, paris, bruxelles])
        brest.addAdjacent([dieppe, paris, pamplona])
        paris.addAdjacent([dieppe, brest, pamplona, marseille, zurich, bruxelles, frankfurt])
        bruxelles.addAdjacent([dieppe, amsterdam, paris, frankfurt])
        amsterdam.addAdjacent([london, bruxelles, essen, frankfurt])

        # --- 2. Central Europe & Germany ---
        essen.addAdjacent([amsterdam, bruxelles, frankfurt, berlin])
        frankfurt.addAdjacent([amsterdam, essen, berlin, praha, munchen, zurich, bruxelles, paris])
        berlin.addAdjacent([essen, frankfurt, praha, warszawa, danzig])
        danzig.addAdjacent([berlin, warszawa, riga])
        munchen.addAdjacent([frankfurt, zurich, venezia, wien, praha])
        zurich.addAdjacent([paris, munchen, venezia, marseille])
        praha.addAdjacent([berlin, frankfurt, munchen, wien, warszawa])

        # --- 3. Iberian Peninsula & Mediterranean ---
        lisboa.addAdjacent([cadiz, madrid])
        madrid.addAdjacent([lisboa, cadiz, barcelona, pamplona])
        cadiz.addAdjacent([lisboa, madrid])
        pamplona.addAdjacent([madrid, brest, paris, marseille, barcelona])
        barcelona.addAdjacent([madrid, pamplona, marseille])
        marseille.addAdjacent([barcelona, pamplona, paris, zurich, nice])
        nice.addAdjacent([marseille, zurich, venezia, roma])
        roma.addAdjacent([nice, venezia, brindisi, palermo])
        palermo.addAdjacent([roma, brindisi, athens])
        brindisi.addAdjacent([roma, palermo, athens])
        venezia.addAdjacent([zurich, munchen, zagrab, roma, nice])

        # --- 4. Eastern Europe & Balkans ---
        warszawa.addAdjacent([berlin, danzig, wilno, kyiv, wien, praha])
        wilno.addAdjacent([riga, petrograd, smolensk, kyiv, warszawa])
        riga.addAdjacent([danzig, wilno, petrograd])
        petrograd.addAdjacent([riga, wilno, moskva])
        moskva.addAdjacent([petrograd, smolensk, kharkov])
        smolensk.addAdjacent([wilno, moskva, kyiv])
        kyiv.addAdjacent([wilno, warszawa, budapest, bucuresti, smolensk, kharkov])
        kharkov.addAdjacent([moskva, kyiv, rostov])
        rostov.addAdjacent([kharkov, sochi, sevastopol])
        wien.addAdjacent([praha, warszawa, budapest, zagrab, munchen])
        budapest.addAdjacent([wien, zagrab, sarajevo, bucuresti, kyiv])
        zagrab.addAdjacent([wien, venezia, sarajevo, budapest])
        sarajevo.addAdjacent([zagrab, budapest, sofia, athens])
        athens.addAdjacent([brindisi, palermo, sarajevo, sofia, smyrna])
        sofia.addAdjacent([sarajevo, bucuresti, constantinople, athens])
        bucuresti.addAdjacent([budapest, kyiv, sevastopol, constantinople, sofia])
        sevastopol.addAdjacent([bucuresti, kyiv, rostov, sochi, constantinople])
        sochi.addAdjacent([rostov, sevastopol, erzurum])

        # --- 5. Turkey & Middle East ---
        constantinople.addAdjacent([sofia, bucuresti, sevastopol, angora, smyrna])
        smyrna.addAdjacent([athens, constantinople, angora])
        angora.addAdjacent([constantinople, smyrna, erzurum])
        erzurum.addAdjacent([angora, sochi])

        cityList.extend([
            edinburgh, london, dieppe, brest, paris, bruxelles, amsterdam, essen, frankfurt, berlin, danzig,
            munchen, zurich, wien, warszawa, wilno, budapest, praha,
            madrid, lisboa, cadiz, barcelona, pamplona, marseille, nice, venezia, roma, brindisi, palermo, athens,
            petrograd, riga, moskva, smolensk, kyiv, kharkov, rostov, sochi, sevastopol, bucuresti, sofia, 
            sarajevo, zagrab, constantinople, angora, erzurum, smyrna
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
            (dieppe, paris, "wild", 1, False),
            (dieppe, bruxelles, "green", 2, False),
            (brest, paris, "black", 3, False),
            (brest, pamplona, "pink", 4, False),
            (paris, bruxelles, "yellow", 2, True),
            (paris, bruxelles, "red", 2, True),
            (paris, frankfurt, "white", 3, True),
            (paris, frankfurt, "orange", 3, True),
            (paris, zurich, "wild", 3, False),
            (paris, marseille, "wild", 4, False),

            # Central / Northern
            (amsterdam, bruxelles, "black", 1, False),
            (amsterdam, essen, "yellow", 3, False),
            (amsterdam, frankfurt, "white", 2, False),
            (bruxelles, frankfurt, "blue", 2, False),
            (essen, berlin, "blue", 4, False),
            (essen, frankfurt, "green", 2, False),
            (frankfurt, berlin, "black", 3, True),
            (frankfurt, berlin, "red", 3, True),
            (frankfurt, munchen, "pink", 2, False),
            (berlin, danzig, "wild", 4, False),
            (berlin, warszawa, "pink", 4, True),
            (berlin, warszawa, "yellow", 4, True),
            (berlin, praha, "red", 3, False),
            (munchen, zurich, "yellow", 2, False),
            (munchen, venezia, "blue", 2, False),
            (munchen, wien, "orange", 3, False),
            (praha, wien, "yellow", 3, False),
            (praha, warszawa, "wild", 4, False),

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
            (marseille, nice, "wild", 2, False),
            (nice, zurich, "wild", 3, False),
            (nice, roma, "wild", 4, False),
            (roma, venezia, "black", 2, False),
            (roma, brindisi, "white", 2, False),
            (roma, palermo, "wild", 4, False),
            (palermo, brindisi, "wild", 3, False),
            (palermo, athens, "wild", 4, False),
            (venezia, zagrab, "wild", 2, False),

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
            (wien, budapest, "white", 1, True),
            (wien, budapest, "red", 1, True),
            (wien, zagrab, "wild", 2, False),
            (budapest, zagrab, "orange", 2, False),
            (budapest, sarajevo, "pink", 3, False),
            (budapest, kyiv, "wild", 6, False),
            (kyiv, smolensk, "wild", 3, False),
            (kyiv, kharkov, "wild", 4, False),
            (kyiv, bucuresti, "wild", 4, False),
            (kharkov, moskva, "wild", 4, False),
            (kharkov, rostov, "green", 2, False),
            (rostov, moskva, "wild", 2, False),
            (rostov, sevastopol, "wild", 4, False),
            (rostov, sochi, "wild", 2, False),
            (bucuresti, budapest, "wild", 4, False),
            (bucuresti, sevastopol, "white", 4, False),
            (bucuresti, constantinople, "yellow", 3, False),
            (bucuresti, sofia, "wild", 2, False),
            (sarajevo, zagrab, "red", 3, False),
            (sarajevo, sofia, "wild", 2, False),
            (sarajevo, athens, "wild", 4, False),
            (athens, sofia, "pink", 3, False),
            (athens, smyrna, "wild", 2, False),
            (constantinople, sevastopol, "wild", 4, False),
            (constantinople, sofia, "blue", 3, False),
            (constantinople, smyrna, "wild", 2, False),
            (constantinople, angora, "wild", 2, False),
            (smyrna, angora, "orange", 3, False),
            (angora, erzurum, "wild", 3, False),
            (erzurum, sochi, "red", 3, False),
            (sevastopol, sochi, "wild", 1, False)
        ]

        # Batch process the data into your Track objects
        trackList = []
        for c1, c2, color, length, is_double in raw_tracks:
            # Create the track object
            new_track = Track(color, length, 0, c1, c2)
            trackList.append(new_track)
            
            # Add to adjacency list (only if not already there to avoid duplicates in BFS)
            c1.addAdjacent([c2])
            c2.addAdjacent([c1])

        return trackList, cityList
    def createRouteCard(self, city1, city2, points):
        newCard = RouteCard(city1, city2, points)
        return newCard
    def draw_track_segments(self, surface, start_pos, end_pos, length, color, track_index=0, total_tracks=1):
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

            # 3. Create a surface for the rectangle to rotate it
            rect_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surf, color, (0, 0, rect_width, rect_height), border_radius=3)
            pygame.draw.rect(rect_surf, (0, 0, 0), (0, 0, rect_width, rect_height), 2, border_radius=3) # Outline

            # 4. Rotate and blit
            rotated_surf = pygame.transform.rotate(rect_surf, -math.degrees(angle))
            rect_center = rotated_surf.get_rect(center=(center_x, center_y))
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
                
                # Pass the index and total count to your updated draw_track_segments
                self.draw_track_segments(
                    surface, start, end, t.length, color, 
                    track_index=index, 
                    total_tracks=total_tracks
                )
        
        for c in self.cityList:
            pygame.draw.circle(surface, (50, 50, 50), c.position, 12) 
            pygame.draw.circle(surface, (255, 215, 0), c.position, 9)
            text_surf = utility.smallfont.render(c.name, True, (0, 0, 0))
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