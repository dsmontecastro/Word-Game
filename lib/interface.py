import os


commands = ["help", "word", "quit"]
modes = ["anagram", "combine"]
modes_short = ["a", "c"]


# Game Launch
ON_LAUNCH = "Hello! Welcome to the Autism Induced Word Unscrambler!\n"
# Select Game Mode
ON_SELECT_MODE = """Select a Game Mode!
	Select the corresponding letter and press enter to start the game.

	> [A]nagram: What else is there!
	> [C]ombine: Unscramble the puzzle!
	> [H]olocaust: Coming out Winter 2018!
	"""
# Anagram Game Mode Launch
ON_ANAGRAM_START = """Welcome to Search the Anagram!
	Try to find all anagrams of the given string.

	E.g. "Reign" -> "Ringe", "Niger",...
	"""
# Combine Game Mode Launch
ON_COMBINE_START = """Welcome to Combine the Words!
	Try to find all words that can be formed from the string.

	E.g. "Holocaust" -> "Cahoots", "Slouch", "Lust",...
	"""
# Game Exit
ON_EXIT = "Thank you for playing Autism Induced Word Unscrambler!"


def ask(string, iterable):
    """Asks the user for valid input.
    The input is valid if it is found in the iterable.
    """

    while True:
        response = input(string).lower().rstrip()

        if response in iterable:
            return response
        else:
            print("Try Again.")


def confirm(string):
    """Prints string and returns True or False depending on user input.
    Only yes or no decisions are accepted.
    """

    decision = ask(string, ("y", "n", "yes", "no"))

    if decision in ("y", "yes"):
        return True
    else:
        return False


class Terminal:
    """Sets up Terminal interface."""

    def __init__(self):
        self.running = True

    def is_running(self):
        if self.running:
            return True

        return False

    def ask(self, string, iterable):
        """Asks the user for valid input.
        The input is valid if it is found in the iterable.
        """

        while True:
            response = input(string).lower().rstrip()

            if response in iterable:
                return response
            else:
                print("Try Again.")

    def confirm(self, string):
        """Prints string and returns True or False depending on user input.
        Only yes or no decisions are accepted.
        """

        decision = self.ask(string, ("y", "n", "yes", "no"))

        if decision in ("y", "yes"):
            return True
        else:
            return False

    def read_input(self, string=""):
        """Reads player input and returns data accordingly.

        When a command is input, returns "c_[command_name]".
        Otherwise, returns the string input.
        """

        while True:
            _string = input(string).lower().rstrip()

            if _string != "":
                if _string[0] == "/":
                    if _string[1:] in commands:
                        if _string[1:] == "help":
                            self.help()
                        else:
                            return "c_{}".format(_string[1:])
                    else:
                        print("Unknown command!")
                else:
                    return _string
            else:
                return _string

    def clear(self):
        """Clears the Terminal Screen"""

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def start_game(self):
        """Prints text upon opening the game."""

        print(ON_LAUNCH)

    def select_mode(self):
        """Prints text to select a game mode and returns the user input.
        Repeatedly prints text to try again if an invalid input is received.
        """

        print(ON_SELECT_MODE)

        mode = self.ask("Choose Mode: ", modes + modes_short)

        if mode in ("anagram", "a"):
            print(ON_ANAGRAM_START)
        elif mode in ("combine", "c"):
            print(ON_COMBINE_START)

        if mode in modes:
            return modes[modes.index(mode)]
        else:
            return modes[modes_short.index(mode)]

    def help(self):
        """Prints help."""
        string = "Commands: "

        for word in commands:
            string += "  /{}".format(word)

        print(string)

    def has_guessed(self):
        """Prints text that you already guessed that word."""

        print("You have already guessed that word! Try again.")

    def on_correct(self, score):
        """Triggers when a valid answer is made"""

        print("Correct! Score: {}".format(score))

    def on_mistake(self, retries):
        """Triggers when an invalid answer is made."""

        print("Wrong! Retries left: {}".format(retries))

    def chosen_word(self, string):
        """Prints the chosen word."""

        print("The word is: {}".format(string))

    def calculate_score(self, score, max_score):
        """Prints score."""

        print("Your score is: {}/{}".format(score, max_score))

    def on_exit(self):
        """Prints text on exit."""

        print(ON_EXIT)
