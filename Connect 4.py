import math
import random
import pygame
import sys

EMPTY = 0
PLAYER = 2
AI = 1

BLUE_RGB = (0,0,255)
BLACK_RGB = (0,0,0)
RED_RGB = (255,0,0)
YELLOW_RGB = (255,255,0)


class Board:


    def initialize_board(self):
        self.board = [[EMPTY for _ in range(self.columns_no)] for _ in range(self.rows_no)]

    def __init__(self, rows_no:int, columns_no:int, window_length:int):
        self.rows_no = rows_no
        self.columns_no = columns_no
        self.window_length = window_length
        self.subtract_value = window_length
        self.initialize_board()

    def update_board(self, row, column, symbol):
        self.board[row][column] = symbol
    
    def is_column_empty(self, column):
        for row in range(self.rows_no):
            if self.board[row][column] == EMPTY:
                return True
        return False
    
    def get_possible_columns(self):
        possible_columns = []
        for column in range(self.columns_no):
            if self.is_column_empty(column):
                possible_columns.append(column)
        return possible_columns


    def get_center_column(self):
        column_index = self.columns_no // 2
        return self.board[:][column_index]
    
    def get_empty_row(self, column):
        for row in range(self.rows_no):
            if self.board[row][column] == EMPTY:
                return row
    

    def get_rows_of_length(self):
        rows = []
        for row in range(self.rows_no):
            for column in range(self.columns_no - self.subtract_value):
                selected_row = [self.board[row][column + i] for i in range(self.window_length)]
                rows.append(selected_row)
        return rows

    def get_columns_of_length(self):
        columns = []
        for column in range(self.columns_no):
            for row in range(self.rows_no - self.subtract_value):
                selected_column = [self.board[row+i][column] for i in range(self.window_length)]
                columns.append(selected_column)
        return columns
    
    def get_diagonals(self):
        diagonals = []
        for row in range(self.rows_no - self.subtract_value):
            for column in range(self.columns_no - self.subtract_value):
                positive_diag = [self.board[row+3-i][column+i] for i in range(self.window_length)]
                negative_diag = [self.board[row+i][column+i] for i in range(self.window_length)]
                diagonals.append(positive_diag)
                diagonals.append(negative_diag)
        return diagonals

        






class Heuristic:

    def __init__(self, board:Board):
        self.board = board

    
    

    def evaluate_state(self, state, symbol):
        opponent = -1 if symbol == 1 else 1
        score = 0
        if state.count(symbol) == 4:
            score += 100
        elif state.count(symbol) == 3 and state.count(EMPTY) == 1:
            score += 60
        elif state.count(symbol) == 2 and state.count(EMPTY) == 2:
            score += 20
        if state.count(opponent) == 3 and state.count(EMPTY) == 1:
            score -= 50

        return score

    

    def get_center_column_score(self, symbol):
        column = self.board.get_center_column()
        return column.count(symbol) * 3


    
    def get_horizontal_score(self, symbol):
        horizontal_score = 0
        for state in self.board.get_rows_of_length():
            horizontal_score += self.evaluate_state(state, symbol)
        return horizontal_score


    def get_vertical_score(self, symbol):
        vertical_score = 0
        for state in self.board.get_columns_of_length():
            vertical_score += self.evaluate_state(state, symbol)
        return vertical_score

    def get_diagonal_score(self, symbol):
        diag_score = 0
        for state in self.board.get_diagonals():
            diag_score += self.evaluate_state(state, symbol)
        return diag_score

    def compute_score(self, symbol):
        center_score = self.get_center_column_score(symbol)
        horizontal_score = self.get_horizontal_score(symbol)
        vertical_score = self.get_vertical_score(symbol)
        diag_score = self.get_diagonal_score(symbol)
        return center_score + horizontal_score + \
               vertical_score + diag_score




    
class View:

    def __init__(self, board:Board):
        self.board = board
        self.SQUARESIZE = 100
        self.width = columns_no * self.SQUARESIZE
        self.height = (rows_no+1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        self.screen = pygame.display.set_mode(self.size)


    def draw_board(self, p1, p2):
        square = self.SQUARESIZE
        radius = self.RADIUS
        for c in range(self.board.columns_no):
            for r in range(self.board.rows_no):
                pygame.draw.rect(self.screen, BLUE_RGB, (c*square, r*square+square, square, square))
                pygame.draw.circle(self.screen, BLACK_RGB, (int(c*square+square/2), int(r*square+square+square/2)), radius)
	
        for c in range(self.board.columns_no):
            for r in range(self.board.rows_no):		
                if self.board.board[r][c] == p1:
                    pygame.draw.circle(self.screen, RED_RGB, (int(c*square+square/2), self.height-int(r*square+square/2)), radius)
                elif self.board.board[r][c] == p2: 
                    pygame.draw.circle(self.screen, YELLOW_RGB, (int(c*square+square/2), self.height-int(r*square+square/2)), radius)

        pygame.display.update()

    def handle_events(self, event, turn, p1):
        column = None
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(self.screen, BLACK_RGB, (0,0, self.width, self.SQUARESIZE))
            posx = event.pos[0]
            if turn == p1:
                pygame.draw.circle(self.screen, RED_RGB, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
            else:
                pygame.draw.circle(self.screen, YELLOW_RGB, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(self.screen, BLACK_RGB, (0,0, self.width, self.SQUARESIZE))
            posx = event.pos[0]
            column = int(math.floor(posx/self.SQUARESIZE))
        return column

    def announce_winner(self, winner):
        self.myfont = pygame.font.SysFont("monospace", 75)
        label = self.myfont.render(f"Player {winner} wins!!", 1, RED_RGB)
        self.screen.blit(label, (10,10))
            


class GameManager:

    def __init__(self, board:Board, view:View):
        self.board = board
        self.view = view
        

    @staticmethod
    def are_all_identical(state, symbol):
        return state.count(symbol) == len(state)

    def check_rows(self, symbol):
        for state in self.board.get_rows_of_length():
            if self.are_all_identical(state, symbol):
                return True
        return False

    def check_columns(self, symbol):
        for state in self.board.get_columns_of_length():
            if self.are_all_identical(state, symbol):
                return True
        return False

    def check_diagonals(self, symbol):
        for state in self.board.get_diagonals():
            if self.are_all_identical(state, symbol):
                return True
        return False

    
    def check_winner(self, symbol):
        if self.check_rows(symbol) or \
           self.check_columns(symbol) or \
           self.check_diagonals(symbol):
           return True
        return False


    def is_terminal_state(self):
        return self.check_winner(PLAYER) or \
               self.check_winner(AI) or \
               len(self.board.get_possible_columns()) == 0

    def PvP(self):
        p1, p2 = 1, 2
        turn = random.randint(p1, p2)
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                column = self.view.handle_events(event, turn, p1)
                if column is not None:
                    if self.board.is_column_empty(column):
                        empty_row = self.board.get_empty_row(column)
                        self.board.update_board(empty_row, column, turn)

                    if self.check_winner(turn):
                        self.view.announce_winner(turn)
                        game_over = True
                    turn += 1
                    if turn > 2 : turn = p1
            self.view.draw_board(p1, p2)
            if game_over:
                pygame.time.wait(3000)
    

    def PvA(self, minimax):
        turn = random.randint(AI, PLAYER)
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                column = self.view.handle_events(event, turn, PLAYER)
                if column is not None:
                    if self.board.is_column_empty(column):
                        empty_row = self.board.get_empty_row(column)
                        self.board.update_board(empty_row, column, turn)

                    if self.check_winner(turn):
                        self.view.announce_winner(turn)
                        pygame.time.wait(3000)
                        game_over = True
                    turn += 1
                    if turn > 2 : turn = AI
            
            if turn == AI and not game_over:
                column, minimax_score = minimax.minimax(-math.inf, math.inf, minimax.depth, True)
                if self.board.is_column_empty(column):
                    empty_row = self.board.get_empty_row(column)
                    self.board.update_board(empty_row, column, AI)

                if self.check_winner(AI):
                    self.view.announce_winner(2)
                    game_over = True

                turn += 1
                if turn > 2 : turn = AI
            self.view.draw_board(PLAYER, AI)
            if game_over:
                pygame.time.wait(3000)

            




    def start_game(self, game_mode, minimax=None):
        if game_mode == 0:
            self.PvP()
    
        elif game_mode == 1:
            self.PvA(minimax)

        else:
            raise Exception("Invalid Game Mode!")


class Minimax:

    def __init__(self, board:Board, heuristic:Heuristic, manager:GameManager, depth:int):
        self.board = board
        self.manager = manager
        self.heuristic = heuristic
        self.depth = depth

    

    def minimax(self, alpha, beta, depth, maximizing_player):
        possible_columns = self.board.get_possible_columns()
        is_terminal_node = self.manager.is_terminal_state()
        if depth == 0 or is_terminal_node:
            if is_terminal_node:
                if self.manager.check_winner(PLAYER):
                    return (None, -1e8)
                elif self.manager.check_winner(AI):
                    return (None, 1e8)
                else:
                    return (None, 0)
            else:
                return (None, self.heuristic.compute_score(AI))
        if maximizing_player:
            max_eval = -math.inf
            current_column = random.choice(possible_columns)
            for column in possible_columns:
                empty_row = self.board.get_empty_row(column)
                self.board.update_board(empty_row, column, AI)
                eval_score = self.minimax(alpha, beta, depth-1, False)[1]
                self.board.update_board(empty_row, column, EMPTY)
                if eval_score > max_eval:
                    max_eval = eval_score
                    current_column = column
                alpha = max(alpha, max_eval)
                if alpha >= beta:
                    break
            return current_column, max_eval
        else:
            min_eval = math.inf
            current_column = random.choice(possible_columns)
            for column in possible_columns:
                empty_row = self.board.get_empty_row(column)
                self.board.update_board(empty_row, column, PLAYER)
                eval_score = self.minimax(alpha, beta, depth-1, True)[1]
                self.board.update_board(empty_row, column, EMPTY)
                if eval_score < min_eval:
                    min_eval = eval_score
                    current_column = column
                beta = min(beta, min_eval)
                if alpha >= beta:
                    break
            return current_column, min_eval








rows_no, columns_no = map(int, input('Please enter size of table : ').split())

board = Board(rows_no, columns_no, 4)
view = View(board)
game_manager = GameManager(board, view)
heuristic = Heuristic(board)
minimax = Minimax(board, heuristic, game_manager, 5)
print('0:PvP , 1:PvA')
game_mode = int(input('Please enter game mode : '))
pygame.init()
game_manager.start_game(game_mode, minimax=minimax)
        

    