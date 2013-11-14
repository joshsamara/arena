import random
import time
import math
from .common import *


class Character(object):

    """Stats and functions for a players Character"""

    def __init__(self, name=""):
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
        save_file = open('save/arena.save', 'w')
        char_dict = self.__dict__
        for key in char_dict.keys():
            save_file.write("%s=%s\n" % (key, char_dict[key]))
        print("Saved!")
        cm()
        save_file.close()

    #
    # STAT MANAGEMENT
    #
    def time_pass(self, hrs=1):
        self.hrs -= hrs

    def spend_gold(self, cost=1):
        self.stat("gold", -cost)

    def stat(self, changed_stat, change=1):
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
                self.hp = max(self.hp + change, self.vit)
            else:
                self.__dict__[changed_stat] += change

        if changed_stat == "day":
            pass_print = True

        if not pass_print and changed_stat != "hrs":
            print "%s %s by %s!" % (PRETTY_STAT[changed_stat],
                                    change_text, change_val)
        elif changed_stat == "hrs":
            print "%s hour(s) passed!" % change

    def not_dead(self):
        if self.hp > 0:
            return True
        else:
            self.stat("day")
            self.hp = int(self.vit / 10)
            self.gold = random.randrange(int(self.gold / 2), self.gold)
            self.hrs = random.randrange(1, 10)
            print "You have passed out!"
            print "You wake up sometime in town"
            print "It looks like some of your gold is missing"
            cm("town")
            town(self)

    def requires(self, gold=1, hours=1, life=1):
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
        added = int(math.floor(self.__dict__[scale_stat] / factor))
        earned = base + added
        self.spend_gold(-earned)

    #
    # STAT PRINTING
    #

    def print_useful(self, noskip=False):
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

    def print_stat(self, stats, showtime=True):
        global PRETTY_STAT
        print_bar(0)
        for a_stat in stats:
            text = PRETTY_STAT[a_stat]
            print "%s: %s" % (text, self.__dict__[a_stat])
        if showtime:
            print "Time: %s" % self.hrs
        print_bar(1)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
    #
    # GENERIC EVENT TEMPLATE
    #
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
    def event(self, gold_req, time_req, life_req, message,
              stats, destination, printing=True):
        if self.requires(gold_req, time_req, life_req):
            print message
            self.time_pass(time_req)
            (None, self.spend_gold(gold_req))[gold_req > 0]
            for field, change in stats:
                self.stat(field, change)
            if printing:
                possibs = [("gold", gold_req),
                           ("hrs", time_req),
                           ("hp", life_req)]
                to_print = [s for s, val in possibs + stats if val > 0]
                # print to_print
                self.print_stat(to_print)
        if self.not_dead():
            cm(destination)
            # TODO: FIX THIS. WHO DOES THIS.
            eval("self." + destination + "()")
        else:
            print "ERROR IN EVENT RETURN: %s" % self

    # @@@@@@@@@@@@@@@@@@@@@@@@@
    #
    # Events
    #
    # @@@@@@@@@@@@@@@@@@@@@@@@@

    def save_prompt(self):
        clear()
        print """

  ____
 / ___|  __ ___   _____
 \___ \ / _` \ \ / / _ \
  ___) | (_| |\ V /  __/
 |____/ \__,_| \_/ \___|
"""

        print_bar(0)
        print "Name:  %s" % self.name
        print "Level: %s" % self.lvl
        print "Gold:  %s" % self.gold
        print "Day:   %s" % self.day
        print_bar(1)
        print "Would you like to save?"
        print "Press Q to exit, S to save, E to save and exit, or R to return"
        val = get_val("qsre")

        if "s" == val:
            self.save()
            self.town(False)

        if "e" == val:
            self.save()
            exit()

        if "q" == val:
            exit()

        if "r" == val:
            self.town(False)

    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    # Town
    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    def town(self, refresh=True):
        clear()
        if refresh:
            self.hrs = 16
        print "Welcome to:"
        print """
  _____
 |_   _|____      ___ __
   | |/ _ \ \ /\ / / '_ \
   | | (_) \ V  V /| | | |
   |_|\___/ \_/\_/ |_| |_|
"""

        self.print_useful()
        print "Here you can do any of the following:"
        print "Enter the Tavern          (T)"
        print "Go to the Library         (L)"
        print "Go to the Trainng Fields  (F)"
        print "Visit the Blacksmith      (B)"
        print "Enter the Arena           (A)"
        print "Save and/or exit the game (S)"

        val = get_val("stlfba9")

        if val == "s":
            self.save_prompt()
        elif val == "t":
            self.tavern()
        elif val == "l":
            self.library()
        elif val == "f":
            self.fields()
        elif val == "b":
            self.smith()
        elif val == "a":
            self.arena()
        elif val == "9":
            self.gold += 100
            self.hrs += 100
            self.hp += 100
        else:
            print "ERROR IN TOWN SELECT"
            cm()
        self.save_prompt()

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    # Tavern
    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    def tavern(self):
        clear()
        print "Welcome to the:"
        print """
  _____
 |_   _|_ ___   _____ _ __ _ __
   | |/ _` \ \ / / _ \ '__| '_ \
   | | (_| |\ V /  __/ |  | | | |
   |_|\__,_| \_/ \___|_|  |_| |_|
"""
        self.print_useful()
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
            self.eat()
        elif val == "d":
            self.drink()
        elif val == "s":
            self.sleep()
        elif val == "g":
            self.gamble()
        elif val == "b":
            self.bartend()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN TAVERN SELECT"
            cm()

    def eat(self):
        gold_req, time_req, life_req = 1, 1, 0
        message = """You order a big steak and devour it
It's relieving after a long day"""
        heal = int(math.ceil(int(self.vit) / 2))
        stats = [("hp", heal)]
        destination = "tavern"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def drink(self):
        gold_req, time_req, life_req = 1, 1, 1
        message = """You have a drink at the bar
You practice some dice and card games"""
        hurt = -int(math.ceil(self.vit / 10))
        stats = [("hp", hurt), ("luck", 1)]
        destination = "tavern"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def sleep(self):
        if self.requires(0, 0, 0):
            print "You sleep for the night"
            heal = int(math.ceil(int(self.vit) / 4))
            self.stat("hp", heal)
            self.stat("day")
        cm("town")
        self.town()

    def gamble(self):
        if self.requires():
            print "You play a hand of cards"
            chance = random.randint(1 + self.luck, 1000)
            if chance > 900:
                print 'You win!'
                self.spend_gold(-10)
            else:
                print 'You lose.'
                self.spend_gold()
            self.time_pass(1)
            self.print_stat(["gold"])
        cm("tavern")
        self.tavern()

    def bartend(self):
        if self.requires(0, 8):
            print "You work at the bar for a few hours"
            self.work(1, "luck", 3)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("tavern")
        self.tavern()

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    # Library
    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    def library(self):
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
        self.print_useful(True)
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
            self.study()
        elif val == "b":
            self.book()
        elif val == "h":
            self.tutor()
        elif val == "r":
            self.read()
        elif val == "m":
            self.magics()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN LIBRARY SELECT"
            cm()

    def study(self):
        gold_req, time_req, life_req = 0, 1, 0
        message = """You spend some time studying battle techniques,
and the arcane arts."""
        stats = [("int", 1)]
        destination = "library"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def book(self):
        gold_req, time_req, life_req = 1, 3, 0
        message = "You borrow and read a book of advanced\nfighting and magics"
        stats = [("int", 4)]
        destination = "library"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def tutor(self):
        gold_req, time_req, life_req = 3, 3, 0
        message = """You have an advanced wizard teach you
some incredibly difficult magic"""
        stats = [("int", 7)]
        destination = "library"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def read(self):
        gold_req, time_req, life_req = 0, 1, 0
        message = "You read a nice fiction book and rest"
        heal = int(math.ceil(int(self.vit) / 10))
        stats = [("hp", heal)]
        destination = "library"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def magics(self):
        if self.requires(0, 8):
            print "You work a day teaching magic to others"
            self.work(5, "int", 10)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("library")
        library(self)

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #

    # Training Fields

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #

    def fields(self):
        clear()
        print "Welcome to the:"
        print """
      _____        _     _
     |  ___(_) ___| | __| |___
     | |_  | |/ _ \ |/ _` / __|
     |  _| | |  __/ | (_| \__ \
     |_|   |_|\___|_|\__,_|___/
"""
        self.print_useful()
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
            self.dummy()
        elif val == "m":
            self.master()
        elif val == "c":
            self.course()
        elif val == "r":
            self.race()
        elif val == "s":
            self.show()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN FIELDS SELECT"
            cm()

    def dummy(self):
        gold_req, time_req, life_req = 0, 2, 0
        message = "You beat up a dummy for a nice work out."
        stats = [("str", 1)]
        destination = "fields"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def master(self):
        gold_req, time_req, life_req = 1, 3, 1
        message = """You spar a master trainer for some time.
He shows you a thing or two about fighting.
You take a few hits though."""
        stats = [("str", 6)]
        destination = "fields"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def course(self):
        gold_req, time_req, life_req = 0, 2, 0
        message = "You dash through obstacle course for a few hours"
        stats = [("agil", 1)]
        destination = "fields"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def race(self):
        gold_req, time_req, life_req = 3, 1, 0
        message = "You run a race and it really works your muscles."
        stats = [("agil", 3)]
        destination = "fields"
        self.event(gold_req, time_req, life_req, message, stats, destination)

    def show(self):
        if self.requires(0, 8):
            print "You spend a day performing tricks"
            self.work(3, "agil", 7)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("fields")
        fields(self)

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    # Black Smith
    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    def smith(self):
        clear()
        print "Welcome to the:"
        print """
      ____            _ _   _
     / ___| _ __ ___ (_) |_| |__
     \___ \| '_ ` _ \| | __| '_ \
      ___) | | | | | | | |_| | | |
     |____/|_|_|_| |_|_|\__|_| |_|
     """
        self.print_useful()
        print "Here you can do any of the following:"
        print "Upgrade your Weapon       (W)  ?g  ---"
        print "Upgrade your Armor        (A)  ?g  ---"
        print "Work the Forge            (F)  --  8hr"
        print "Return to Town            (T)  --  ---"

        val = get_val("waft")

        clear()
        if val == "w":
            self.wepup()
        elif val == "a":
            self.armup()
        elif val == "f":
            self.forge()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN FIELDS SELECT"
            cm()

    def wepup(self):
        clear()
        cost = int(math.pow(10, self.wep))
        print_bar(0)
        print "Current weapon level:   %s" % self.wep
        print "Current upgrade cost:   %s gold" % cost
        print_bar(1)
        print "Would you like to upgrade your weapon? (y/n)"

        val = get_val("yn")
        clear()
        if val == "y":
            if self.requires(cost, 0):
                print "You upgrade your weapon."
                self.stat("wep")
                self.print_stat(["wep"])
        elif val == "n":
            print "You decide to save upgrading for later"
        cm("smith")
        smith(self)

    def armup(self):
        clear()
        cost = int(math.pow(10, self.defense))
        print_bar(0)
        print "Current armor level:    %s" % self.defense
        print "Current upgrade cost:   %s gold" % cost
        print_bar(1)
        print "Would you like to upgrade your armor? (y/n)"

        val = get_val("yn")
        clear()

        if val == "y":
            if self.requires(cost, 0):
                print "You upgrade your armor."
                self.stat("defense")
                self.print_stat(["defense"])
        elif val == "n":
            print "You decide to save upgrading for later"
        cm("smith")
        smith(self)

    def forge(self):
        if self.requires(0, 8):
            print "You forging weapons and armor"
            self.work(10, "str", 10)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("smith")
        smith(self)

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #

    #     _
    #    / \   _ __ ___ _ __   __ _
    #   / _ \ | '__/ _ \ '_ \ / _` |
    #  / ___ \| | |  __/ | | | (_| |
    # /_/   \_\_|  \___|_| |_|\__, _|

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #

    def arena(self):
        clear()
        print "Welcome to the:"
        print """
         _
        / \\   _ __ ___ _ __   __ _
       / _ \\ | '__/ _ \\ '_ \\ / _` |
      / ___ \\| | |  __/ | | | (_| |
     /_/   \\_\\_|  \\___|_| |_|\\__,_|
     """
        self.print_useful()
        print "Here you must either fight or return to town"
        print "Fight!                    (F)  --  1hr"
        print "Return to Town            (T)  --  ---"

        val = get_val("ft")

        clear()
        if val == "f":
            self.fight()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN ARENA SELECT"
            cm()

    def fight(self):
        if self.requires(0, 1):
            self.time_pass(1)
            enemy = make_enemy(pick_diff(self))
            battle(self, enemy)
        cm()
        self.town(False)

    def enemy_range(diff, lvl):
        if diff == 1:
            if lvl < 90:
                return 90 - lvl
            else:
                return 0
        elif diff == 3:
            return lvl / 5 * 2
        elif diff == 4:
            if lvl > 25:
                return math.floor(lvl / 5) * 2 - 10
            else:
                return 0
        elif diff == 5:
            if lvl > 40:
                return lvl / 5 * 2 - 20
            else:
                return 0
        elif diff == 6:
            if lvl > 75:
                return lvl / 5 * 2 - 30
            else:
                return 0

    def pick_diff(self):
        range1 = enemy_range(1, self.lvl)
        range3 = range1 + enemy_range(3, self.lvl)
        range4 = range3 + enemy_range(4, self.lvl)
        range5 = range4 + enemy_range(5, self.lvl)
        range6 = range5 + enemy_range(6, self.lvl)
        pick = random.randint(1, 100)
        if pick < range1:
            difficulty = 1  # 1/10
        elif pick < range3:
            difficulty = 3  # 3/10
        elif pick < range4:
            difficulty = 4  # 4/10
        elif pick < range5:
            difficulty = 5  # 5/10
        elif pick < range6:
            difficulty = 6  # 10/10
        else:
            difficulty = 2  # 2/10
        return difficulty

    def make_enemy(diff):
        global ENEMY_TYPES
        return (
            {'type': random.choice(
                ENEMY_TYPES[diff - 1]),
                'level': diff,
                'hp': diff * 1000}
        )

    def battle(self, enemy, message="\n>" * 4):
        battle_display(self, enemy, message)
        val = get_val("ar")
        clear()
        if val == "a":
            enemy, message = attack(self, enemy)
            if self.not_dead():
                battle(self, enemy, message)
            else:
                print "Error in battle"
        elif val == "r":
            self.town(False)
        else:
            print "ERROR IN BATTLE SELECT"

    def battle_display(self, enemy, message):
        print "-" * 40
        print "Enemy: %s" % enemy['type']
        print "Level: %s" % enemy['level']
        equals = min(
            int(math.ceil(enemy["hp"] / (enemy['level'] * 1000.0) * 25.0)),
            25)
        healthbar = "[" + "=" * equals + " " * (25 - equals) + "]"
        print "HP: %s" % healthbar
        print "-" * 40

        print message
        print_bar(2)
        print "Options:"
        print "Attack!                   (A)"
        print "Run!                      (R)"
        print_bar(2)

        print "\n"
        print "-" * 40
        your_equals = min(
            int(math.ceil(float(self.hp) / self.vit * 25.0)),
            25)
        your_healthbar = "[" + "=" * your_equals + \
            " " * (25 - your_equals) + "]"
        print "You:"
        print "HP: %s %s/%s" % (your_healthbar, self.hp, self.vit)
        print "-" * 40

    def attack(self, enemy):
        my_damage = damage_calc(self, char=True)
        enemy_damage = damage_calc(enemy, char=False)
        damage_to_me = damage_reduce(self, enemy_damage, char=True)
        damage_to_enemy = damage_reduce(enemy, my_damage, char=False)
        self.hp -= damage_to_me
        self.hp = max(self.hp, 0)  # SAFEGAURD AGAINST NEGATIVE HP
        enemy["hp"] -= damage_to_enemy
        enemy["hp"] = max(enemy["hp"], 0)
        message = """
    >
    > You deal:    %s damage
    > Enemy deals: %s damage
    > """ % (damage_to_enemy, damage_to_me)
        return enemy, message

    def damage_calc(stats, char=True):
        if char:
            # TODO: balance, crits?
            base = int(stats.wep * (5 + stats.str + stats.int))
            rand = random.randrange(
                int(stats.agil),
                1 + int(stats.luck + stats.agil))
            return random.randrange(base, base + rand)
        else:
            base = stats["level"] * 5
            rand = stats["level"] * 2
            return random.randrange(base, base + rand)

    def damage_reduce(stats, damage, char=True):
        # TODO: agi = Dodge?
        if char:
            return int(damage - stats.defense)
        else:
            return int(damage)
