import event
import math

#DUMMY
DUMMY = event.Event(
    gold_req=0,
    time_req=2,
    life_req=0,
    message="You beat up a dummy for a nice work out.",
    stats=[("str", 1)],
    destination="fields")

def master_process(self, character):
    hurt = int(math.ceil(character.vit / 10))
    self.life_req = hurt

#MASTER
MASTER = event.Event(
    gold_req=1,
    time_req=3,
    life_req=1,
    message="""You spar a master trainer for some time.
He shows you a thing or two about fighting.
You take a few hits though.""",
    stats=[("str", 6)],
    destination="fields",
    process= master_process)

#COURSE
COURSE = event.Event(
    gold_req=0,
    time_req=2,
    life_req=0,
    message="You dash through obstacle course for a few hours",
    stats=[("agil", 1)],
    destination="fields")

#RACE
RACE = event.Event(
    gold_req=3,
    time_req=1,
    life_req=0,
    message="You run a race and it really works your muscles.",
    stats=[("agil", 3)],
    destination="fields")

#SHOW
def show_process(self, character):
    self.stats = event.work(character, 3, "agil", 7)

SHOW = event.Event(
    gold_req=0,
    time_req=8,
    life_req=0,
    message="You spend a day performing tricks",
    stats=[],
    destination="fields",
    process=show_process
    )
