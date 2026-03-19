import pygame

clock = pygame.time.Clock()

def pointsQuiz(correctPoints):
    quizScreen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Points Quiz")

    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    numberInput = ''

    correctPointsStr = str(correctPoints)

    font = pygame.font.Font(None, 32)
    text_surface = font.render('How many points did you earn?', True, (255, 255, 255))

    isRunning = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # if the user clicked on the input_box
                if input_box.collidepoint(event.pos):
                    # toggle the active variable
                    active = not active
                else:
                    active = False
                # change the current color of the input box
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN: # let player type their answer
                if active:
                    if event.key == pygame.K_RETURN:
                        if numberInput == correctPointsStr: # if player is correct
                            text_surface = font.render('Correct!', True, (255, 255, 255))
                        else: # if player is incorrect
                            displayText = 'Incorrect! The correct answer is ' + correctPointsStr + '.'
                            text_surface = font.render(displayText, True, (255, 255, 255))
                        numberInput = ''
                    elif event.key == pygame.K_BACKSPACE:
                        numberInput = numberInput[:-1]
                    else:
                        numberInput += event.unicode

        quizScreen.fill((30, 30, 30))
        # render the text
        textbox_surface = font.render(numberInput, True, color)
    
        # blit the text
        quizScreen.blit(textbox_surface, (input_box.x+5, input_box.y+5))
        quizScreen.blit(text_surface, (100, 300))
        # blit the input_box rect
        pygame.draw.rect(quizScreen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)
