#!/usr/bin/env python
from resources.character import *

# TODO LIST:
# Generic work function
# MAX Stats (999) stop increasing after?
# Color printing?
# Balance
# End Game
# More comments!
# Windows compatibility (independent app?)
# Pickle for saving
# Better intro
# Version next: Graphics (Pygame, PyGTK)?


def load():
    global NEW_GAME
    loaded = False
    try:
        save_file = open('save/arena.save', 'r')
        loaded_char = pickle.load(save_file)
        save_file.close()
        valid = loaded_char.__dict__.keys() == Character().__dict__.keys()

        if valid:
        # print len(save_text)
            print "Save file found"
            print "Name:  %s" % loaded_char.name
            print "Level: %s" % loaded_char.lvl
            print "Gold:  %s" % loaded_char.gold
            print "Day:   %s" % loaded_char.day
            print "Would you like to load? (y/n)"
            val = get_val("ny")
            print "in function print"
            print val
            if "n" in val:
                pass
            if "y" in val:
                MY_CHAR = loaded_char
                loaded = True
                NEW_GAME = False
        else:
            print "Invalid save file"
            NEW_GAME = True
            cm()

    except IOError as ErrorMessage:
        # print ErrorMessage
        print "No save file found!"
        NEW_GAME = True
        cm()
    except EOFError as e:
        print "Invalid save file found!"
        NEW_GAME = True
        cm()
    clear()
    if loaded:
        return MY_CHAR
    else:
        return Character()
#
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
#

# START GAME EVENTS

#
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
#

if __name__ == "__main__":
    clear()
    intro = """___________________________________________________

   /$$$$$$
  /$$__  $$
 | $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$
 | $$$$$$$$ /$$__  $$ /$$__  $$| $$__  $$ |____  $$
 | $$__  $$| $$  \__/| $$$$$$$$| $$  \ $$  /$$$$$$$
 | $$  | $$| $$      | $$_____/| $$  | $$ /$$__  $$
 | $$  | $$| $$      |  $$$$$$$| $$  | $$|  $$$$$$$
 |__/  |__/|__/       \_______/|__/  |__/ \_______/



                 A Gladiator's Tale
-===========]=        Beta 0.90      =[===========-
                   By Josh Samara
___________________________________________________"""

    print intro
    cm()
    clear()
    character = load()
    if NEW_GAME:
        name = raw_input("What is your name?\n")
        character.name = name
        clear()
        print """Greetings, %s.
Here you start your trials in the arena.
Travel the town to train your skills and combat abilities.
Enter the arena to fight and gain experience.
""" % character.name
        cm()
        print """
.
.
.

You have a room in the tavern.
You can spend the nights there.
Your adventure starts here.
"""
        cm("Press any key to proceed to Town.....")
        character.next = character.town
    else:
        print "Welcome back, %s" % character.name
        cm("Press any key to proceed to Town.....")
        character.next = character.town
        character.args = [False]

    while 1:
        ## Run character next action
        character.run()
