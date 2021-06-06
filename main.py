import math
import random
import string
import time
from itertools import chain
from art import *
from huepy import *
import numpy

# This creates a dictionary of letters mapped to their corresponding
# number in the alphabet
LETTERS = {
    letter: index for index, letter in enumerate(
        string.ascii_uppercase,
        start=0)}
# This inverts the dictionary of Letters allowing us to search for letters
# by their number
LETTERS2 = {v: k for k, v in LETTERS.items()}
usable_words = []


def parse_words(number: int) -> list:
    """
    This function parses the words in words.txt, and applies some
    filters ensuring that the words that are used are of optimum
    length.

    """
    words = open('words.txt', 'r')
    words = words.read().split('\n')
    for word in words:
        if 1 < len(word) < number - 1:
            usable_words.append(word.upper())

    return usable_words


def create_word_search_board(number: int):
    """
    This function creates a numpy array of zeros, with dimensions of
    number x number, which is set by the user. The array is then
    iterated through, and zeros are replaced with -1's to avoid
    confusion with the alphabet (A) beginning at 0.

    """
    board = numpy.zeros((number, number))

    for i in range(len(board)):
        for x in range(number):
            board[i][x] = -1

    return board


def convert_word_search_to_readable(board) -> str:
    """
    This function takes the board, in any state, and converts the
    values of the elements to their corresponding letter in the
    alphabet using the dictionary LETTERS2 created above.

    :param board: Board is the word search array we are working on
    :return: This function returns a string that contains the
            human-readable word search board
    :rtype: str
    """
    # Creates the top labels and uses unicode underline characters to line the
    # table
    board_string = '\033[4m' + "\t | " + ''.join(["\t" + str(i)
                                                  for i in range(1, len(board) + 1)]) + '\033[0m'
    temp = ""
    z = 0
    for x in board:
        if z != 0:
            board_string += str(z) + '\t | \t' + temp + "\n"
        else:
            board_string = board_string + '\n'
        temp = ""
        z += 1
        for i in x:
            if i != -1:
                temp += LETTERS2[i] + "\t"
            else:
                temp += random.choice(string.ascii_uppercase) + "\t"
    board_string += str(z) + "\t | \t" + temp + "\n"

    return board_string


words_and_positions = []  # List of dictionaries that the answers will be added to


def add_word_vertical(board, number: int):
    """
    This function places words vertically in the word search board. It uses a random
    start point for both the column and the row and tries to fit each word into a random
    spot with each while loop iteration, once a suitable spot is located, it breaks from
    the loop and updates the values of the elements with the letters converted to their
    corresponding numbers in the alphabet. Functionality to allow overlapping of words
    with the same character is in place but is unreliable at best. At the end, the function
    adds the word to a list of dictionaries, that map the words onto their start and end
    coordinates.
    :param board: This is the current word search board we are working on
    :param number: This is the number of columns / rows that the array contains
    :type number: int
    :return: This function returns the numpy array called board that is the
            word search board
    """
    temp_variable = 0
    while temp_variable != 1:
        curr_word = random.choice(usable_words)
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
        elif board[selected_row + i][selected_col - 1] != curr_word[i] and \
                board[selected_row + i][selected_col - 1] != -1:
            return board

    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row + 1,
                                          selected_col, selected_row + len_word, selected_col]
    usable_words.remove(curr_word)
    return board


def add_word_horizontal(board, number: int):
    """
    This function places words horizontally in the word search board. It uses a random
    start point for both the column and the row and tries to fit each word into a random
    spot with each while loop iteration, once a suitable spot is located, it breaks from
    the loop and updates the values of the elements with the letters converted to their
    corresponding numbers in the alphabet. Functionality to allow overlapping of words
    with the same character is in place but is unreliable at best. At the end, the function
    adds the word to a list of dictionaries, that map the words onto their start and end
    coordinates.
    :param board: This is the numpy array that we are currently working on that makes up
                the word search board.
    :param number: This is the number of rows / columns that the user set.
    :return: This function returns the finished numpy array that contains the word search
            board
    """
    curr_word = random.choice(usable_words)
    selected_row = random.randint(1, number)
    selected_col = random.randint(1, number)
    len_word = len(curr_word)
    space_available = number - selected_col
    while space_available <= len_word:
        curr_word = random.choice(usable_words)
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
    usable_words.remove(curr_word)
    return board


def add_word_diagonal_up(board, number: int):
    """
    This function places words diagonally upwards in reverse in the word search board.
    It uses a random start point for both the column and the row and tries to fit each
    word into a random spot with each while loop iteration, once a suitable spot is located,
    it breaks from the loop and updates the values of the elements with the letters converted
    to their corresponding numbers in the alphabet. Functionality to allow overlapping of words
    with the same character is in place but is unreliable at best. This function is especially
    prone to producing unsolvable words and the logic for creating correct answers is also very
    touch and go. I have tried my best to mitigate this, but will hopefully be fixed ASAP.
    At the end, the function adds the word to a list of dictionaries, that map the words onto
    their start and end coordinates.
    :param board: This is the numpy we are currently working on that contains our word search board
    :param number: This is the number of columns / rows that the user has set
    :return: This function returns the updated board with a word added
    """
    curr_word = random.choice(usable_words)
    selected_row = random.randint(len(curr_word), number)
    selected_col = random.randint(len(curr_word), number)
    len_word = len(curr_word)
    space_available = math.floor(
        (selected_col ** 2 + selected_row ** 2) ** (1 / 2))
    while space_available <= len_word and not space_available % len_word:
        curr_word = random.choice(usable_words)
        selected_row = random.randint(len(curr_word), number)
        selected_col = random.randint(len(curr_word), number)
        len_word = len(curr_word)
        space_available = math.floor(
            (selected_col ** 2 + selected_row ** 2) ** (1 / 2))
    if space_available >= len_word:
        for i in range(len_word):
            if board[selected_row - 1 - i][selected_col - 1 - i] == -1:
                board[selected_row - 1 - i][selected_col - 1 -
                                            i] = LETTERS[curr_word[i]]
            elif board[selected_row - 1 - i][selected_col - 1 - i] == curr_word[i]:
                board[selected_row - 1 - i][selected_col - 1 -
                                            i] = LETTERS[curr_word[i]]
            else:
                return board
    else:
        return board
    words_and_positions.append({})
    words_and_positions[-1][curr_word] = [selected_row,
                                          selected_col,
                                          selected_row - 1 - math.ceil(len_word / 2),
                                          selected_col - 1 - math.ceil(len_word / 2)]
    usable_words.remove(curr_word)
    zero_check = words_and_positions[-1][curr_word]
    if 0 in zero_check:
        words_and_positions.pop(-1)
        add_word_diagonal_up(board, number)
    return board


def get_curr_time():
    """
    This function gets the current time when called
    :return: Returns time object
    """
    ret_time = time.time()
    return ret_time


def check_answer(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        ans_index: int,
        word: str) -> bool:
    """
    This function checks the user's supplied coordinates with the information stored in the
    list of dictionaries.
    :param x1: first x coordinate that is given by the user
    :param y1: first y coordinate that is given by the user
    :param x2: second x coordinate that is given by the user
    :param y2: second y coordinate that is given by the user
    :param ans_index: the index of the word and answers in the list of dictionaries
    :param word: the word that is used as the key after we access the index of the
            dictionary in the list of dictionaries
    :return: Returns a boolean True or False value based on if the answer is correct or not
    """
    if x1 == words_and_positions[ans_index][word][0]:
        if y1 == words_and_positions[ans_index][word][1]:
            if x2 == words_and_positions[ans_index][word][2]:
                if y2 == words_and_positions[ans_index][word][3]:
                    return True
    else:
        return False


def check_inputs(inp: str, points: int, time_elapsed: float) -> bool:
    """

    :param inp: This is the inputted info by the user that is parsed for the keywords
    :param points: These are the number of points the user has accumulated up until this
                point
    :param time_elapsed: This is the amount of time that has elapsed since the start of the
                word search game.
    :return: Returns true if none of the keywords are found.
    """
    if "FINISH" in inp:
        print("You have scored a total of " +
              str(points) +
              " points over the course of " +
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
              " points over the course of " +
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
              " points over the course of " +
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
    """
    This is the main function that contains all the of nested functions necessary for the
    word search to function. A random number between 6 and 8 is chosen, and then a for loop
    is used to choose between horizontal, vertical, or diagonal between 6 and 8 times. A while
    loop is then created after the user is displayed the list of words and the word search board.
    The timer begins, and the while loop continuously repeats until there are no words left or an
    exit keyword has been entered.

    """
    print(bold(red(text2art("Word   Search   Game"))))
    points = 0
    number = int(
        input(
            bold(
                cyan(
                    "Please input the number of columns you want (i.e. size of the grid) \t"))))
    parse_words(number)
    board = create_word_search_board(number)
    for i in range(random.randint(6, 8)):
        temp = random.randint(0, 2)
        if temp == 0:
            add_word_vertical(board, number)
        if temp == 1:
            add_word_diagonal_up(board, number)
        if temp == 2:
            add_word_horizontal(board, number)

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
    print(str(headers_as_set).strip("{}'\',\"").replace("'", ""))
    time_start = get_curr_time()
    ongoing = 1
    while ongoing == 1:
        word_in = input(bold(cyan("Input the word \t"))).upper()
        if check_inputs(
                word_in,
                points,
                get_curr_time() -
                time_start) and isinstance(
                word_in,
                type("hello")):
            pass
        user_in = input(bold(cyan(
            "Input the starting x and y coordinates of the word, separated by a comma (i.e. x1, y1) \t")))
        if check_inputs(
            user_in,
            points,
            get_curr_time() -
            time_start) and int(
            user_in.replace(
                " ",
                "").split(",")[0]) <= number and int(
                user_in.replace(
                    " ",
                    "").split(",")[1]) <= number:
            pass
        user_in2 = input(bold(cyan(
            "Input the ending x and y coordinates of the word, separated by a comma (i.e. x2, y2) \t")))
        if check_inputs(
            user_in2,
            points,
            get_curr_time() -
            time_start) and int(
            user_in.replace(
                " ",
                "").split(",")[0]) <= number and int(
                user_in.replace(
                    " ",
                    "").split(",")[1]) <= number:
            pass

        saved_index = -1

        for i in range(len(words_and_positions)):
            try:
                temp = words_and_positions[i][word_in]
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
        print(str(headers_as_set).strip("{}'\',\"").replace("'", ""))
        if len(set(headers_as_set)) == 0:
            check_inputs("FINISHED", points, get_curr_time() - time_start)
            ongoing = 0


main()
