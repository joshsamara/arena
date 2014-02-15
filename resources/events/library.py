"""Library Events."""
import event
import math

#STUDY
STUDY = event.Event(
    gold_req=0,
    time_req=1,
    life_req=0,
    message="""You spend some time studying battle techniques,
and the arcane arts.""",
    stats=[("int", 1)],
    destination="library")

#BOOK
BOOK = event.Event(
    gold_req=1,
    time_req=3,
    life_req=0,
    message="You borrow and read a book of advanced\nfighting and magics",
    stats=[("int", 4)],
    destination="library")

#TUTOR
TUTOR = event.Event(
    gold_req=3,
    time_req=3,
    life_req=0,
    message="""You have an advanced wizard teach you
some incredibly difficult magic""",
    stats=[("int", 7)],
    destination="library")


#READ
def read_process(self, character):
    """Process read event."""
    heal = int(math.ceil(int(character.vit) / 10))
    self.stats = [("hp", heal)]

READ = event.Event(
    gold_req=0,
    time_req=1,
    life_req=0,
    message="You read a nice fiction book and rest",
    stats=[],
    destination="library",
    process=read_process)


#MAGICS
def magics_process(self, character):
    """Process magics event."""
    self.stats = event.work(character, 5, "int", 10)

MAGICS = event.Event(
    gold_req=0,
    time_req=8,
    life_req=0,
    message="You work a day teaching magic to others",
    stats=[],
    destination="library",
    process=magics_process
    )
