#!/usr/bin/python
from character import *


# TODO LIST:
# Generic work function
# Vitality training (smith?)
# Leveling up/xp system + rewards
# Color printing?
# Decide: All functions in character class vs wrapper class vs ???
# ^ Split into multiple files? based on this -> better organization
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
        save_file = open('arena.save', 'r')
        save_text = save_file.read()
        split_file = save_text.split("\n")
        loaded_char = Character()
        valid = True
        if len(split_file) - 1 == len(loaded_char.__dict__):
            for line in split_file:
                if "=" in line:
                    field, value = line.split("=")
                    if field in Character().__dict__.keys():
                        if field != "name":
                            value = int(value)
                        loaded_char.__dict__[field] = value
                    else:
                        print "Invalid field in save file %s" % field
                        # print Character().__dict__.keys()
                        valid = False
        else:
            valid = False

        save_file.close()

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

    except NameError as ErrorMessage:
        print ErrorMessage
        print "No save file found"
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
-===========]=        Beta 0.7       =[===========-
                   By Josh Samara
___________________________________________________"""

for line in intro.split("\n"):
    print line
    time.sleep(.01)


cm()
clear()


character = load()
if NEW_GAME:
    name = raw_input("What is your name?\n")
    character.name = name
    clear()
    print "Greetings, %s" % character.name
    print "You are a mighty gladiator of the Emporer's Arena"
    print "You are just starting out your gladiator career"
    print "However the hard truth is that you are forced to fight"
    print "Every day you must fight or the emperorer's legion will imprison you"
    print "You are allowed to wander town and train your skills in between fights"
    print "The emperorer will become bored with you in 100 days and have you killed"
    print "Can you become the ultimate warrior?"
    print "Will you get strong enough to fight your way to freedom?"
    cm()
    print ".\n.\n.\n.\n."
    print "For today, you have finished your battle and are ready to relax."
    print "Feel free to train in the fields, visit the smith and more"
    print "The tavern has given you a permanent room. You can rest there"
    cm("Press any key to proceed to Town.....")
    character.town()
else:
    print "Welcome back, %s" % character.name
    cm("Press any key to proceed to Town.....")
    character.town(False)
