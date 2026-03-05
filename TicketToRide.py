import pygame
import random
import queue
import time
import sys
import math
from collections import deque
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ticket to Ride")
clock = pygame.time.Clock()
running = True
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


def buytrack(player, track, deck):
    # 1. Make sure track is not already claimed
    if track.Owner is not None:
        message_log.add("Track already claimed.")
        return False

    # 2. Try to spend cards equal to the track length
    # track.color must be a number 0–8 
    numofcolor = colortonumber(track.color)
    
    success = player.spend(numofcolor, track.length, deck)
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

class deck:
    def __init__(self):
        self.piles = [0,0,0,0,0]
        self.cards = queue.Queue()
        self.graveyard = [12,12,12,12,12,12,12,12,14]
        self.todraw = [9,9]
        self.drawfirst = False
        self.routedrawbutton = pygame.Rect(screen.get_width() -250, 100, 230, 40)
        self.carddrawbuttons = []
        for i in range(0,5):
            self.carddrawbuttons.append(pygame.Rect(30+(120*i),350,100,40))
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
        self.routeCards = []
        self.awns = 0

    def get(self):
        ret = self.cards.get()
        if self.cards.empty():
            self.shuffle()
        return ret
   
    def drawroutes(self, user, given):
        choice = Choicemenu(self, ['1','2','3'], "chose at least one of these three cards: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points))
        screenshot = screen.copy()
        self.awns = 0

        # First (mandatory) pick
        while self.awns != '1' and self.awns != '2' and self.awns != '3':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice.buttoncheck()
            screen.fill("grey")
            screen.blit(screenshot, (0, 0))
            choice.draw()
            pygame.display.flip()

        first_idx = int(self.awns) - 1
        selected = [first_idx]
        del choice

        # Second (optional) pick or 'no'
        opts2 = [o for o in ['1','2','3'] if (int(o)-1) != first_idx] + ['no']
        choice = Choicemenu(self, opts2, "take another?: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points) + ", no")
        self.awns = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice.buttoncheck()
            if self.awns in opts2:
                if self.awns == 'no':
                    # finalize 1 pick
                    for idx in sorted(selected, reverse=True):
                        user.routeCardList.append(given[idx])
                        self.routeCards.remove(given[idx])
                    user.checkRouteCompletion()
                    del choice
                    return
                else:
                    second_idx = int(self.awns) - 1
                    selected.append(second_idx)
                    break

            screen.fill("grey")
            screen.blit(screenshot, (0, 0))
            choice.draw()
            pygame.display.flip()

        del choice

        # Third (optional): take the last remaining one? [y/n]
        last_idx = ({0,1,2} - set(selected)).pop()
        choice = Choicemenu(self, ['y','n'], "take the last card?: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points) + ", no")
        self.awns = 0
        while self.awns not in ('y','Y','n','N'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice.buttoncheck()
            screen.fill("grey")
            screen.blit(screenshot, (0, 0))
            choice.draw()
            pygame.display.flip()

        if self.awns in ('y','Y'):
            selected.append(last_idx)

        # finalize 2 or 3 picks
        for idx in sorted(selected, reverse=True):
            user.routeCardList.append(given[idx])
            self.routeCards.remove(given[idx])
        user.checkRouteCompletion()
        del choice
        return

            
    def findpusedbuttons(self,user):
        if self.routedrawbutton.collidepoint(pygame.mouse.get_pos()):
            if len(self.routeCards) < 3:
                message_log.add("Not enough route cards remaining to draw (need 3).")
                return
            exclude = []
            one = random.randrange(0,len(self.routeCards),1)
            exclude.append(one)
            two =  random.choice([i for i in range(len(self.routeCards)) if i not in exclude])
            exclude.append(two)
            three = random.choice([i for i in range(len(self.routeCards)) if i not in exclude])
            self.drawroutes(user,[self.routeCards[one],self.routeCards[two],self.routeCards[three]])
            return
        for i in range(0,5):
            if self.carddrawbuttons[i].collidepoint(pygame.mouse.get_pos()):
                
                self.todraw[self.drawfirst] = i
                if self.piles[i] != 8:
                    self.drawfirst = not self.drawfirst
                else:
                    self.todraw[0] = i
                    self.todraw[1] = 9
                    self.drawfirst = False
                    
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
    def drawfrompile(self,user):
        if self.todraw[0] != 9:
            user.addtohand(self.piles[self.todraw[0]])
            if self.todraw[1] != 9:
                user.addtohand(self.piles[self.todraw[1]])
            if self.todraw[0] != 9:
                self.piles[self.todraw[0]] = self.get()
            if self.todraw[1] != 9:
                self.piles[self.todraw[1]] = self.get()
            self.todraw[1] = 9
            self.todraw[0] = 9
            self.drawfirst = False
        
    def draw(self):
        pygame.draw.rect(screen,TRACK_COLORS.get("red"),self.routedrawbutton, border_radius=3)
        text = font.render('Draw new route' , True , (0,0,0))
        screen.blit(text, text.get_rect(center=self.routedrawbutton.center))
        for i in range(0,5):
            pygame.draw.rect(screen,TRACK_COLORS.get(numbertocolor(self.piles[i])),[30+(120*i),350,100,40], border_radius=3)
            if i == self.todraw[0] or i == self.todraw[1]:
                pygame.draw.rect(screen,(0,0,0),[30+(120*i),350,100,40], 2,border_radius=3)
            if self.piles[i] == 4:
                text = font.render(f'{i+1}' , True , (255,255,255))
            else:
                text = font.render(f'{i+1}' , True , (0,0,0))
            screen.blit(text, text.get_rect(center=(30+(120*i)+50, 350+20)))
        

class player:

    def __init__(self, pull):
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0,0]
        self.routes = []
        self.ending =  False
        self.cars = 17#real max should be 45
        deal = 4
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.adjacencyList = {}
        self.routeCardList = []
        self.ownedTrackList = []
        self.awns = 0
        pass
    def spend(self, color, amount, dis):
        if self.cars > amount:
            if amount <= self.hand[color]:
                self.hand[color] -=amount
                self.cars -=amount
                dis.discard(color,amount)
                return True
            elif amount <= self.hand[color] + self.hand[8]:
                spendw = amount - self.hand[color]
                choice = Choicemenu(self,['y','n'],f"do you want to spend {spendw} wild cards to buy this rail?")
                screenshot = screen.copy()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            choice.buttoncheck()

                    if self.awns == 'Y' or self.awns == 'y':
                        self.hand[color] = 0
                        self.hand[8] -= spendw
                        self.cars -=amount
                        dis.discard(color,amount - spendw)
                        dis.discard(8,spendw)
                        del choice
                        return True
                    elif self.awns == 'N' or self.awns == 'n':
                        del choice
                        return False
                    screen.fill("grey")
                    screen.blit(screenshot, (0, 0))  
                    choice.draw()
                    pygame.display.flip()
        
        return False
    def addtohand(self,color):
        self.hand[color] +=1
    def draw(self):
        if self.cars <=2:
            self.ending = True
        for i in range(0,9):
            pygame.draw.rect(screen,TRACK_COLORS.get(numbertocolor(i)),[30+(60*i),15,30,40], border_radius=3)
            if i == 4:
                text = font.render(f'{self.hand[i]}' , True , (255,255,255))
            else:
                text = font.render(f'{self.hand[i]}' , True , (0,0,0))
            screen.blit(text, text.get_rect(center=(30+(60*i)+15, 15+20)))
            i = 0 
        for r in self.routeCardList:
            r.drawRouteCard(screen,1000,200+(100*i))
            i+=1
        
        traintext = font.render(f"Trains: {self.cars}", True, (0,0,0))
        trainrect = traintext.get_rect(bottomright=(screen.get_width() - 20, screen.get_height() - 20))
        screen.blit(traintext, trainrect)

        pass
    def addConnection(self, city_a, city_b):
        if city_a not in self.adjacencyList:
            self.adjacencyList[city_a] = []
        if city_b not in self.adjacencyList:
            self.adjacencyList[city_b] = []
        
        self.adjacencyList[city_a].append(city_b)
        self.adjacencyList[city_b].append(city_a)
    def checkRouteCompletion(self):
        for r in self.routeCardList:
            if not r.completed:
                start = r.city1
                end = r.city2
                if self.checkConnection(start, end):
                    message_log.add("Route from "+r.city1.name+" to "+r.city2.name+" Completed")
                    self.score += r.points
                    r.completed = True
                    message_log.add("Your Score: " + str(user.score))
    def checkConnection(self, start, end):
        # If the player hasn't even visited these cities, they aren't connected
        if start not in self.adjacencyList or end not in self.adjacencyList:
            return False
            
        # Standard BFS setup
        queue_ = deque([start])
        visited = {start}
        
        while queue_:
            current_city = queue_.popleft()
            
            # Did we find the destination?
            if current_city == end:
                return True
            
            # Check all neighbors of the current city
            for neighbor in self.adjacencyList[current_city]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue_.append(neighbor)
                    
        return False # No path found after checking everything

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
            text_surf = font.render(c.name, True, (0, 0, 0))
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
            text_surf = font.render(self.city1.name + " to " + self.city2.name + " Points: " + str(self.points) + " Completed", True, (0, 0, 0))
        else:
            text_surf = font.render(self.city1.name + " to " + self.city2.name + " Points: " + str(self.points), True, (0, 0, 0))
        text_rect = text_surf.get_rect(midright=(surface.get_width() - 20, y))
        surface.blit(text_surf, text_rect)

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

    def draw(self):
        for i in range(len(self.options)):
            pygame.draw.rect(screen,(0,0,0),(30+(120*i),500,100,40),border_radius=3)
            text = font.render(f"{self.options[i]}" , True , (255,255,255))
            screen.blit(text,(50+(120*i),500))
            screen.blit(self.text,(50,450))


choice = -1
cards = deck()
user = player(cards)
map = Map(cards.routeCards)

#test codes
user.routeCardList.append(cards.routeCards[0])
del cards.routeCards[0]
#for i in range(9):
#    user.hand[i] = 20

game_over = False
game_over_processed = False
exit_button = pygame.Rect(500, 300, 280, 60)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left mouse click
                    mousepos = pygame.mouse.get_pos()

                    track = findtrackundermouse(mousepos, map)

                    if track is not None:
                        success = buytrack(user, track, cards)

                        if success:
                            message_log.add("Track bought!")
                            message_log.add("Your Score: " + str(user.score))
                            user.checkRouteCompletion()
                        else:
                            message_log.add("Could not buy this track.")
                    else:
                        cards.findpusedbuttons(user)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cards.drawfrompile(user)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    map.drawMap(screen)

    if user.ending and not game_over_processed:
        for r in user.routeCardList:
            if not r.completed:
                user.score -= r.points
        message_log.add(f"game over you got: {user.score} points")
        game_over = True
        game_over_processed = True

    user.draw() 
    cards.draw()
    message_log.draw(screen)

    if game_over:
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        screen.blit(overlay, (0, 0))

        title = font.render("Game Over", True, (255, 255, 255))
        score_txt = font.render(f"Final Score: {user.score}", True, (255, 255, 255))
        tip_txt = smallfont.render("Click Exit to close the game", True, (220, 220, 220))

        screen.blit(title, (520, 180))
        screen.blit(score_txt, (500, 230))
        screen.blit(tip_txt, (520, 265))

        pygame.draw.rect(screen, (200, 60, 60), exit_button, border_radius=8)
        exit_label = font.render("Exit", True, (255, 255, 255))
        label_rect = exit_label.get_rect(center=exit_button.center)
        screen.blit(exit_label, label_rect.topleft)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()