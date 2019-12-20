class TimeKeeper:
    class __TimeKeeper:
        def __init__(self, time=None):
            self.time = time
    instance = None

    def __init__(self, time=None):
        if not TimeKeeper.instance:
            TimeKeeper.instance = TimeKeeper.__TimeKeeper(time)
        else:
            TimeKeeper.instance.time = time

    def set_time(self, time):
        self.instance.time = time

    def get_time(self):
        return self.instance.time