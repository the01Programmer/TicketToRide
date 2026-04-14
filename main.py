import pygame
import random
import queue
import time
import sys
import player_classes 
import map_classes
import utility
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
hint_button = pygame.Rect(1100, 55, 160, 40)
rules_button = pygame.Rect(1100, 5, 160, 40)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left mouse click
                    mousepos = pygame.mouse.get_pos()

                    track = utility.findtrackundermouse(mousepos, map)
                    city = utility.findcityundermouse(mousepos, map)

                    if track is not None:
                        success = utility.buytrack(user, track, map.trackList, cards, screen)
                        if success:
                            utility.message_log.add("Track bought!")
                            utility.message_log.add("Your Score: " + str(user.score))
                            utility.message_log.add("")
                            user.checkRouteCompletion()
                            cpu.turn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not buy this track.")
                            utility.message_log.add("")

                    if city is not None:
                        success = utility.placestation(user, city)
                        if success:
                            utility.message_log.add("Station placed!")
                            utility.message_log.add("")
                            user.checkRouteCompletion()
                            cpu.turn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not place a station.")
                            utility.message_log.add("")
                        
                    elif hint_button.collidepoint(mousepos):
                        utility.show_hints(user, map, screen, clock)

                    elif rules_button.collidepoint(mousepos):
                        utility.show_rules(screen, clock)

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

    if (user.ending or cpu.ending) and not game_over_processed:
        
        # station logic
        used_temp_track = None
        if user.stations < 1: 
            station_city = next((c for c in map.cityList if c.station), None)
            if station_city:
                # get all tracks touching that city, BUT only CPU-owned ones
                options = [t for t in map.get_tracks_touching_city(station_city) if isinstance(t.Owner, player_classes.enemy)]
                if options:
                    chosen = utility.choose_track_from_list(options, screen, station_city)
                    if chosen:
                        user.addConnection(chosen.city1, chosen.city2)
                        used_temp_track = chosen

        # re-check all routes now that station track is applied
        for r in user.routeCardList:
            if not r.completed and user.checkConnection(r.city1, r.city2):
                user.score += r.points
                r.completed = True

        for r in user.routeCardList:
            if not r.completed:
                user.score -= r.points

        for r in cpu.routeCardList:
            if not r.completed and user.checkConnection(r.city1, r.city2):
                user.score += r.points
                r.completed = True

        for r in cpu.routeCardList:
            if not r.completed:
                user.score -= r.points

        user.score += 4 * user.stations
        
        user_longest = utility.longest_route_length(user)
        cpu_longest = utility.longest_route_length(cpu)

        if user_longest > cpu_longest:
            user.score += 10
            utility.message_log.add("You got Longest Route (+10)")
            utility.message_log.add("")
        elif cpu_longest > user_longest:
            cpu.score += 10
            utility.message_log.add("CPU got Longest Route (+10)")
            utility.message_log.add("")

        utility.message_log.add(f"Game over! You got: {user.score} points and the CPU got {cpu.score} points.")
        if user.score > cpu.score:
            utility.message_log.add(f"You won!")
        else:
            utility.message_log.add(f"The CPU won")
        game_over = True
        game_over_processed = True

    user.draw(screen) 
    cards.draw(screen)

    pygame.draw.rect(screen, (90, 180, 90), hint_button, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), hint_button, 2, border_radius=8)
    hint_text = font.render("Hints", True, (0, 0, 0))
    screen.blit(hint_text, hint_text.get_rect(center=hint_button.center))

    pygame.draw.rect(screen, (90, 90, 180), rules_button, border_radius=8)
    pygame.draw.rect(screen, (0, 0, 0), rules_button, 2, border_radius=8)
    rules_text = font.render("Rules", True, (0, 0, 0))
    screen.blit(rules_text, rules_text.get_rect(center=rules_button.center))

    utility.message_log.draw(screen)
        
    if game_over:
        overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        title = font.render("GAME OVER", True, (255, 240, 240))
        title_rect = title.get_rect(center=(640, 200))
        
        score_txt = font.render(f"Final Score: {user.score}", True, (240, 240, 240))
        score_rect = score_txt.get_rect(center=(640, 260))
        
        screen.blit(title, title_rect)
        screen.blit(score_txt, score_rect)

        pygame.draw.rect(screen, (220, 80, 80), exit_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), exit_button, 2, border_radius=12)
        exit_label = font.render("Exit", True, (255, 255, 255))
        label_rect = exit_label.get_rect(center=exit_button.center)
        screen.blit(exit_label, label_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60


pygame.quit()
