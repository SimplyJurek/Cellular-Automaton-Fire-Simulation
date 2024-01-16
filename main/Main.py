# * Pygame initialization
import pygame
pygame.init()

# * IMPORTS
import Core as C
import Global as G
from typing import List
from typing import Tuple
from HexagonGrid import FlatTopHexagonTile
from HexagonGrid import HexagonTile
from Button import Button


# * Options menu
def options():
    terminated = False
    # Options menu loop
    while not terminated:
        G.SCREEN.fill(G.BACKGROUND_COLOUR)

        # Forest density 
        forestDensityText = G.FONT.render('Forest Density', True, (255, 255, 255))
        forestDensityTextRect = forestDensityText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 175))
        G.SCREEN.blit(forestDensityText, forestDensityTextRect)

        # Forest density buttons
        forestDensity_25  = Button('25%',  ((G.SCREEN_WIDTH / 2) - 200, 150), [150, 52, 25])
        forestDensity_50  = Button('50%',  ((G.SCREEN_WIDTH / 2) + 34, 150), [150, 52, 25])
        forestDensity_75  = Button('75%',  ((G.SCREEN_WIDTH / 2) + 270,  150), [150, 52, 25])
        forestDensity_100 = Button('100%', ((G.SCREEN_WIDTH / 2) + 500, 150), [150, 52, 25])
        
        forestDensity_25.draw(G.forest_density  == 25)
        forestDensity_50.draw(G.forest_density  == 50)
        forestDensity_75.draw(G.forest_density  == 75)
        forestDensity_100.draw(G.forest_density == 100)

        if forestDensity_25.check_click(): 
            forestDensity_25.draw(True)
        if forestDensity_50.check_click(): 
            forestDensity_50.draw(True)
        if forestDensity_75.check_click(): 
            forestDensity_75.draw(True)
        if forestDensity_100.check_click(): 
            forestDensity_100.draw(True)

        # Grid size
        gridSizeText = G.FONT.render('Grid size', True, (255, 255, 255))
        gridSizeTextRect = gridSizeText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 300))
        G.SCREEN.blit(gridSizeText, gridSizeTextRect)

        # Grid size buttons
        gridSize_small  = Button('Min',  ((G.SCREEN_WIDTH / 2) - 200, 275), [150, 52, 25])
        gridSize_mid  = Button('Mid',  ((G.SCREEN_WIDTH / 2) + 34, 275), [150, 52, 25])
        gridSize_big  = Button('Big',  ((G.SCREEN_WIDTH / 2) + 270,  275), [150, 52, 25])
        gridSize_max = Button('Max', ((G.SCREEN_WIDTH / 2) + 500, 275), [150, 52, 25])
        
        gridSize_small.draw(G.grid_size == 'min')
        gridSize_mid.draw(G.grid_size   == 'mid')
        gridSize_big.draw(G.grid_size   == 'big')
        gridSize_max.draw(G.grid_size   == 'max')

        if gridSize_small.check_click(): 
            gridSize_small.draw(True)
        if gridSize_mid.check_click(): 
            gridSize_mid.draw(True)
        if gridSize_big.check_click(): 
            gridSize_big.draw(True)
        if gridSize_max.check_click(): 
            gridSize_max.draw(True)

        # Grid orientation
        gridSizeText = G.FONT.render('Grid orientation', True, (255, 255, 255))
        gridSizeTextRect = gridSizeText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 425))
        G.SCREEN.blit(gridSizeText, gridSizeTextRect)

        # Grid size buttons
        gridSize_flat  = Button('Flat top',  ((G.SCREEN_WIDTH / 2) - 200, 400), [380, 52, 25])
        gridSize_point  = Button('Pointy top',  ((G.SCREEN_WIDTH / 2) + 270, 400), [380, 52, 25])
        
        gridSize_flat.draw(G.grid_orientation)
        gridSize_point.draw(not G.grid_orientation)

        if gridSize_flat.check_click(): 
            gridSize_flat.draw(True)
        if gridSize_point.check_click(): 
            gridSize_point.draw(True)

        # Return to main menu button
        backButton = Button('Back', ((G.SCREEN_WIDTH / 2) - 150, (G.SCREEN_HEIGHT - 300)), [300, 150, 48])

        backButton.draw()

        if backButton.check_click():
            backButton.draw(True)

        # Event Handler
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:
                if forestDensity_25.check_click(): 
                    G.forest_density = 25
                if forestDensity_50.check_click(): 
                    G.forest_density = 50
                if forestDensity_75.check_click(): 
                    G.forest_density = 75
                if forestDensity_100.check_click(): 
                    G.forest_density = 100

                if gridSize_small.check_click(): 
                    G.grid_size = 'min'
                if gridSize_mid.check_click(): 
                    G.grid_size = 'mid'
                if gridSize_big.check_click(): 
                    G.grid_size = 'big'
                if gridSize_max.check_click(): 
                    G.grid_size = 'max'

                if gridSize_flat.check_click(): 
                    G.grid_orientation = True
                if gridSize_point.check_click(): 
                    G.grid_orientation = False

                if backButton.check_click(): 
                    main()
                    
        pygame.display.update()
        G.CLOCK.tick(G.FPS)

    pygame.display.quit()

# * Main simulation function
def automata_main():
    C.display_loading_screen()
    hexagons = C.init_hexagons(G.gridSize())
    terminated = False
    pause = True
    mouse_dragging = False
    original_mouse_position = None
    buttons = []
    # Simulation loop    
    while not terminated:
        G.SCREEN.fill(G.BACKGROUND_COLOUR)
        # Simulation buttons
        startButton = Button('Start', (G.SCREEN_WIDTH/2 - 375, G.SCREEN_HEIGHT - 125), [150, 75, 36])
        pauseButton = Button('Pause', (G.SCREEN_WIDTH/2 - 175, G.SCREEN_HEIGHT - 125), [150, 75, 36])
        resetButton = Button('Reset', (G.SCREEN_WIDTH/2 + 25, G.SCREEN_HEIGHT - 125), [150, 75, 36])
        backButton = Button('Back', (G.SCREEN_WIDTH/2 + 225, G.SCREEN_HEIGHT - 125), [150, 75, 36])

        # Event handler
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:

                # Left click
                if event.button == 1:
                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 2
                        hexagon.colour = [120, 0, 0]    
                
                # Middle click
                if event.button == 2:
                    mouse_dragging = False

                # Right click
                if event.button == 3:
                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 1
                        hexagon.colour = [0, 0, 120]
                
                if startButton.check_click():
                    if pause == True: pause = False
                    else: pass
                if pauseButton.check_click():
                    if pause == False: pause = True
                    else: pass
                if resetButton.check_click(): 
                    automata_main()
                if backButton.check_click(): 
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # camera handling
                if event.button == 2:  
                    mouse_dragging = True
                    original_mouse_position = pygame.mouse.get_pos()

                # zoom handling
                if event.button == 4:  # Scroll Up
                    G.zoom_factor += G.ZOOM_DETENT * (1 + G.zoom_factor)**2
                    if G.zoom_factor > G.MAX_ZOOM:
                        G.zoom_factor = G.MAX_ZOOM

                if event.button == 5:  # Scroll Down
                    G.zoom_factor -= G.ZOOM_DETENT * (1 + G.zoom_factor)**2
                    if G.zoom_factor < G.MIN_ZOOM:
                        G.zoom_factor = G.MIN_ZOOM

        if mouse_dragging:
            current_mouse_position = pygame.mouse.get_pos()
            offset_x = current_mouse_position[0] - original_mouse_position[0]
            offset_y = current_mouse_position[1] - original_mouse_position[1]
            G.camera_offset[0] += offset_x
            G.camera_offset[1] += offset_y
            original_mouse_position = current_mouse_position       

        if not pause:
            C.change_hexagon_states(hexagons)        
            C.update_grid(hexagons)
        
        C.render(G.SCREEN, hexagons)

        startButton.draw(not pause)
        pauseButton.draw(pause)
        resetButton.draw()
        backButton.draw()

        if startButton.check_click():
            startButton.draw(True)
        if pauseButton.check_click():
            pauseButton.draw(True)
        if resetButton.check_click():
            resetButton.draw(True)
        if backButton.check_click():
            backButton.draw(True)

        pygame.display.flip()
        G.CLOCK.tick(G.FPS)
    pygame.display.quit()

# * Main menu
def main():
    terminated = False
    # Main menu loop
    while not terminated:
        G.SCREEN.fill(G.BACKGROUND_COLOUR)  

        # Main menu buttons
        startButton = Button('Start', ((G.SCREEN_WIDTH / 2) - 150, 150), [300, 150, 48])
        optionsButton = Button('Options', ((G.SCREEN_WIDTH / 2) - 150, 330), [300, 150, 48],)
        exitButton = Button('Exit', ((G.SCREEN_WIDTH / 2) - 150, 510), [300, 150, 48])

        startButton.draw()
        optionsButton.draw()
        exitButton.draw()

        if startButton.check_click():
            startButton.draw(True)
        if optionsButton.check_click():
            optionsButton.draw(True)
        if exitButton.check_click():
            exitButton.draw(True)

        # Event handler
        for event in pygame.event.get():
            # Quit
            if event.type == pygame.QUIT:
                terminated = True
            # On click
            if event.type == pygame.MOUSEBUTTONUP:
                if startButton.check_click():
                    G.camera_offset = [0, 0] #      reset camera offset 
                    G.zoom_factor = 1.0 #       and zoom between simulations
                    automata_main()
                if optionsButton.check_click(): 
                    options()
                if exitButton.check_click(): 
                    terminated = True   

        pygame.display.update()
        G.CLOCK.tick(G.FPS)
        
    pygame.display.quit()

if __name__ == "__main__":
    main()