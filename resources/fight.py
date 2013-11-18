import random

ENEMY_TYPES = [["Peasant"],
               ["Fighter",
                "Thief",
                "Apprentice"],
               ["Warrior",
                "Ranger",
                "Mage"],
               ["Paladin",
                "Assassin",
                "Wizard]"],
               ["Minotaur",
                "Ninja",
                "Archon"],
               ["Shadow"]]


def pick_diff(lvl):
    range1 = enemy_range(1, lvl)
    range3 = range1 + enemy_range(3, lvl)
    range4 = range3 + enemy_range(4, lvl)
    range5 = range4 + enemy_range(5, lvl)
    range6 = range5 + enemy_range(6, lvl)
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


class Enemy(object):

    """docstring for Enemy"""

    def __init__(self, diff):
        super(Enemy, self).__init__()
        self.type = random.choice(ENEMY_TYPES[diff - 1])
        self.lvl = diff
        self.hp = diff * 250

    def damage_calc(self):
        base = self.lvl * 5
        rand = self.lvl * 2
        return random.randrange(base, base + rand)

    def damage_reduce(self, damage):
        # TODO: agi = Dodge?
        return int(damage)

    def not_dead(self):
        return self.hp > 0
