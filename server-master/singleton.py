class Singleton:
    __instance = None

    @staticmethod
    def get_instance():
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception
        else:
            Singleton.__instance = self
            self.__data = {}

    def update_data(self, key, value):
        self.__data.update({ key: value })

    def get_data(self, key):
        return self.__data.get(key)
