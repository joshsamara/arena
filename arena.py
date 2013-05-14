#!/usr/bin/python
import random, time, os, sys,random, math
from mygetch import *

global DEFAULT_CHAR 
DEFAULT_CHAR = {"name":"", "lvl":0 , "xp":0, "gold":10, "hp":10, "str":10, "int":10, "agil":10, "vit":10, "def":10, "wep":1, "luck":0, "hrs":0}
global MY_CHAR
MY_CHAR = DEFAULT_CHAR
global TIME
TIME = 10
global PRETTY_STAT
PRETTY_STAT = {"name":"Name", "lvl":"Lvl." , "xp":"Exp.", "gold":"Gold", "hp":"Life", "str":"Str.", "int":"Int.", "agil":"Agi.", "vit":"Vit.", "def":"Def", "wep":"Weapon", "luck":"Luck", "hrs":"Hours"}

#################
##Text management
#################

def cm(text = None):
	if text is None:
		print "Press any key to continue..."
	elif text != None:
		if text.lower() == "tavern":
			print "\nPress any key to retun to the Tavern..."
		if text.lower() == "library":
			print "\nPress any key to retun to the Library..."
	else:
		print text
	getch()


def clear():
	os.system('clear')

##just give a string of valid inputs
##you could give an array if you wanted
##idk why you would
##wasting finger strokes
def get_val(inputs):
	inputs = inputs.lower()
	val = getch().lower()
	invalid = True
	for char in inputs:
		invalid = invalid and not char in val

	if invalid:
		print "Invalid input"
		val = get_val(inputs)
	return val

#################
##File management
#################
global NEW_GAME
NEW_GAME = True
def load():
	global MY_CHAR
	global DEFAULT_CHAR
	global NEW_GAME
	try:
		save_file = open('arena.save','r')
		save_text = save_file.read()
		split_file = save_text.split("\n")
		loaded_char = {}
		valid = True
		if len(split_file)-1 == len(MY_CHAR.keys()):
			for line in split_file:
				if "=" in line and line != "":
					values = line.split("=")
					if values[0] in MY_CHAR.keys():
						this_val = values[1]
						if values[0] != "name":
							this_val = int(values[1])
						loaded_char[values[0]] = this_val
					else:
						valid = False
		else:
			valid = False

		if valid:
		# print len(save_text)
			print "Save file found"
			print "Name:  %s" % loaded_char["name"]
			print "Level: %s" % loaded_char["lvl"]
			print "Gold:  %s" % loaded_char["gold"]
			print "Time:  %s" % loaded_char["hrs"]
			print "Would you like to load? (y/n)"
			val = get_val("ny")
			print "in function print"
			print val 
			if "n" in val:
				pass
			if "y" in val:
				MY_CHAR=loaded_char
				save_file.close()
				NEW_GAME = False
		else:
			print "Invalid save file"
			NEW_GAME = True
			cm()

	except Exception, ErrorMessage:
		print ErrorMessage
		print "No save file found"
		NEW_GAME = True
		cm()

	
	clear()

def save():
	save_file = open('arena.save','w')
	for key in MY_CHAR.keys():
		save_file.write("%s=%s\n" % (key, MY_CHAR[key]))
	print("Saved!")
	cm()
	save_file.close()


def save_propt():
	global TIME
	TIME = 10
	clear()
	if TIME >= 10:
		print "Current Data\n"
		print "Name:  %s" % MY_CHAR["name"]
		print "Level: %s" % MY_CHAR["lvl"]
		print "Gold:  %s" % MY_CHAR["gold"]
		print "Would you like to save?"
		print "Press Q to exit, S to save, E to save and exit, or R to return"
		val = get_val("qsre")

		if "s" == val:
			save()
			town(False)

		if "e" == val:
			save()
			exit()

		if "q" == val:
			exit()

		if "r" == val:
			town(False)
	else:
		print "Unable to save"
		print "You may only save at the start of the day"
		cm()
		town(False)
###########################
##Activities
###########################
def time_pass(hrs = 1):
	global TIME
	global MY_CHAR
	TIME -= hrs
	MY_CHAR["hrs"] += hrs

def spend_gold(cost = 1):
	global MY_CHAR
	MY_CHAR["gold"] -= cost

def stat(stat, change = 1):
	global MY_CHAR
	MY_CHAR[stat] += change

def print_useful():
	global TIME
	global MY_CHAR
	print "Time Remaining:           %shrs" % TIME
	print "Life Remaining:           %s" % MY_CHAR["hp"]
	print "Gold Remaining:           %s" % MY_CHAR["gold"]

def print_stat(stats, showtime = True):
	global PRETTY_STAT
	global TIME
	for stat in stats:
		text = PRETTY_STAT[stat]
		print "%s: %s" % (text, MY_CHAR[stat])
	if showtime:
		print "Time: %s" % TIME

def requires(gold = 1, hours = 1, life = 0):
	global MY_CHAR
	global TIME
	goldcheck = MY_CHAR["gold"] < gold
	hourcheck = TIME < hours
	lifecheck = MY_CHAR["hp"] < life

	if goldcheck or hourcheck or lifecheck:
		print "Impossible!"
		if goldcheck:
			print "You need %s gold" % gold
			print "You have %s gold" % MY_CHAR["gold"]
		if hourcheck:
			print "You neeed %s hours" % hours
			print "There are %s hours left" % TIME
		if lifecheck:
			print "You need %s life" % lifecheck
			print "You have %s life" % MY_CHAR["life"]
		return False
	else:
		return True

###########################
##Town
###########################
def town(refresh = True):
	global TIME
	clear()
	if refresh:
		TIME = 10
	def greeting():
		print "Welcome to Town!"
		print_useful()
		print "You can do any of the following:"
		print "Save and/or exit the game (S)*"
		print "Enter the Tavern          (T)"
		print "Go to the Library         (L)"
		print "Go to the Trainng Fields  (F)"
		print "Visit the Blacksmith      (B)" 
		print "Return to the Arena       (A)"
		print "\nNote: You must have 10hrs in the day"
		print "to be able to save the game."

	greeting()
	val = get_val("stlfba")

	if val == "s":
		save_propt()
	elif val == "t":
		tavern()
	elif val == "l":
		library()
	save_propt()


def exit():
	print "Goodbye"
	sys.exit()
###########################
##Tavern
###########################
def tavern():
	clear()
	print "Welcome to the Tavern!"
	print_useful()
	print "Here you can do any of the following:"
	print "Buy a Meal                (M)  1g  1hr"
	print "Grab a Drink              (D)  1g  1hr"
	print "Rent a Room               (R)  0g  5hr"
	print "Gamble some gold          (G)  1g  1hr"
	print "Return to town            (T)  0g  0hr"

	val = get_val("mdrgt")
	clear()
	if val == "m":
		eat()
	elif val == "d":
		drink()
	elif val == "r":
		sleep()
	elif val == "g":
		gamble()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN TAVERN SELECT"
		cm()


def eat():
	if requires():
		global MY_CHAR
		print "You order a big steak and devour it"
		print "It's relieving after a long day"
		MY_CHAR["hp"] += int(math.ceil(int(MY_CHAR["vit"])/3))
		spend_gold()
		time_pass()
		print_stat(["hp","gold"])
	cm("tavern")
	tavern()

def drink():
	if requires(1, 1, 1):
		global MY_CHAR
		print "You ask the bartender for a drink"
		print "and drink it up in one gulp."
		print "It's a little rough on the stomach,"
		print "but you feel a little bit luckier"
		MY_CHAR["hp"] -= int(math.ceil(MY_CHAR["vit"]/10))
		stat("luck")
		spend_gold()
		time_pass()
		print_stat(["hp","luck", "gold"])
	cm("tavern")
	tavern()

def sleep():
	if requires(0, 5, 0):
		global MY_CHAR
		print "You sleep for a few hours"
		MY_CHAR["hp"] = MY_CHAR["vit"]
		time_pass(5)
		print_stat(["hp"])
	cm("tavern")
	tavern()
	
def gamble():
	if requires():
		global MY_CHAR
		print "You play a hand of cards"
		chance = random.randint(1+MY_CHAR["int"],1000)
		if chance > 900:
			print 'You win!'
			spend_gold(-1)
		else:
			print 'You lose.'
			spend_gold()

		time_pass(1)
		print_stat(["gold"])
	cm("tavern")
	tavern()



###########################
##Tavern
###########################
def library():
	clear()
	print "Welcome to the Library!"
	print_useful()
	print "Here you can do any of the following:"
	print "Study Magics              (S)  0g  1hr"
	print "Borrow a book             (B)  1g  3hr"
	print "Hire a tutor              (H)  3g  3hr"
	print "Read and relax            (R)  0g  1hr"
	print "Return to town            (T)  0g  0hr"

	val = get_val("sbhrt")
	clear()
	if val == "s":
		study()
	elif val == "b":
		book()
	elif val == "h":
		tutor()
	elif val == "r":
		read()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN TAVERN SELECT"
		cm()


def study():
	if requires(0,1):
		global MY_CHAR
		print "You spend some time studying battle techniques,"
		print "weapon varience, and the arcane arts."
		time_pass()
		stat("int")
		print_stat(["int"])
	cm("library")
	library()

def book():
	if requires(1,3):
		global MY_CHAR
		print "You borrow and read a book of advanced"
		print "fighting and magics"
		time_pass(3)
		stat("int", 4)
		print_stat(["int","gold"])
	cm("library")
	library()

def tutor():
	if requires(3,3):
		global MY_CHAR
		print "You have an advanced wizard teach you"
		print "some incredibly difficult magic"
		time_pass(3)
		stat("int", 7)
		print_stat(["int","gold"])
	cm("library")
	library()


def read():
	if requires(0):
		global MY_CHAR
		print "You read a nice fiction and rest"
		time_pass(1)
		stat("hp", 1)
		print_stat(["hp"])
	cm("library")
	library()





########################################

##START GAME EVENTS

###########################################
clear()
intro ="""___________________________________________________

   /$$$$$$                                         
  /$$__  $$                                        
 | $$  \ $$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ 
 | $$$$$$$$ /$$__  $$ /$$__  $$| $$__  $$ |____  $$
 | $$__  $$| $$  \__/| $$$$$$$$| $$  \ $$  /$$$$$$$
 | $$  | $$| $$      | $$_____/| $$  | $$ /$$__  $$
 | $$  | $$| $$      |  $$$$$$$| $$  | $$|  $$$$$$$
 |__/  |__/|__/       \_______/|__/  |__/ \_______/


 		        
-===========]=   A Gladiator's Tale  =[===========-
                      Beta 0.1
___________________________________________________"""

for line in intro.split("\n"):
	print line
	time.sleep(.01)


cm()
clear()


load()
if NEW_GAME:
	name = raw_input("What is your name?\n")
	MY_CHAR["name"] = name
	clear()
print "Greetings, %s" % MY_CHAR["name"]
print "You are a mighty gladiator of the Emporer's Arena"
print "You are a celebrity among the people"
print "However the hard truth is that you are forced to fight"
print "Every day you must fight or the emperorer's legion will imprison you"
print "You are allowed to wander town and train your skills in between fights"
print "Can you become the ultimate warrior?"
print "Will you get strong enough to fight your way to freedom?"
cm()
print ".\n.\n.\n.\n."

print "For today, you have finished your battle and are ready to relax."
print "Feel free to train in the fields, visit the smith and more"
print "The tavern has given you a permanent room. You can rest there"
cm("Press any key to proceed to town.....")

town()
