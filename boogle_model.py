from tkinter import *
from tkinter.font import Font
import boggle_board_randomizer as bg


from ex11_utils import is_valid_path
from pygame import mixer



class BoggleDisplay:
    """This class represent the model display to a boggle game"""

    """constants section"""

    TITLE = 'Omer and Orly boggle game'  # main root title
    PAD = 5
    # dict of colors
    COLORS = {'TOP_BAR_COLOR': "#8B8B83", 'CLOCK_COLOR': '#4D4D4D', 'MAIN_ROOT_COLOR': '#1F1F1F',
              'BUTTON_FG': '#7A7A7A',
              'BUTTON_BG': 'black'
              }
    # dict of sizes
    FONT = {'small': 12, 'big': 16, 'medium': 14, 'enormous': 30}
    # dict of texts
    TEXT = \
        {
            'CHECK': 'Check', 'START_TEXT': 'Welcome the the boggle game, \n please press start to reveal the board',
            'END_TITLE': "let's see how you did: "
        }
    # the game time
    GAME_TIME = 180

    def __int__(self):
        """call two methods that initialize the game"""
        self.__init_display()  # initialize the game display
        self.__init_vars()  # initialize the game vars

    def __init_vars(self):
        """ initialize the game vars"""
        self.__words_found = []  # a list of word the user has found
        self.__key_pressed = []  # the key the user pressed
        self.__cur_word = ''  # the current word the user creating
        self.__player_score = 0  # sets player score
        self.clock_running = False  # indicator tell if the clock runs
        self.game_started = False  # indicator tell if the game runs
        self.path = []  # list hold the current path
        self.restart = False
        self.finish= False

    def __init_display(self):
        """intialize the game display"""
        self.__root = Tk()  # The base screen
        # Gets the user's screen size so the game screen size will be
        # relative
        self.screen_width = self.__root.winfo_screenwidth() // 2
        self.screen_height = self.__root.winfo_screenheight() // 2
        self.__root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.__root.config(bg=self.COLORS['MAIN_ROOT_COLOR'])

        self.__root.resizable(False, False)
        self.set_title()  # set the title of the screen

        self.upper_frame()  # sets the upper frame

        self.middle_frame()  # sets the middle frame

        self.side_frame()  # sets the side frame

    """setters methods"""

    def set_dict(self, dict):
        """initialize the game dict to check the words"""
        self.dict = dict

    def set_board(self, board):
        """sets the board game"""
        self.__board = board

    def set_title(self):
        """sets the main window title"""
        self.__root.title(self.TITLE)

    def board_size(self):
        """return the size of the board, both sides are in the same length"""
        return len(self.__board)

    """upper frame methods"""

    def upper_frame(self):
        """creates the upper frame and its widget with other methods"""

        self.top = Frame(self.__root, bg=self.COLORS['TOP_BAR_COLOR'])  # create the frame it's style
        self.top.place(rely=0, relwidth=1, height=self.screen_height * 0.15)  # places the frame
        self.start_button()  # Creates the Start\Check button
        self.forming_word()  # Creates the forming word box
        self.clock()  # Creates the clock

    def start_button(self):
        """creates a start button the changes to check button after the game starts """
        start_font = Font(
            family='Times',
            size=20,
            weight='bold',
            slant='roman',
            underline=1,
            overstrike=0
        )
        self.start_check_button = Button(self.top,
                                         text='Start', font=start_font, command=self.start)  # create the start button

        self.start_check_button.pack(padx=5, side=LEFT)  # packing the button



    def start(self):
        """this function activate after the user press the start button.
        the start button will change to check button and the board will reveal"""

        self.game_started = True  # change the game started indicator to true
        #plays the start sound
        mixer.init()
        sound = mixer.Sound(r"EA_Sports.wav")
        sound.play()
        # initialize the screen after the uset hit start buttons
        self.start_check_button.config(text='Check',command=self.check)
        self.__root.after(4000, self.display_board)
        self.__root.after(100, self.initial_label.config(text='Lets go!'))
        self.__root.after(4000, self.welcome_window_frame.destroy)
        self.__root.after(4000, self.run_clock, self.GAME_TIME)

    def check(self):
        """this function when the user press the check button in order to check the word he formed"""
        # this if checks if the path the user created is valid with the is valid path function from ex 11 utils
        # also we check that the word don't appears already in the

        if is_valid_path(self.__board, self.path, self.dict) and self.__cur_word not in self.__words_found:
            self.__words_found.append(self.__cur_word)  # add the word to the founded words
            self.update_score(len(self.__cur_word) ** 2)  # update the uset score
            self.__cur_word = ''  # reset the current word
            self.update_founds()  # update the found words on the screen
            self.update_formed()  # delete the word that has been checked from the screen

        self.path = []  # reset the path
        self.__cur_word = ''  # reset the current word
        self.update_formed()  # delete the word that has been checked from the screen
        self.reset_state()  # reset the state of the buttons

    def forming_word(self):
        """display the forming word"""
        # setting the formed word title font and the word formed font itself
        formed_title_font = Font(
            family='Times',
            size=13,
            weight='bold',
            slant='roman',
            underline=1,
            overstrike=0
        )
        forming_font = Font(
            family='Times',
            size=13,
            weight='bold',
            slant='roman',
            underline=0,
            overstrike=0
        )
        # Creates the forming word container box
        self.forming_word_container = Frame(self.top, bg=self.COLORS['TOP_BAR_COLOR'])
        self.forming_word_container.pack(side=LEFT, padx=self.PAD)
        # Creates the forming word static title
        self.forming_word_title = Label(self.forming_word_container,
                                        text=f'Forming Word:',
                                        font=formed_title_font,
                                        bg=self.COLORS['TOP_BAR_COLOR'])
        self.forming_word_title.pack(side=LEFT, padx=self.PAD)
        # Creates the forming word dynamic label
        self.forming_word = Label(self.forming_word_container,
                                  text=f'{self.__cur_word}',
                                  font=forming_font,
                                  bg=self.COLORS['TOP_BAR_COLOR'])
        self.forming_word.pack(side=LEFT, padx=self.PAD)

    def clock(self):
        """this method creates the clock widget in the upper frame"""
        # sets the clock font
        clock_font = Font(
            family='Times',
            size=15,
            weight='normal',
            slant='italic',
            underline=0,
            overstrike=0
        )
        # calculate the minutes and seconds
        minutes, second = self.GAME_TIME // 60, self.GAME_TIME % 60
        # creating the clock label
        self.clock_label = Label(self.top, text=f'Time remains {minutes}:{second:0>2}', font=clock_font,
                                 bg=self.COLORS['CLOCK_COLOR'], height=2)

        self.clock_label.pack(side=RIGHT, padx=10, pady=0, )

    def run_clock(self, time):
        """this method make the clock runs"""
        # changes the start button to cehck button

        # set the clock font
        clock_font = Font(
            family='Times',
            size=15,
            weight='normal',
            slant='italic',
            underline=0,
            overstrike=0
        )
        # if the clock is not running we will update it
        if not self.clock_running:
            self.clock_running = True
        # calculate the minutes and seconds
        minutes, second = time // 60, time % 60
        now = f'Time remains: {minutes:0>1}:{second:0>2}'
        # update the clock label
        self.clock_label.config(text=now, font=clock_font)
        # if time is over set the clock running method to false and call to the another round method
        if time == 0:
            self.clock_running = False
            self.another_round()
        # update the time and the root
        else:
            time -= 1
            self.__root.after(1000, self.run_clock, time)

    """middle frame methods"""

    def middle_frame(self):
        """creates the game middle frame contains the board"""
        # initialize the middle frame
        self.middle = Frame(self.__root, bg=self.COLORS['TOP_BAR_COLOR'])
        self.middle.place(relx=0.4, rely=0.7, relwidth=0.7, relheight=1, anchor='center')
        # display the board if the game started(if is inside the method)
        self.display_board()
        # display a welcome window to the user before the game strats
        self.welcome_window()

    def display_board(self):
        """this method sets the board"""
        # cheks if game started to set the board
        if self.game_started == True:
            self.board_frame = Frame(self.middle, bg='black')  # creating a frame to the board inside the middle frame
            self.board_frame.pack(pady=40)
            self.buttons = {}  # dictionary that will hold the buttons
            # irritating over the board size and add the buttons
            for i in range(self.board_size()):
                for j in range(self.board_size()):
                    # adding the button to a dictionary which each key is the location of the button
                    self.buttons[(i, j)] = (
                        Button(self.board_frame,
                               text=str(self.__board[i][j]),
                               command=lambda i=i, j=j, x=self.__board[i][j]: self.update_word(x, i, j),
                               font=self.FONT['big'],
                               width=12,
                               height=4,
                               fg=self.COLORS['BUTTON_FG'],
                               bg=self.COLORS['BUTTON_BG']))

                    # places each button in a grid
                    self.buttons[(i, j)].grid(row=i, column=j,
                                              padx=self.PAD, pady=self.PAD)

    def update_word(self, x, i, j):
        """get from every button the string it represents and the location to update the forming word and
        the state of the board"""
        self.path.append((i, j))  # adding the current loction to the path
        self.__cur_word += x  # adding the current string to the current word
        self.update_formed()  # update the shows of the current word
        self.disable((i, j))  # update the path on the board game and disable and activate buttons

    def in_trail(self, button):
        """checks if a buttons is in the curren path"""
        if button in self.path:
            return True
        return False

    def check_neighbors(self, x, y, prev_x, prev_y):
        """checks if two buttons are neighbors"""
        # if the distance in one of the axis is more than one return false
        if abs(x - prev_x) > 1 or abs(y - prev_y) > 1:
            return False
        return True

    def last_clicked(self):
        """return the last clicked button"""
        return self.path[-1]

    def disable(self, loc):
        """disable buttons that are not neighbors of the current cell and also highlights tha path"""
        # checks all our button from the dictionary
        for button in self.buttons:
            # if the button is last one clicked disable it and paint it bg to black
            if button == self.last_clicked():
                self.buttons[button].config(bg='black', disabledforeground='red', state=DISABLED)
            # if it neighbors of the current button and in trail we will make the bg white and fg red
            elif self.check_neighbors(button[1], button[0], loc[1], loc[0]) and self.in_trail(button):
                self.buttons[button].config(state=DISABLED, bg='black', fg='red')
            # if it just neighbors of the current button and in trail we will make the bg white
            elif self.check_neighbors(button[1], button[0], loc[1], loc[0]):
                self.buttons[button].config(state=NORMAL, bg='white')
            # if it just in trail we will make it disable and turn fg to red
            elif self.in_trail(button):
                self.buttons[button].config(state=DISABLED, bg='black', disabledforeground='red')
            # if none of the above,we just disable it
            else:
                self.buttons[button].config(state=DISABLED, bg='black')

    def reset_state(self):
        """reset the state of the buttons and configuration after path is finished"""
        if self.clock_running:
            for button in self.buttons:
                self.buttons[button].config(state=NORMAL, fg=self.COLORS['BUTTON_FG'],
                                            bg=self.COLORS['BUTTON_BG'], disabledforeground='white')

    def update_formed(self):
        """update the forming word label"""
        self.forming_word.config(text=self.__cur_word)

    def welcome_window(self):
        """creates a welcome window with title """
        # sets the welcome font
        welcome_font = Font(
            family='Times',
            size=15,
            weight='bold',
            slant='roman',
            underline=1,
            overstrike=0
        )
        # creates the welcome frame inside the muddle frame
        self.welcome_window_frame = Frame(self.middle, bg=self.COLORS['TOP_BAR_COLOR'])
        self.welcome_window_frame.place(rely=0.3, relx=0, relheight=1,
                                        relwidth=1)
        # sets the initial lable
        self.initial_label = Label(self.welcome_window_frame,
                                   bg=self.COLORS['TOP_BAR_COLOR'],
                                   text=self.TEXT['START_TEXT'],
                                   font=welcome_font,
                                   wraplength=self.screen_width // 2,
                                   padx=3, pady=3)
        self.initial_label.pack()

    """side frame methods"""

    def side_frame(self):
        """sets the side frame the holds the score and the list of found words"""
        self.side = Frame(self.__root, bg=self.COLORS['TOP_BAR_COLOR'])
        self.side.place(relx=1, rely=0.7, relwidth=0.2, relheight=1, anchor='e')
        self.player_hub()

    def player_hub(self):
        """creating the side frame where we will show the player score,and the list of found words"""
        self.player_hub_con = Frame(self.side, bg='gray')
        self.player_hub_con.place(relx=0,
                                  relheight=1,
                                  relwidth=1.0)

        self.score()  # sets the score section

        self.found_words()  # sets the found word section

    def score(self):
        """set the score section"""
        score_font = Font(
            family='Adobe Garamond Pro',
            size=13,
            weight='bold',
            slant='roman',
            underline=1,
            overstrike=0
        )
        # creating a score frame
        self.score_frame = Frame(self.player_hub_con)
        # creating the score label
        self.score_label = Label(self.player_hub_con, text=f'Score: {self.__player_score}', font=score_font,
                                 bg=self.COLORS['TOP_BAR_COLOR'])
        self.score_label.pack(side=TOP, padx=self.PAD)

    def update_score(self, new_score):
        """updates the player score"""
        # update the player score variable
        self.__player_score += new_score
        # update the score label on the screen
        self.score_label.config(text=f'Score: {self.__player_score}')

    def found_words(self):
        """show the list of found words"""
        # set the font of the fonded words
        founded_font = Font(
            family='Adobe Garamond Pro',
            size=15,
            weight='bold',
            slant='roman',
            underline=0,
            overstrike=0
        )
        # creates the found words frame
        self.found_words_frame = Frame(self.player_hub_con)
        self.found_words_frame.pack(side='top')
        # set a listbox to the founded word
        self.found_words_listbox = Listbox(self.found_words_frame, bg=self.COLORS['TOP_BAR_COLOR'], font=founded_font
                                           )
        self.found_words_listbox.pack()

    def reset_founds(self):
        """reset the found words listbox on the screen"""
        self.found_words_listbox.delete(0, END)

    def update_founds(self):
        """updates the found listbox on the screen"""
        self.found_words_listbox.insert(END, self.__words_found[-1])

    def another_round(self):
        """reset the screen and asks the user if he wants to play another round"""
        end_title = Font(
            family='Times',
            size=26,
            weight='bold',
            slant='italic',
            underline=0,
            overstrike=0
        )
        # sets end round font
        end_font = Font(
            family='Adobe Garamond Pro',
            size=16,
            weight='bold',
            slant='roman',
            underline=0,
            overstrike=0
        )
        # delete the last word was formed
        self.__cur_word = ''
        self.update_formed()
        # creating end frame inside the middle frame
        self.end_frame = Frame(self.middle, bg=self.COLORS['TOP_BAR_COLOR'])
        self.end_frame.pack()
        # disable the start button
        self.start_check_button.config(state=DISABLED)
        # unpack the board
        self.board_frame.pack_forget()
        # creats an end title
        self.end_title = Label(self.end_frame,
                               text=self.TEXT["END_TITLE"],
                               bg=self.COLORS['TOP_BAR_COLOR'],
                               font=end_title)
        self.end_title.pack(side=TOP, pady=10)
        # cheks the player score and display it with appropiate message
        if self.__player_score > 40:
            self.end_score = Label(self.end_frame,
                                   text=f'you found {len(self.__words_found)} words and scored {self.__player_score} '
                                        f'points, well done!',
                                   bg=self.COLORS['TOP_BAR_COLOR'],
                                   font=end_font, pady=4)
        else:
            self.end_score = Label(self.end_frame,
                                   text=f'you found {len(self.__words_found)} words and scored {self.__player_score} '
                                        f'points\n,good luck next time!',
                                   bg=self.COLORS['TOP_BAR_COLOR'],
                                   font=end_font, pady=4)
        self.end_score.pack(anchor='center')
        # creates an exit button
        self.exitbtn = Button(self.middle,
                              text='Exit',
                              command= self.quit, font=end_font, bg=self.COLORS['BUTTON_BG'],
                              fg=self.COLORS['BUTTON_FG'])
        self.exitbtn.place(relx=0.38, rely=0.3)
        # creates a retry button
        self.retrybtn = Button(self.middle,
                               text='Retry',
                               command=self.retry, font=end_font, bg=self.COLORS['BUTTON_BG'],
                               fg=self.COLORS['BUTTON_FG'])
        self.retrybtn.place(relx=0.5, rely=0.3)



    def destroy_end_screen(self):
        """destroy the end screen if the user wants another round"""
        self.end_frame.destroy()
        self.exitbtn.destroy()
        self.retrybtn.destroy()

    def retry(self):
        """reset the screen if the player wants to play another round"""

        self.destroy_end_screen()  # destroy the end screen
        self.__init_vars()  # init the vars
        self.start_check_button.config(text='Start', command=self.start,
                                       state=NORMAL)  # config the check button to start button again
        self.set_board(bg.randomize_board())
        self.welcome_window()
        self.update_score(self.__player_score)  # update score on the screen
        self.update_formed()  # reset the formed word on the screen
        self.reset_founds()  # reset the found words on the screen
        minutes, second = self.GAME_TIME // 60, self.GAME_TIME % 60
        self.clock_label.config(text=f'Time remains {minutes}:{second:0>2}')



    def quit(self):
        """end the game and show goodbye title"""
        self.end_title.config(text='See you next time!')
        self.end_score.destroy()
        self.__root.after(2000, self.__root.destroy)

    def run(self):
        """this function runs the model"""
        self.__init_vars()
        self.__init_display()
        self.__root.mainloop()
    def get_root(self):
        return self.__root
    def start_root(self):
        self.__root.mainloop()



