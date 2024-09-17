from boogle_model import *
from boggle_board_randomizer import *


def fix_line(line):
    """this function gets a line and remove \n from the end"""
    if line[len(line) - 1:] == '\n':
        return line[:len(line) - 1]
    else:
        return line


def boggle_read():
    """read the dict and store it as list"""
    with open('boggle_dict.txt') as words:
        words_ls = []
        for line in words:
            words_ls.append(fix_line(line))
    return words_ls


class BoggleController:
    """This class represent the controller for the Boggle display"""

    def __init__(self):
        """create BoggleController object"""
        self.__boggle_display = BoggleDisplay()
        self.init_game()

    def init_game(self):
        """intialize the game"""
        self.__board = randomize_board()
        self.__boggle_display.set_board(self.__board)
        self.__boggle_display.set_dict(boggle_read())


    def play(self):
        """
        starts the game
        """
        self.__boggle_display.run()




boggle = BoggleController()
boggle.play()
