import pygame
import random
import queue
import time
import sys
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont('Corbel',35)


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

class deck:
    def __init__(self):
        self.piles = [0,0,0,0,0]
        self.cards = queue.Queue()
        self.graveyard = [12,12,12,12,12,12,12,12,14]
        total = 110
        while total >0:
            draw = random.randrange(0,9,1)
            if self.graveyard[draw]>0:
                self.graveyard[draw]-=1
                self.cards.put(draw)
                total-=1
        self.piles[0] = self.get()
        self.piles[1] = self.get()
        self.piles[2] = self.get()
        self.piles[3] = self.get()
        self.piles[4] = self.get()

    def get(self):
        ret = self.cards.get()
        if self.cards.empty():
            self.shuffle()
        return ret
    
    def discard(self,color, amount):
        self.graveyard[color]+=amount
        pass
    def shuffle(self):
        total = 0
        for i in self.graveyard:
            total += i
        while total >0:
            draw = random.randrange(0,9,1)
            if self.graveyard[draw]>0:
                self.graveyard[draw]-=1
                self.cards.put(draw)
                total-=1
    def drawfrompile(self,num):
        ret = self.piles[num]
        self.piles[num] = self.get()
        return ret
    def draw(self, play):
        c=1
        #c = ["null","null","null","null","null"]
        #f = 0
        #for i in self.piles:
        #    c[f] = numbertocolor(c[f])
        #    f+=1
        #print(f"1: {c[0]} ,2: {c[1]} , 3: {c[2]} , 4: {c[3]} , 5: {c[4]}")
        #get = int(input("draw whitch: ")) - 1
        #draw = self.drawfrompile(get)
        #play.hand[draw] += 1
        #got = get
        #while draw != 8 & get != got:
        #    get = int(input("draw whitch: ")) - 1
        #    if get != got:
        #        play.hand[self.drawfrompile(get)] += 1*

class player:

    def __init__(self):
        #never call this
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0]
        #self.wild = 0
        self.cars = 45#should be lowered for testing
        deal = 4
        while deal > 0:
            gven = random.randrange(1,4,1)
            if gven <= deal:
                self.hand[random.randrange(0,7,1)] = gven
                deal-=gven
        pass
    def __init__(self, pull):
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0,0]
        self.routes = []
        self.ending =  False
        self.cars = 45#should be lowered for testing
        deal = 4
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        pass
    def spend(self, color, amount, dis):
        if self.cars > amount:
            if amount <= self.hand[color]:
                self.hand[color] -= amount
                self.cars -=amount
                dis.discard(color,amount)
                return True
            elif amount <= self.hand[color] + self.hand[8]:
                spendw = amount - self.hand[color]
                print(f"do you want to spend {spendw} wild cards to buy this rail?\n")
                awns = input("[y/n]: ")
                while True:
                    if awns == "Y":
                        self.hand[color] = 0
                        self.hand[8] -= spendw
                        self.cars -=amount
                        dis.discard(color,amount - spendw)
                        dis.discard(8,spendw)
                        return True
                    elif awns == "N":
                        return False
        
        return False
    
    def draw(self):
        if self.cars <=2:
            self.ending = True
        #print(f"current hand state: red: {self.hand[0]}, green: {self.hand[1]}, blue: {self.hand[2]}, white: {self.hand[3]}, black: {self.hand[4]}, orange: {self.hand[5]}, pink: {self.hand[6]}, yellow: {self.hand[7]}, wild: {self.hand[8]}")
        for i in range(0,8):
            pygame.draw.rect(screen,TRACK_COLORS.get(numbertocolor(i)),[30+(60*i),15,30,40], border_radius=3)
            if i == 4:
                text = font.render(f'{self.hand[i]}' , True , (255,255,255))
            else:
                text = font.render(f'{self.hand[i]}' , True , (0,0,0))
            screen.blit(text,(30+(60*i),15))
        
        pass


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
    def __init__(self):
        self.trackList, self.cityList = self.setUpTracks()
    def setUpTracks(self):
        trackList = []
        cityList = []
        #set up default tracks manually
        a = City("A", 100, 100)
        b = City("B", 100, 300)
        c = City("C", 400, 300)
        d = City("D", 300, 80)

        a.addAdjacent([b,c,d])
        b.addAdjacent([a,c])
        c.addAdjacent([a,b])
        d.addAdjacent([a])

        cityList.append(a)
        cityList.append(b)
        cityList.append(c)
        cityList.append(d)
        
        t1 = Track("red", 4, 0, a, b)
        t2 = Track("blue", 7, 0, a, c)
        t3 = Track("green", 5, 0, b, c)
        t4 = Track("white", 3, 0, a, d)

        trackList.append(t1)
        trackList.append(t2)
        trackList.append(t3)
        trackList.append(t4)

        return trackList, cityList
    def draw_track_segments(self, surface, start_pos, end_pos, length, color):
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

            # 3. Create a surface for the rectangle to rotate it
            rect_surf = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            pygame.draw.rect(rect_surf, color, (0, 0, rect_width, rect_height), border_radius=3)
            pygame.draw.rect(rect_surf, (0, 0, 0), (0, 0, rect_width, rect_height), 2, border_radius=3) # Outline

            # 4. Rotate and blit
            rotated_surf = pygame.transform.rotate(rect_surf, -math.degrees(angle))
            rect_center = rotated_surf.get_rect(center=(center_x, center_y))
            surface.blit(rotated_surf, rect_center)
    def drawMap(self, surface):
        for t in self.trackList:
            start = t.city1.position
            end = t.city2.position
            color = TRACK_COLORS.get(t.color)
            self.draw_track_segments(surface, start, end, t.length, color)
        for c in self.cityList:
            pygame.draw.circle(surface, (50, 50, 50), c.position, 15) 
            pygame.draw.circle(surface, (255, 215, 0), c.position, 12)


cards = deck()
user = player(cards)
map = Map()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    map.drawMap(screen)

    if user.ending:
        print(f"game over you got: {user.score} points")
        input("end game?: ")
        pygame.quit()
        sys.exit()
    #commented these out for now so it doesn't freeze and I can see the drawn map
    user.draw() 
    #cards.draw(user)
    #input("continue?: ")
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()

