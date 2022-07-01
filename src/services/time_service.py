# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class TimeService(object):

    def __init__(self):
        self.running = True
    
    def run(self):
        while (self.running):
            # TODO: sleep
            pass
    
    def isRunning(self):
        return self.running
    
    def setRunning(self, bool):
        self.running = bool
    
    def elapse(self):
        # abstract
        pass