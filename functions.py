# Python 3.7.3 x64

# Imports
import random as rd
import pickle as pk
import time as tm
import config as cfg

# Functions

def hgprint(*arguments, end="\n", prompt=cfg.GAMEPROMPT) :
    """Wrapper of 'print' method including game's custom prompt."""
    print(prompt, *arguments, end=end)

def hginput(string) :
    """Wrapper of 'input' method including game's custom prompt."""
    hgprint(string, end="")
    return input()

def menu_prompt(playername) :
    """Print main menu options and get user input."""
    hgprint(" BASTOC'S ULTIMATE HANGMAN ".center(cfg.TITLEWIDTH,"*"))
    hgprint("You are logged in as '{}'.".format(playername))
    if playername == cfg.GUESTNAME :
        hgprint("To have your progress saved, select an existing player or create one.")
    hgprint("What do you want to do? Type one of the following commands:")
    for (command,description) in cfg.COMMANDSLIST.items() :
        hgprint("'{}' to {}".format(command,description))
    choicevalid = False
    while not choicevalid :
        choice = hginput("Command: ").lower()
        if len(choice) != 1 :
            hgprint("ERROR: input must be one letter.")
        elif choice not in cfg.COMMANDSLIST.keys() :
            hgprint("ERROR: command not supported.")
        else : # All good
            choicevalid = True
    return choice

def scoreboard_load() :
    """Load scoreboard from save file or create an empty one."""
    scoreboard = dict()
    try :
        savefile = open(cfg.SAVEFILENAME,"rb")
    except FileNotFoundError :
        hgprint("NOTE: savefile was not found.")
    except PermissionError :
        hgprint("ERROR: file could not be opened in read mode.")
    else :
        upkscore = pk.Unpickler(savefile)
        try :
            scoreboard = upkscore.load()
        except EOFError :
            hgprint("WARNING: savefile was found empty.")
        else :
            hgprint("NOTE: savefile loaded.")
        savefile.close()
    return scoreboard

def scoreboard_dump(scoreboard) :
    """Dump scoreboard to save file."""
    try :
        savefile = open(cfg.SAVEFILENAME,"wb")
    except PermissionError :
        hgprint("ERROR: file could not be opened in write mode.")
    else :
        pkscore = pk.Pickler(savefile)
        pkscore.dump(scoreboard)
        savefile.close()

def scoreboard_print(scoreboard) :
    """Print scoreboard in a table-like manner."""
    if len(scoreboard) > 0 :
        hgprint(" SCOREBOARD ".center(cfg.SCOREBOARD_WIDTH, "="))
        hgprint(cfg.SCOREBOARD_WIDTH * "-")
        hgprint("{:<18} | {:<6}".format("PLAYER","SCORE"))
        hgprint(cfg.SCOREBOARD_WIDTH * "-")
        for (playername, score) in scoreboard.items() :
            hgprint("{:<18} | {:<6}".format(playername, score))
        hgprint(cfg.SCOREBOARD_WIDTH * "-")
    else :
        hgprint("The scoreboard is empty for now...")

def login(scoreboard) :
    """Select player in loaded scoreboard or create a new one."""
    hgprint("Who's playing? Enter player name.")
    # Get proper player name
    namevalid = False
    while not namevalid :
        playername = hginput("Player: ")
        if not playername.isalnum() :
            hgprint("ERROR: name must contain only alphanumeric characters.")
        elif len(playername) < 3 or len(playername) > 16 :
            hgprint("ERROR: name must contain between 3 and 16 characters.")
        elif  playername == cfg.GUESTNAME :
            hgprint("ERROR: '{}' name is reserved.".format(cfg.GUESTNAME))
        elif playername in scoreboard :
            hgprint("Player '{}' is already registered. Use this profile?".format(playername))
            answervalid = False
            while not answervalid :
                answer = hginput("[Y/n]: ").lower()
                if answer == "y" or len(answer) == 0 :
                    answervalid = True
                    namevalid = True
                elif answer == "n" :
                    answervalid = True
                else :
                    hgprint("ERROR: invalid answer.")
        else : # New player
            namevalid = True
    return playername
    
def score_load(playername, scoreboard) :
    """Load score in scoreboard or initialize it."""
    if playername in scoreboard :
        hgprint("Welcome back '{}'!".format(playername))
        hgprint("Your previous score has been loaded.")
    else :
        hgprint("Welcome '{}'!".format(playername))
        scoreboard[playername] = 0
        hgprint("Your profile has been created.")
    return scoreboard

def word_gen() :
    """Pick a random word and create a view of masked characters."""
    word = rd.choice(cfg.WORDSLIST)
    wordview = list(cfg.MASKCHAR*len(word))
    return (word, wordview)

def newgame_print() :
    """Print game rules and newgame message."""
    hgprint("GAME RULES".center(cfg.TITLEWIDTH))
    hgprint("Goal: Find the secret word to earn reward points.")
    hgprint("You get a restricted number of attempts. You can use them to:")
    hgprint("- Pick a letter. If it's part of the words, its occurences will be shown.")
    hgprint("- Try to guess the word. WARNING: This ends the game, it's fail or pass!")
    hgprint("Success grants reward points, while failure inflicts penalty points.")
    hgprint("The more letters you reveal, the higher the reward, and the lower the penalty.")
    hgprint("NOW, PLAY!".center(cfg.TITLEWIDTH))

def wordview_update(word, attempt, wordview) :
    """Update word view according to attempt."""
    for (idx,letter) in enumerate(word) :
        if letter == attempt :
            wordview[idx] = letter
    return wordview

def hanging_print() :
    """Print something goofy."""
    hgprint("You're silent...")
    tm.sleep(1)
    hgprint("You're chilled...")
    tm.sleep(1)
    hgprint("You're hanging out...")
    tm.sleep(1)
    hgprint("Hanging...")
    tm.sleep(1)
    hgprint("Hanging...")
    tm.sleep(1)
    hgprint("Hanging...")
    tm.sleep(1)
    hgprint("Oh yeah...")
    tm.sleep(1)

def attempts_init(word_len) :
    """Compute number of attempts depending of word length and game configuration."""
    return word_len + cfg.EXTRA_ATTEMPTS

def attempt_prompt(word_len, attempts_history) :
    """Get player attempt. It can be 1 letter only OR a word of proper length."""
    hgprint("Type a letter OR a word.")
    attemptvalid = False
    while not attemptvalid :
        attempt = hginput("Try: ")
        if not attempt.isalpha() :
            hgprint("ERROR: only letters (i.e. alpha characters) are accepted.")
        elif len(attempt) == 1 :
            if attempt in attempts_history :
                hgprint("ERROR: you already picked this letter previously.")
            else : # Valid letter
                attemptvalid = True
        elif len(attempt) == word_len : # Valid word
            attemptvalid = True
        else :
            hgprint("ERROR: attempt must be only 1 letter or a string that matches the word's length.")
    # Log attempt and return
    attempts_history.append(attempt)
    return (attempt, attempts_history)


def wordview_print(wordview, attempts, max_attempts) :
    hgprint("Word: {}\t\tAttempts: {}/{}".format(" ".join(wordview),
        attempts, max_attempts))
        

def success_mod(word_len, attempts_left) :
    """Compute success reward depending of word length, attempts left, and game configuration."""
    return word_len + attempts_left*cfg.ATTEMPTSFACTOR

def fail_mod(wordview) :
    """Compute failure penalty depending of characters revealed, attempts left, and game configuration."""
    masked_letters = wordview.count(cfg.MASKCHAR)
    return -masked_letters

def comment(score, highscore) :
    """Print player score and comment."""
    hgprint("You current score is: {}".format(score))
    if score > highscore :
        hgprint("It's a new highscore!")
    elif score <= cfg.BADSCOREALERT :
        hgprint("That's... depressing. Please go hang yourself!")

def game_quit(playername, scoreboard) :
    """Save scores (except for 'guest') and print quit message."""
    score = scoreboard.pop(cfg.GUESTNAME) # Pop 'guest' score
    # Check player name and prompt for save
    if playername == cfg.GUESTNAME :
        hgprint("You were logged in as '{}'. Do you want to create a new profile to save your score?".format(cfg.GUESTNAME))
        hgprint("WARNING: using an existing profile at this point will overwrite it.")
        answervalid = False
        while not answervalid :
            answer = hginput("[Y/n]: ").lower()
            if answer == "y" or len(answer) == 0 :
                playername = login(scoreboard)
                scoreboard[playername] = score
                hgprint("Your score will be saved.")
                answervalid = True
            elif answer == "n" :
                hgprint("Your score will NOT be saved.")
                answervalid = True
            else :
                hgprint("ERROR: invalid answer.")
    # Save scores and print quit message
    scoreboard_dump(scoreboard)
    if playername != cfg.GUESTNAME :
        hgprint("See you later '{}'!".format(playername))
    hgprint("The game will now quit.")