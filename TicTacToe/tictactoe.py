#from ast import main
import sys
import copy
import random
from tkinter import OFF
from turtle import bgcolor, width
from xmlrpc.client import MAXINT
import pygame
import numpy as np

from constants import *

#PYGAME Setup
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT))
pygame.display.set_caption('TICTACTOE AI')
screen.fill(Background_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares # [squares]
        self.marked_squares = 0

    def final_state(self, show=False):
        '''
            return 0 if there is no win yet 
            return 1 if player 1 wins 
            return 2 if player 2 wins 
        '''
        # vertical wins 
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    fPos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # down diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                iPos = (20,20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # up diagonal 
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                iPos = (20,HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        

        # no win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1
    
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row,col))
        
        return empty_sqrs

    def isfull(self):
        return self.marked_squares == 9
    
    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rand(self, board):
        empty_sqrs = board.get_empty_sqrs()
        index = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[index] # (row, col)

    def minimax(self, board, maximizing):

        # Terminal case
        case = board.final_state()

        # player 1 wins 
        if case == 1:
            return 1, None
        
        # player 2 wins (AI)
        if case == 2:
            return -1, None
        
        # Draw
        elif board.isfull():
            return 0, None 

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move


    
    def eval(self, main_board):
        if self.level == 0:
            # random choice 
            eval = 'random'
            move = self.rand(main_board)
        
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # (row, col)



class Game:
    
    #init called everytime u call a game object 
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  # 1: cross, 2: circles 
        self.gamemode = 'ai'
        self.running = True

        self.showLines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    
    def showLines(self):

        screen.fill(Background_COLOR)
        # vertical lines 
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE,0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARE_SIZE,0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # horizontal lines 
        pygame.draw.line(screen, LINE_COLOR, (0,SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw X
            # neg slope
            start_neg = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_neg = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_neg, end_neg, CROSS_WIDTH)

            # pos slope
            start_pos = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_pos = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_pos, end_pos, CROSS_WIDTH)

        elif self.player == 2:
            # draw O
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)



    def next_turn(self):
        # code to change players 
        self.player = self.player % 2 + 1


    def change_gamemode(self):
        if self.gamemode == 'pvp': 
            self.gamemode = 'ai'
        else: 
            self.gamemode = 'pvp'

    def isover(self):
        return self.board.final_state(show = True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():
    
    #object 
    game = Game()

    board = game.board
    ai = game.ai

    # main loop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:

                # g = gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r = restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                
                # 0 = random AI
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 = minimax AI
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                
                if board.empty_sqr(row, col):
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

            
   
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False


                    
        pygame.display.update()




main()
