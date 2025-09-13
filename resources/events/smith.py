"""Smith events."""
from . import event
import math
from .. import common


def upgrade(char, uptype):
    """Generic upgrade function."""
    #type 0 for wep, type 1 for armor
    if uptype == 0:
        upstats = {"name": "weapon", "level": char.wep, "stat": "wep"}
    else:
        upstats = {"name": "armor", "level": char.defense, "stat": "defense"}
    common.clear()
    cost = int(math.pow(10, upstats["level"]))
    common.print_bar(0)
    print("%-20s:   %s" % ("Current %s level" % upstats["name"],
                           upstats["level"]))
    print("Current upgrade cost:   %s gold" % cost)
    print("Current gold        :   %s gold" % char.gold)
    common.print_bar(1)
    print("Would you like to upgrade your %s? (y/n)" % (upstats["name"]))

    val = common.get_val("yn")
    common.clear()
    if val == "y":
        if char.requires(cost, 0):
            print("You upgrade your %s." % (upstats["name"]))
            char.stat(upstats["stat"])
            char.print_stat([upstats["stat"]])
    elif val == "n":
        print("You decide to save upgrading for later.")
    char.move("smith")
    return


def wepup(character):
    """Weapon upgrade function."""
    upgrade(character, 0)


def armup(character):
    """Armor upgrade function."""
    upgrade(character, 1)

#MINE
MINE = event.Event(
    gold_req=0,
    time_req=4,
    life_req=0,
    message="""You mine some ore for the smith\nmaking you more able
to endure pain""",
    stats=[("vit", 5)],
    destination="smith")


#FORGE
def forge_process(self, character):
    """Forge process function."""
    self.stats = event.work(character, 10, "str", 10)

FORGE = event.Event(
    gold_req=0,
    time_req=8,
    life_req=0,
    message="You forging weapons and armor",
    stats=[],
    destination="smith",
    process=forge_process
    )
