import pygame
import subprocess
import sys


pygame.init()
screen = pygame.display.set_mode((1280/2, 720/2))
clock = pygame.time.Clock()
running = True
#set up rects, fonts and text
button = pygame.Rect(240,250,100,40)
buttonset = pygame.Rect(120,250,100,40)

titlefont = pygame.font.SysFont('Corbel',50)
font = pygame.font.SysFont('Corbel',35)
smallfont = pygame.font.SysFont('Corbel',15)

title  = titlefont.render('Ticket to Ride tutorial' , True , (0,0,0))
textsetplay = smallfont.render("play a tutorial that walks you through all basic actions" , True , (0,0,0))
textnormalplay = smallfont.render("play a tutorial against a cpu on a the map from eroup ed" , True , (0,0,0))
setplaytitle = smallfont.render("intro game" , True , (255,255,255))
normalplaytitle = smallfont.render("test game" , True , (255,255,255))

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #opens a subproses of the selected tutorial
        if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.collidepoint(pygame.mouse.get_pos()):
                        subprocess.Popen([sys.executable, "main.py"], )
                        #if uncommented this code ends the program but if it isn't being run using the cmp it will end the subproses 
                        #running = False
                        #sys.exit()
                    if buttonset.collidepoint(pygame.mouse.get_pos()):
                        subprocess.Popen([sys.executable, "tutorial_main.py"], )
                        #running = False
                        #sys.exit()    
    screen.fill("white")

    
    #draw the buttons
    pygame.draw.rect(screen,(0, 0, 127),button, border_radius=3)
    screen.blit(normalplaytitle,normalplaytitle.get_rect(center = button.center) )

    pygame.draw.rect(screen,(0, 0, 127),buttonset, border_radius=3)
    screen.blit(setplaytitle,setplaytitle.get_rect(center = buttonset.center) )

    #draw the title
    screen.blit(title, title.get_rect(center=(320,100)))
    
    #draw the description of the tutorial when hovered over by the mouse
    if button.collidepoint(pygame.mouse.get_pos()):
        x,y = pygame.mouse.get_pos()
        pygame.draw.rect(screen,(240, 240, 240),pygame.Rect(x+15,y+15,335,15), border_radius=0)
        screen.blit(textnormalplay, textsetplay.get_rect(topleft=(x+15,y+15)))

    if buttonset.collidepoint(pygame.mouse.get_pos()):
        x,y = pygame.mouse.get_pos()
        pygame.draw.rect(screen,(240, 240, 240),pygame.Rect(x+15,y+15,320,15), border_radius=0)
        screen.blit(textsetplay, textsetplay.get_rect(topleft=(x+15,y+15)))

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()