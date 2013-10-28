#!/usr/bin/python
import random, time, os, sys, math
from mygetch import *

# DEFAULT_CHAR = {"name":"", "lvl":0 , "xp":0, "gold":10, "hp":10, "str":10, "int":10, "agil":10, "vit":10, "def":1, "wep":1, "luck":0, "day":0, "hrs": 10}
# MY_CHAR = DEFAULT_CHAR
PRETTY_STAT = {"name":"Name", "lvl":"Lvl." , "xp":"Exp.", "gold":"Gold", "hp":"Life", "str":"Str.", "int":"Int.", "agil":"Agi.", "vit":"Vit.", "def":"Armor Level", "wep":"Weapon Level", "luck":"Luck", "day":"Day"}
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

	def save():
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
	def time_pass(hrs = 1):
		self.hrs -= hrs

	def spend_gold(cost = 1):
		stat("gold", -cost)

	def stat(stat, change = 1):
		global PRETTY_STAT
		pass_print = False
		if stat == "hp" and self.hp >= self.vit and change > 0:
			print "Already at max HP"
			pass_print = True
		else:
			if change < 0:
				change_text = "decreased"
				change_val = change * -1
			else:
				change_text = "increased"
				change_val = change

			if stat == "hp":
				self.hp = max(self.hp+change, self.vit)
			else:
				self.stat += change

		if stat == "day":
			pass_print = True

		if not pass_print:
			print "%s %s by %s!"%(PRETTY_STAT[stat],change_text,change_val)

	def not_dead():
		if self.hp > 0:
			return True
		else:
			stat("day")
			self.hp = int(self.vit/10)
			self.gold = random.randrange(int(self.gold/2), self.gold)
			self.hrs = random.randrange(1,10)
			print "You have passed out!"
			print "You wake up sometime in town"
			print "It looks like some of your gold is missing"
			cm("town")
			town(self)

	def requires(gold = 1, hours = 1, life = 1):
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

	def work(base, stat, factor):
		added = int(math.floor(self.stat/factor))
		earned = base + added
		spend_gold(-earned)

	####
	# STAT PRINTING
	####

	def print_useful(noskip = False):
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

	def print_stat(stats, showtime = True):
		global PRETTY_STAT
		print_bar(0)
		for stat in stats:
			text = PRETTY_STAT[stat]
			print "%s: %s" % (text, self.stat)
		if showtime:
			print "Time: %s" % self.hrs
		print_bar(1)

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
				if "=" in line and line != "":
					values = line.split("=")
					if values[0] in Character().__dict__.keys():
						this_val = values[1]
						if values[0] != "name":
							this_val = int(values[1])
						loaded_char.values[0] = this_val
					else:
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

	except Exception, ErrorMessage:
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
	def greeting():
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

	greeting()
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
		town(False)
	else:
		print "ERROR IN TAVERN SELECT"
		cm()


def eat(character):
	if requires():
		print "You order a big steak and devour it"
		print "It's relieving after a long day"
		heal = int(math.ceil(int(character.vit)/2))
		character.stat("hp", heal)
		character.spend_gold()
		character.time_pass()
		character.print_stat(["hp","gold"])
	cm("tavern")
	tavern(character)

def drink(character):
	if requires(1, 1, 1):
		print "You ask the bartender for a drink"
		print "and drink it up in one gulp."
		print "It's a little rough on the stomach,"
		print "but you feel a little bit luckier"
		hurt = -int(math.ceil(character.vit/10))
		character.stat("hp", hurt)
		character.stat("luck")
		character.spend_gold()
		character.time_pass()
		character.print_stat(["hp","luck", "gold"])
	if character.not_dead():
		cm("tavern")
		tavern(character)
	else:
		print "ERROR: broken direct in drink"

def sleep():
	if requires(0, 0, 0):
		global MY_CHAR
		print "You sleep for the night"
		heal = int(math.ceil(int(character.vit)/4))
		character.stat("hp", heal)
		character.stat("day")
		# print_stat(["hp"])
		# print_stat(["day"])
	cm("town")
	town(character)
	
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
		print "ERROR IN LIBRARY SELECT"
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
	if not_dead():
		cm("fields")
		fields()
	else:
		print "ERROR: broken direct in master()"

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

##Black Smith

######################################
## @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
######################################
def smith():
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
		wepup()
	elif val == "a":
		armup()
	elif val == "f":
		forge()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN FIELDS SELECT"
		cm()


def wepup():
	global MY_CHAR
	clear()
	cost = int(math.pow(10,MY_CHAR["wep"]))
	print_bar(0)
	print "Current weapon level:   %s"% MY_CHAR["wep"]
	print "Current upgrade cost:   %s gold" % cost
	print_bar(1)
	print "Would you like to upgrade your weapon? (y/n)"

	val = get_val("yn")
	clear()
	if val == "y":
		if requires(cost, 0):
			print "You upgrade your weapon."
			stat("wep")
			print_stat(["wep"])
	elif val == "n":
		print "You decide to save upgrading for later"
	cm("smith")
	smith()

def armup():
	global MY_CHAR
	clear()
	cost = int(math.pow(10,MY_CHAR["def"]))
	print_bar(0)
	print "Current armor level:    %s"% MY_CHAR["def"]
	print "Current upgrade cost:   %sgold" % cost
	print_bar(1)
	print "Would you like to upgrade your armor? (y/n)"

	val = get_val("yn")
	clear()

	if val == "y":
		if requires(cost, 0):
			print "You upgrade your armor."
			stat("def")
			print_stat(["def"])
	elif val == "n":
		print "You decide to save upgrading for later"
	cm("smith")
	smith()

def forge():
	if requires(0,8):
		global MY_CHAR
		print "You spend a day performing tricks"
		work(10, "str", 10)
		time_pass(8)
		print_stat(["gold"])
	cm("smith")
	smith()

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
def arena():
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
		fight()
	elif val == "t":
		town(False)
	else:
		print "ERROR IN ARENA SELECT"
		cm()

def fight():
	if requires(0,1):
		time_pass(1)
		enemy = make_enemy(pick_diff())
		battle(enemy)
	cm()
	town(False)

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

def pick_diff():
	global MY_CHAR
	range1 = enemy_range(1, MY_CHAR["lvl"])
	range3 = range1 + enemy_range(3, MY_CHAR["lvl"])
	range4 = range3 + enemy_range(4, MY_CHAR["lvl"])
	range5 = range4 + enemy_range(5, MY_CHAR["lvl"])
	range6 = range5 + enemy_range(6, MY_CHAR["lvl"])
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

def battle(enemy, message = "\n>"*4):
	global MY_CHAR
	battle_display(enemy, message)
	val = get_val("ar")
	clear()
	if val == "a":
		enemy, message = attack(enemy)
		if not_dead():
			battle(enemy, message)
		else:
			print "Error in battle"
	elif val == "r":
		town(False)
	else:
		print "ERROR IN BATTLE SELECT"

def battle_display(enemy, message):
	global MY_CHAR
	print "-"*40
	print "Enemy: %s" % enemy['type']
	print "Level: %s" % enemy['level']
	equals = int(math.ceil(enemy["hp"]/(enemy['level']*1000.0)*25.0))
	print equals
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
	your_equals = int(math.ceil(float(MY_CHAR["hp"])/MY_CHAR["vit"]*25.0))
	your_healthbar = "[" + "="*your_equals+" "*(25-your_equals) + "]"
	print "You:" 
	print "HP: %s %s/%s" % (your_healthbar,MY_CHAR["hp"],MY_CHAR["vit"])
	print "-"*40

def attack(enemy):
	pass
	global MY_CHAR
	my_damage = damage_calc(MY_CHAR, char = True)
	enemy_damage = damage_calc(enemy, char = False)
	damage_to_me = damage_reduce(MY_CHAR,  enemy_damage, char = True)
	damage_to_enemy = damage_reduce(enemy, my_damage, char = False)
	MY_CHAR["hp"] -= damage_to_me
	MY_CHAR["hp"] = max(MY_CHAR["hp"],0) #SAFEGAURD AGAINST NEGATIVE HP
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
		base = int(stats["wep"]*(5+stats["str"]+stats["int"]))
		rand = random.randrange(int(stats["agil"]),1+int(stats["luck"]+stats["agil"]))
		return random.randrange(base, base+rand)
	else:
		base = stats["level"] * 5
		rand = stats["level"] * 2
		return random.randrange(base, base+rand)


def damage_reduce(stats,damage, char = True):
	#TODO: agi = Dodge?
	if char:
		return int(damage-stats["def"])
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
	town()
else:
	print "Welcome back, %s" % MY_CHAR["name"]
	cm("Press any key to proceed to Town.....")
	town(False)
