# -------------- I M P O R T S ----------------#
# from ex11_utils import *
from boggle_gui import *
from boggle_logic import *


# -------------- GAME RUNNER ----------------#


class BoggleController:
    """
    The BoggleController class is a class that uses the BoggleGUI and
    BoggleLogic classes to control the flow of the game, by handling user
    input and updating the GUI and game logic accordingly.
    When the game is over, it allows the user to start a new game.


    Attributes:
    1. words: a set of words that are used for the game
    2. gui: an object of the BoggleGUI class that represents the GUI of the game
    3. logic: an object of the BoggleLogic class that represents the logic of the game


    Methods:
    1. __init__: Initializes the class by setting the words, GUI object, and logic object.
    2. user_submission: Handles the user's submission when s/he submits a word.
    3. game_is_over: Ends the game by calling the game_over method of the gui
    object and passing the score.
    4. new_game: Creates new game objects and starts a new game.
    5. run: Runs the main loop of the game.
    """

    def __init__(self, gui_obj, board):

        """
        This function initializes the Boggle controller, it takes two arguments, a gui_obj and board.
        It first retrieves a set of all possible words from a dictionary file,
        then it creates the gui and logic objects, passing the board and words set to the logic object.
        """

        # Step 1: get all possible words
        self._words = get_words_set("boggle_dict.txt")

        # Step 2: create gui and logic objects
        self._gui = gui_obj
        self._logic = BoggleLogic(board, self._words)

    # ------------ class API ------------ #
    def user_submission(self):
        """
        This function handles the user's submission of a word after clicking
        the submission button in the GUI.
        It retrieves the path of the clicked word, checks if it is a valid word
        on the board, and updates the GUI accordingly.
        If the submitted word is valid, the function updates the found words
        canvas, score label, and possibly the long word label.
        If the submitted word is invalid, the function prompts the user to try again.
        """
        # get the path of clicked word
        path = self._gui.submit_on_click()

        # check if it is a word on board
        is_a_word = self._logic.after_submit(path)

        if is_a_word:

            # get the last word (in get_words_found list)
            word = self._logic.get_words_found()[-1]

            # get the score
            score = str(self._logic.get_score())

            # check if a long word
            is_long_word = self._logic.is_long_word(path)
            if is_long_word:
                self._gui.long_word_label()

            # update gui found words canvas
            self._gui.update_words_found(word)

            # update gui score label
            self._gui.update_score_label(score)

        else:
            self._gui.try_again()

    def get_all_words_found(self):
        """
        This function return all words found by user.
        """
        return self._logic.get_words_found()

    def game_is_over(self):
        """
        This function triggers when the game is over.
        It retrieves the final score from the game logic and passes it to the
        GUI to display the game over screen with the final score.
        """
        score = str(self._logic.get_score())
        self._gui.game_over(score)

    def new_game(self):
        """
        This function starts a new game.
        It first destroys the current main window of the GUI, then creates new
        instances of the BoggleGUI, BoggleController, and the board.
        It then sets the controller for the new GUI and starts the game by
        running the new controller.
        """
        # destroy pre root:
        self._gui.get_main_window().destroy()

        # create new game objects
        new_gui = BoggleGUI()
        new_cont = BoggleController(new_gui, new_gui.get_board())
        new_gui.set_controller(new_cont)
        new_cont.run()

    def run(self) -> None:
        self._gui.run()


if __name__ == "__main__":
    gui = BoggleGUI()
    cont = BoggleController(gui, gui.get_board())
    gui.set_controller(cont)
    cont.run()
