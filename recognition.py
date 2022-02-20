import time
import cv2
import numpy as np
from ctypes import windll
import win32com.client
from PIL import ImageGrab
import win32gui
from position import get_all_variations, get_best_pos, move
from tetrominoes import TETROMINOES_BRG

APP_NAME = 'TETRIS'
windows_list = []


# Fix problems with dpi
def configure_win32():
    user32 = windll.user32
    user32.SetProcessDPIAware()


def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))


def get_all_windows():
    top_list = []
    win32gui.EnumWindows(enum_win, top_list)


def set_foreground(hwnd):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


def find_game_window():
    configure_win32()
    while True:
        get_all_windows()
        for (hwnd, win_text) in windows_list:
            if win_text == APP_NAME:
                set_foreground(hwnd)
                return hwnd

        time.sleep(1)
        print('Please, open the app', end='\r')


def take_screenshot(position):
    screenshot = ImageGrab.grab(position)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot


def detect_the_board(screenshot):
    board_color = (np.array([12, 12, 12]), np.array([18, 18, 18]))
    board_mask = cv2.inRange(screenshot, board_color[0], board_color[1])
    contours, _ = cv2.findContours(board_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    return contours[0], board_mask


def set_position_on_the_board(board_arr, x, y, board_x, board_y, board_w, block_width, block_height):
    if x < board_x or x > board_x + board_w:
        return

    board_arr[int((y - board_y) / block_height), int((x - board_x) / block_width)] = 1


def create_cells(board, board_x, board_y, block_width, block_height):
    for row in range(20):
        for col in range(10):
            block_x = block_width * col
            block_y = block_height * row

            cv2.rectangle(board, (board_x + block_x, board_y + block_y),
                          (board_x + block_x + block_width, board_y + block_y + block_height),
                          (255, 255, 255), 1)


def check_first_2_lines(x, y, board_x, board_y, board_w, block_width, block_height):
    if board_x + block_height * 3 <= x <= board_x + board_w - block_width * 3 \
            and board_y <= y <= board_y + block_height * 3:
        return True

    return False


def show_text(frame_name, board=None, txt=None):
    img = np.zeros((400, 400, 1), np.uint8)
    for i in range(board.shape[0]):
        cv2.putText(img, str(board[i, :]),
                    (100, 16 * i + 50),
                    cv2.FONT_HERSHEY_TRIPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    1)
        cv2.putText(img, txt, (20, 336 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, 1)
        cv2.imshow(frame_name, img)


def visualize(frames: list, board_x, board_y, block_width, block_height):
    frames_resized = []
    for frame in frames:
        print(len(frames))
        # create_cells(frame, board_x, board_y, block_width, block_height)
        frames_resized.append(cv2.resize(frame, (400, 400)))

    cv2.imshow('Screen', frames_resized[0])
    cv2.imshow('Virtual board', frames_resized[1])
    cv2.imshow("Mask", frames_resized[2])
    cv2.waitKey(25)


def recognize_board_game(game_hwnd):
    position = win32gui.GetWindowRect(game_hwnd)
    screenshot = take_screenshot(position)
    rows, cols, _ = screenshot.shape

    # Creating virtual board
    # virtual_board = np.zeros((rows, cols, 3), dtype=np.uint8)

    cnt, board_mask = detect_the_board(screenshot)
    (board_x, board_y, board_w, board_h) = cv2.boundingRect(cnt)
    cv2.drawContours(screenshot, [cnt], -1, (0, 255, 0), 3)
    # cv2.drawContours(virtual_board, [cnt], -1, (0, 255, 0), 3)

    if board_h / board_w != 2:
        print('Waiting the game...', end='\r')
        time.sleep(1)
        return

    block_width = int(board_w / 10)
    block_height = int(board_h / 20)

    board_array = np.zeros((20, 10), dtype=int)
    current_tetromino = ''

    for key in TETROMINOES_BRG:
        bgr_color = TETROMINOES_BRG[key]
        bgr_color = np.array(bgr_color)
        mask = cv2.inRange(screenshot, bgr_color, bgr_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if check_first_2_lines(x, y, board_x, board_y, board_w, block_width, block_height):
                current_tetromino = key

            set_position_on_the_board(board_array, x, y, board_x, board_y, board_w, block_width, block_height)
            # cv2.rectangle(virtual_board, (x, y), (x + w, y + h),
            #               (0, 0, 255), 2)

    # Visualize computer vision
    # visualize([screenshot, virtual_board, board_mask], board_x, board_y, block_width, block_height)

    if current_tetromino == '':
        return

    var = get_all_variations(board_array[3:, :], current_tetromino)

    print(current_tetromino)
    print(board_array)

    position, rotation = get_best_pos(var)
    move(game_hwnd, position, rotation)

    return board_array
