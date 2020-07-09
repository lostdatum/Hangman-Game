# Game parameters
EXTRA_ATTEMPTS = 3
ATTEMPTSFACTOR = 2
BADSCOREALERT = -20

# Names
SAVEFILENAME = "hangman.saves"
GUESTNAME = "guest"

# Graphics
SCOREBOARD_WIDTH = 30
TITLEWIDTH = 60
MASKCHAR = "_"
GAMEPROMPT  = "\\_(ಥ‿ಥ)_/ >>>"
DEADPROMPT  =  " _(X╭╮X)_ >>>"
HAPPYPROMPT =  "^-(°v°)-^ >>>"


# List of available commands (as dictionary)
# Effects of commands are implemented in 'hangman.py'
COMMANDSLIST = {
"s":"show scoreboard",
"p":"select player",
"g":"play the game",
"h":"hang out",
"q":"quit",
}

# List of available words (as tuple)
WORDSLIST = (
"angry",
"awake",
"bitter",
"black",
"boiling",
"bright",
"broken",
"brown",
"certain",
"cheap",
"chemical",
"clean",
"clear",
"common",
"complete",
"complex",
"cruel",
"delicate",
"dirty",
"early",
"elastic",
"electric",
"equal",
"false",
"feeble",
"female",
"fertile",
"first",
"fixed",
"foolish",
"frequent",
"future",
"general",
"great",
"green",
"hanging",
"happy",
"healthy",
"hollow",
"living",
"loose",
"married",
"material",
"medical",
"military",
"mixed",
"narrow",
"natural",
"normal",
"open",
"opposite",
"parallel",
"past",
"present",
"private",
"public",
"quick",
"quiet",
"ready",
"regular",
"right",
"rough",
"round",
"second",
"secret",
"separate",
"serious",
"sharp",
"short",
"simple",
"small",
"smooth",
"solid",
"special",
"sticky",
"stiff",
"straight",
"strange",
"strong",
"sudden",
"sweet",
"thick",
"tight",
"tired",
"true",
"violent",
"waiting",
"white",
"wrong",
"yellow",
"young"
)