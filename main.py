import pygame
import random
import queue
import time
import sys
import player_classes 
import map_classes
import utility
import math
#import player_classes
from collections import deque
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Ticket to Ride")
clock = pygame.time.Clock()
running = True
font = pygame.font.SysFont('Corbel',35)
smallfont = pygame.font.SysFont('Corbel',15)

choice = -1
cards = player_classes.deck(screen)
user = player_classes.player(cards)
map = map_classes.Map(cards.routeCards)
cpu = player_classes.enemy(cards)
map.trackList[0].Owner = cpu

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

                    track = utility.findtrackundermouse(mousepos, map)
                    city = utility.findcityundermouse(mousepos, map)

                    if track is not None:
                        success = utility.buytrack(user, track, cards,screen)
                        if success:
                            utility.message_log.add("Track bought!")
                            utility.message_log.add("Your Score: " + str(user.score))
                            user.checkRouteCompletion()
                            cpu.turn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not buy this track.")

                    elif city is not None:
                        success = utility.usestation(user, city, screen)
                        if success:
                            utility.message_log.add("Station used!")
                            user.checkRouteCompletion()
                            cpu.turn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not use a station.")
                        
                    else:
                        if cards.findpusedbuttons(user,screen):
                            cpu.turn(map.trackList, cards)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cards.drawfrompile(user)
                    cpu.turn(map.trackList, cards)
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
        if user.stations > 0:
            user.score += 4 * user.stations
        utility.message_log.add(f"game over you got: {user.score} points")
        game_over = True
        game_over_processed = True

    user.draw(screen) 
    cards.draw(screen)
    utility.message_log.draw(screen)

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

