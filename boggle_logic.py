from ex11_utils import *


class BoggleLogic:
    """
    This class is used to implement the logic for the game Boggle.


    The class takes in two arguments in its constructor:
    1. board: A two-dimensional list which represents the game board.
    2. words: An iterable of strings representing the words that might be found
    on the board.


    Attributes:
    1. _score: an integer representing the current score of the user.
    2. _words_found: a list of the words found on the board,
    3. _board: a Board which represents the game board.
    4. _words: a list of words that might be found on the board, this list is
    updated during the game as words are found.


    API methods:
    1. after_submit -> None : This method checks if the path passed in argument
    describes a word on the board. If it does, it updates the score, adds the
    word to the found words list, removes the word from the list of words.


    2. is_long_word -> bool: This method checks if the length of the word
    passed in the argument path is bigger enough. If it does it return True,
    and False otherwise.


    3. get_score -> int: This method returns the current score of the user.


    4. get_words_found -> list: This method returns a list of the words
    found during the game.


    Other methods:
    1. _update_score -> None: This method updates the score.
   """

    def __init__(self, board: Board, words: Iterable[str]):

        """
        This function initializes the Boggle logic object, it takes two
        arguments, a board and words(Iterable of strings).
        It sets the score to 0, creates an empty list for words found,
        assigns the board and finds all possible words from the board using
        the possible_words_on_board helper function.
        """

        self._score = 0
        self._words_found = []
        self._board = board
        self._words = possible_words_on_board(self._board, words)

    # ------------ class Encapsulated helpers ------------ #
    def _update_score(self, path: Path):
        """
        Updates the score.
        """
        self._score += (len(path)) ** 2

    # ------------ class API ------------ #
    def after_submit(self, path: Path) -> bool:
        """
        Checks if the clicked list of tuples describing a word on board. If it
        does - return True and update the score, the words the found and remove the given word
        from words list and reset clicked list. If it is not a word returns False.
        """
        # check if path is empty
        if not path:
            return False

        word = is_valid_path(self._board, path, self._words)
        if word and word not in self._words_found:
            # update score:
            self._update_score(path)
            # add to found word:
            self._words_found.append(word)
            # remove word from words list:
            self._words.remove(word)

            return True

        return False

    def is_long_word(self, path) -> bool:
        """
        :return: True if length of word is bigger enough, False otherwise
        """
        wanted_length = len(self._board) + 1
        word_length = get_word_length(path, self._board)
        if word_length >= wanted_length:
            return True
        return False

    def get_score(self) -> int:
        return self._score

    def get_words_found(self) -> list[str]:
        return self._words_found
