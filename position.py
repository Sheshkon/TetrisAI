import time
import win32api
import win32con
import numpy as np
from tetrominoes import START_POS_TETROMINOES, TETROMINOES_SHAPES
import criteria
import recognition

KEY_DOWN_DELAY = 0.04


class PredictedBoard:

    def __init__(self, board=None, pos=-100):
        self.board = board
        self.pos = pos

    def is_empty(self):
        return self.pos == -100


def try_put(board, board_col, board_row, tetromino, tetromino_name, rotation):

    new_board = board.copy()

    for tetromino_col in range(tetromino.shape[1]):
        for tetromino_row in range(tetromino.shape[0]):
            if board_row == board.shape[0] - tetromino.shape[0] + 1 or new_board[
                board_row + tetromino_row, board_col + tetromino_col] + tetromino[tetromino_row, tetromino_col] > 1:

                return PredictedBoard()

            else:
                new_board[board_row + tetromino_row, board_col + tetromino_col] += tetromino[
                    tetromino_row, tetromino_col]

    return PredictedBoard(new_board, board_col - START_POS_TETROMINOES[tetromino_name][rotation] + 1)


def get_all_variations(board, tetromino_name):

    tetromino = TETROMINOES_SHAPES[tetromino_name]
    variations = []
    pre_ans = None

    for rotation in range(4):
        variations.append([])
        for board_col in range(board.shape[1] - tetromino.shape[1] + 1):
            for board_row in range(board.shape[0] - tetromino.shape[0] + 2):
                answer = try_put(board, board_col, board_row, tetromino, tetromino_name, rotation)
                if answer.is_empty() and pre_ans is not None and not pre_ans.is_empty():
                    variations[rotation].append(pre_ans)
                    break

                pre_ans = answer

        tetromino = np.rot90(tetromino)

    return variations


def fitness_func(board, peaks):
    return criteria.HEIGHT_COEFFICIENT * criteria.get_height(board) - \
           criteria.LINES_COEFFICIENT * criteria.get_lines(board) + \
           criteria.HOLES_COEFFICIENT * criteria.get_holes(board, peaks) + \
           criteria.BUMPINESS_COEFFICIENT * criteria.get_bumpiness(peaks) + \
           criteria.WEIGHT_COEFFICIENT * criteria.get_aggregate_weight(peaks)


def get_best_pos(var):
    score = 10000000
    rotation = -10
    position = -10
    board = None

    for i in range(len(var)):
        current_rotation = i
        for variant in var[i]:
            current_pos = variant.pos
            peaks = criteria.get_peaks(variant.board)
            current_score = fitness_func(variant.board, peaks)

            if current_score < score:
                score = current_score
                rotation = current_rotation
                position = current_pos
                board = variant.board

    # recognition.show_text('Best position', board=board, txt=f'position  {position} rotation {rotation} score {score}')
    print("position", position, 'rotation', rotation, 'score', score)
    return position, rotation


def move(game_hwnd, position, rotation):

    for _ in range(rotation):
        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, ord('A'))
        # win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, ord('A'))
        time.sleep(KEY_DOWN_DELAY)

    for _ in range(abs(position)):
        if position < 0:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_LEFT)
            # win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_LEFT)
        else:
            win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_RIGHT)
            # win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_RIGHT)
        time.sleep(KEY_DOWN_DELAY)
    win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE)
    # win32api.SendMessage(game_hwnd, win32con.WM_KEYUP, win32con.VK_SPACE)
    time.sleep(KEY_DOWN_DELAY)
