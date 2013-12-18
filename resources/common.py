import sys
import os
from mygetch import *

NEW_GAME = True
PRETTY_STAT = {
    "name": "Name",
    "lvl": "Lvl.",
    "xp": "Exp.",
    "gold": "Gold",
    "hp": "Life",
    "str": "Str.",
    "int": "Int.",
    "agil": "Agi.",
    "vit": "Vit.",
    "defense": "Armor Level",
    "wep": "Weapon Level",
    "luck": "Luck",
    "day": "Day",
    "hrs": "Hours"}

#
# Text management
#

# 'Continue message'


def cm(text=None):
    if text is None:
        print "Press any key to continue..."
    elif text is not None:
        pretty_message = {"tavern": "Tavern", "library":
                          "Library", "town": "Town",
                          "fields": "Fields",
                          "smith": "Blacksmith"}
        try:
            message = pretty_message[text.lower()]
            print "\nPress any key to retun to the %s..." % message
        except KeyError:
            print text
    getch()


def clear():
    os.system('clear')


def print_bar(version):
    if version == 0:
        print "\n#################################"
    elif version == 1:
        print "#################################\n"
    else:
        print "#################################"


# just give a string of valid inputs
# you could give an array or something if you wanted
# idk why you would
# wasting finger strokes
def get_val(inputs):
    inputs = inputs.lower()
    val = getch().lower()
    invalid = True
    for char in inputs:
        invalid = invalid and not char in val

    if invalid:
        # print ".",
        val = get_val(inputs)
    clear()
    return val


def exit():
    print "Goodbye"
    sys.exit()

def color(text, color):
    BASE    = '\033[%dm'
    WHITE   = 0
    #BASIC WHITE MANIP
    WHITEB  = 1 #bold
    WHITEU  = 4 #underline
    WHITEF  = 5 #flashing
    WHITEH  = 7 #highlighted
    #BASIC COLORS
    GREY    = 90
    RED     = 91
    GREEN   = 92
    YELLOW  = 93
    BLUE    = 94
    PINK    = 95
    TEAL    = 96
    #HIGHLIGHTS
    REDH    = 41
    GREENH  = 42
    YELLOWH = 43
    BLUEH   = 44
    PINKH   = 45
    TEALH   = 46
    WHITEH2 = 47
    GREYH   = 100

    #prooooobably not a good way to do things
    choices = locals().copy()
    for item in ['text', 'color', 'BASE']:
        choices.pop(item)

    END = BASE % WHITE
    color = color.upper()
    if color in choices.keys():
        modifier = BASE % choices[color]
    else:
        modifier = END

    return "%s%s%s" % (modifier, text, END)

# print "Here you can do any of the following:"
# print "Study Magics              (S)  --  1hr  ----"
# print "Borrow a book             (B)  1g  3hr  ----"
# print "Hire a tutor              (H)  3g  3hr  ----"
# print "Read and relax            (R)  --  1hr  ----"
# print "Tutor Magics              (M)  --  8hr  ----"
# print "Return to Town            (T)  --  ---  ----"

def make_option(description, hotkey, gold = 0, time = 0, hp = 0):
    if gold == 0: 
        gold = '--'
    else:
        gold = '%sg' % gold

    if time == 0:
        time = '---'
    else:
        time = '%shr' % time

    if hp == 0:
        hp = '---'
    else:
        hp = "%shp" % hp

    hotkey = hotkey.upper()


    return {'description':description, 'hotkey': hotkey, 'gold':gold, 'time':time, 'hp':hp}

def nav_menu(option_list, short = False):
    text = "Here you can do any of the following:\n"
    line_start = "%-26s(%s)"
    if short:
        line_end = "\n"
    else:
        line_end = "  %s  %s  %s\n"

    for option in option_list:
        description = option['description']
        hotkey = option['hotkey']
        tmp_line_start = line_start % (description,hotkey)
        tmp_line_start = tmp_line_start.replace(hotkey, color(hotkey, 'green'))
        if short:
            text += tmp_line_start + line_end
        else:
            gold = color(option['gold'], 'yellow')
            time = color(option['time'], 'teal')
            hp = color(option['hp'], 'pink')
            text += tmp_line_start + line_end % (gold, time, hp)
    return text.rstrip("\n")
