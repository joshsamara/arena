import event

MINE = event.Event(
    gold_req=0,
    time_req=4,
    life_req=0,
    message="""You mine some ore for the smith\n making you more able
to endure pain""",
    stats=[("vit", 5)],
    destination="smith") 