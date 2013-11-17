import event

DUMMY = event.Event(
    gold_req=0,
    time_req=2,
    life_req=0,
    message="You beat up a dummy for a nice work out.",
    stats=[("str", 1)],
    destination="fields")

MASTER = event.Event(
    gold_req=1,
    time_req=3,
    life_req=1,
    message="""You spar a master trainer for some time.
He shows you a thing or two about fighting.
You take a few hits though.""",
    stats=[("str", 6)],
    destination="fields")

COURSE = event.Event(
    gold_req=0,
    time_req=2,
    life_req=0,
    message="You dash through obstacle course for a few hours",
    stats=[("agil", 1)],
    destination="fields")

RACE = event.Event(
    gold_req=3,
    time_req=1,
    life_req=0,
    message="You run a race and it really works your muscles.",
    stats=[("agil", 3)],
    destination="fields")
