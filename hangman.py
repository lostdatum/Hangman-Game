#!/user/bin/python3
# -*- coding: utf-8 -*-

# Imports
import config as cfg
import functions as fct

# Load scoreboard
scoreboard = fct.scoreboard_load()

# Log in as guest
playername = cfg.GUESTNAME
scoreboard[playername] = 0

# Start app
while True:
    # Show main menu
    choice = fct.menu_prompt(playername) # NB: 'choice' output will be valid at this point
    if choice == 's': # Print scoreboard
        fct.scoreboard_print(scoreboard)
    elif choice == 'p': # Prompt for login and update score
        playername = fct.login(scoreboard)
        scoreboard = fct.score_load(playername, scoreboard)
    elif choice == 'h': # Print goofy message
        fct.hanging_print()
    elif choice == 'g': # New game
        # Initialize score
        score = scoreboard[playername]
        highscore = max(scoreboard.values())
        # Print rules
        fct.newgame_print()
        # Select word and create view
        (word, wordview) = fct.word_gen()
        # Initialize attempts
        max_attempts = fct.attempts_init(len(word))
        attempts_history = list()
        # Start playing
        fct.status_print(wordview, len(attempts_history), max_attempts)
        (victory, defeat) = (False, False)
        # New attempt
        while not (victory or defeat):
            # Prompt for attempt
            (attempt, attempts_history) = fct.attempt_prompt(len(word), attempts_history)
            # Update view
            if len(attempt) > 1: # Tried to guess word
                if attempt == word:
                    victory = True
                else:
                    defeat = True
            else: # Chose 1 letter
                wordview = fct.wordview_update(word, attempt, wordview)
                if wordview == list(word): # Found all letters
                    victory = True
                elif len(attempts_history) >= max_attempts: # Used all attempts
                    defeat = True
                else: # Game goes on
                    fct.status_print(wordview, len(attempts_history), max_attempts)
            # Check success or failure
            if victory:
                fct.hgprint("Congratulations, you found it!", prompt=cfg.HAPPYPROMPT)
                mod = fct.success_mod(len(word), max_attempts-len(attempts_history))
            elif defeat:
                fct.hgprint("You failed. It's okay... hang in there!", prompt=cfg.DEADPROMPT)
                mod = fct.fail_mod(wordview)
        # Conclude, update score and save
        fct.hgprint("The word was: '{}'".format(word))
        fct.hgprint("You get {} points!".format(mod))
        score +=mod # Update score
        scoreboard[playername] = score
        fct.comment(score, highscore)
    elif choice == 'q': # Save scoreboard & quit
        fct.game_quit(playername, scoreboard)
        break