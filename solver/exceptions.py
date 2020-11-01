
class badInput(Exception):
    def __init__(self, reason):
        self.reason = reason
        print("Error: %s"%(reason))
