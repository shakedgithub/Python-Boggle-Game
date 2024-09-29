# -------------- I M P O R T S ----------------#
# our files:
from boggle_board_randomizer import *
from boggle import BoggleController

# python modules:
import tkinter as tk
from tkinter import messagebox
import copy


# -------------- G U I  C L A S S ----------------#
class BoggleGUI:
    """
    The BoggleGUI class is a Tkinter GUI class for the Boggle Game.


    The class includes the following API methods:


    1. __init__: Initializes the BoggleGUI class, creates the main window and
    all necessary frames, buttons and labels.
    2. set_controller: Sets the controller of the game
    3. game_over: Ends the game, displays the user's final score and asks if
     s/he wants to play again.
    4. get_board: Returns the current boggle board.
    5. submit_on_click: This method is called when the user clicks the submit
    button. It returns a deep copy of list contains all the buttons on board
    that the user clicked on and resets that list.
    6. update_words_found: Updates the words found by user with the given word.
    7. update_score_label: Updates the score label with the given score.
    8. run: Runs the main loop of the GUI, displaying the window to the user.


   """

    def __init__(self) -> None:
        """
        This function initializes the Boggle GUI, creating the main window and
        all necessary frames, buttons and widgets for the game.
        It also assigns a random board and sets the controller to None.
        It also uploads the cover image, creates the Start button and defines
        empty objects for storing the path of clicked word and the timer.
        """

        # Step 1: Create main window and initialize object
        root = tk.Tk()
        root.geometry("650x620")
        root.title("Boggle Game")
        root.resizable(False, False)
        root.config(bg="gray99")

        self._main_window = root
        self._board = randomize_board()
        self._controller = None

        # Step 2: upload open cover image using helper
        self.__add_pic("cover.PNG")

        # Step 3: Create frames for object on main_window
        # 1) board frame
        self._board_frame = tk.Frame(self._main_window)
        self._board_frame.pack(expand=True)

        # 2) score frame
        self._score_frame = tk.Frame(self._main_window)
        self._score_frame.pack(expand=True)

        # 3) start frame
        self._start_button_frame = tk.Frame(self._main_window)
        self._start_button_frame.pack()
        self._start_button_frame.place(x=170, y=510)

        # 4) submit, delete and quit buttons frames
        self._submit_button_frame = tk.Frame(self._main_window)
        self._submit_button_frame.pack()
        self._submit_button_frame.place(x=20, y=570)

        self._delete_button_frame = tk.Frame(self._main_window)
        self._delete_button_frame.pack()
        self._delete_button_frame.place(x=280, y=570)

        self._quit_button_frame = tk.Frame(self._main_window)
        self._quit_button_frame.pack()
        self._quit_button_frame.place(x=540, y=570)

        # 5) time label frame
        self._time_frame = tk.Frame(self._main_window)
        self._time_frame.pack()

        # 6) temp word frame
        self._temp_word_frame = tk.Frame(self._main_window)
        self._temp_word_frame.pack()

        # Step 4: Create start game button
        self._start_button = tk.Button(self._start_button_frame,
                                       text=" * S t a r t  *  G a m e * ",
                                       font=("Berlin Sans FB Demi Bold", 20),
                                       bg="DodgerBlue2", fg="gray99",
                                       command=self.__start_game)
        self._start_button.pack(side=tk.TOP)

        # Step 5: define empty objects for path and timer
        self._coor_clicked = []
        self._clock = 180

    # ------- class encapsulated helpers ------- #

    # buttons
    def __special_buttons(self):
        """
        This function creates 3 buttons, a submit button, restart button, and delete button,
        each with specific text, font, background color, and foreground color.
        Each button also has a command function that is called when the button is clicked.
        The buttons are then packed into their respective frames.
        """
        # 1) submit button
        self._submit_button = tk.Button(self._submit_button_frame,
                                        text="* Submit *",
                                        font=("Berlin Sans FB Demi Bold", 13),
                                        bg="white",
                                        fg="DodgerBlue2",
                                        command=self._controller.user_submission)
        self._submit_button.pack()

        # 2) quit button
        self._quit_button = tk.Button(self._quit_button_frame,
                                      text="* Restart *",
                                      font=("Berlin Sans FB Demi Bold", 13),
                                      bg="white",
                                      fg="DodgerBlue2",
                                      command=self._controller.game_is_over)
        self._quit_button.pack()

        # 3) delete button
        self._delete_button = tk.Button(self._delete_button_frame,
                                        text="* Delete *",
                                        font=("Berlin Sans FB Demi Bold", 13),
                                        bg="white",
                                        fg="DodgerBlue2",
                                        command=self.__delete_on_click)
        self._delete_button.pack()

    # labels
    def __create_time_label(self):
        """
        Creating time label.
        """
        # create time label:
        self._time_label = tk.Label(self._time_frame, text="",
                                    font=("Berlin Sans FB Demi", 20),
                                    fg="goldenrod1",
                                    bg="gray99", relief="flat")

        self._time_label.pack()

        # configure frame
        self._time_frame.config(height=20, width=100)
        self._time_frame.place(x=380, y=505)

    def __create_score_label(self):
        """
        Creating score label.
        """
        # create score label:
        self._score_label = tk.Label(self._score_frame, text="Score : ",
                                     font=("Berlin Sans FB Demi", 17),
                                     fg="red",
                                     bg="gray99", relief="flat")
        self._score_label.pack()

        # configure frame
        self._score_frame.config(height=20, width=100)
        self._score_frame.place(x=20, y=450)

    def __create_temp_word_label(self):
        """
        Creating temporal word label when user clicks letters on board.
        """

        self._temp_word_label = tk.Label(self._temp_word_frame, text="",
                                         font=("Berlin Sans FB Demi", 20),
                                         fg="goldenrod1",
                                         bg="gray99", relief="flat")
        self._temp_word_label.pack()

        # configure frame
        self._temp_word_frame.config(height=20, width=100)
        self._temp_word_frame.place(x=430, y=90)

    # board
    def __create_board(self):
        """
        Creating clickable board.
        """

        # defining board values variables
        board_row = len(self._board)
        board_col = len(self._board[0])

        # create clickable board with its letters
        self._buttons = []

        for i in range(board_row):
            single_button = []
            for j in range(board_col):
                # create button and add it to list of buttons
                button = tk.Button(self._board_frame, text=self._board[i][j],
                                   width=6, height=3, bg="DodgerBlue2",
                                   fg="gray99",
                                   font="Ariel",
                                   command=lambda x=i, y=j:
                                   self.__button_clicked(x, y))
                button.grid(row=i, column=j)

                # add button to list of buttons
                single_button.append(button)

            self._buttons.append(single_button)

        # configure frame
        self._board_frame.config(height=450, width=450)
        self._board_frame.place(x=325, y=140)

    def __button_clicked(self, x, y):
        """
        Checks if letter clicked at coordinate (x,y) is next to previous
        letter clicked and update the path list.
        """
        if self._coor_clicked == []:
            # add to coor list
            self._coor_clicked.append((x, y))
            # change temp letter label text
            cube_cont = self._board[x][y]
            self._temp_word_label["text"] += cube_cont


        elif self.__check_flow(x, y):
            # add to coor list
            self._coor_clicked.append((x, y))
            # change temp letter label text
            cube_cont = self._board[x][y]
            self._temp_word_label["text"] += cube_cont

    def __check_flow(self, x, y) -> bool:
        """
        Checks if user clicked on the next cube, it returns a boolean depending
        on whether the provided x,y coordinates have been clicked before or not.
        """
        # user cant choose same cube
        if (x, y) in self._coor_clicked:
            return False

        # take last coor
        last_coor = self._coor_clicked[-1]

        # check if coor is valid
        diff = [-1, 0, 1]
        if ((last_coor[0] - x) in diff) and ((last_coor[1] - y) in diff):
            return True

        return False

    # other functions
    def __add_pic(self, pic_name: str):
        """
        This function is a helper for every time we
        want to add a picture.
        """

        # img = Image.open(pic_name)
        # cover_image = ImageTk.PhotoImage(img)
        # self._img_label = tk.Label(image=cover_image)
        # self._img_label.image = cover_image
        # self._img_label.pack(expand=True)
        # Open an image file
        img = tk.PhotoImage(file=pic_name)

        # Create a label to display the image
        self._img_label = tk.Label(image=img)
        self._img_label.image = img
        self._img_label.pack()

    def __set_time(self):
        """
        Set timer for game
        """
        # Count Down
        if self._clock >= 1:
            min, sec = divmod(self._clock, 60)
            self._time_label.config(
                text="Time left: " + "{:02d}:{:02d}".format(min, sec))
            self._clock -= 1
            # set time will be called again in 1 second
            self._time_label.after(1000, self.__set_time)
        else:
            self._controller.game_is_over()

    def __delete_on_click(self) -> None:
        """
        Reset the temp word label and the coor clicked list - when user
        click on delete button
        """
        # reset the temp word label
        self._temp_word_label["text"] = ""

        # reset the coor clicked list:
        self._coor_clicked = []

    # ------- class main function using helpers ------- #

    def __start_game(self):

        """
        Responsible for start game UI
        """

        # Step 1: delete start button
        self._start_button.destroy()
        self._start_button_frame.destroy()

        # Step 2: delete cover image label
        self._img_label.destroy()

        # Step 3: add title picture
        self.__add_pic("boggle_title.PNG")
        self._img_label.place(x=23, y=0)

        # Step 4: create board
        self.__create_board()

        # Step 5: create special buttons
        self.__special_buttons()

        # Step 6: create timer
        self.__create_time_label()
        self.__set_time()

        # Step 7: create score
        self.__create_score_label()

        # Step 8: create temp letter label
        self.__create_temp_word_label()

        # Step 9: create words found canvas
        self._words_found_canvas = tk.Canvas(self._main_window, width=250,
                                             height=290,
                                             bg='forest green')
        self._words_found_canvas.place(x=20, y=140)
        self._words_found_canvas.create_text(125, 15, text="WORDS FOUND:",
                                             fill="#F9F5EB", font=(
                "Berlin Sans FB Demi Bold", 15), )

        # Step 10: create scrollbar next to words found canvas
        self._scrollbar = tk.Scrollbar(self._main_window, orient="vertical")
        self._scrollbar.place(x=270, y=142, height=291)

        # Set the yscrollcommand of the canvas to the set method of the scrollbar
        self._words_found_canvas.config(yscrollcommand=self._scrollbar.set)

        # Set the command attribute of the scrollbar to be yview
        self._scrollbar.config(command=self._words_found_canvas.yview)

    # ------------ class API ------------ #
    def try_again(self):
        """
        When user choose not valid word, a label written "Try again" appears and
        disappears after 1 second
        """

        # create try again label
        self._try_again_label = tk.Label(self._main_window, text="Try again",
                                         font=("Berlin Sans FB Demi bold", 18),
                                         fg="red",
                                         bg="black", relief="flat")

        # activate Try again label
        self._try_again_label.place(x=420, y=90)
        self._main_window.after(1000, self._try_again_label.place_forget)

    def long_word_label(self):
        """
        When user found a long word on board - appears "YOU ROCK" label
        that disappears in 1 second.
        """
        # create long word label
        self._long_word_label = tk.Label(self._main_window, text="YOU ROCK!!!",
                                         font=("Berlin Sans FB Demi bold", 50),
                                         fg="red",
                                         bg="black", relief="flat")

        # activate long word label
        self._long_word_label.place(x=140, y=270)
        self._main_window.after(1000, self._long_word_label.place_forget)

    def set_controller(self, controller: BoggleController):
        """
        Define a controller object to connect the controller
        class with gui class.
        """
        self._controller = controller

    def get_board(self):
        return self._board

    def get_main_window(self):
        return self._main_window

    def submit_on_click(self) -> list[tuple]:
        """
        This function creates a deep copy of the _coor_clicked list,
        resets _coor_clicked list and _temp_word_label and returns the deep
        copy of the _coor_clicked list.
        """

        if self._coor_clicked != []:
            # Step 1: create deep copy of coor_clicked
            coor_clicked_copy = copy.deepcopy(self._coor_clicked)

            # Step 2: resets coor_clicked
            self._coor_clicked = []

            # step 3: resets temp_word
            self._temp_word_label["text"] = ""

            return coor_clicked_copy

    def update_words_found(self, word):
        """
        Updating the words found canvas
        """
        # get list of all words using controller API func
        all_words = self._controller.get_all_words_found()

        # add word to words_found canvas
        self._words_found_canvas.create_text(40, 17 * (len(all_words) + 2),
                                             text="* " + word, fill="gray99",
                                             font=('Berlin Sans FB Demi', 13))

        # adapt scrollbar to canvas
        self._words_found_canvas.config(
            scrollregion=self._words_found_canvas.bbox("all"))

    def update_score_label(self, score: str):
        """
        Updating the score label
        """
        self._score_label.config(text="Score : " + score)

    def game_over(self, score: str):

        """
        When time is up:
        1. destroy all unnecessary buttons
        2. upload 'game_over' img
        3. your score was label
        4. add a ques for user if he wants to play another game
        """
        # Step 1: destroy unnecessary buttons, frames and labels
        # destroy buttons and labels
        self._time_label.destroy()
        self._temp_word_label.destroy()
        self._quit_button.destroy()
        self._delete_button.destroy()
        self._submit_button.destroy()
        self._scrollbar.destroy()
        self._img_label.destroy()

        # destroy frames and canvases
        self._time_frame.destroy()
        self._board_frame.destroy()
        self._score_frame.destroy()
        self._temp_word_frame.destroy()
        self._words_found_canvas.destroy()
        self._submit_button_frame.destroy()
        self._quit_button_frame.destroy()
        self._delete_button_frame.destroy()

        # Step 2: create label that shows user's score from prev game
        self._prev_score_frame = tk.Frame(self._main_window)
        self._prev_score_frame.pack(side=tk.TOP)
        self._prev_score = tk.Label(self._prev_score_frame, fg="red",
                                    bg="black",
                                    font=("Berlin Sans FB Demi", 30),
                                    text=f"Your final score:\n {score}")
        self._prev_score.pack()
        self._prev_score_frame.place(x=150, y=10)

        # Step 3: upload game_over img
        self.__add_pic("game_over.PNG")
        self._main_window.config(bg="black")
        self._img_label.pack(expand=True)

        # Step 4: ask the user if he wants another game
        ques = messagebox.askyesno("GAME IS OVER",
                                   "Do you want to play another game?")
        if ques:
            # START THE GAME AGAIN FROM THE CONTROLLER
            self._controller.new_game()


        else:
            self._main_window.destroy()

    def run(self) -> None:
        self._main_window.mainloop()



