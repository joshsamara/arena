#!/usr/bin/python
import random, time, os, sys, math
from mygetch import *

# TODO PICKLE
# DEFAULT_CHAR = {"name":"", "lvl":0 , "xp":0, "gold":10, "hp":10, "str":10, "int":10, "agil":10, "vit":10, "def":1, "wep":1, "luck":0, "day":0, "hrs": 10}
# MY_CHAR = DEFAULT_CHAR
PRETTY_STAT = {"name":"Name", "lvl":"Lvl." , "xp":"Exp.", "gold":"Gold", "hp":"Life", "str":"Str.", "int":"Int.", "agil":"Agi.", "vit":"Vit.", "defense":"Armor Level", "wep":"Weapon Level", "luck":"Luck", "day":"Day", "hrs":"Hours"}
ENEMY_TYPES = [["Peasant"], ["Fighter", "Thief", "Apprentice"], ["Warrior", "Ranger", "Mage"], ["Paladin", "Assassin", "Wizard]"], ["Minotaur", "Ninja", "Archon"], ["Shadow"]]



class Character(object):
	"""Stats and functions for a players Character"""
	def __init__(self, name = ""):
		super(Character, self).__init__()
		self.name = name
		self.lvl = 0
		self.xp = 0
		self.gold = 10
		self.hp = 10
		self.str = 10
		self.int = 10
		self.agil = 10
		self.vit = 10
		self.defense = 1
		self.wep = 1
		self.luck = 0
		self.day = 0
		self.hrs = 10

	def save(self):
		save_file = open('arena.save','w')
		char_dict = self.__dict__
		for key in char_dict.keys():
			save_file.write("%s=%s\n" % (key, char_dict[key]))
		print("Saved!")
		cm()
		save_file.close()

	####
	# STAT MANAGEMENT
	####
	def time_pass(self,hrs = 1):
		self.hrs -= hrs

	def spend_gold(self, cost = 1):
		self.stat("gold", -cost)

	def stat(self, changed_stat, change = 1):
		global PRETTY_STAT
		pass_print = False
		if changed_stat == "hp" and self.hp >= self.vit and change > 0:
			print "Already at max HP"
			pass_print = True
		else:
			if change < 0:
				change_text = "decreased"
				change_val = change * -1
			else:
				change_text = "increased"
				change_val = change

			if changed_stat == "hp" and change < 0:
				self.hp = max(self.hp+change, self.vit)
			else:
				self.__dict__[changed_stat] += change

		if changed_stat == "day":
			pass_print = True

		if not pass_print and changed_stat != "hrs":
			print "%s %s by %s!"%(PRETTY_STAT[changed_stat],change_text,change_val)
		elif changed_stat == "hrs":
			print "%s hour(s) passed!" % change

	def not_dead(self):
		if self.hp > 0:
			return True
		else:
			self.stat("day")
			self.hp = int(self.vit/10)
			self.gold = random.randrange(int(self.gold/2), self.gold)
			self.hrs = random.randrange(1,10)
			print "You have passed out!"
			print "You wake up sometime in town"
			print "It looks like some of your gold is missing"
			cm("town")
			town(self)

	def requires(self, gold = 1, hours = 1, life = 1):
		goldcheck = self.gold < gold
		hourcheck = self.hrs < hours
		lifecheck = self.hp < life

		if goldcheck or hourcheck or lifecheck:
			print "Impossible!"
			if goldcheck:
				print "You need %s gold" % gold
				print "You have %s gold" % self.gold
			if hourcheck:
				print "You neeed %s hours" % hours
				print "There are %s hours left" % self.hrs
			if lifecheck:
				print "You need %s life" % life
				print "You have %s life" % self.hp
			return False
		else:
			return True

	def work(self, base, scale_stat, factor):
		added = int(math.floor(self.__dict__[scale_stat]/factor))
		earned = base + added
		self.spend_gold(-earned)

	####
	# STAT PRINTING
	####

	def print_useful(self, noskip = False):
		if noskip:
			bar1 = 2
		else:
			bar1 = 0
		print_bar(bar1)	
		print "Day:                      %s" % self.day
		print "Time Remaining:           %s hrs" % self.hrs
		print "Life Remaining:           %s hp" % self.hp
		print "Gold Remaining:           %s gold" % self.gold
		print_bar(1)

	def print_stat(self, stats, showtime = True):
		global PRETTY_STAT
		print_bar(0)
		for a_stat in stats:
			text = PRETTY_STAT[a_stat]
			print "%s: %s" % (text, self.__dict__[a_stat])
		if showtime:
			print "Time: %s" % self.hrs
		print_bar(1)


	###
	# GENERIC EVENT
	###

	def event(self, gold_req, time_req, life_req, message, stats, destination, printing = True):
		if self.requires(gold_req, time_req, life_req):
			print message
			self.time_pass(time_req)
			(None, self.spend_gold(gold_req))[gold_req > 0]
			for field,change in stats:
				self.stat(field, change)
			if printing:
				to_print = [a_stat for a_stat,a_val in [("gold",gold_req), ("hrs", time_req), ("hp",life_req)] + stats if a_val > 0]
				# print to_print
				self.print_stat(to_print)
		if self.not_dead():
			cm(destination)
			eval(destination)(self)
		else:
			print "ERROR IN EVENT RETURN: %s" % self


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
	clear()
	return val

#################	
##File management
#################
global NEW_GAME
NEW_GAME = True
def load():
	# global MY_CHAR
	# global DEFAULT_CHAR
	global NEW_GAME
	loaded = False
	try:
		save_file = open('arena.save','r')
		save_text = save_file.read()
		split_file = save_text.split("\n")
		loaded_char = Character()
		valid = True
		if len(split_file)-1 == len(loaded_char.__dict__):
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
				MY_CHAR=loaded_char
				loaded = True
				NEW_GAME = False
		else:
			print "Invalid save file"
			NEW_GAME = True
			cm()

	except NameError, ErrorMessage:
		print ErrorMessage
		print "No save file found"
		NEW_GAME = True
		cm()
	clear()
	if loaded:
		return MY_CHAR
	else:
		return Character()


def save_prompt(character):
	clear()
	print """

  ____                               
 / ___|  __ ___   _____              
 \___ \ / _` \ \ / / _ \             
  ___) | (_| |\ V /  __/             
 |____/ \__,_| \_/ \___|  
 """

	print_bar(0)
	print "Name:  %s" % character.name
	print "Level: %s" % character.lvl
	print "Gold:  %s" % character.gold
	print "Day:   %s" % character.day
	print_bar(1)
	print "Would you like to save?"
	print "Press Q to exit, S to save, E to save and exit, or R to return"
	val = get_val("qsre")

	if "s" == val:
		character.save()
		town(character, False)

	if "e" == val:
		character.save()
		exit()

	if "q" == val:
		exit()

	if "r" == val:
		town(character, False)

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Town

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def town(chracter, refresh = True):
	clear()
	if refresh:
		character.hrs = 16
	print "Welcome to:"
	print """
  _____
 |_   _|____      ___ __             
   | |/ _ \ \ /\ / / '_ \            
   | | (_) \ V  V /| | | |           
   |_|\___/ \_/\_/ |_| |_|  
		"""

	character.print_useful()
	print "Here you can do any of the following:"
	print "Enter the Tavern          (T)"
	print "Go to the Library         (L)"
	print "Go to the Trainng Fields  (F)"
	print "Visit the Blacksmith      (B)" 
	print "Enter the Arena           (A)"
	print "Save and/or exit the game (S)"

	val = get_val("stlfba9")

	if val == "s":
		save_prompt(character)
	elif val == "t":
		tavern(character)
	elif val == "l":
		library(character)
	elif val == "f":
		fields(character)
	elif val == "b":
		smith(character)
	elif val == "a":
		arena(character)
	elif val == "9":
		character.gold += 100
		character.hrs += 100
		character.hp += 100
	else:
		print "ERROR IN TOWN SELECT"
		cm()
	save_prompt(character)


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

def tavern(character):
	clear()
	print "Welcome to the:"
	print """
  _____ 
 |_   _|_ ___   _____ _ __ _ __      
   | |/ _` \ \ / / _ \ '__| '_ \     
   | | (_| |\ V /  __/ |  | | | |    
   |_|\__,_| \_/ \___|_|  |_| |_| 
	"""
	character.print_useful()
	print "Here you can do any of the following:"
	print "Buy a Meal                (M)  1g  1hr"
	print "Grab a Drink              (D)  1g  1hr"
	print "Go to sleep               (S)  --  ---"
	print "Gamble some gold          (G)  1g  1hr"
	print "Bartend                   (B)  --  8hr"	
	print "Return to town            (T)  --  ---"

	val = get_val("mdsgbt")
	clear()
	if val == "m":
		eat(character)
	elif val == "d":
		drink(character)
	elif val == "s":
		sleep(character)
	elif val == "g":
		gamble(character)
	elif val == "b":
		bartend(character)
	elif val == "t":
		town(character, False)
	else:
		print "ERROR IN TAVERN SELECT"
		cm()

def eat(character):
	gold_req, time_req, life_req = 1,1,0
	message = "You order a big steak and devour it\nIt's relieving after a long day"
	heal = int(math.ceil(int(character.vit)/2))
	stats = [("hp", heal)]
	destination = "tavern"
	character.event(gold_req, time_req, life_req, message, stats, destination)

def drink(character):
	gold_req, time_req, life_req = 1,1,1
	message = "You have a drink at the bar\nYou practice some dice and card games"
	hurt = -int(math.ceil(character.vit/10))
	stats = [("hp", hurt),("luck", 1)]
	destination = "tavern"
	character.event(gold_req, time_req, life_req, message, stats, destination)

def sleep(character):
	if character.requires(0, 0, 0):
		print "You sleep for the night"
		heal = int(math.ceil(int(character.vit)/4))
		character.stat("hp", heal)
		character.stat("day")
	cm("town")
	town(character)

def gamble(character):
	if character.requires():
		print "You play a hand of cards"
		chance = random.randint(1+character.luck,1000)
		if chance > 900:
			print 'You win!'
			character.spend_gold(-10)
		else:
			print 'You lose.'
			character.spend_gold()

		character.time_pass(1)
		character.print_stat(["gold"])
	cm("tavern")
	tavern(character)

def bartend(character):
	if character.requires(0,8):
		print "You work at the bar for a few hours"
		character.work(1, "luck", 3)
		character.time_pass(8)
		character.print_stat(["gold"])
	cm("tavern")
	tavern(character)


######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Library

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

def library(character):
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
	character.print_useful(True)
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
		study(character)
	elif val == "b":
		book(character)
	elif val == "h":
		tutor(character)
	elif val == "r":
		read(character)
	elif val == "m":
		magics(character)
	elif val == "t":
		town(character,False)
	else:
		print "ERROR IN LIBRARY SELECT"
		cm()


def study(character):
	if character.requires(0,1):
		print "You spend some time studying battle techniques,"
		print "weapon varience, and the arcane arts."
		character.time_pass()
		character.stat("int")
		character.print_stat(["int"])
	cm("library")
	library(character)

def book(character):
	if character.requires(1,3):
		print "You borrow and read a book of advanced"
		print "fighting and magics"
		character.time_pass(3)
		character.stat("int", 4)
		character.print_stat(["int","gold"])
	cm("library")
	library(character)

def tutor(character):
	if character.requires(3,3):
		print "You have an advanced wizard teach you"
		print "some incredibly difficult magic"
		character.time_pass(3)
		character.stat("int", 7)
		character.print_stat(["int","gold"])
	cm("library")
	library(character)


def read(character):
	if character.requires(0):
		print "You read a nice fiction and rest"
		character.time_pass(1)
		character.stat("hp", 1)
		character.print_stat(["hp"])
	cm("library")
	library(character)

def magics(character):
	if character.requires(0,8):
		print "You work a day teaching magic to others"
		character.work(5, "int", 10)
		character.time_pass(8)
		character.print_stat(["gold"])
	cm("library")
	library(character)

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Training Fields

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################
def fields(character):
	clear()
	print "Welcome to the:"
	print """
  _____        _     _
 |  ___(_) ___| | __| |___           
 | |_  | |/ _ \ |/ _` / __|          
 |  _| | |  __/ | (_| \__ \          
 |_|   |_|\___|_|\__,_|___/         
 """
	character.print_useful()
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
		dummy(character)
	elif val == "m":
		master(character)
	elif val == "c":
		course(character)
	elif val == "r":
		race(character)
	elif val == "s":
		show(character)
	elif val == "t":
		town(character, False)
	else:
		print "ERROR IN FIELDS SELECT"
		cm()


def dummy(character):
	if character.requires(0,2):
		print "You beat up a dummy for a nice work out."
		character.time_pass(2)
		character.stat("str")
		character.print_stat(["str"])
	cm("fields")
	fields(character)

def master(character):
	if character.requires(1,3,1):
		print "You spar a master trainer for some time."
		print "He shows you a thing or two about fighting."
		print "You take a few hits though."
		character.time_pass(3)
		character.stat("str", 6)
		character.stat("hp", -1)
		character.print_stat(["str","hp","gold"])
	if character.not_dead():
		cm("fields")
		fields(character)
	else:
		print "ERROR: broken direct in master()"

def course(character):
	if character.requires(0,2):
		print "You dash through obstacle course for a few hours"
		character.time_pass(2)
		character.stat("agil")
		character.print_stat(["agil"])
	cm("fields")
	fields(character)

def race(character):
	if character.requires(3,1):
		print "You run a race and it really works your muscles."
		character.time_pass(1)
		character.stat("agil", 3)
		character.print_stat(["agil"])
	cm("fields")
	fields(character)

def show(character):
	if character.requires(0,8):
		print "You spend a day performing tricks"
		character.work(3, "agil", 7)
		character.time_pass(8)
		character.print_stat(["gold"])
	cm("fields")
	fields(character)


######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

##Black Smith

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################
def smith(character):
	clear()
	print "Welcome to the:"
	print """
  ____            _ _   _            
 / ___| _ __ ___ (_) |_| |__         
 \___ \| '_ ` _ \| | __| '_ \        
  ___) | | | | | | | |_| | | |       
 |____/|_|_|_| |_|_|\__|_| |_|        
 """
	character.print_useful()
	print "Here you can do any of the following:"
	print "Upgrade your Weapon       (W)  ?g  ---"
	print "Upgrade your Armor        (A)  ?g  ---"
	print "Work the Forge            (F)  --  8hr"
	print "Return to Town            (T)  --  ---"

	val = get_val("waft")

	clear()
	if val == "w":
		wepup(character)
	elif val == "a":
		armup(character)
	elif val == "f":
		forge(character)
	elif val == "t":
		town(character,False)
	else:
		print "ERROR IN FIELDS SELECT"
		cm()


def wepup(character):
	clear()
	cost = int(math.pow(10,character.wep))
	print_bar(0)
	print "Current weapon level:   %s"% character.wep
	print "Current upgrade cost:   %s gold" % cost
	print_bar(1)
	print "Would you like to upgrade your weapon? (y/n)"

	val = get_val("yn")
	clear()
	if val == "y":
		if character.requires(cost, 0):
			print "You upgrade your weapon."
			character.stat("wep")
			character.print_stat(["wep"])
	elif val == "n":
		print "You decide to save upgrading for later"
	cm("smith")
	smith(character)

def armup(character):
	clear()
	cost = int(math.pow(10,character.defense))
	print_bar(0)
	print "Current armor level:    %s"% character.defense
	print "Current upgrade cost:   %s gold" % cost
	print_bar(1)
	print "Would you like to upgrade your armor? (y/n)"

	val = get_val("yn")
	clear()

	if val == "y":
		if character.requires(cost, 0):
			print "You upgrade your armor."
			character.stat("defense")
			character.print_stat(["defense"])
	elif val == "n":
		print "You decide to save upgrading for later"
	cm("smith")
	smith(character)

def forge(character):
	if character.requires(0,8):
		print "You forging weapons and armor"
		character.work(10, "str", 10)
		character.time_pass(8)
		character.print_stat(["gold"])
	cm("smith")
	smith(character)

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################

#     _                         
#    / \   _ __ ___ _ __   __ _ 
#   / _ \ | '__/ _ \ '_ \ / _` |
#  / ___ \| | |  __/ | | | (_| |
# /_/   \_\_|  \___|_| |_|\__,_|         

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################
def arena(character):
	clear()
	print "Welcome to the:"
	print """
     _                         
    / \\   _ __ ___ _ __   __ _ 
   / _ \\ | '__/ _ \\ '_ \\ / _` |
  / ___ \\| | |  __/ | | | (_| |
 /_/   \\_\\_|  \\___|_| |_|\\__,_| 
 """
	character.print_useful()
	print "Here you must either fight or return to town"
	print "Fight!                    (F)  --  1hr"
	print "Return to Town            (T)  --  ---"

	val = get_val("ft")

	clear()
	if val == "f":
		fight(character)
	elif val == "t":
		town(character,False)
	else:
		print "ERROR IN ARENA SELECT"
		cm()

def fight(character):
	if character.requires(0,1):
		character.time_pass(1)
		enemy = make_enemy(pick_diff(character))
		battle(character, enemy)
	cm()
	town(character, False)

def enemy_range(diff, lvl):
	if diff == 1:
		if lvl < 90:
			return 90 - lvl
		else:
			return 0
	elif diff == 3:
		return lvl/5 * 2
	elif diff == 4:
		if lvl > 25:
			return math.floor(lvl/5) * 2 - 10
		else:
			return 0
	elif diff ==5:
		if lvl > 40:
			return lvl/5 * 2 - 20
		else:
			return 0
	elif diff == 6:
		if lvl > 75:
			return lvl/5 * 2 - 30
		else:
			return 0

def pick_diff(character):
	range1 = enemy_range(1, character.lvl)
	range3 = range1 + enemy_range(3, character.lvl)
	range4 = range3 + enemy_range(4, character.lvl)
	range5 = range4 + enemy_range(5, character.lvl)
	range6 = range5 + enemy_range(6, character.lvl)
	pick = random.randint(1,100)
	if pick < range1:
		difficulty = 1  # 1/10
	elif pick < range3:
		difficulty = 3   #3/10
	elif pick < range4:
		difficulty = 4   #4/10
	elif pick < range5:
		difficulty = 5  #5/10
	elif pick < range6:
		difficulty = 6  #10/10
	else:
		difficulty = 2  #2/10
	return difficulty

def make_enemy(diff):
	global ENEMY_TYPES
	return {'type':random.choice(ENEMY_TYPES[diff-1]), 'level': diff, 'hp': diff*1000 }

def battle(character, enemy, message = "\n>"*4):
	battle_display(character, enemy, message)
	val = get_val("ar")
	clear()
	if val == "a":
		enemy, message = attack(character, enemy)
		if character.not_dead():
			battle(character, enemy, message)
		else:
			print "Error in battle"
	elif val == "r":
		town(character, False)
	else:
		print "ERROR IN BATTLE SELECT"

def battle_display(character, enemy, message):
	print "-"*40
	print "Enemy: %s" % enemy['type']
	print "Level: %s" % enemy['level']
	equals = min(int(math.ceil(enemy["hp"]/(enemy['level']*1000.0)*25.0)), 25)
	healthbar = "[" + "="*equals+" "*(25-equals) + "]"
	print "HP: %s" % healthbar
	print "-"*40

	print message
	print_bar(2)
	print "Options:"
	print "Attack!                   (A)"
	print "Run!                      (R)"
	print_bar(2)

	print "\n"
	print "-"*40
	your_equals = min(int(math.ceil(float(character.hp)/character.vit*25.0)), 25)
	your_healthbar = "[" + "="*your_equals+" "*(25-your_equals) + "]"
	print "You:" 
	print "HP: %s %s/%s" % (your_healthbar,character.hp,character.vit)
	print "-"*40

def attack(character, enemy):
	my_damage = damage_calc(character, char = True)
	enemy_damage = damage_calc(enemy, char = False)
	damage_to_me = damage_reduce(character,  enemy_damage, char = True)
	damage_to_enemy = damage_reduce(enemy, my_damage, char = False)
	character.hp -= damage_to_me
	character.hp = max(character.hp,0) #SAFEGAURD AGAINST NEGATIVE HP
	enemy["hp"] -= damage_to_enemy
	enemy["hp"] = max(enemy["hp"], 0)
	message = """
>
> You deal:    %s damage
> Enemy deals: %s damage
> """ % (damage_to_enemy, damage_to_me)
	return enemy, message

def damage_calc(stats, char = True):
	if char:
		##TODO: balance, crits?
		base = int(stats.wep*(5+stats.str+stats.int))
		rand = random.randrange(int(stats.agil),1+int(stats.luck+stats.agil))
		return random.randrange(base, base+rand)
	else:
		base = stats["level"] * 5
		rand = stats["level"] * 2
		return random.randrange(base, base+rand)


def damage_reduce(stats,damage, char = True):
	#TODO: agi = Dodge?
	if char:
		return int(damage-stats.defense)
	else:
		return int(damage)
	

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
	town(character)
else:
	print "Welcome back, %s" % character.name
	cm("Press any key to proceed to Town.....")
	town(False)
