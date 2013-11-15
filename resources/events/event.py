def process_default(self, character):
    pass

class Event(object):

    """Generic events"""

    #redefine if you need character based fields

    def __init__(self, gold_req, time_req, life_req, message, stats, destination, process = process_default, printing = True):
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
        return self.process(self, character)

    #Before running events, allways run EVENT.run_process(character) to set character based fields
        


