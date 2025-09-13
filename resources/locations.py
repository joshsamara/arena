"""Functions for hubs of activatable events."""
from .common import *
from . import events

#TODO, abstract over these things


def goto_town(character, refresh=True):
    """Move character to town seletion screen."""
    clear()
    if refresh:
        character.hrs = 16
        character.day += 1
    print("""Welcome to:

  _____
 |_   _|____      ___ __
   | |/ _ \ \ /\ / / '_ \\
   | | (_) \ V  V /| | | |
   |_|\___/ \_/\_/ |_| |_|
""")

    character.print_useful()
    town_options = [make_option('Enter the Tavern', 'T'),
                    make_option('Go to the Library', 'L'),
                    make_option('Go to the Trainng Fields', 'F'),
                    make_option('Visit the Blacksmith', 'B'),
                    make_option('Enter the Arena', 'A'),
                    make_option('Save and/or exit the game', 'S')]
    print(nav_menu(town_options, short=True))
    val = get_val("stlfba9")

    if val == "s":
        character.save_prompt()
    elif val == "t":
        character.move("tavern", False)
    elif val == "l":
        character.move("library", False)
    elif val == "f":
        character.move("fields", False)
    elif val == "b":
        character.move("smith", False)
    elif val == "a":
        character.move("arena", False)
    elif val == "9":
        character.gold += 100
        character.hrs += 100
        character.hp += 100
        character.move("town")
    else:
        character.save_prompt()
        raise Exception("ERROR IN TOWN SELECT")
    return


def goto_tavern(character):
    """Move character to tavern seletion screen."""
    clear()
    print("Welcome to the:")
    print(color("""
  _____
 |_   _|_ ___   _____ _ __ _ __
   | |/ _` \ \ / / _ \ '__| '_ \\
   | | (_| |\ V /  __/ |  | | | |
   |_|\__,_| \_/ \___|_|  |_| |_|
""", "yellow"))

    character.print_useful()

    tavern_options = [make_option('Buy a Meal', 'M', gold=1, time=1),
                      make_option('Grab a Drink', 'D', gold=1, time=1, hp=.1),
                      make_option('Go to Sleep', 'S'),
                      make_option('Gamble some gold', 'G', gold=1, time=1),
                      make_option('Bartend', 'B', time=8),
                      make_option('Return to Town', 'T')]
    print(nav_menu(tavern_options))

    val = get_val("mdsgbt")
    clear()
    if val == "m":
        character.run_event(events.tavern.EAT)
    elif val == "d":
        character.run_event(events.tavern.DRINK)
    elif val == "s":
        character.run_event(events.tavern.SLEEP)
    elif val == "g":
        character.run_event(events.tavern.GAMBLE)
    elif val == "b":
        character.run_event(events.tavern.BARTEND)
    elif val == "t":
        character.move("town", False)
    else:
        character.save_prompt()
        raise Exception("ERROR IN TAVERN SELECT")
    return


def goto_library(character):
    """Move character to library seletion screen."""
    clear()
    print("Welcome to the:")
    print(color(""")
  _       _
 | |   (_) |__  _ __ __ _ _ __ _   _
 | |   | | '_ \| '__/ _` | '__| | | |
 | |___| | |_) | | | (_| | |  | |_| |
 |_____|_|_.__/|_|  \__,_|_|   \__, |
                                |___/
""", "teal"))

    character.print_useful(True)
    library_options = [make_option('Study Magics', 'S', time=1),
                       make_option('Borrow a book', 'B', gold=1, time=3),
                       make_option('Hire a tutor', 'H', gold=3, time=3),
                       make_option('Read and relax', 'R', time=1),
                       make_option('Tutor Magics', 'M', time=8),
                       make_option('Return to Town', 'T')]
    print(nav_menu(library_options))

    val = get_val("sbhrmt")
    clear()
    if val == "s":
        character.run_event(events.library.STUDY)
    elif val == "b":
        character.run_event(events.library.BOOK)
    elif val == "h":
        character.run_event(events.library.TUTOR)
    elif val == "r":
        character.run_event(events.library.READ)
    elif val == "m":
        character.run_event(events.library.MAGICS)
    elif val == "t":
        character.move("town", False)
    else:
        character.save_prompt()
        raise Exception("ERROR IN LIBRARY SELECT")
    return


def goto_fields(character):
    """Move character to field seletion screen."""
    clear()
    print("Welcome to the:")
    print(color("""
  _____        _     _
 |  ___(_) ___| | __| |___
 | |_  | |/ _ \ |/ _` / __|
 |  _| | |  __/ | (_| \__ \\
 |_|   |_|\___|_|\__,_|___/
""", "green"))
    character.print_useful()

    field_options = [make_option('Fight a training Dummy', 'D', time=2),
                     make_option('Spar a Battle Master',  'M', gold=1, time=3,
                                 hp=.1),
                     make_option('Run an obstacle Course', 'C', time=2),
                     make_option('Enter a Race',          'R', gold=3, time=1),
                     make_option('Perform Show tricks',   'S', time=8),
                     make_option('Return to Town',        'T')]
    print(nav_menu(field_options))

    val = get_val("dmcrst")
    clear()
    if val == "d":
        character.run_event(events.fields.DUMMY)
    elif val == "m":
        character.run_event(events.fields.MASTER)
    elif val == "c":
        character.run_event(events.fields.COURSE)
    elif val == "r":
        character.run_event(events.fields.RACE)
    elif val == "s":
        character.run_event(events.fields.SHOW)
    elif val == "t":
        character.move("town", False)
    else:
        character.save_prompt()
        raise Exception("ERROR IN FIELDS SELECT")
    return


def goto_smith(character):
    """Move character to smith seletion screen."""
    clear()
    print("Welcome to the:")
    print(color("""
  ____            _ _   _
 / ___| _ __ ___ (_) |_| |__
 \___ \| '_ ` _ \| | __| '_ \\
  ___) | | | | | | | |_| | | |
 |____/|_|_|_| |_|_|\__|_| |_|
 """, "blue"))
    character.print_useful()

    smith_options = [make_option('Upgrade your Weapon', 'W', gold='?'),
                     make_option('Upgrade your Armor ', 'A', gold='?'),
                     make_option('Mine ores', 'M', time=4),
                     make_option('Work the Forge', 'F', time=8),
                     make_option('Return to Town', 'T')]

    print(nav_menu(smith_options))
    val = get_val("wamft")

    clear()
    if val == "w":
        events.smith.wepup(character)
    elif val == "a":
        events.smith.armup(character)
    elif val == "m":
        character.run_event(events.smith.MINE)
    elif val == "f":
        character.run_event(events.smith.FORGE)
    elif val == "t":
        character.move("town", False)
    else:
        character.save_prompt()
        raise Exception("ERROR IN FIELDS SELECT")
    return
