import event
import math

def eat_process(self, character):
    heal = int(math.ceil(int(character.vit) / 2))
    self.stats = [("hp", heal)]


EAT = event.Event(
    gold_req = 1,
    time_req = 1,
    life_req = 0,
    message = """You order a big steak and devour it
It's relieving after a long day""",
    stats = [], #placeholder until processed
    destination = "tavern",
    process = eat_process)


def drink_process(self, character):
    hurt = -int(math.ceil(character.vit / 10))
    self.stats = [("hp", hurt), ("luck", 2)]


DRINK = event.Event(
    gold_req = 1,
    time_req = 1,
    life_req = 1,
    message = """You have a drink at the bar
You practice some dice and card games""",
    stats = [] ,
    destination = "tavern",
    process = drink_process)
