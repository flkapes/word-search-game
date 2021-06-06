import math
import random
import string
import time
from itertools import chain
from art import *
from huepy import *


import numpy

LETTERS = {
    letter: index for index,
    letter in enumerate(
        string.ascii_uppercase,
        start=0)}
LETTERS2 = {v: k for k, v in LETTERS.items()}
useable_words = []


def parse_words(number):
    words = open('words.txt', 'r')
    words = words.read().split('\n')
    for word in words:
        if 1 < len(word) < number - 1:
            useable_words.append(word.upper())

    return useable_words


def create_word_search_board(number):
    board = numpy.zeros((number, number))

    for i in range(len(board)):
        for x in range(number):
            board[i][x] = -1

    return board


def convert_word_search_to_readable(board):
    lol = '\033[4m' + "\t | \t1\t2\t3\t4\t5\t6\t7\t" + '\033[0m'
    temp = ""
    z = 0
    for x in board:
        if z != 0:
            lol += str(z) + '\t | \t' + temp + "\n"
        else:
            lol = lol + '\n'
        temp = ""
        z += 1
        for i in x:
            if i != -1:
                temp += LETTERS2[i] + "\t"
            else:
                temp += random.choice(string.ascii_uppercase) + "\t"
    lol += str(z) + "\t | \t" + temp + "\n"

    return lol


words_and_positions = []


def add_word_vertical(board, number):
    temp_variable = 0
    while temp_variable != 1:
        curr_word = random.choice(useable_words)
        selected_row = random.randint(0, number)
        selected_col = random.randint(0, number)
        len_word = len(curr_word)
        space_available = number - selected_row
        if space_available >= len_word:
            temp_variable = 1
    for i in range(len_word):
        if board[selected_row + i][selected_col - 1] == -1:
            board[selected_row + i][selected_col - 1] = LETTERS[curr_word[i]]
        elif board[selected_row + i][selected_col - 1] == curr_word[i]:
            board[selected_row + i][selected_col - 1] = LETTERS[curr_word[i]]
        elif board[selected_row + i][selected_col - 1] != curr_word[i] and board[selected_row + i][selected_col] != -1:
            return board

    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row + 1,
                                          selected_col, selected_row + len_word, selected_col]
    useable_words.remove(curr_word)
    return board


def add_word_horizontal(board, number):
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
        space_available = number - selected_col - 1
    if space_available >= len_word:
        for i in range(len_word):
            if board[selected_row - 1][selected_col + i] == -1:
                board[selected_row - 1][selected_col +
                                        i] = LETTERS[curr_word[i]]
            elif board[selected_row - 1][selected_col + i] == curr_word[i]:
                board[selected_row - 1][selected_col +
                                        i] = LETTERS[curr_word[i]]
            else:
                return board
    else:
        return board
    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row,
                                          selected_col + 1, selected_row, selected_col + len_word]
    useable_words.remove(curr_word)
    return board


def get_curr_time():
    ret_time = time.time()
    return ret_time


def check_answer(x1, y1, x2, y2, ans_index, word):
    if x1 == words_and_positions[ans_index][word][0]:
        if y1 == words_and_positions[ans_index][word][1]:
            if x2 == words_and_positions[ans_index][word][2]:
                if y2 == words_and_positions[ans_index][word][3]:
                    return True
    else:
        return False


def check_inputs(inp, points, time_elapsed):
    if "FINISH" in inp:
        print("You have scored a total of " +
              str(points) +
              " over the course of " +
              str(math.floor(time_elapsed //
                             60)) +
              " minutes and " +
              str(math.floor((time_elapsed /
                              60 -
                              time_elapsed //
                              60) *
                             60)) +
              " seconds")
        quit()
    elif "ANSWERS" in inp:
        print("You have scored a total of " +
              str(points) +
              " over the course of " +
              str(math.floor(time_elapsed //
                             60)) +
              " minutes and " +
              str(math.floor((time_elapsed /
                              60 -
                              time_elapsed //
                              60) *
                             60)) +
              " seconds")
        print(words_and_positions)
        quit()
    elif "AGAIN" in inp:
        print("You have scored a total of " +
              str(points) +
              " over the course of " +
              str(math.floor(time_elapsed //
                             60)) +
              " minutes and " +
              str(math.floor((time_elapsed /
                              60 -
                              time_elapsed //
                              60) *
                             60)) +
              " seconds")
        main()
    else:
        return True


def main():
    print(bold(red(text2art("Word   Search   Game"))))
    points = 0
    number = int(
        input(
            bold(
                cyan(
                    "Please input the number of columns you want (i.e. size of the grid) \t"))))
    parse_words(number)
    board = create_word_search_board(number)
    for i in range(random.randint(3, 5)):
        temp = random.randint(0, 1)
        if temp == 0:
            add_word_horizontal(board, number)
        if temp == 1:
            add_word_vertical(board, number)
    try:
        temp = random.randint(0, 1)
        if temp == 0:
            add_word_horizontal(board, number)
        if temp == 1:
            add_word_vertical(board, number)
    except BaseException:
        pass

    print(convert_word_search_to_readable(board))
    headers_as_set = set(chain.from_iterable(words_and_positions))
    print(headers_as_set)
    time_start = get_curr_time()
    ongoing = 1
    while ongoing == 1:
        word_in = input(bold(cyan("Input the word \t"))).upper()
        if check_inputs(word_in, points, get_curr_time() - time_start):
            pass
        user_in = input(bold(cyan(
            "Input the starting x and y coordinates of the word, separated by a comma (i.e. x1, y1) \t")))
        if check_inputs(user_in, points, get_curr_time() - time_start):
            pass
        user_in2 = input(bold(cyan(
            "Input the ending x and y coordinates of the word, separated by a comma (i.e. x2, y2) \t")))
        if check_inputs(user_in2, points, get_curr_time() - time_start):
            pass

        saved_index = -1

        for i in range(len(words_and_positions)):
            try:
                kek = words_and_positions[i][word_in]
                saved_index = i
                print(good(word_in + ' found'))
            except KeyError:
                continue

        print(run('Checking coordinates now...'))

        x1 = int(user_in.replace(" ", "").split(",")[0])
        y1 = int(user_in.replace(" ", "").split(",")[1])
        x2 = int(user_in2.replace(" ", "").split(",")[0])
        y2 = int(user_in2.replace(" ", "").split(",")[1])

        if check_answer(
                x1,
                y1,
                x2,
                y2,
                saved_index,
                word_in) and get_curr_time() - time_start < 320:
            points += len(word_in)
            print(good(green("Answer Correct!")))
            headers_as_set.remove(word_in)
        elif check_answer(x1, y1, x2, y2, saved_index, word_in) and not get_curr_time() - time_start < 320:
            points = points
            print(
                info(
                    lightred(
                        "Answer Correct, but time has elapsed so no points have been awarded.")))
        elif not check_answer(x1, y1, x2, y2, saved_index, word_in):
            print(bad(red("Answer incorrect.")))

        print(convert_word_search_to_readable(board))
        print(headers_as_set)


main()
