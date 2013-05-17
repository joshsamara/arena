#!/usr/bin/python
import random, time, os, sys,random, math
from mygetch import *

global DEFAULT_CHAR 
DEFAULT_CHAR = {"name":"", "lvl":0 , "xp":0, "gold":10, "hp":10, "str":10, "int":10, "agil":10, "vit":10, "def":10, "wep":1, "luck":0, "day":0, "hrs": 10}
global MY_CHAR
MY_CHAR = DEFAULT_CHAR
global TIME
TIME = 10
global PRETTY_STAT
PRETTY_STAT = {"name":"Name", "lvl":"Lvl." , "xp":"Exp.", "gold":"Gold", "hp":"Life", "str":"Str.", "int":"Int.", "agil":"Agi.", "vit":"Vit.", "def":"Def", "wep":"Weapon", "luck":"Luck", "day":"Day"}

#################
##Text management
#################

def cm(text = None):
	if text is None:
		print "Press any key to continue..."
	elif text != None:
		if text.lower() == "tavern":
			print "\nPress any key to retun to the Tavern..."
		elif text.lower() == "library":
			print "\nPress any key to retun to the Library..."
		elif text.lower() == "town":
			print "\nPress any key to retun to Town..."
		elif text.lower() == "fields":
			print "\nPress any key to retun to the Fields.."
	else:
		print text
	getch()


def clear():
	os.system('clear')

##just give a string of valid inputs
##you could give an array or something if you wanted
##idk why you would
##wasting finger strokes
def get_val(inputs):
	inputs = inputs.lower()
	val = getch().lower()
	invalid = True
	for char in inputs:
		invalid = invalid and not char in val

	if invalid:
		print ".",	
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
			print "Day:   %s" % loaded_char["day"]
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
	clear()
	print """
  ____                               
 / ___|  __ ___   _____              
 \___ \ / _` \ \ / / _ \             
  ___) | (_| |\ V /  __/             
 |____/ \__,_| \_/ \___|  
 """
	print "Current Data"
	print "Name:  %s" % MY_CHAR["name"]
	print "Level: %s" % MY_CHAR["lvl"]
	print "Gold:  %s" % MY_CHAR["gold"]
	print "Day:   %s" % MY_CHAR["day"]
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

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Activities

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def time_pass(hrs = 1):
	global MY_CHAR
	MY_CHAR["hrs"] -= hrs

def spend_gold(cost = 1):
	global MY_CHAR
	MY_CHAR["gold"] -= cost

def stat(stat, change = 1):
	global MY_CHAR
	MY_CHAR[stat] += change

def print_useful(noskip = False):
	global MY_CHAR
	if noskip:
		skip = ""
	else:
		skip = "\n"
	print "%s#################################" % skip
	print "Day:                      %s" % MY_CHAR["day"]
	print "Time Remaining:           %s hrs" % MY_CHAR["hrs"]
	print "Life Remaining:           %s hp" % MY_CHAR["hp"]
	print "Gold Remaining:           %s gold" % MY_CHAR["gold"]
	print "#################################\n"

def print_stat(stats, showtime = True):
	global PRETTY_STAT
	for stat in stats:
		text = PRETTY_STAT[stat]
		print "%s: %s" % (text, MY_CHAR[stat])
	if showtime:
		print "Time: %s" % MY_CHAR["hrs"]

def requires(gold = 1, hours = 1, life = 0):
	global MY_CHAR
	goldcheck = MY_CHAR["gold"] < gold
	hourcheck = MY_CHAR["hrs"] < hours
	lifecheck = MY_CHAR["hp"] < life

	if goldcheck or hourcheck or lifecheck:
		print "Impossible!"
		if goldcheck:
			print "You need %s gold" % gold
			print "You have %s gold" % MY_CHAR["gold"]
		if hourcheck:
			print "You neeed %s hours" % hours
			print "There are %s hours left" % MY_CHAR["hrs"]
		if lifecheck:
			print "You need %s life" % lifecheck
			print "You have %s life" % MY_CHAR["life"]
		return False
	else:
		return True

def work(base, stat, factor):
	global MY_CHAR
	added = int(math.floor(MY_CHAR[stat]/factor))
	earned = base + added
	MY_CHAR["gold"] += earned

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Town

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def town(refresh = True):
	global MY_CHAR
	clear()
	if refresh:
		MY_CHAR["hrs"] = 16
	def greeting():
		print "Welcome to:"
		print """
  _____
 |_   _|____      ___ __             
   | |/ _ \ \ /\ / / '_ \            
   | | (_) \ V  V /| | | |           
   |_|\___/ \_/\_/ |_| |_|  
		"""
		print_useful()
		print "Here you can do any of the following:"
		print "Enter the Tavern          (T)"
		print "Go to the Library         (L)"
		print "Go to the Trainng Fields  (F)"
		print "Visit the Blacksmith      (B)" 
		print "Enter the Arena           (A)"
		print "Save and/or exit the game (S)"

	greeting()
	val = get_val("stlfba9")

	if val == "s":
		save_propt()
	elif val == "t":
		tavern()
	elif val == "l":
		library()
	elif val == "f":
		fields()
	elif val == "9":
		town(True)
	else:
		print "ERROR IN TOWN SELECT"
		cm()
	save_propt()


def exit():
	print "Goodbye"
	sys.exit()

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Tavern

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def tavern():
	clear()
	print "Welcome to the:"
	print """
  ______  
 |_   _|_ ___   _____ _ __ _ __      
   | |/ _` \ \ / / _ \ '__| '_ \     
   | | (_| |\ V /  __/ |  | | | |    
   |_|\__,_| \_/ \___|_|  |_| |_| 
	"""
	print_useful()
	print "Here you can do any of the following:"
	print "Buy a Meal                (M)  1g  1hr"
	print "Grab a Drink              (D)  1g  1hr"
	print "Go to sleep               (s)  --  ---"
	print "Gamble some gold          (G)  1g  1hr"
	print "Bartend                   (B)  --  8hr"	
	print "Return to town            (T)  --  ---"

	val = get_val("mdsgbt")
	clear()
	if val == "m":
		eat()
	elif val == "d":
		drink()
	elif val == "s":
		sleep()
	elif val == "g":
		gamble()
	elif val == "b":
		bartend()
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
	if requires(0, 0, 0):
		global MY_CHAR
		print "You sleep for the night"
		MY_CHAR["hp"] = MY_CHAR["vit"]
		stat("day")
		print_stat(["hp"])
		print_stat(["day"])
	cm("town")
	town()
	
def gamble():
	if requires():
		global MY_CHAR
		print "You play a hand of cards"
		chance = random.randint(1+MY_CHAR["int"],1000)
		if chance > 900:
			print 'You win!'
			spend_gold(-10)
		else:
			print 'You lose.'
			spend_gold()

		time_pass(1)
		print_stat(["gold"])
	cm("tavern")
	tavern()

def bartend():
	if requires(0,8):
		global MY_CHAR
		print "You work at the bar for a few hours"
		work(1, "luck", 3)
		time_pass(8)
		print_stat(["gold"])
	cm("tavern")
	tavern()





######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Library

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def library():
	clear()
	print "Welcome to the:"
	print """
  _       _
 | |   (_) |__  _ __ __ _ _ __ _   _ 
 | |   | | '_ \| '__/ _` | '__| | | |
 | |___| | |_) | | | (_| | |  | |_| |
 |_____|_|_.__/|_|  \__,_|_|   \__, |
                                |___/ 
"""
	print_useful(True)
	print "Here you can do any of the following:"
	print "Study Magics              (S)  --  1hr"
	print "Borrow a book             (B)  1g  3hr"
	print "Hire a tutor              (H)  3g  3hr"
	print "Read and relax            (R)  --  1hr"
	print "Tutor Magics              (M)  --  8hr"
	print "Return to Town            (T)  --  ---"

	val = get_val("sbhrmt")
	clear()
	if val == "s":
		study()
	elif val == "b":
		book()
	elif val == "h":
		tutor()
	elif val == "r":
		read()
	elif val == "m":
		magics()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN LIRARY SELECT"
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

def magics():
	if requires(0,8):
		global MY_CHAR
		print "You work a day teaching magic to others"
		work(5, "int", 10)
		time_pass(8)
		print_stat(["gold"])
	cm("library")
	library()

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Training Fields

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################
def fields():
	clear()
	print "Welcome to the:"
	print """
  _____        _     _
 |  ___(_) ___| | __| |___           
 | |_  | |/ _ \ |/ _` / __|          
 |  _| | |  __/ | (_| \__ \          
 |_|   |_|\___|_|\__,_|___/         
 """
	print_useful()
	print "Here you can do any of the following:"
	print "Fight a training Dummy    (D)  --  2hr"
	print "Spar a Battle master      (M)  1g  3hr"
	print "Run an obstacle Course    (C)  --  2hr"
	print "Enter a Race              (R)  3g  1hr"
	print "Perform Show tricks       (S)  --  8hr"
	print "Return to Town            (T)  --  ---"

	val = get_val("dmcrst")

	clear()
	if val == "d":
		dummy()
	elif val == "m":
		master()
	elif val == "c":
		course()
	elif val == "r":
		race()
	elif val == "s":
		show()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN FIELDS SELECT"
		cm()


def dummy():
	if requires(0,2):
		global MY_CHAR
		print "You beat up a dummy for a nice work out."
		time_pass(2)
		stat("str")
		print_stat(["str"])
	cm("fields")
	fields()

def master():
	if requires(1,3,1):
		global MY_CHAR
		print "You spar a master trainer for some time."
		print "He shows you a thing or two about fighting."
		print "You take a few hits though."
		time_pass(3)
		stat("str", 6)
		stat("hp", -1)
		print_stat(["str","hp","gold"])
	cm("fields")
	fields()

def course():
	if requires(0,2):
		global MY_CHAR
		print "You dash through obstacle course for a few hours"
		time_pass(2)
		stat("agil")
		print_stat(["agil"])
	cm("fields")
	fields()

def race():
	if requires(3,1):
		global MY_CHAR
		print "You run a race and it really works your muscles."
		time_pass(1)
		stat("agil", 3)
		print_stat(["agil"])
	cm("fields")
	fields()

def show():
	if requires(0,8):
		global MY_CHAR
		print "You spend a day performing tricks"
		work(3, "agil", 7)
		time_pass(8)
		print_stat(["gold"])
	cm("fields")
	fields()



######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################


##START GAME EVENTS

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

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


 		        
                 A Gladiator's Tale  
-===========]=        Beta 0.1       =[===========-
                   By Josh Samara
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
if NEW_GAME:
	town()
else:
	town(False)
