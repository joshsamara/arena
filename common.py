#!/usr/bin/python
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
ENEMY_TYPES = [["Peasant"],
               ["Fighter",
                "Thief",
                "Apprentice"],
               ["Warrior",
                "Ranger",
                "Mage"],
               ["Paladin",
                "Assassin",
                "Wizard]"],
               ["Minotaur",
                "Ninja",
                "Archon"],
               ["Shadow"]]


#
# Text management
#
def cm(text=None):
    if text is None:
        print "Press any key to continue..."
    elif text is not None:
        if text.lower() == "tavern":
            print "\nPress any key to retun to the Tavern..."
        elif text.lower() == "library":
            print "\nPress any key to retun to the Library..."
        elif text.lower() == "town":
            print "\nPress any key to retun to Town..."
        elif text.lower() == "fields":
            print "\nPress any key to retun to the Fields.."
        elif text.lower() == "smith":
            print "\nPress any key to retun to the Blacksmith.."
    else:
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
        print ".",
        val = get_val(inputs)
    clear()
    return val



def exit():
    print "Goodbye"
    sys.exit()
