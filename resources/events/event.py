"""Make, manage and run events interacted with."""
import math
import random


def process_default(self, character):
    """
    By default just do nothing special.

    This is made to be overridden for events that require
    character data to judge their effect (ie cost 10%% hp)

    """
    pass


class Event(object):

    """Class to represent objects the character encounters."""

    # redefine if you need character based fields

    def __init__(self, gold_req, time_req, life_req, message, stats,
                 destination, process=process_default, printing=True):
        super(Event, self).__init__()
        self.gold_req = gold_req
        self.time_req = time_req
        self.life_req = life_req
        self.message = message
        self.stats = stats
        self.destination = destination
        self.process = process
        self.printing = printing

    def run_process(self, character):
        """Preprocess the event before running."""
        self.process(self, character)

    def run_default(self, character):
        """Run the event and effect the character."""
    # print "RUNNING EVENT"
        self.run_process(character)
        if character.requires(self.gold_req, self.time_req, self.life_req):
            print self.message

            #handle requirements
            character.time_pass(self.time_req)
            if self.gold_req > 0:
                character.spend_gold(self.gold_req)
            if self.life_req != 0:
                character.stat("hp", -1 * self.life_req)

            #handle field changes
            for field, change in self.stats:
                if field != "hp":
                    minVal = math.fabs(change)
                    toChange = random.randint(minVal, minVal * 2)
                    if change < 0:
                        toChange = -toChange
                else:
                    toChange = change
                character.stat(field, toChange)  # MORE RANDOM!

            #print
            if self.printing:
                possibs = [("gold", self.gold_req),
                           ("hrs", self.time_req),
                           ("hp", self.life_req)]
                to_print = [s for s, val in possibs + self.stats if val > 0]
                character.print_stat(to_print)

        #alive check
        if character.not_dead():
            character.move(self.destination)
            return
        else:
            #handled in not_dead()
            return

    # Before running events, allways run EVENT.run_process(character) to set
    # character based fields


def work(char, base, scale_stat, factor):
    """Calculate generic work event fields. Return gold earnings."""
    added = int(math.floor(char.__dict__[scale_stat] / factor))
    earned = base + added
    return [("gold", earned)]
