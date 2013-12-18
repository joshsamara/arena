import time
import math
import events
import pickle
from common import *
from fight import *


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
        pickle.dump(self, save_file)
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
        if changed_stat == "hp" and self.hp + change >= self.vit:
            self.hp = self.vit
            print color("Already at max HP", "blue")
            pass_print = True
        else:
            if change < 0:
                to_color = "red"
                change_text = "decreased"
                change_val = change * -1
            else:
                to_color = "green"
                change_text = "increased"
                change_val = change

            if changed_stat == "hp" and change < 0:
                self.hp = max(self.hp + change, 0)
            else:
                self.__dict__[changed_stat] += change

        if changed_stat == "day":
            pass_print = True

        if not pass_print and changed_stat != "hrs":
            print color("%s %s by %s!",to_color) % (PRETTY_STAT[changed_stat],
                                    change_text, change_val)
        elif changed_stat == "hrs":
            print color("%s hour(s) passed!", "red") % change

    def not_dead(self):
        if self.hp > 0:
            return True
        else:
            self.stat("day")
            self.hp = int(self.vit / 10)
            self.gold = random.randint(int(self.gold / 2), self.gold)
            self.hrs = random.randint(1, 10)
            print color("You have passed out!", "red")
            print "You wake up sometime in town"
            print "It looks like some of your gold is missing"
            cm("town")
            self.town()

    def requires(self, gold=1, hours=1, life=1):
        goldcheck = self.gold < gold
        hourcheck = self.hrs < hours
        lifecheck = self.hp < life

        if goldcheck or hourcheck or lifecheck:
            print "Impossible!"
            if goldcheck:
                print color("You need %s gold","red") % gold
                print "You have %s gold" % self.gold
            if hourcheck:
                print color("You neeed %s hours","red") % hours
                print "There are %s hours left" % self.hrs
            if lifecheck:
                print color("You need %s life", "red") % life
                print "You have %s life" % self.hp
            return False
        else:
            return True

    def calc_needed_xp(self, lvl = None):
        # return i * i + 10 * i + 25 + (self.lvl * self.lvl + 10 * self.lvl + 25)
        # 2*lvl^2 + 22*lvl + 61 (simplified)
        if lvl == None:
            lvl = self.lvl

        if lvl < 0:
            return 0
        else:
            return 2 * math.pow(lvl, 2) + 22 * lvl + 61 

    def check_lvlup(self):
        # A1*A1 +10*A1 + 25
        i = self.lvl + 1
        needed =  self.calc_needed_xp()
        # print needed   print some sort of bar here 
        if self.xp >= needed:
            self.lvl = i
            print color("Your level has increased to %d!","green") % i
            for aStat in ["str", "int", "agil", "luck", "vit"]:
                self.stat(aStat, random.randint(3,10))
                #add a little randomness to leveling for kicks
        else:
            pass

    def xp_perc(self):
        this_lvl = self.xp - self.calc_needed_xp(self.lvl - 1)
        next_lvl = self.calc_needed_xp() - self.calc_needed_xp(self.lvl - 1)
        return int(100 * this_lvl/next_lvl)

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

#$: XXXXXX  TIME: XXX  LIFE: XXX/XXX
#STR:  XXX  AGI:  XXX  INT:  XXX
#LCK:  XXX  WEP:  XXX  DEF:  XXX
#DAY:  XXX  EXP:  XXX  LVL:  XXX
        to_print = """$: %s  TIME: %s  LIFE: %s/%-3d
STR:  %3d  AGI:  %3d  INT:  %3d
LCK:  %3d  WEP:  %3d  DEF:  %3d
DAY:  %3d  EXP:  %2d%%  LVL:  %3d"""

        money_print = color("%6d" % self.gold, "yellow")
        time_print =  color("%3d" % self.hrs, "teal")
        life_print =  color("%3d"  % self.hp, "pink")
        text_fill = (money_print, time_print, life_print, self.vit,
                     self.str,  self.agil, self.int,
                     self.luck, self.wep,  self.defense,
                     self.day,  self.xp_perc(),   self.lvl)
        print to_print % text_fill
        # print "Day:                      %s" % self.day
        # print "Time Remaining:           %s hrs" % self.hrs
        # print "Life Remaining:           %s hp" % self.hp
        # print "Gold Remaining:           %s gold" % self.gold
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
    def run_event(self, anEvent):
        if self.requires(anEvent.gold_req, anEvent.time_req, anEvent.life_req):
            anEvent.run_process(self)
            print anEvent.message
            self.time_pass(anEvent.time_req)
            if anEvent.gold_req > 0:
                self.spend_gold(anEvent.gold_req)
            for field, change in anEvent.stats:
                if field != "hp":
                    minVal = math.fabs(change)
                    toChange = random.randint(minVal, minVal * 2)
                    if change < 0: toChange = -toChange
                else:
                    toChange = change
                self.stat(field, toChange) #MORE RANDOM!
            if anEvent.printing:
                possibs = [("gold", anEvent.gold_req),
                           ("hrs", anEvent.time_req),
                           ("hp", anEvent.life_req)]
                to_print = [s for s, val in possibs + anEvent.stats if val > 0]
                # print to_print
                self.print_stat(to_print)
        if self.not_dead():
            cm(anEvent.destination)
            # TODO: FIX THIS. WHO DOES THIS.
            eval("self." + anEvent.destination + "()")
        else:
            print "ERROR IN EVENT RETURN: %s" % self

    # @@@@@@@@@@@@@@@@@@@@@@@@@
    #
    # Events
    #
    # @@@@@@@@@@@@@@@@@@@@@@@@@

    def save_prompt(self):
        clear()
        print color("""

  ____
 / ___|  __ ___   _____
 \___ \ / _` \ \ / / _ \\
  ___) | (_| |\ V /  __/
 |____/ \__,_| \_/ \___|
""", "pink")

        print_bar(0)
        print "Name:  %s" % self.name
        self.print_useful(True)
        save_options = [make_option('Save', 'S'),
                        make_option('Save and Exit', 'E'),
                        make_option('Quit', 'Q'),
                        make_option('Return', 'R')]

        print nav_menu(save_options, short=True)
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

    #
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
        print """Welcome to:

  _____
 |_   _|____      ___ __
   | |/ _ \ \ /\ / / '_ \\
   | | (_) \ V  V /| | | |
   |_|\___/ \_/\_/ |_| |_|
"""

        self.print_useful()
        town_options = [make_option('Enter the Tavern', 'T'),
                        make_option('Go to the Library', 'L'),
                        make_option('Go to the Trainng Fields', 'F'),
                        make_option('Visit the Blacksmith', 'B'),
                        make_option('Enter the Arena', 'A'),
                        make_option('Save and/or exit the game', 'S')]         
        print nav_menu(town_options, short=True)
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
        print color("""
  _____
 |_   _|_ ___   _____ _ __ _ __
   | |/ _` \ \ / / _ \ '__| '_ \\
   | | (_| |\ V /  __/ |  | | | |
   |_|\__,_| \_/ \___|_|  |_| |_|
""", "yellow")

        self.print_useful()

        tavern_options = [make_option('Buy a Meal', 'M', gold=1, time=1),
                          make_option('Grab a Drink', 'D', gold=1, time=1, hp=1),
                          make_option('Go to Sleep', 'S'),
                          make_option('Gamble some gold', 'G', gold=1, time=1),
                          make_option('Bartend', 'B', time = 8),
                          make_option('Return to Town', 'T')]
        print nav_menu(tavern_options)

        val = get_val("mdsgbt")
        clear()
        if val == "m":
            self.run_event(events.tavern.EAT)
        elif val == "d":
            self.run_event(events.tavern.DRINK)
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
        print color("""
  _       _
 | |   (_) |__  _ __ __ _ _ __ _   _
 | |   | | '_ \| '__/ _` | '__| | | |
 | |___| | |_) | | | (_| | |  | |_| |
 |_____|_|_.__/|_|  \__,_|_|   \__, |
                                |___/
""", "teal")


        self.print_useful(True)
        library_options = [make_option('Study Magics', 'S', time=1),
                           make_option('Borrow a book', 'B', gold=1, time=3),
                           make_option('Hire a tutor', 'H', gold=3, time=3),
                           make_option('Read and relax', 'R', time=1),
                           make_option('Tutor Magics', 'M', time = 8),
                           make_option('Return to Town', 'T')]
        print nav_menu(library_options)


        val = get_val("sbhrmt")
        clear()
        if val == "s":
            self.run_event(events.library.STUDY)
        elif val == "b":
            self.run_event(events.library.BOOK)
        elif val == "h":
            self.run_event(events.library.TUTOR)
        elif val == "r":
            self.run_event(events.library.READ)
        elif val == "m":
            self.magics()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN LIBRARY SELECT"
            cm()

    def magics(self):
        if self.requires(0, 8):
            print "You work a day teaching magic to others"
            self.work(5, "int", 10)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("library")
        self.library()

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
        print color("""
  _____        _     _
 |  ___(_) ___| | __| |___
 | |_  | |/ _ \ |/ _` / __|
 |  _| | |  __/ | (_| \__ \\
 |_|   |_|\___|_|\__,_|___/
""", "green")
        self.print_useful()

        field_options = [make_option('Fight a training Dummy','D', time=2),
                         make_option('Spar a Battle Master',  'M', gold=1, time=3, hp=1),
                         make_option('Run an obstacle Course','C', time=2),
                         make_option('Enter a Race',          'R', gold=3, time=1),
                         make_option('Perform Show tricks',   'S', time = 8),
                         make_option('Return to Town',        'T')]
        print nav_menu(field_options)

        val = get_val("dmcrst")

        clear()
        if val == "d":
            self.run_event(events.fields.DUMMY)
        elif val == "m":
            self.run_event(events.fields.MASTER)
        elif val == "c":
            self.run_event(events.fields.COURSE)
        elif val == "r":
            self.run_event(events.fields.RACE)
        elif val == "s":
            self.show()
        elif val == "t":
            self.town(False)
        else:
            print "ERROR IN FIELDS SELECT"
            cm()

    def show(self):
        if self.requires(0, 8):
            print "You spend a day performing tricks"
            self.work(3, "agil", 7)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("fields")
        self.fields()

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
        print color("""
  ____            _ _   _
 / ___| _ __ ___ (_) |_| |__
 \___ \| '_ ` _ \| | __| '_ \\
  ___) | | | | | | | |_| | | |
 |____/|_|_|_| |_|_|\__|_| |_|
 """, "blue")
        self.print_useful()

        smith_options = [make_option('Upgrade your Weapon', 'W', gold='?'),
                         make_option('Upgrade your Armor ', 'A', gold='?'),
                         make_option('Mine ores', 'M', time = 4),
                         make_option('Work the Forge', 'F', time = 8),
                         make_option('Return to Town', 'T')]

        print nav_menu(smith_options)
        val = get_val("wamft")

        clear()
        if val == "w":
            self.wepup()
        elif val == "a":
            self.armup()
        elif val == "m":
            self.run_event(events.smith.MINE)
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
        print "Current gold        :   %s gold" % self.gold
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
        self.smith()

    def armup(self):
        clear()
        cost = int(math.pow(10, self.defense))
        print_bar(0)
        print "Current armor level:    %s" % self.defense
        print "Current upgrade cost:   %s gold" % cost
        print "Current gold        :   %s gold" % self.gold
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
        self.smith()

    def forge(self):
        if self.requires(0, 8):
            print "You forging weapons and armor"
            self.work(10, "str", 10)
            self.time_pass(8)
            self.print_stat(["gold"])
        cm("smith")
        self.smith()

    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #
    #     _
    #    / \   _ __ ___ _ __   __ _
    #   / _ \ | '__/ _ \ '_ \ / _` |
    #  / ___ \| | |  __/ | | | (_| |
    # /_/   \_\_|  \___|_| |_|\__,_|
    #
    # @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @
    #

    def arena(self):
        clear()
        print "Welcome to the:"
        print color("""
     _
    / \\   _ __ ___ _ __   __ _
   / _ \\ | '__/ _ \\ '_ \\ / _` |
  / ___ \\| | |  __/ | | | (_| |
 /_/   \\_\\_|  \\___|_| |_|\\__,_|
 """, "red")
        self.print_useful()
        arena_options = [make_option('Fight!', 'F', time=1, hp='?'),
                         make_option('Return to Town', 'T')]

        print nav_menu(arena_options)

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
            enemy = Enemy(pick_diff(self.lvl))
            self.battle(enemy)
        cm()
        self.town(False)

    def victory(self, enemy):
        print "You win!"
        self.stat("xp", enemy.calc_exp())
        self.stat("gold", enemy.calc_gold())
        self.check_lvlup()
        cm("town")
        self.town(False)

    def battle(self, enemy, message="\n>" * 4):
        self.battle_display(enemy, message)
        val = get_val("ar")
        clear()
        if val == "a":
            enemy, message = self.attack(enemy)
            if self.not_dead():
                if enemy.not_dead():
                    self.battle(enemy, message)
                else:
                    self.victory(enemy)
            else:
                print "Error in battle"
        elif val == "r":
            self.town(False)
        else:
            print "ERROR IN BATTLE SELECT"

    def battle_display(self, enemy, message):
        print "-" * 40
        print "Enemy: %s" % enemy.type
        print "Level: %s" % enemy.lvl
        ticks = min(
            int(math.ceil(enemy.hp / (enemy.lvl * 250.0) * 25.0)),
            25)
        healthbar = color(" " * ticks, "redh") + " " * (25 - ticks)
        print "HP: [%s]" % healthbar
        print "-" * 40
        print message
        print_bar(2)
        print "Options:"
        print "Attack!                   (A)"
        print "Run!                      (R)"
        print_bar(2)
        print "\n"
        print "-" * 40
        your_ticks = min(
            int(math.ceil(float(self.hp) / self.vit * 25.0)),
            25)
        your_healthbar = color(" " * your_ticks, "greenh") + " " * (25 - your_ticks)
        print "You:"
        print "HP: [%s] %s/%s" % (your_healthbar, self.hp, self.vit)
        print "-" * 40

    def attack(self, enemy):
        my_damage = self.damage_calc()
        enemy_damage = enemy.damage_calc()
        damage_to_me = self.damage_reduce(enemy_damage)
        damage_to_enemy = enemy.damage_reduce(my_damage)
        self.hp -= damage_to_me
        self.hp = max(self.hp, 0)  # SAFEGAURD AGAINST NEGATIVE HP
        enemy.hp -= damage_to_enemy
        enemy.hp = max(enemy.hp, 0)
        you_deal = color("You deal:    %s damage", "green") % damage_to_enemy
        enemy_deal = color("Enemy deals: %s damage", "red") % damage_to_me
        message = """
>
> %s
> %s
> """ % (you_deal, enemy_deal)
        return enemy, message

    def damage_calc(stats):
        # TODO: balance, crits?
        base = int(stats.wep * (stats.str + stats.int))
        rand = random.randint(
            int(stats.agil),
            1 + int(stats.luck + stats.agil))
        return random.randint(base, base + rand)

    def damage_reduce(stats, damage, char=True):
        # TODO: agi = Dodge?
        return int(damage - stats.defense)
