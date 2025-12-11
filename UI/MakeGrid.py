import pygame

def MakeGrid(screen, stepx, stepy, nx, ny, col, HEIGHT, WIDTH):
    for i in range(ny+1):
        for j in range(nx+1):
            pygame.draw.line(surface = screen, color = col, start_pos=(0+i*(stepy), 0),
                             end_pos=(0+i*(stepx), HEIGHT) )
            pygame.draw.line(surface=screen, color=col, start_pos=(0,0 + j * (stepx)),
                             end_pos=(WIDTH, 0 + j * (stepy)))