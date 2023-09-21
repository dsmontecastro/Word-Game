import random
from get_file import get_file


def read_file(file):
    """Returns a list of words given in a file."""

    f = open(get_file(file))

    words = [i.rstrip() for i in f]

    return words


def pick_word(dictionary, index):
    """Returns the n-th word from a given dicitonary with n = index."""

    return dictionary[index]


def check_word(word, string):
    """Returns True if a word can be formed from a string.
    Otherwise, False.
    """

    count = 0

    for char in word:
        if char in string:
            index = string.index(char)
            string = string[:index] + string[index + 1 :]
            count += 1

    if count == len(word):
        return True

    return False


def scrabble_score(string):
    """Returns the scrabble score from a given string."""

    string = string.lower()
    score = 0
    scores = [
        1,
        3,
        3,
        2,
        1,
        4,
        2,
        4,
        1,
        8,
        5,
        1,
        3,
        1,
        1,
        3,
        10,
        1,
        1,
        1,
        1,
        4,
        4,
        8,
        4,
        10,
    ]

    for char in string:
        index = ord(char) - ord("a")
        score += scores[index]

    return score


def max_score(iterable):
    """Returns the maximum scrabble score in an iterable of strings."""

    max_score = 0

    for word in iterable:
        max_score += scrabble_score(word)

    return max_score


def seed(seed=""):
    """Sets the random seed for use in other random functions."""

    if seed != "":
        random.seed(seed)
    else:
        random.seed()


class AnagramMode:
    """Creates a class specifically for Anagram Game Mode."""

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.min_length = 3  # Minimum word length
        self.max_length = 6  # Maximum word length
        self.score = 0
        self.lives = 3
        self.word = self.random_word(dictionary)
        self.words = self.find_anagrams(dictionary, self.word)
        self.max_score = max_score(self.words)
        self.correct_answers = []

    def is_correct(self, string):
        """Returns True if the word is a valid anagram.
        Returns False if not a valid anagram.
        """

        if string in self.words:
            self.correct_answers.append(string)
            self.score += scrabble_score(string)

            if self.score == self.max_score:
                self.lives = 0

            return True

        self.lives -= 1
        return False

    def has_guessed(self, string):
        """Returns True if the word has already been guessed:
        otherwise returns False.
        """

        if string in self.correct_answers:
            return True

        return False

    def is_alive(self):
        """Returns True if it is not game over yet, return false otherwise."""

        if self.lives > 0:
            return True

        return False

    def random_word(self, dictionary):
        """Returns a random word from a given dictionary
        with length in range [min_length, max_length].
        """

        word = pick_word(dictionary, random.randrange(len(dictionary)))

        while (
            not self.min_length <= len(word) <= self.max_length
            or len(self.find_anagrams(dictionary, word)) < 2
        ):
            word = pick_word(dictionary, random.randrange(len(dictionary)))

        return word

    def find_anagrams(self, dictionary, string):
        """Returns a list of all anagrams that can be formed from a word
        from a given dictionary.
        """

        anagrams = []

        for word in dictionary:
            if sorted(word) == sorted(string):
                anagrams.append(word)

        return anagrams


class CombineMode:
    """Creates a class specifically for Combine Game Mode."""

    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.min_length = 3  # Min. number of words
        self.score = 0
        self.lives = 3
        self.word = self.random_word(dictionary)
        self.words = self.find_words(dictionary, self.word)
        self.correct_answers = []
        self.max_score = max_score(self.words)

    def is_correct(self, string):
        """Returns True if the word is a valid answer. If not, returns False."""

        if string in self.words:
            self.correct_answers.append(string)
            self.score += scrabble_score(string)

            if self.score == self.max_score:
                self.lives = 0

            return True

        self.lives -= 1
        return False

    def has_guessed(self, string):
        """Returns True if the word has already been guessed.
        If not, returns False.
        """

        if string in self.correct_answers:
            return True

        return False

    def is_alive(self):
        """Returns True if it is not game over yet, return false otherwise."""

        if self.lives > 0:
            return True

        return False

    def random_word(self, dictionary):
        """Returns a random word from a given dictionary.

        Also makes sure the word can form at least 10
        words from its letters.
        """

        word = random.choice(dictionary)

        while len(word) < 4 or not 5 <= len(self.find_words(dictionary, word)) <= 50:
            word = random.choice(dictionary)

        return word

    def find_words(self, dictionary, string):
        """Returns all the words that can be formed in a string."""

        words = []

        for word in dictionary:
            if check_word(word, string):
                words.append(word)

        return words

    def combine_words(self, iterable):
        """Returns a shuffled string, combining all strings from an iterable
        into one string.
        """

        min_word = [0] * 26
        combined_word = ""

        for i in iterable:
            letter_count = [0] * 26

            for letter in i:
                index = ord(letter) - ord("a")
                letter_count[index] += 1

            for j in range(26):
                if min_word[j] < letter_count[j]:
                    min_word[j] = letter_count[j]

        for i in range(26):
            if min_word[i] == 0:
                continue

            char_key = ord("a") + i
            combined_word += chr(char_key) * min_word[i]

        _combined_word = [i for i in combined_word]
        random.shuffle(_combined_word)
        combined_word = "".join(_combined_word)

        return combined_word
