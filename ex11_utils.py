from typing import List, Tuple, Iterable, Optional, Set

Board = List[List[str]]
Path = List[Tuple[int, int]]


def is_valid_path(board: Board, path: Path, words: Iterable[str]):
    """
    This function takes in a 2D board and a list of tuples representing a path,
    and a collection of legal words, and returns a Boolean indicating whether
    the path is a valid path and forms a valid word on the board.

    A path is considered valid if it is non-empty, starts and ends within the bounds
    of the board, and consists of neighboring positions.

    :param board: 2D list representing the Boggle board
    :param path: list of tuples representing the positions on the board in the order visited
    :param words: collection of legal words
    :return: word if the path is valid and the word exist
    """
    # Check if the path is empty
    if not path:
        return None

    # Check if the starting point is within the bounds of the board
    if path[0][0] < 0 or path[0][0] >= len(board) or path[0][1] < 0 or path[0][1] >= len(board[0]):
        return None
    words_set = set()
    for word in words:
        words_set.add(word)

    # Keep track of the previous position
    prev_y, prev_x = path[0]
    # Create a string to store the word formed by the path
    word = ""
    # checks if the path is longer than max available
    if len(path) > (len(board) * len(board[0])):
        return None
    # dict of booleans to know which values are inside the path already
    path_created = dict()
    # Check each position in the path
    for y, x in path:
        # updates our dict to know in which cell we have been already
        if (y, x) in path_created:
            if path_created[(y, x)]:
                return None
        if (y, x) not in path_created:
            path_created[(y, x)] = True
        # Check if the position is within the bounds of the board
        if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
            return None
        # Check if the position is a neighbor of the previous position
        if abs(x - prev_x) > 1 or abs(y - prev_y) > 1:
            return None
        # Add the letter at the current position to the word
        word += board[y][x]
        # Update the previous position
        prev_y, prev_x = y, x

    # Check if the word is in the collection of legal words
    if word not in words_set:
        return None

    # If all checks passed, the path is valid
    return word


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    this function takes a 2D list representing a board,integer n and collection of words
    the function return all the possible paths on the board of length n that represent a word from
    the collection, if  different paths represent the same word all of them will appear in the list

    :param board: 2D list representing the Boggle board
    :param n: integer represent the length of the path
    :param words: collection of legal words
    :return: list of all legal paths
     """
    words_set = set_from_iterable(words)
    pre_words_set = pre_set_from_iterable(words)
    # initialize an empty list for all the paths
    possible_paths = []
    if not words:
        return possible_paths
    if n == 0:
        return possible_paths
    # initialize a grid of booleans represent the cells to know if we have been in a cell
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            # for each cell we look around for n paths
            find_words(board, n, i, j, "", [], possible_paths, pre_words_set, words_set, visited, 'paths')

    return possible_paths


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
        this function takes a 2D list representing a board,integer n and collection of words
        the function return all the possible paths on the board that represent a word length n from
        the collection, if  different paths represent the same word all of them will appear in the list

        :param board: 2D list representing the Boggle board
        :param n: integer represent the length of the path
        :param words: collection of legal words
        :return: list of all legal paths represent a word length n
         """

    words_set = set_from_iterable(words)
    pre_words_set = pre_set_from_iterable(words)
    # initialize an empty list for all the paths
    possible_paths = []
    # initialize a grid of booleans represent the cells to know if we have been in a cell
    visited = [[False for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            # for each cell we look around for n length words
            find_words(board, n, i, j, "", [], possible_paths, pre_words_set, words_set, visited, 'words')
    return possible_paths


def find_words(board, n, y, x, word, path, possible_paths, pre_words_set, words_set, visited, mode):
    """
      This function takes in a 2D board, an integer n representing the length of the word/path, a starting point
      represented by y and x coordinates, an empty path to create list of tuples representing the current path,
      a list of lists to store all possible paths, a collection of legal words and a 2D list of booleans representing
      the visited cells.The function
      finds all possible paths represent a word length n/path n represent a word.
      It uses backtracking approach to find the paths.

      :param words_set: a set with all the words for fast lookups
      :param board: 2D list representing the Boggle board
      :param n: integer representing the length of the word
      :param y: integer representing the starting y coordinate
      :param x: integer representing the starting x coordinate
      :param word: an empty string to store the word we create
      :param path: empty list the function creates list of tuples representing the current path
      :param possible_paths: empty list of lists to store all possible paths
      :param words_set: collection of legal words
      :param pre_words_set: collection of legal prefix words
      :param visited: 2D list of booleans representing the visited cells
      :param mode: changed according to the calling function
      :return: possible_paths: with all the paths we found
    """

    # takes the board height and width
    board_height = len(board)
    board_width = len(board[0])
    # append curren coordinate to path and appropriate value from the board to the word we create
    path.append((y, x))
    word += board[y][x]
    if not relevant_path(word, pre_words_set):
        return
    # we change the checking for return according to the mode
    # if we created a word length is n we check if the path represent a valid word and add it
    if mode == 'words':
        if n == len(word):
            if word in words_set:
                possible_paths.append(path.copy())
            return
    if mode == 'paths':
        if n == len(path):
            # if the path represent a word on the board we will add it to the possible paths
            if word in words_set:
                possible_paths.append(path.copy())
            return
    # updates the value of the of y,x according to list of directions
    directions = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]
    for dy, dx in directions:
        new_y, new_x = y + dy, x + dx
        if not (new_x < 0 or new_y < 0 or new_y >= board_width or new_x >= board_height or visited[new_y][new_x]):
            # Checks whether we have gone out of the bounds of the board or whether this coordinate already belongs to a
            # valid route
            if len(path) <= n:
                # mark cell and call the function again
                visited[y][x] = True
                find_words(board, n, new_y, new_x, word, path, possible_paths, pre_words_set, words_set, \
                           visited, mode)
                # backtrack case, unmark cell and pop it from the path
                path.pop()
                visited[y][x] = False


def pre_set_from_iterable(words):
    """this function gets an iterable of string and returns the set of all possible initials to the
    words in the iterable"""
    words_set = set()
    for word in words:
        for i in range(1, len(word) + 2):
            words_set.add(word[:i])
    return words_set


def set_from_iterable(words):
    """this function gets an iterable of string and returns the set of all of the
    words in the iterable"""
    words_set = set()
    for word in words:
        words_set.add(word)
    return words_set


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
        This function takes in a 2D board and a collection of legal words,
        and returns the maximum score path of each word exist  on the board.

        :param board: 2D list representing the Boggle board
        :param words: collection of legal words
        :return: a list of the paths,each one is the longest on the board for a specific word
        """
    words_set = set_from_iterable(words)  # initializing a words_set
    pre_word_set = pre_set_from_iterable(words)  # initialize a prefix word set
    # initializing a paths dict
    max_paths = {}
    for word in words_set:
        max_paths[word] = []
    # doing a dfs from every cell to get all needed paths
    for row in range(len(board)):
        for col in range(len(board[0])):
            dfs(row, col, [], board, "", pre_word_set, words_set, max_paths)
    # return the max paths created in the dictionary
    results = []
    for word, path in max_paths.items():
        if path:
            results.append(path)
    return results


def dfs(row, col, path, board, current_word, pre_words_set, words_set, max_paths):
    """this function its like the find words function in terms that is use a dfs algorithm to find
    a paths on the board, for each path created we check if it's valid and represent a word on the board.
     and update the max paths dict so under each word in the dict we have the longets path"""
    current_word += board[row][col]
    path.append((row, col))

    if current_word not in pre_words_set:
        return
    if not check_path_for_m_s(path, board):
        return
    if current_word in words_set:
        if len(path) > len(max_paths[current_word]):
            max_paths[current_word] = path[:]

    for row_offset, col_offset in [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (1, -1), (-1, 1)]:
        new_row = row + row_offset
        new_col = col + col_offset
        if not (new_row < 0 or new_row >= len(board) or new_col < 0 or new_col >= len(board[0])):
            dfs(new_row, new_col, path, board, current_word, pre_words_set, words_set, max_paths)
            path.pop()


def check_path_for_m_s(path, board):
    """checks if the current path created in the dfs function is valid,
    no coordiantes are repeated"""
    prev_y, prev_x = path[0]
    path_created = dict()
    for y, x in path:
        if (y, x) in path_created:
            if path_created[(y, x)]:
                return None
        if (y, x) not in path_created:
            path_created[(y, x)] = True
        # Check if the position is within the bounds of the board
        if x < 0 or x >= len(board[0]) or y < 0 or y >= len(board):
            return None
        # Check if the position is a neighbor of the previous position
        if abs(x - prev_x) > 1 or abs(y - prev_y) > 1:
            return None
        # Add the letter at the current position to the word

        # Update the previous position
        prev_y, prev_x = y, x
    return True


def relevant_path(partial_word, word_set):
    """checks if the current word forming can be a word in the dictionary"""
    if partial_word in word_set:
        return True
    return False
