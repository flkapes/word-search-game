import random
import string
import string as k
import numpy

LETTERS = {letter: index for index, letter in enumerate(k.ascii_uppercase, start=0)}
LETTERS2 = {v: k for k, v in LETTERS.items()}
print(LETTERS2)

useable_words_pre = []
useable_words = []


def parse_words(number):
    words = open('words.txt', 'r')
    words = words.read().split('\n')
    for word in words:
        if 1 < len(word) < number-1:
            useable_words_pre.append(word.upper())

    for x in range(number):
        useable_words.append(random.choice(useable_words_pre))
    useable_words_pre.clear()

    return useable_words


def create_word_search_board(number):
    board = numpy.zeros((number, number))

    for i in range(len(board)):
        for x in range(number):
            board[i][x] = -1

    print(board)
    return board


board = create_word_search_board(7)


def convert_word_search_to_readable():
    lol = ""
    temp = ""
    for x in board:
        lol += temp + "\n"
        temp = ""
        for i in x:
            if i != -1:
                temp += LETTERS2[i] + "\t"
            else:
                temp += random.choice(string.ascii_uppercase) + "\t"
    lol += temp + "\n"

    print(lol)


words_and_positions = []


def add_word_vertical(number):
    temp_variable = 0
    temp_variable_2 = 0
    while temp_variable != 1:
        curr_word = random.choice(useable_words)
        selected_row = random.randint(0, number)
        selected_col = random.randint(0, number)
        len_word = len(curr_word)
        space_available = number - selected_row
        if space_available >= len_word:
            temp_variable = 1
    for i in range(len_word):
        if board[selected_row+i][selected_col] == -1:
            board[selected_row+i][selected_col] = LETTERS[curr_word[i]]
        elif board[selected_row+i][selected_col] == curr_word[i]:
            board[selected_row+i][selected_col] = LETTERS[curr_word[i]]
        elif board[selected_row+i][selected_col] != curr_word[i] and board[selected_row+i][selected_col] != -1:
            break

    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row, selected_col, selected_col + len_word]
    useable_words.remove(curr_word)
    print(words_and_positions)
    return board


def add_word_horizontal(number):
    curr_word = random.choice(useable_words)
    selected_row = random.randint(1, number)
    selected_col = random.randint(1, number)
    len_word = len(curr_word)
    space_available = number - selected_col
    while space_available <= len_word:
        curr_word = random.choice(useable_words)
        selected_row = random.randint(1, number)
        selected_col = random.randint(1, number)
        len_word = len(curr_word)
        space_available = number - selected_col-1
    if space_available >= len_word:
        for i in range(len_word):
            if board[selected_row][selected_col+i] == -1:
                board[selected_row][selected_col+i] = LETTERS[curr_word[i]]
            elif board[selected_row][selected_col+i] == curr_word[i]:
                board[selected_row][selected_col+i] = LETTERS[curr_word[i]]
            else:
                return board
    else:
        return board
    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row, selected_col, selected_row+len_word]
    useable_words.remove(curr_word)
    print(words_and_positions)
    return board

parse_words(7)
board = add_word_horizontal(7)
board = add_word_horizontal(7)
board = add_word_horizontal(7)
board = add_word_vertical(7)
convert_word_search_to_readable()
