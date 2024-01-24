# * Pygame initialization
import pygame
import time
pygame.init()

# * IMPORTS
import Core as C
import Global as G
from Button import Button
from Clock import Clock

# * Options menu
def options():
    """
    Displays the options menu and handles user input for selecting various options.

    This function renders the options menu on the screen and handles the user's selection
    for forest density, grid size, grid orientation, wind direction, wind strength, cell humidity,
    cell density, and cell duff. It uses the Button class to create interactive buttons for each option.
    """
    terminated = False
    offset = -70
    # Options menu loop
    while not terminated:
        G.SCREEN.fill(G.BACKGROUND_COLOUR)

        # Forest density 
        forestDensityText = G.FONT.render('Forest Density', True, (255, 255, 255))
        forestDensityTextRect = forestDensityText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 175 + offset))
        G.SCREEN.blit(forestDensityText, forestDensityTextRect)

        # Forest density buttons
        forestDensity_70  = Button('70%',  ((G.SCREEN_WIDTH / 2) - 200, 150 + offset), [150, 52, 16])
        forestDensity_80  = Button('80%',  ((G.SCREEN_WIDTH / 2) + 34, 150 + offset), [150, 52, 16])
        forestDensity_90  = Button('90%',  ((G.SCREEN_WIDTH / 2) + 270,  150 + offset), [150, 52, 16])
        forestDensity_100 = Button('100%', ((G.SCREEN_WIDTH / 2) + 500, 150 + offset), [150, 52, 16])
        
        forestDensity_70.draw(G.forest_density  == 70)
        forestDensity_80.draw(G.forest_density  == 80)
        forestDensity_90.draw(G.forest_density  == 90)
        forestDensity_100.draw(G.forest_density == 100)

        if forestDensity_70.check_click(): 
            forestDensity_70.draw(True)
        if forestDensity_80.check_click(): 
            forestDensity_80.draw(True)
        if forestDensity_90.check_click(): 
            forestDensity_90.draw(True)
        if forestDensity_100.check_click(): 
            forestDensity_100.draw(True)

        # Grid size
        gridSizeText = G.FONT.render('Grid size', True, (255, 255, 255))
        gridSizeTextRect = gridSizeText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 250 + offset))
        G.SCREEN.blit(gridSizeText, gridSizeTextRect)

        # Grid size buttons
        gridSize_small  = Button('Min',  ((G.SCREEN_WIDTH / 2) - 200, 225 + offset), [150, 52, 16])
        gridSize_mid  = Button('Mid',  ((G.SCREEN_WIDTH / 2) + 34, 225 + offset), [150, 52, 16])
        gridSize_big  = Button('Big',  ((G.SCREEN_WIDTH / 2) + 270,  225 + offset), [150, 52, 16])
        gridSize_max = Button('Max', ((G.SCREEN_WIDTH / 2) + 500, 225 + offset), [150, 52, 16])
        
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
        gridSizeTextRect = gridSizeText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 325 + offset))
        G.SCREEN.blit(gridSizeText, gridSizeTextRect)

        # Grid orientation buttons
        gridSize_flat  = Button('Flat top',  ((G.SCREEN_WIDTH / 2) - 200, 300 + offset), [380, 52, 16])
        gridSize_point  = Button('Pointy top',  ((G.SCREEN_WIDTH / 2) + 270, 300 + offset), [380, 52, 16])
        
        gridSize_flat.draw(G.grid_orientation)
        gridSize_point.draw(not G.grid_orientation)

        if gridSize_flat.check_click(): 
            gridSize_flat.draw(True)
        if gridSize_point.check_click(): 
            gridSize_point.draw(True)
                        
        # Wind direction
        if G.wind_strength != 0.0:     
            windDirectionText = G.FONT.render('Wind Direction', True, (255, 255, 255))
            windDirectionTextRect = windDirectionText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 400 + offset))
            G.SCREEN.blit(windDirectionText, windDirectionTextRect)

        # Wind direction buttons
        wind_direction_top_left = Button('Top Left', ((G.SCREEN_WIDTH / 2) - 200, 375 + offset), [380, 52, 16])
        wind_direction_top_right = Button('Top Right', ((G.SCREEN_WIDTH / 2) + 270, 375 + offset), [380, 52, 16])
        wind_direction_bottom_left = Button('Bottom Left', ((G.SCREEN_WIDTH / 2) - 200, 435 + offset), [380, 52, 16])
        wind_direction_bottom_right = Button('Bottom Right', ((G.SCREEN_WIDTH / 2) + 270, 435 + offset), [380, 52, 16])
        if G.grid_orientation:
            wind_direction_top = Button('Top', ((G.SCREEN_WIDTH / 2) - 200, 495 + offset), [380, 52, 16])
            wind_direction_bottom = Button('Bottom', ((G.SCREEN_WIDTH / 2) + 270, 495 + offset), [380, 52, 16])
        else:
            wind_direction_left = Button('Left', ((G.SCREEN_WIDTH / 2) - 200, 495 + offset), [380, 52, 16])
            wind_direction_right = Button('Right', ((G.SCREEN_WIDTH / 2) + 270, 495 + offset), [380, 52, 16])
        
        if G.wind_strength != 0.0:
            wind_direction_top_left.draw(G.wind_direction == 'bottom_right')
            wind_direction_top_right.draw(G.wind_direction == 'bottom_left')
            wind_direction_bottom_left.draw(G.wind_direction == 'top_right')
            wind_direction_bottom_right.draw(G.wind_direction == 'top_left')
            if G.grid_orientation:
                wind_direction_top.draw(G.wind_direction == 'bottom')
                wind_direction_bottom.draw(G.wind_direction == 'top')
            else:
                wind_direction_left.draw(G.wind_direction == 'right')
                wind_direction_right.draw(G.wind_direction == 'left')

            if wind_direction_top_left.check_click():
                wind_direction_top_left.draw(True)
            if wind_direction_top_right.check_click():
                wind_direction_top_right.draw(True)
            if wind_direction_bottom_left.check_click():
                wind_direction_bottom_left.draw(True)
            if wind_direction_bottom_right.check_click():
                wind_direction_bottom_right.draw(True)
            if G.grid_orientation:
                if wind_direction_top.check_click():
                    wind_direction_top.draw(True)
                if wind_direction_bottom.check_click():
                    wind_direction_bottom.draw(True)
            else:
                if wind_direction_left.check_click():
                    wind_direction_left.draw(True)
                if wind_direction_right.check_click():
                    wind_direction_right.draw(True)
            
        # Wind strength
        windStrengthText = G.FONT.render('Wind Strength', True, (255, 255, 255))
        windStrengthTextRect = windStrengthText.get_rect(center=(G.SCREEN_WIDTH/2 - 500, 595 + offset))
        G.SCREEN.blit(windStrengthText, windStrengthTextRect)

        # Wind strength buttons
        wind_strength_weak = Button('Weak', ((G.SCREEN_WIDTH / 2) - 200, 570 + offset), [150, 52, 16])
        wind_strength_moderate = Button('Moderate', ((G.SCREEN_WIDTH / 2) + 34, 570 + offset), [150, 52, 16])
        wind_strength_strong = Button('Strong', ((G.SCREEN_WIDTH / 2) + 270, 570 + offset), [150, 52, 16])
        wind_strength_none = Button('None', ((G.SCREEN_WIDTH / 2) + 500, 570 + offset), [150, 52, 16])

        wind_strength_weak.draw(G.wind_strength == 1.5)
        wind_strength_moderate.draw(G.wind_strength == 2.3)
        wind_strength_strong.draw(G.wind_strength == 3.0)
        wind_strength_none.draw(G.wind_strength == 0.0)

        if wind_strength_weak.check_click():
            wind_strength_weak.draw(True)
        if wind_strength_moderate.check_click():
            wind_strength_moderate.draw(True)
        if wind_strength_strong.check_click():
            wind_strength_strong.draw(True)
        if wind_strength_none.check_click():
            wind_strength_none.draw(True)

        # Cell Humidity
        cellHumidityText = G.FONT.render('Cell Humidity', True, (255, 255, 255))
        cellHumidityTextRect = cellHumidityText.get_rect(center=((G.SCREEN_WIDTH / 2) - 500, 670 + offset))
        G.SCREEN.blit(cellHumidityText, cellHumidityTextRect)

        # Cell Humidity Buttons
        cell_humidity_dry = Button('Dry', ((G.SCREEN_WIDTH / 2) - 200, 645 + offset), [150, 52, 16])
        cell_humidity_medium = Button('Medium', ((G.SCREEN_WIDTH / 2) + 34, 645 + offset), [150, 52, 16])
        cell_humidity_high = Button('Humid', ((G.SCREEN_WIDTH / 2) + 270, 645 + offset), [150, 52, 16])

        cell_humidity_dry.draw(G.cell_humidity == [0, 30, 5])
        cell_humidity_medium.draw(G.cell_humidity == [10, 50, 5])
        cell_humidity_high.draw(G.cell_humidity == [25, 75, 5])

        if cell_humidity_dry.check_click():
            cell_humidity_dry.draw(True)
        if cell_humidity_medium.check_click():
            cell_humidity_medium.draw(True)
        if cell_humidity_high.check_click():
            cell_humidity_high.draw(True)

        # Cell Density
        cellDensityText = G.FONT.render('Cell Density', True, (255, 255, 255))
        cellDensityTextRect = cellDensityText.get_rect(center=((G.SCREEN_WIDTH / 2) - 500, 745 + offset))
        G.SCREEN.blit(cellDensityText, cellDensityTextRect)

        # Cell density Buttons
        cell_density_sparse = Button('Sparse', ((G.SCREEN_WIDTH / 2) - 200, 720 + offset), [150, 52, 16])
        cell_density_medium = Button('Medium', ((G.SCREEN_WIDTH / 2) + 34, 720 + offset), [150, 52, 16])
        cell_density_dense = Button('Dense', ((G.SCREEN_WIDTH / 2) + 270, 720 + offset), [150, 52, 16])

        cell_density_sparse.draw(G.cell_density == [25, 75, 5])
        cell_density_medium.draw(G.cell_density == [50, 100, 5])
        cell_density_dense.draw(G.cell_density == [75, 150, 5])

        if cell_density_sparse.check_click():
            cell_density_sparse.draw(True)
        if cell_density_medium.check_click():
            cell_density_medium.draw(True)
        if cell_density_dense.check_click():
            cell_density_dense.draw(True)

        # Cell Duff
        cellDuffText = G.FONT.render('Cell Duff', True, (255, 255, 255))
        cellDuffTextRect = cellDuffText.get_rect(center=((G.SCREEN_WIDTH / 2) - 500, 820 + offset))
        G.SCREEN.blit(cellDuffText, cellDuffTextRect)

        # Cell duff Buttons
        cell_duff_sparse = Button('Sparse', ((G.SCREEN_WIDTH / 2) - 200, 795 + offset), [150, 52, 16])
        cell_duff_medium = Button('Medium', ((G.SCREEN_WIDTH / 2) + 34, 795 + offset), [150, 52, 16])
        cell_duff_dense = Button('Dense', ((G.SCREEN_WIDTH / 2) + 270, 795 + offset), [150, 52, 16])

        cell_duff_sparse.draw(G.cell_duff == [25, 75, 5])
        cell_duff_medium.draw(G.cell_duff == [50, 100, 5])
        cell_duff_dense.draw(G.cell_duff == [75, 150, 5])

        if cell_duff_sparse.check_click():
            cell_duff_sparse.draw(True)
        if cell_duff_medium.check_click():
            cell_duff_medium.draw(True)
        if cell_duff_dense.check_click():
            cell_duff_dense.draw(True)

        # Sim visuals
        simVisualsText = G.FONT.render('Visuals', True, (255, 255, 255))
        simVisualsTextRect = simVisualsText.get_rect(center=((G.SCREEN_WIDTH / 2) - 500, 890 + offset))
        G.SCREEN.blit(simVisualsText, simVisualsTextRect)

        # Sim visuals buttons
        simVisualsTrueButton = Button('Simulation', ((G.SCREEN_WIDTH / 2) - 200, 870 + offset), [380, 52, 16])
        simVisualsFalseButton = Button('Eye candy', ((G.SCREEN_WIDTH / 2) + 270, 870 + offset), [380, 52, 16])

        simVisualsTrueButton.draw(G.sim_visuals)
        simVisualsFalseButton.draw(not G.sim_visuals)

        # Return to main menu button
        backButton = Button('Back', ((G.SCREEN_WIDTH / 2) - 150, (G.SCREEN_HEIGHT - 200)), [300, 150, 48])
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
                if forestDensity_70.check_click(): 
                    G.forest_density = 70
                if forestDensity_80.check_click(): 
                    G.forest_density = 80
                if forestDensity_90.check_click(): 
                    G.forest_density = 90
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
                    
                if wind_direction_top_left.check_click():
                    G.wind_direction = 'bottom_right'
                if wind_direction_top_right.check_click():
                    G.wind_direction = 'bottom_left'
                if wind_direction_bottom_left.check_click():
                    G.wind_direction = 'top_right'
                if wind_direction_bottom_right.check_click():
                    G.wind_direction = 'top_left'
                if G.grid_orientation:
                    if wind_direction_top.check_click():
                        G.wind_direction = 'bottom'
                    if wind_direction_bottom.check_click():
                        G.wind_direction = 'top'
                else:
                    if wind_direction_left.check_click():
                        G.wind_direction = 'right'
                    if wind_direction_right.check_click():
                        G.wind_direction = 'left'

                if gridSize_flat.check_click(): 
                    G.grid_orientation = True
                    if G.wind_direction == 'right' or G.wind_direction == 'left':
                        G.wind_direction = 'bottom_right'
                if gridSize_point.check_click(): 
                    G.grid_orientation = False
                    if G.wind_direction == 'top' or G.wind_direction == 'bottom':
                        G.wind_direction = 'bottom_right'
                    
                if wind_strength_weak.check_click():
                    G.wind_strength = 1.5
                if wind_strength_moderate.check_click():
                    G.wind_strength = 2.3
                if wind_strength_strong.check_click():
                    G.wind_strength = 3
                if wind_strength_none.check_click():
                    G.wind_strength = 0.0

                if cell_humidity_dry.check_click():
                    G.cell_humidity = [0, 30, 5]
                if cell_humidity_medium.check_click():
                    G.cell_humidity = [10, 50, 5]
                if cell_humidity_high.check_click():
                    G.cell_humidity = [25, 75, 5]

                if cell_density_sparse.check_click():
                    G.cell_density = [25, 75, 5]
                if cell_density_medium.check_click():
                    G.cell_density = [50, 100, 5]
                if cell_density_dense.check_click():
                    G.cell_density = [75, 150, 5]

                if cell_duff_sparse.check_click():
                    G.cell_duff = [25, 75, 5]
                if cell_duff_medium.check_click():
                    G.cell_duff = [50, 100, 5]
                if cell_duff_dense.check_click():
                    G.cell_duff = [75, 150, 5]
                    
                if simVisualsTrueButton.check_click():
                    G.sim_visuals = True
                if simVisualsFalseButton.check_click():
                    G.sim_visuals = False

                if backButton.check_click(): 
                    main()
                    
        pygame.display.update()
        G.CLOCK.tick(G.FPS)

    pygame.display.quit()

# * Main simulation function
def automata_main():
    """
    Main function for running the automata simulation.

    This function initializes the necessary variables and objects, handles user input,
    updates the simulation state, and renders the simulation on the screen.
    """
    C.display_loading_screen()
    hexagons = C.init_hexagons(G.gridSize())
    clock = Clock(time.time())
    terminated = False
    pause = True
    mouse_dragging = False
    original_mouse_position = None
    buttons = []
    # Simulation loop    
    while not terminated:
        clock.update()
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
                    if startButton.check_click():
                        if pause == True: pause = False
                        else: pass
                        break
                    if pauseButton.check_click():
                        if pause == False: pause = True
                        else: pass
                        break
                    if resetButton.check_click(): 
                        automata_main()
                        break
                    if backButton.check_click(): 
                        main()
                        break

                    colliding_hexagons = [
                        hexagon for hexagon in hexagons if hexagon.collide_with_point(mouse_pos)
                    ]
                    for hexagon in colliding_hexagons:
                        hexagon.state = 2
                        hexagon.colour = [255, 128, 0]    
                
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
                        hexagon.colour = [84, 45, 28]                

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
            clock.resume()
            C.change_hexagon_states(hexagons)        
            C.update_grid(hexagons)
        else:
            clock.pause()
        
        C.render(G.SCREEN, hexagons)

        startButton.draw(not pause)
        pauseButton.draw(pause)
        resetButton.draw()
        backButton.draw()

        clock.draw()

        if G.wind_strength != 0.0:
            C.draw_wind_triangle(G.SCREEN, G.wind_direction, G.WIND_ARROW_LENGTH, (100, 100))

        if startButton.check_click():
            startButton.draw(True)
        if pauseButton.check_click():
            pauseButton.draw(True)
        if resetButton.check_click():
            resetButton.draw(True)
        if backButton.check_click():
            backButton.draw(True)

        fps = G.CLOCK.get_fps()
        fps_text = f"FPS: {int(fps)}"
        
        pygame.display.set_caption(fps_text) 
        
        pygame.display.flip()
        G.CLOCK.tick(G.FPS)
        
    pygame.display.quit()

# * Main menu
def main():
    """
    Main function that runs the game loop for the main menu.
    """
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