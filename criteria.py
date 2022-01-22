import numpy as np

HEIGHT_COEFFICIENT = 0
LINES_COEFFICIENT = 0.760666
HOLES_COEFFICIENT = 0.35663
BUMPINESS_COEFFICIENT = 0.184483
WEIGHT_COEFFICIENT = 0.510066


def get_peaks(board):
    peaks = np.array([])

    for j in range(board.shape[1]):
        if 1 in board[:, j]:
            value = board.shape[0] - np.argmax(board[:, j])
        else:
            value = 0
        peaks = np.append(peaks, value)

    return peaks


def get_aggregate_weight(peaks):
    return np.sum(peaks)


def get_holes(board, peaks):
    holes_count = np.array([])

    for i in range(board.shape[1]):
        if peaks[i] == 0:
            holes_count = np.append(holes_count, 0)
        else:
            holes_count = np.append(holes_count, peaks[i] - np.sum(board[int(-peaks[i]):, i]))

    return sum(holes_count)


def get_bumpiness(peaks):
    bumpiness = 0
    for i in range(len(peaks) - 1):
        bumpiness += abs(peaks[i] - peaks[i + 1])

    return bumpiness


def get_lines(board):
    lines_count = 0
    for i in range(board.shape[0]):
        if 0 not in board[i, :]:
            lines_count += 1

    return lines_count


def get_height(board):
    return np.max(get_peaks(board))


def get_peaks_number(peaks):
    peaks_count = 0
    for i in range(len(peaks)):
        if peaks[i] != 0:
            peaks_count += 1
    return peaks_count
