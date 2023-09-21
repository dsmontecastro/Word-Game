import time
from get_file import get_file

import lib.engine as engine
import lib.interface as interface


dictionary = engine.read_file(get_file("assets/dictionary.txt"))

if not interface.confirm("Use GUI? [Y/n]: "):
    screen = interface.Terminal()

    while screen.is_running():
        # ------ GAME LAUNCH ------

        screen.clear()

        screen.start_game()
        mode = screen.select_mode()  # Select Game Mode

        if not screen.confirm("START GAME? [Y/n]: "):  # Game Start Confirm
            continue

        # Randomization
        engine.seed(screen.read_input("Enter seed (Leave blank if unsure): "))

        # ------ GAME START ------

        if mode == "anagram":
            game = engine.AnagramMode(dictionary)
        elif mode == "combine":
            game = engine.CombineMode(dictionary)

        screen.chosen_word(game.word)

        while game.is_alive():
            guess = screen.read_input()

            if guess[0:2] == "c_":  # If user typed a command
                if guess == "c_word":
                    screen.chosen_word(game.word)
                elif guess == "c_quit":
                    if screen.confirm("Quit? [Y/n]: "):
                        screen.running = False
                        break
            else:
                if game.has_guessed(guess):
                    screen.has_guessed()
                else:
                    if game.is_correct(guess):
                        screen.on_correct(game.score)
                        if mode == "combine":
                            screen.chosen_word(game.word)
                    else:  # If user is wrong
                        screen.on_mistake(game.lives)

        if not screen.is_running():
            break

        # ------ POST GAME ------

        screen.calculate_score(game.score, game.max_score)

        if not screen.confirm("Play Again? [Y/n]: "):
            screen.on_exit()
            time.sleep(3)
            break

else:
    import lib.gui as gui
    gui.menu_screen()
