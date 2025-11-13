"""Define character object and handle all actions directly involving."""
import math
import random
from . import save
from .arena import goto_arena
from .locations import *
from .common import *


class Character(object):

    """Stats and functions for a players Character. """

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
        """
        Continue on to the next queued action.

        This is done basically to break running into chunks.
        Otherwise the stack becomes increasingly large.

        """
        self.next(*self.args)

    def move(self, place, printing=True):
        """Move Character to a given location."""
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

    #
    # STAT MANAGEMENT
    #
    def stat(self, changed_stat, change=1):
        """Increment/decrement a character stat and report change."""
        global PRETTY_STAT
        pass_print = False
        if changed_stat == "hp" and self.hp + change >= self.vit:
            self.hp = self.vit
            print(color("Max HP!", "green"))
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
            print(color("%s %s by %s!", to_color) % (PRETTY_STAT[changed_stat],
                                                     change_text, change_val))
        elif changed_stat == "hrs":
            print(color("%s hour(s) passed!", "red") % change)

    def time_pass(self, hrs=1):
        """Increment/decrement a character's time."""
        self.hrs -= hrs

    def spend_gold(self, cost=1):
        """Increment/decrement a character's gold."""
        self.stat("gold", -cost)

    def not_dead(self):
        """
        Return true if a character isn't dead.

        If the character is dead, punish the character and
        return to town the next day.

        """
        if self.hp > 0:
            return True
        else:
            self.stat("day")
            self.hp = self.vit // 10
            self.gold = random.randint(self.gold // 2, self.gold)
            self.hrs = random.randint(1, 10)
            print(color("You have passed out!", "red"))
            print("You wake up sometime in town")
            print("It looks like some of your gold is missing")
            self.move("town")
            return False

    def requires(self, gold=1, hours=1, life=1):
        """
        Check requirements against a character.

        Return True if possible
        Otherwise return False and report why

        """
        goldcheck = self.gold < gold
        hourcheck = self.hrs < hours
        lifecheck = self.hp <= life

        if goldcheck or hourcheck or lifecheck:
            print("Impossible!")
            if goldcheck:
                print(color("You need %s gold", "red") % gold)
                print("You have %s gold" % self.gold)
            if hourcheck:
                print(color("You neeed %s hours", "red") % hours)
                print("There are %s hours left" % self.hrs)
            if lifecheck:
                print(color("You need %s life", "red") % life)
                print("You have %s life" % self.hp)
            return False
        else:
            return True

    def calc_needed_xp(self, lvl=None):
        """
        Return the xp needed to level up.

        Currently calculated as 2*lvl^2 + 22*lvl + 61

        """
        if lvl is None:
            lvl = self.lvl

        if lvl < 0:
            return 0
        else:
            return 2 * math.pow(lvl, 2) + 22 * lvl + 61

    def check_lvlup(self):
        """Check if a character is valid for a level up. Increase stats."""
        i = self.lvl + 1
        needed = self.calc_needed_xp()
        # TODO
        # print needed
        # print some sort of bar here [========    ]
        if self.xp > needed:
            self.lvl = i
            print(color("Your level has increased to %d!", "green") % i)
            for aStat in ["str", "int", "agil", "luck", "vit"]:
                self.stat(aStat, random.randint(3, 10))
                #add a little randomness to leveling for kicks
        else:
            pass

    def xp_perc(self):
        """Return the % xp until the next level."""
        this_lvl = self.xp - self.calc_needed_xp(self.lvl - 1)
        next_lvl = self.calc_needed_xp() - self.calc_needed_xp(self.lvl - 1)
        return int(100 * this_lvl/next_lvl)

    def damage_calc(stats):
        """Return the damage a character does based on stats."""
        # TODO: balance, crits?
        base = int(stats.wep * (stats.str + stats.int))
        rand = random.randint(
            int(stats.agil),
            1 + int(stats.luck + stats.agil))
        return random.randint(base, base + rand)

    def damage_reduce(stats, damage, char=True):
        """Return the damage done to a character based on stats."""
        # TODO: agi = Dodge?
        return int(damage - stats.defense)

    def run_event(self, anEvent):
        """Run any event on a character."""
        anEvent.run_default(self)
        return

    #
    # Go places
    #
    def save_prompt(self):
        """Move to the save prompt."""
        save.prompt(self)

    def town(self, refresh=True):
        """Move to town."""
        goto_town(self, refresh)

    def tavern(self):
        """Move to the tavern."""
        goto_tavern(self)

    def library(self):
        """Move to the library."""
        goto_library(self)

    def fields(self):
        """Move to the fields."""
        goto_fields(self)

    def smith(self):
        """Move to the smith."""
        goto_smith(self)

    def arena(self):
        """Move to the arena."""
        goto_arena(self)

    #
    # STAT PRINTING (TODO: Move these)
    #

    def print_useful(self, noskip=False):
        """Print useful stats in an organized manner."""
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
        time_print = color("%3d" % self.hrs, "teal")
        life_print = color("%3d" % self.hp, "pink")
        text_fill = (money_print, time_print, life_print, self.vit,
                     self.str,  self.agil, self.int,
                     self.luck, self.wep,  self.defense,
                     self.day,  self.xp_perc(),   self.lvl)
        print(to_print % text_fill)
        print_bar(1)

    def print_stat(self, stats, showtime=True):
        """Print a stat in a pretty manner."""
        global PRETTY_STAT
        print_bar(0)
        for a_stat in stats:
            text = PRETTY_STAT[a_stat]
            print("%s: %s" % (text, self.__dict__[a_stat]))
        if showtime:
            print("Time: %s" % self.hrs)
        print_bar(1)
