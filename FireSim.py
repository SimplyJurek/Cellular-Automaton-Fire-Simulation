import pygame, os
from bin.Core import ON, OFF, WIDTH, HEIGHT, \
                     display, clock, font1, font2, font3, font4, \
			         Text, HEXW, HEXH
import bin.Grid as G
import bin.Automaton as A

def splash(): # splash screen
	running = True
	while running:

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
				pygame.quit()
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running=False
					pygame.quit()
					exit()
				if event.key == pygame.K_RETURN:
					running=False
			
		display.fill(ON)
	
		pygame.draw.rect(display,OFF,[10,10,WIDTH-20,HEIGHT-20])				

		# logo = pygame.image.load(os.path.abspath('Assets\\GUI\\logo.png'))
		# display.blit(logo,(70,130))

		Desciption = Text("Press RETURN to start", 320, 350, font2)
		Desciption.draw(display, ON)

		Credit = Text("Projekt gr. 1/1 8)", 55, 460, font1)
		Credit.draw(display, ON)

		pygame.display.update()
		clock.tick(60)

# -----------------------------------------------------------------------------------------------------

def game():
    automaton = A.HexAutomaton(8, 6)  # Assuming this creates the grid

    running = True
    
    while running:
        click = False    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            
        display.fill(ON)

        pygame.draw.rect(display, OFF, [10, 10, WIDTH-20, HEIGHT-20])

        mx, my = pygame.mouse.get_pos()

        for row in automaton.grid:
            for hex in row:
                hex.draw()
                if hex.collidepoint(mx, my):
                    if click:
                        hex.cycleState()
            
        automaton.draw()  # Assuming this method draws the entire grid
        automaton.update()

        pygame.display.update()
        clock.tick(2)

# -----------------------------------------------------------------------------------------------------

splash()
game()
pygame.quit()
exit()