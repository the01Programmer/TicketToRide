import pygame
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

class player:
    def __init__(self):
        self.score = 0
        self.hand = [0,0,0,0,0,0,0,0]
        self.wild = 0
        self.cars = 45#should be lowered for testing
        deal = 4
        while deal > 0:
            gven = random.randrange(1,4,1)
            if gven <= deal:
                self.hand[random.randrange(0,7,1)] = gven
                deal-=gven
        pass
    def spend(self, color, amount):
        if self.cars > amount:
            if amount <= self.hand[color]:
                self.hand[color] -= amount
                self.cars -=amount
                return True
            elif amount <= self.hand[color] + self.wild:
                spendw = amount - self.hand[color]
                print(f"do you want to spend {spendw} wild cards to buy this rail?\n")
                awns = input("[y/n]: ")
                while True:
                    if awns == "Y":
                        self.hand[color] = 0
                        self.wild -= spendw
                        self.cars -=amount
                        return True
                    elif awns == "N":
                        return False
        
        return False
    def draw(self):
        print(f"current hand state: red: {self.hand[0]}, green: {self.hand[1]}, blue: {self.hand[2]}, white: {self.hand[3]}, black: {self.hand[4]}, orange: {self.hand[5]}, pink: {self.hand[6]}, yellow: {self.hand[7]}, wild: {self.wild}")
        pass

user = player()
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    user.draw()
    input("continue?: ")
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
