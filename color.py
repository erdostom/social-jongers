COLOR_ENABLED = True
COLORS = {
    "ENDC":         '\033[0m',
    "BOLD":         '\033[1m',
    "ITALIC":       '\033[3m',
    "UNDERLINE":    '\033[4m',
    "BLACK":        '\033[0;30m',
    "GREY":         '\033[1;30m',
    "GRAY":         '\033[1;30m',
    "RED":          '\033[0;31m',
    "LIGHT_RED":    '\033[1;31m',
    "GREEN":        '\033[0;32m',
    "LIGHT_GREEN":  '\033[1;32m',
    "BROWN":        '\033[0;33m',
    "YELLOW":       '\033[1;33m',
    "BLUE":         '\033[0;34m',
    "LIGHT_BLUE":   '\033[1;34m',
    "PURPLE":       '\033[0;35m',
    "LIGHT_PURPLE": '\033[1;35m',
    "CYAN":         '\033[0;36m',
    "LIGHT_CYAN":   '\033[1;36m',
    "LIGHT_GRAY":   '\033[0;37m',
    "WHITE":        '\033[1;37m' ,
}

def color(colorKey=None):
    if COLOR_ENABLED:
        if colorKey == None:
            print(COLORS["ENDC"], end="")
        elif type(colorKey)==str:
            colorKey = colorKey.strip().upper()
            if colorKey.strip().upper() in COLORS:
                print(COLORS[colorKey], end="")
