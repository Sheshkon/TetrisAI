import cv2
from recognition import find_game_window, recognize_board_game


if __name__ == '__main__':
    game_hwnd = find_game_window()

    while True:
        try:
            board_array = recognize_board_game(game_hwnd)
        except:
            cv2.destroyAllWindows()
            print('The app was closed or collapsed')
            break

    cv2.destroyAllWindows()

input("Program is finished, press ENTER")