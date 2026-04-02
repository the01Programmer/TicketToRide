import pygame
import random
import queue
import time
import sys
import player_classes 
import small_map_classes
import utility
import math
import tutorial
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
setupdeck = queue.Queue()
setupdeck.put(3)
setupdeck.put(3)
setupdeck.put(5)
setupdeck.put(8)
setupdeck.put(3)
setupdeck.put(0)
setupdeck.put(0)
setupdeck.put(0)
setupdeck.put(0)
setupdeck.put(3)
setupdeck.put(3)
setupdeck.put(3)
setupdeck.put(8)
setupdeck.put(1)
setupdeck.put(2)
setupdeck.put(1)
dumpcards = [8,10,12,6,12,7,12,12,12]
for i in range(97):
    draw = random.randrange(0,9,1)
    if dumpcards[draw]>0:
        dumpcards[draw]-=1
        setupdeck.put(draw)

cards = player_classes.deck(screen,setupdeck)
user = player_classes.setplayer(cards,tutorial.setplay([['b',0],['s','D',['A','D']],['d',[1,4]],['r',1,["C","D"]]]))#player(cards)
map = small_map_classes.Map(cards.routeCards)
cpu = player_classes.smartenemy(cards,tutorial.setplay([['b',3],['d',[1,2]],['d',[3,4]]]))#player_classes.enemy(cards)
#map.trackList[0].Owner = cpu

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
        
        elif not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left mouse click
                    mousepos = pygame.mouse.get_pos()

                    track = utility.findtrackundermouse(mousepos, map)
                    city = utility.findcityundermouse(mousepos, map)

                    if track is not None:
                        success = utility.buytrack(user, track, map.trackList, cards, screen, user.turns.currentE)
                        if success:
                            utility.message_log.add("Track bought!")
                            utility.message_log.add("Your Score: " + str(user.score))
                            utility.message_log.add("")
                            user.checkRouteCompletion()
                            cpu.smartturn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not buy this track.")
                            utility.message_log.add("")

                    if city is not None:
                        success = utility.placestation(user, city,user.turns.currentE)
                        if success:
                            utility.message_log.add("Station placed!")
                            utility.message_log.add("")
                            user.checkRouteCompletion()
                            cpu.smartturn(map.trackList, cards)
                        else:
                            utility.message_log.add("Could not place a station.")
                            utility.message_log.add("")
                        
                    else:
                        if cards.findpusedbuttons(user,screen,user.turns.currentE):
                            cpu.smartturn(map.trackList, cards)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if cards.todraw[0] != 9:
                        cards.drawfrompile(user)
                        user.turns.completeactionE()
                        cpu.smartturn(map.trackList, cards)
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
            station_city = next((c for c in map.cityList if c.station and c.stationowner == user), None)
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
        utility.message_log.add(f"Game over you got: {user.score} points and the cpu got {cpu.score} points")
        if user.score > cpu.score:
            utility.message_log.add(f"you won")
        else:
            utility.message_log.add(f"the cpu won")
        game_over = True
        game_over_processed = True

    user.draw(screen) 
    cards.draw(screen)
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