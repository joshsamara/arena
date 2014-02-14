import time
import math
import events
import pickle
from locations import *
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
        self.next = self.town
        self.args = []

    def __str__(self):
        d = self.__dict__
        r = ""
        for key in d:
            r += "%-5s: %5s\n" % (key, d[key])
        return r

    def run(self):
        self.next(*self.args)

    def move(self, place, printing = True):
        self.args = []
        if place == "town":
            # cm("moving to town")
            self.next = self.town
            self.args = [False]
        elif place == "townR":
            self.next = self.town
            place = "town"
        elif place == "tavern":
            self.next = self.tavern
        elif place == "library":
            self.next = self.library
        elif place == "fields":
            self.next = self.fields
        elif place == "smith":
            self.next = self.smith
        elif place == "arena":
            self.next = self.arena
        else:
            raise Exception("Invalid move location: %s" % place)
        if printing:
            cm(place)
        return

    def save(self):
        save_file = open('save/arena.save', 'w')
        temp = self.next
        self.next = None
        pickle.dump(self, save_file)
        self.next = temp
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
            print color("Max HP!", "green")
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
            self.move("town")
            return False

    def requires(self, gold=1, hours=1, life=1):
        goldcheck = self.gold < gold
        hourcheck = self.hrs < hours
        lifecheck = self.hp <= life

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
        to_print = """$:  %s    TIME: %2s/16   HP:  %2s/%-d
STR:   %3d    AGI:  %3d     INT:  %3d
LCK:   %3d    WEP:  %3d     DEF:  %3d
DAY:   %3d    EXP:  %2d%%     LVL:  %3d"""

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
        return anEvent.run_default(self)


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
            self.move("town")

        elif "e" == val:
            self.save()
            exit()

        elif "q" == val:
            exit()

        elif "r" == val:
            self.move("town", printing = False)
        return


    def town(self, refresh=True):
        goto_town(self, refresh)

    def tavern(self):
        goto_tavern(self)

    def library(self):
        goto_library(self)

    def fields(self):
        goto_fields(self)

    def smith(self):
        goto_smith(self)
        

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
            self.move("town", False)
        else:
            self.save_prompt()
            print "ERROR IN ARENA SELECT"
        return
            

    def fight(self):
        if self.requires(0, 1):
            self.time_pass(1)
            enemy = Enemy(pick_diff(self.lvl))
            self.battle(enemy)
        self.move("town")
        return

    def victory(self, enemy):
        print "You win!"
        self.stat("xp", enemy.calc_exp())
        self.stat("gold", enemy.calc_gold())
        self.check_lvlup()
        self.move("town")
        return

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
            self.move("town")
        else:
            self.save_prompt()
            raise Exception ("ERROR IN BATTLE SELECT")
        return

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
        return

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
