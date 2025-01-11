import pygame  # Import the Pygame library

class SudokuGame:
    def __init__(self):
        pygame.init()  # Initialize all Pygame modules

        # Create the game window and set its size to 970x550 pixels
        self.screen = pygame.display.set_mode((970, 550))
        pygame.display.set_caption('Sudoku')

        # Define constants
        self.cell_size = 540 // 9  # Size of each cell in the Sudoku grid
        self.font = pygame.font.Font(None, 50)

        self.colors = {
            'red': (255, 0, 0),
            'black': (0, 0, 0),
            'grey': (242, 243, 245),
            'white': (255, 255, 255),
            'green': (0, 255, 0)
        }

        # Game variables
        self.grid = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
                     [0, 1, 0, 0, 0, 4, 0, 0, 0],
                     [4, 0, 7, 0, 0, 0, 2, 0, 8],
                     [0, 0, 5, 2, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 9, 8, 1, 0, 0],
                     [0, 4, 0, 0, 0, 3, 0, 0, 0],
                     [0, 0, 0, 3, 6, 0, 0, 7, 2],
                     [0, 7, 0, 0, 0, 0, 0, 0, 3],
                     [9, 0, 3, 0, 0, 0, 6, 0, 4]]

        self.pre_filled = [(row, col) for row in range(9) for col in range(9) if self.grid[row][col] != 0]
        self.selected_row, self.selected_col = None, None
        self.game_state = 'playing'

    def valid_move(self, row, col, num):
        # Check if the number exists in the row
        if num in self.grid[row]:
            return False
        # Check if the number exists in the column
        if num in [self.grid[i][col] for i in range(9)]:
            return False

        # Check if the number exists in the 3x3 subgrid
        subgrid_row_start = (row // 3) * 3
        subgrid_col_start = (col // 3) * 3
        for i in range(subgrid_row_start, subgrid_row_start + 3):
            for j in range(subgrid_col_start, subgrid_col_start + 3):   
                if self.grid[i][j] == num:
                    return False
        return True

    def check_grid(self):
        for row in range(9):
            if sorted(self.grid[row]) != list(range(1, 10)):
                return False

        for col in range(9):
            if sorted([self.grid[row][col] for row in range(9)]) != list(range(1, 10)):
                return False

        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                subgrid = [
                    self.grid[row][col]
                    for row in range(box_row, box_row + 3)
                    for col in range(box_col, box_col + 3)
                ]
                if sorted(subgrid) != list(range(1, 10)):
                    return False

        return True

    def draw_grid(self):
        for i in range(10):
            x = i * self.cell_size
            y = i * self.cell_size

            if i % 3 == 0:
                pygame.draw.line(self.screen, self.colors['white'], (x, 0), (x, 540), 2)
                pygame.draw.line(self.screen, self.colors['white'], (0, y), (540, y), 2)
            else:
                pygame.draw.line(self.screen, self.colors['grey'], (x, 0), (x, 540), 1)
                pygame.draw.line(self.screen, self.colors['grey'], (0, y), (540, y), 1)

        for row in range(9):
            for col in range(9):
                if self.grid[row][col] != 0:
                    color = self.colors['white'] if (row, col) in self.pre_filled else self.colors['green']
                    text = self.font.render(str(self.grid[row][col]), True, color)
                    x_pos = col * self.cell_size + self.cell_size // 3
                    y_pos = row * self.cell_size + self.cell_size // 3
                    self.screen.blit(text, (x_pos, y_pos))

        if self.selected_row is not None and self.selected_col is not None:
            pygame.draw.rect(self.screen, self.colors['red'], pygame.Rect(
                self.selected_col * self.cell_size, self.selected_row * self.cell_size, self.cell_size, self.cell_size), 3)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == 'playing':
                if pygame.mouse.get_pressed():
                    x_pos, y_pos = pygame.mouse.get_pos()
                    self.selected_row = y_pos // self.cell_size
                    self.selected_col = x_pos // self.cell_size

            elif event.type == pygame.KEYDOWN:
                if event.key in range(pygame.K_1, pygame.K_9 + 1):
                    number = event.key - pygame.K_0
                    if self.grid[self.selected_row][self.selected_col] == 0 and self.valid_move(self.selected_row, self.selected_col, number):
                        self.grid[self.selected_row][self.selected_col] = number
                        if self.check_grid():
                            self.game_state = 'solved'

                elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    if (self.selected_row, self.selected_col) not in self.pre_filled:
                        self.grid[self.selected_row][self.selected_col] = 0

                elif event.key == pygame.K_SPACE and self.game_state == 'solved':
                    self.__init__()

                elif event.key == pygame.K_UP:
                    if self.selected_row is not None:
                        self.selected_row = max(0, self.selected_row - 1)

                elif event.key == pygame.K_DOWN:
                    if self.selected_row is not None:
                        self.selected_row = min(8, self.selected_row + 1)

                elif event.key == pygame.K_LEFT:
                    if self.selected_col is not None:
                        self.selected_col = max(0, self.selected_col - 1)

                elif event.key == pygame.K_RIGHT:
                    if self.selected_col is not None:
                        self.selected_col = min(8, self.selected_col + 1)

        return True

    def run(self):
        running = True
        while running:
            self.screen.fill(self.colors['black'])
            self.draw_grid()

            if self.game_state == 'solved':
                text = self.font.render('Puzzle Solved!', True, self.colors['white'])
                text1 = self.font.render('Press SPACE to restart', True, self.colors['white'])
                self.screen.blit(text, (550, 200))
                self.screen.blit(text1, (550, 250))

            running = self.handle_events()
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    SudokuGame().run()
