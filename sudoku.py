import pygame

pygame.init()

screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption('Sudoku')

x,y = screen.get_size()
grid = []

cell_size = 540 // 9
selected_col, selected_row = None, None
font = pygame.font.Font(None, 50)

red = (255,0,0)
black = (0, 0, 0)
grey = (242,243,245)
white = (255, 255, 255)
green = (0,255,0)

game_state = 'playing'

def valid_move(grid, row, col, num):
    if num in grid[row]:
        return False
    if num in [grid[i][col] for i in range(9)]:
        return False

    subgrid_row_start = (row // 3) * 3
    subgrid_col_start = (col // 3) * 3
    for i in range(subgrid_row_start, subgrid_row_start + 3):
        for j in range(subgrid_col_start, subgrid_col_start + 3):
            if grid[i][j] == num:
                return False
    return True 
    
def find_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return row, col
    return None

def check_grid():
    for row in range(9):
        if sorted(grid[row]) != list(range(1, 10)):
            return False
    for col in range(9):
        if sorted([grid[row][col] for row in range(9)]) != list(range(1, 10)):
            return False
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            subgrid = [
                grid[row][col]
                for row in range(box_row, box_row + 3)
                for col in range(box_col, box_col + 3)
            ]
            if sorted(subgrid) != list(range(1, 10)):
                return False

    return True
    
def draw_grid():
    for i in range(10):
        x = i * cell_size
        y = i * cell_size
        
        if i % 3 == 0:
            pygame.draw.line(screen, white, (x, 0), (x, 540), 2)
        else:
            pygame.draw.line(screen, grey, (x, 0), (x, 540), 1)

        if i % 3 == 0:
            pygame.draw.line(screen, white, (0, y), (540, y), 2)
        else:
            pygame.draw.line(screen, grey, (0, y), (540, y), 1)
    
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:                  
                if (row, col) in pre_filled:
                    colour = white 
                else:
                    colour = green                
                text = font.render(str(grid[row][col]), True, colour)
                x_pos = col * cell_size + cell_size // 3
                y_pos = row * cell_size + cell_size // 3
                screen.blit(text, (x_pos, y_pos))
    
    if selected_row is not None and selected_col is not None:
                pygame.draw.rect(screen, red, pygame.Rect(selected_col * cell_size, selected_row * cell_size, cell_size, cell_size), 3)

grid = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
	[4, 0, 7, 0, 0, 0, 2, 0, 8],
	[0, 0, 5, 2, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 9, 8, 1, 0, 0],
	[0, 4, 0, 0, 0, 3, 0, 0, 0],
	[0, 0, 0, 3, 6, 0, 0, 7, 2],
	[0, 7, 0, 0, 0, 0, 0, 0, 3],
	[9, 0, 3, 0, 0, 0, 6, 0, 4]]

pre_filled = [(row, col) for row in range(9) for col in range(9) if grid[row][col] != 0]

running = True
while running == True:
    screen. fill(black)

    draw_grid()

    if game_state == 'solved':
        text = font.render('Puzzle Solved!', True, white)
        text1 = font.render('Press SPACE to restart', True, white)
        screen.blit(text, (150, 520))
        screen.blit(text1, (150, 550))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == 'playing':
            if pygame.mouse.get_pressed(): 
                x_pos, y_pos = pygame.mouse.get_pos()
                selected_row = y_pos // cell_size 
                selected_col = x_pos // cell_size
            
        elif event.type == pygame.KEYDOWN:
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                number = event.key - pygame.K_0
                if grid[selected_row][selected_col] == 0 and valid_move(grid, selected_row, selected_col, number):
                    grid[selected_row][selected_col] = number

                    if check_grid():
                        game_state = 'solved'                   
           
            elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    if (selected_row, selected_col) not in pre_filled:
                        grid[selected_row][selected_col] = 0
            
            elif event.key == pygame.K_SPACE and game_state == 'solved':
                grid = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
                        [0, 1, 0, 0, 0, 4, 0, 0, 0],
                        [4, 0, 7, 0, 0, 0, 2, 0, 8],
                        [0, 0, 5, 2, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 9, 8, 1, 0, 0],
                        [0, 4, 0, 0, 0, 3, 0, 0, 0],
                        [0, 0, 0, 3, 6, 0, 0, 7, 2],
                        [0, 7, 0, 0, 0, 0, 0, 0, 3],
                        [9, 0, 3, 0, 0, 0, 6, 0, 4]
                        ]
                pre_filled = [
                    (row, col)
                    for row in range(9)
                    for col in range(9)
                    if grid[row][col] != 0
                ]
                selected_row, selected_col = None, None
                game_state = 'playing'

            elif event.key == pygame.K_UP:
                if selected_row is not None:
                    selected_row = max(0, selected_row - 1)

            elif event.key == pygame.K_DOWN:
                if selected_row is not None:
                    selected_row = min(8, selected_row + 1)

            elif event.key == pygame.K_LEFT:
                if selected_col is not None:
                    selected_col = max(0, selected_col - 1)

            elif event.key == pygame.K_RIGHT:  
                if selected_col is not None:
                    selected_col = min(8, selected_col + 1)   

    pygame.display.flip()

pygame.quit()

