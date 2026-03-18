import pygame
import random
import queue
import time
import sys
import math
import utility; print('Import successful')
from collections import deque

class deck:
    def __init__(self, screen):
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
   
    def drawroutes(self, user, given, screen):
        self.awns = None
        choice = utility.Choicemenu(self, ['1','2','3'], "chose at least one of these three cards: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points))
        screenshot = screen.copy()

        # First (mandatory) pick
        while self.awns != '1' and self.awns != '2' and self.awns != '3':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice.buttoncheck()
            screen.fill("grey")
            screen.blit(screenshot, (0, 0))
            choice.draw(screen)
            pygame.display.flip()

        first_idx = int(self.awns) - 1
        selected = [first_idx]
        del choice

        # Second (optional) pick or 'no'
        opts2 = [o for o in ['1','2','3'] if (int(o)-1) != first_idx] + ['no']
        self.awns = None
        choice = utility.Choicemenu(self, opts2, "take another?: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points) + ", no")
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
            choice.draw(screen)
            pygame.display.flip()

        del choice

        # Third (optional): take the last remaining one? [y/n]
        last_idx = ({0,1,2} - set(selected)).pop()
        self.awns = None
        choice = utility.Choicemenu(self, ['y','n'], "take the last card?: " + given[0].city1.name + " to " + given[0].city2.name + " Points: " + str(given[0].points) + ", " + given[1].city1.name + " to " + given[1].city2.name + " Points: " + str(given[1].points) + ", " + given[2].city1.name + " to " + given[2].city2.name + " Points: " + str(given[2].points) + ", no")
        while self.awns not in ('y','Y','n','N'):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    choice.buttoncheck()
            screen.fill("grey")
            screen.blit(screenshot, (0, 0))
            choice.draw(screen)
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

    def cpudrawroutes(self,cpu,amount):
        if len(self.routeCards) < 3:
                utility.message_log.add("Not enough route cards remaining to draw (need 3).")
                utility.message_log.add("")
                return
        exclude = []
        for i in range(amount):
            temp = (random.choice([f for f in range(len(self.routeCards)) if i not in exclude]))
            exclude.append(temp)
            cpu.routeCardList.append(self.routeCards[temp])
            utility.message_log.add(f"cpu drew a route")

    def findpusedbuttons(self,user,screen):
        if self.routedrawbutton.collidepoint(pygame.mouse.get_pos()):
            if len(self.routeCards) < 3:
                utility.message_log.add("Not enough route cards remaining to draw (need 3).")
                utility.message_log.add("")
                return False
            exclude = []
            one = random.randrange(0,len(self.routeCards),1)
            exclude.append(one)
            two =  random.choice([i for i in range(len(self.routeCards)) if i not in exclude])
            exclude.append(two)
            three = random.choice([i for i in range(len(self.routeCards)) if i not in exclude])
            self.drawroutes(user,[self.routeCards[one],self.routeCards[two],self.routeCards[three]],screen)
            return True
        for i in range(0,5):
            if self.carddrawbuttons[i].collidepoint(pygame.mouse.get_pos()):
                self.todraw[self.drawfirst] = i
                if self.piles[i] != 8:
                    self.drawfirst = not self.drawfirst
                else:
                    self.todraw[0] = i
                    self.todraw[1] = 9
                    self.drawfirst = False
        return False
                    
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
    def drawfrompile(self,user,targ = None):
        if targ != None:
            user.addtohand(self.piles[targ])
            self.piles[targ] = self.get()
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
        
    def draw(self,screen):
        pygame.draw.rect(screen,utility.TRACK_COLORS.get("red"),self.routedrawbutton, border_radius=3)
        text = utility.font.render('Draw new route' , True , (0,0,0))
        screen.blit(text, text.get_rect(center=self.routedrawbutton.center))
        for i in range(0,5):
            pygame.draw.rect(screen,utility.TRACK_COLORS.get(utility.numbertocolor(self.piles[i])),[30+(120*i),350,100,40], border_radius=3)
            if i == self.todraw[0] or i == self.todraw[1]:
                if self.piles[i] == 4:
                    pygame.draw.rect(screen,(255,255,255),[30+(120*i),350,100,40], 2,border_radius=3)
                else:
                    pygame.draw.rect(screen,(0,0,0),[30+(120*i),350,100,40], 2,border_radius=3)
            if self.piles[i] == 4:
                text = utility.font.render(f'{i+1}' , True , (255,255,255))
            else:
                text = utility.font.render(f'{i+1}' , True , (0,0,0))
            screen.blit(text, text.get_rect(center=(30+(120*i)+50, 350+20)))

class player:

    def __init__(self, pull):
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0,0]
        self.routes = []
        self.ending =  False
        self.cars = 18 # real max should be 45
        self.stations = 1 # real number of stations should be 3
        deal = 4
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.adjacencyList = {}
        self.routeCardList = []
        self.ownedTrackList = []
        self.usedTrackList = []
        self.awns = None
        pass
    def spend(self, color, amount, dis,screen):
        if self.cars > amount:
            if amount <= self.hand[color]:
                self.hand[color] -=amount
                self.cars -=amount
                dis.discard(color,amount)
                return True
            elif amount <= self.hand[color] + self.hand[8]:
                spendw = amount - self.hand[color]
                self.awns = None
                choice = utility.Choicemenu(self,['y','n'],f"do you want to spend {spendw} wild cards to buy this rail?")
                screenshot = screen.copy()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return False
        
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
                    choice.draw(screen)
                    pygame.display.flip()
        
        return False
    def addtohand(self,color):
        self.hand[color] +=1
    def draw(self, screen):
        if self.cars <=2:
            self.ending = True
        for i in range(0,9):
            pygame.draw.rect(screen,utility.TRACK_COLORS.get(utility.numbertocolor(i)),[30+(60*i),15,30,40], border_radius=3)
            if i == 4:
                text = utility.font.render(f'{self.hand[i]}' , True , (255,255,255))
            else:
                text = utility.font.render(f'{self.hand[i]}' , True , (0,0,0))
            screen.blit(text, text.get_rect(center=(30+(60*i)+15, 15+20)))
            i = 0 
        for r in self.routeCardList:
            r.drawRouteCard(screen,1000,200+(100*i))
            i+=1
        
        traintext = utility.font.render(f"Trains: {self.cars}", True, (0,0,0))
        trainrect = traintext.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 60))
        stationtext = utility.font.render(f"Stations: {self.stations}", True, (0,0,0))
        stationrect = stationtext.get_rect(bottomright=(screen.get_width() - 25, screen.get_height() - 20))
        screen.blit(traintext, trainrect)
        screen.blit(stationtext, stationrect)

        pass
    def addConnection(self, city_a, city_b):
        if city_a not in self.adjacencyList:
            self.adjacencyList[city_a] = []
        if city_b not in self.adjacencyList:
            self.adjacencyList[city_b] = []
        
        self.adjacencyList[city_a].append(city_b)
        self.adjacencyList[city_b].append(city_a)
    def checkRouteCompletion(self, ):
        for r in self.routeCardList:
            if not r.completed:
                start = r.city1
                end = r.city2
                if self.checkConnection(start, end):
                    utility.message_log.add("Route from "+r.city1.name+" to "+r.city2.name+" Completed")
                    self.score += r.points
                    r.completed = True
                    utility.message_log.add("Your Score: " + str(self.score))
                    utility.message_log.add("")
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

class enemy:
    def __init__(self, pull):
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0,0]
        self.routes = []
        self.ending =  False
        self.cars = 18#real max should be 45
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.hand[pull.get()] += 1
        self.adjacencyList = {}
        self.routeCardList = []
        self.ownedTrackList = []
        self.awns = 0
        pass

    def turn(self,tracks,deck):
        routesdone = True 
        for i in self.routeCardList:
            if i.completed == False:
                routesdone = False
        if  routesdone == True:
            self.drawroute(deck)
            return


        if not self.buy(tracks,deck):
            self.drawcard(deck)

    def addtohand(self,color):
        self.hand[color] +=1

    def addroute(self,route):
        self.routes.append(route)

    def addConnection(self, city_a, city_b):
        if city_a not in self.adjacencyList:
            self.adjacencyList[city_a] = []
        if city_b not in self.adjacencyList:
            self.adjacencyList[city_b] = []

    def buy(self, tracks, dis):
        for i in tracks:
            if i.Owner is not None:
                return False
            elif self.hand[utility.colortonumber(i.color)] >= i.length:
                i.Owner = self
                self.ownedTrackList.append(i)
                self.addConnection(i.city1, i.city2)
                self.score += utility.scoreforlength(i.length)
                self.hand[utility.colortonumber(i.color)] -=i.length
                self.cars -=i.length
                dis.discard(utility.colortonumber(i.color),i.length)
                utility.message_log.add(f"CPU bought a track")
                utility.message_log.add("")

                if all(t.Owner is not None for t in tracks):
                    self.ending = True

                return True
            
        return False
    
    def drawcard(self,deck):
        first = random.randrange(0,4)
        card = deck.piles[first]
        deck.drawfrompile(self,first)
        utility.message_log.add(f"CPU drew {utility.numbertocolor(card)}")
        if card != 8:

            second = first

            # Try up to 10 times to find a non-wild in a different slot
            attempts = 0
            while attempts < 10:
                second = random.randrange(0,4)
                if second != first and deck.piles[second] != 8:
                    break
                attempts += 1

            # If we failed, CPU just draws one card and ends turn
            if attempts == 10:
                return

            deck.drawfrompile(self,second)
            card = deck.piles[first]
            utility.message_log.add(f"CPU drew {utility.numbertocolor(card)}")
            utility.message_log.add("")
        

    def drawroute(self,deck):
        drawammount = random.randrange(0,3)
        deck.cpudrawroutes(self,drawammount)




            
        
