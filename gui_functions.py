# Drawing GUI functions for the game

import pygame, sys
from time import time
import copy
from kenken import *

width = 450
cell_size = 60
cage_size = cell_size * 2
background_color = (255, 255, 255)
cage_hint_margin = 5

# function to check if the coordinate in the cage_cells forms a square through distance square formula
def euclidean_distance(p, q):
    return ((p[0] - q[0]) **2)  + ((p[1] - q[1])**2)

def check_square(cage_cells):
    p1= cage_cells[0]
    p2= cage_cells[1]
    p3= cage_cells[2]
    p4= cage_cells[3]
    d2 = euclidean_distance(p1, p2)
    d3 = euclidean_distance(p1, p3) 
    d4 = euclidean_distance(p1, p4) 

    if d2 == 0 or d3 == 0 or d4 == 0:   
        return False
    if d2 == d3 and 2 * d2 == d4 and \
                    2 * euclidean_distance(p2, p4) == euclidean_distance(p2, p3):
        return True
    if d3 == d4 and 2 * d3 == d2 and \
                    2 * euclidean_distance(p3, p2) == euclidean_distance(p3, p4):
        return True

    if d2 == d4 and 2 * d2 == d3 and \
                    2 * euclidean_distance(p2, p3) == euclidean_distance(p2, p4):
        return True

    return False
        
# Draw cage's outside border according to the coordinates of the cage's cells [(x1, y1), (x2, y2), ...] where x, y start from 1
def draw_cage_border(cage_cells,current_cell_coordinate,skip_flag,starting_coordinate,screen):
    x1 = current_cell_coordinate[0]
    y1 = current_cell_coordinate[1]
    # if skip_flag doesn't equal to 'above' then check if cage_cells has adjacent cells above then call draw_cage_border recursively, else draw the border from the top
    # Remove the current cell from cage_cells tuple
    #cage_cells = tuple(filter(lambda x: x != (x1, y1), cage_cells))
    if skip_flag != 'above':
        if (x1, y1 - 1) in cage_cells:
            draw_cage_border(cage_cells, (x1, y1 - 1), 'bottom', starting_coordinate, screen)
        else:
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * (x1-1)), starting_coordinate[1] + (cell_size * (y1 - 1))), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * (y1-1))),3)
    # if skip_flag doesn't equal to 'bottom' then check if cage_cells has adjacent cells below then call draw_cage_border recursively, else draw the border from the bottom
    if skip_flag != 'bottom':
        if (x1, y1 + 1) in cage_cells:
            draw_cage_border(cage_cells, (x1, y1 + 1), 'above', starting_coordinate, screen)
        else:
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * (x1-1)), starting_coordinate[1] + (cell_size * y1)), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1)),3)
    # if skip_flag doesn't equal to 'left' then check if cage_cells has adjacent cells left then call draw_cage_border recursively, else draw the border from the left
    if skip_flag != 'left' :
        if (x1 - 1, y1) in cage_cells:
            draw_cage_border(cage_cells, (x1 - 1, y1), 'right', starting_coordinate, screen)
        else:
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * (x1-1)), starting_coordinate[1] + (cell_size * (y1-1))), (starting_coordinate[0] + (cell_size * (x1-1)), starting_coordinate[1] + (cell_size * y1)),3)
    # if skip_flag doesn't equal to 'right' then check if cage_cells has adjacent cells right then call draw_cage_border recursively, else draw the border from the right
    if skip_flag != 'right':
        if (x1 + 1, y1) in cage_cells:
            draw_cage_border(cage_cells, (x1 + 1, y1), 'left', starting_coordinate, screen)
        else:
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * (y1-1))), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1)),3)
    pygame.display.update()


def draw_empty_puzzle_board(cliques,starting_coordinate,screen,font):
    # Cliques on the board 
    # cliques=[(((1, 1), (2, 1), (2, 2)), '*', 12), (((3, 1), (3, 2), (3, 3)), '+', 6), (((1, 2),), '=', 1), (((1, 3),), '=', 3), (((2, 3),), '=', 1)]
    # Iterate over the cliques and draw each cage border from the first given list in each clique using draw_cage_border function and the operation symbol in the second item in each clique and the result in the third item in each clique
    
    for clique in cliques:
        # Write the operation symbol in the first cell of each clique at the top left of the cage
        screen.blit(font.render(str(clique[2])+' '+ clique[1], True, (0, 0, 0)), (starting_coordinate[0] + (cell_size * (clique[0][0][0] - 1)) + cage_hint_margin, starting_coordinate[1] + (cell_size * (clique[0][0][1] - 1)) + cage_hint_margin))
        # Check if the clique cells is a square cage using check_square_cage function and draw the cage border around the square cage using pygame.draw.line function
        if len(clique[0])==4 and check_square(clique[0]):
            x1 = clique[0][0][0] -1
            y1 = clique[0][0][1] -1
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1 )), (starting_coordinate[0] + (cell_size * x1) + cage_size, starting_coordinate[1] + (cell_size * y1)),3)
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1)), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1) + cage_size),3)
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * x1) + cage_size, starting_coordinate[1] + (cell_size * y1)), (starting_coordinate[0] + (cell_size * x1) + cage_size, starting_coordinate[1] + (cell_size * y1) + cage_size),3)
            pygame.draw.line(screen, (0, 0, 0), (starting_coordinate[0] + (cell_size * x1), starting_coordinate[1] + (cell_size * y1) + cage_size), (starting_coordinate[0] + (cell_size * x1) + cage_size, starting_coordinate[1] + (cell_size * y1) + cage_size),3)
            pygame.display.update()
        else: 
            draw_cage_border(clique[0], clique[0][0], skip_flag=None, starting_coordinate=starting_coordinate,screen=screen)

# draw puzzle vertical and horizontal lines
def draw_puzzle_lines(screen,size):
    # Draw the grid lines and the borders of the board of size 'size' centered in the screen
    for i in range(size+1):
        start_x = (width - (cell_size * size)) / 2
        start_y = (width - (cell_size * size)) / 2
        end_x = start_x + (cell_size * size)
        end_y = start_y + (cell_size * size)
        pygame.draw.line(screen, (0, 0, 0), (start_x + (cell_size * i), start_y), (start_x + (cell_size * i), end_y))
        pygame.draw.line(screen, (0, 0, 0), (start_x, start_y + (cell_size * i)), (end_x, start_y + (cell_size * i)))
    pygame.display.update()

# Kenken game round
class kenken_round():
    def __init__(self, size):
        # Integration code
        self.size, self.cliques = make_new_random_board(size)
        start_x = (width - (cell_size * size)) / 2
        start_y = (width - (cell_size * size)) / 2
        self.starting_coordinate = (start_x, start_y)


    # Draw kenken round
    def draw_kenken_round(self):
        pygame.init()
        # init pygame font
        pygame.font.init()
        font = pygame.font.SysFont("Grobold", 20)
        self.screen = pygame.display.set_mode((width, width))
        pygame.display.set_caption('Kenken game')
        self.screen.fill(background_color)
        # Draw the grid lines and the borders of the board of size 'size' centered in the screen
        draw_puzzle_lines(self.screen, self.size)


        # Draw the empty puzzle board
        draw_empty_puzzle_board(self.cliques, self.starting_coordinate, self.screen,font)
        
        quit = False
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    pygame.display.quit()

    
    # Drawing board answer integration function
    def draw_board_answer_integration(self,entered_inference):
        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont("Grobold", 20)
        screen = pygame.display.set_mode((width, width))
        pygame.display.set_caption('Kenken game')
        screen.fill(background_color)
        
        # Draw the cage's answer
        def draw_board_answer(self,board_answer,starting_coordinate,font):
            # Access the cage's answer dictionary and write the answer for each cell in the cage in the center of the cell
            for cage_cells, answer in board_answer.items():
                for i,cell in enumerate(cage_cells):
                    x = cell[0]
                    y = cell[1]
                    # Write the answer in the center of the cell
                    text = font.render(str(answer[i]), True, (0, 0, 0))
                    text_rect = text.get_rect()
                    text_rect.center = (starting_coordinate[0] + (cell_size * ((x-1)+0.5)), starting_coordinate[1] + (cell_size * ((y-1)+0.5)))
                    screen.blit(text, text_rect)
                    screen.blit(text, text_rect)
            pygame.display.update()
        # board_answer={((1, 1), (2, 1), (2, 2)): [12, 12, 12], ((3, 1), (3, 2), (3, 3)): [6, 6, 6], ((1, 2),): [1], ((1, 3),): [3], ((2, 3),): [1]}

        draw_puzzle_lines(screen,self.size)
        draw_empty_puzzle_board(self.cliques, self.starting_coordinate, screen, font)
        
        ken = Kenken(self.size, copy.deepcopy(self.cliques))
        # calculate the time taken to solve the puzzle
        start_time = time()
        assignment = csp.backtracking_search(ken, inference=entered_inference)
        end_time = time() 

        # show the time taken to solve the puzzle in seconds
        print("Time taken to solve the puzzle: ", end_time - start_time)
        draw_board_answer(self,assignment,starting_coordinate=self.starting_coordinate,font=font)
        print('solve using' + str(entered_inference))
        pygame.display.update()
        print('updated')
        quit = False
        while not quit:
            pygame.init()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    pygame.display.quit()
                    sys.exit()
