# Word Game (Demo)

![Screenshot](https://dsmontecastro.github.io/Portfolio/word_game.png)

## Description
__Made in conjunction with fellow groupmates Ayrton Dave Bautista and Josh Aleczi Merlin, A.Y. 2018.__
A Wordle-esque game demo, serving as our 1st machine project for our 1st Semester, made in around 1 month. My main role in this task was to create the logic for the GUI, connecting both the assets and interfacing elements made by my teammates.

The app was developed through _Python_, making use of _PyGame_ for its GUI. Without the GUI, it runs with no dependencies. The word processing and scoring is based on a __Scrabble__ _dictionary_ and its letter-point system, with the former saved as a static text file and the latter hardcoded in the _engine_ component.

## Installation
Install the necessary dependencies in _requirements.txt_. Afterwards, the app can be opened through __main.py__ via the standard python run command, e.g. `py main.py`. Opening it through the command-line interface (CLI) allows the user to choose between running the program on either the GUI or terminal itself.

A simple executable made with _PyInstaller_ is also available.

## Controls
After choosing to use either the GUI or pure CLI, the player is prompted to select their chosen mode and difficulty level.

    Game Modes
    * Anagram - Find all the words that use all the letters!
    * Combine - Unscramble every word you can out of the given letters!

    Difficulties (CLI is locked to ZEN)
    * Zen - Take it easy, but watch your lives...
    * Challenge - Beat the clock! You have 99 seconds!
    * Hell - Can you handle both?

In the game proper, the app follows the expected key-controls, such as:
* `<alphanumeric>` - inserts letters and numbers into the text field
* `BACKSPACE` - deletes the last character in the text field
* `ENTER` - submits the current word in the text field

##### GUI-specific Controls
* `ESC` Key or Button
    > Main Menu: exits the game
    > Game Menu: pauses the game and opens the sub-menu

##### CLI Commands - Type `c_<command>`:
* `c_help` - displays available commands
* `c_word` - prints out the scrambled letters
* `c_quit` - prompts user to quit the program