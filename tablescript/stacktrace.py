

class StackTrace:

    def __init__(self, trace):

        self.trace = [trace]

    def pushTrace(self, trace):

        self.trace.append(trace)

    def __repr__(self):

        ret = ""

        for i in range(0, len(self.trace)):
            ret += "at " + self.trace[i] + '\n'

        return ret