import pygame
import random
import queue
import time
import sys
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

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
        c = ["null","null","null","null","null"]
        f = 0
        for i in self.piles:
            if i == 0:
                c[f] = "red"
            if i == 1:
                c[f] = "Green"
            if i == 2:
                c[f] = "Blue"
            if i == 3:
                c[f] = "white"
            if i == 4:
                c[f] = "black"
            if i == 5:
                c[f] = "orange"
            if i == 6:
                c[f] = "pink"
            if i == 7:
                c[f] = "yellow"
            if i == 8:
                c[f] = "wild"
            f+=1
        print(f"1: {c[0]} ,2: {c[1]} , 3: {c[2]} , 4: {c[3]} , 5: {c[4]}")
        get = int(input("draw whitch: ")) - 1
        draw = self.drawfrompile(get)
        play.hand[draw] += 1
        got = get
        while draw != 8 & get != got:
            get = int(input("draw whitch: ")) - 1
            if get != got:
                play.hand[self.drawfrompile(get)] += 1

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
        print(f"current hand state: red: {self.hand[0]}, green: {self.hand[1]}, blue: {self.hand[2]}, white: {self.hand[3]}, black: {self.hand[4]}, orange: {self.hand[5]}, pink: {self.hand[6]}, yellow: {self.hand[7]}, wild: {self.hand[8]}")
        pass


cards = deck()
user = player(cards)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    if user.ending:
        print(f"game over you got: {user.score} points")
        input("end game?: ")
        pygame.quit()
        sys.exit()

    user.draw()
    cards.draw(user)
    input("continue?: ")
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
