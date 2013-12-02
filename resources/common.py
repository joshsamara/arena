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
