"""Tavern events."""
from . import event
import math
import random


#SLEEP
def sleep_process(self, character):
    """Process sleep event."""
    heal = int(math.ceil(int(character.vit) / 4))
    self.life_req = -1 * heal

SLEEP = event.Event(
    gold_req=0,
    time_req=1,
    life_req=0,
    message="You sleep for the night",
    stats=[],
    destination="townR",
    process=sleep_process)


#EAT
def eat_process(self, character):
    """Process eat event."""
    heal = int(math.ceil(int(character.vit) / 2))
    self.stats = [("hp", heal)]

EAT = event.Event(
    gold_req=1,
    time_req=1,
    life_req=0,
    message="""You order a big steak and devour it
It's relieving after a long day""",
    stats=[],  # placeholder until processed
    destination="tavern",
    process=eat_process)


#DRINK
def drink_process(self, character):
    """Process drink event."""
    hurt = int(math.ceil(character.vit / 10))
    self.life_req = hurt

DRINK = event.Event(
    gold_req=1,
    time_req=1,
    life_req=1,
    message="""You have a drink at the bar
You practice some dice and card games""",
    stats=[("luck", 2)],
    destination="tavern",
    process=drink_process)


#GAMBLE
def gamble_process(self, character):
    """Process gamble event."""
    msg = "You play a hand of cards\n"
    chance = random.randint(1 + character.luck, 1000)
    if chance > 90:
        msg += 'You win!'
        self.stats = [("gold", 10)]
    else:
        msg += 'You lose.'
        self.stats = []
    self.message = msg

GAMBLE = event.Event(
    gold_req=1,
    time_req=1,
    life_req=0,
    message="You play a hand of cards",
    stats=[],
    destination="tavern",
    process=gamble_process)


#BARTEND
def bartend_process(self, character):
    """Process bartend event."""
    self.stats = event.work(character, 1, "luck", 3)

BARTEND = event.Event(
    gold_req=0,
    time_req=8,
    life_req=0,
    message="You work at the bar for a few hours",
    stats=[],
    destination="tavern",
    process=bartend_process
    )
