# Just Singleton patters, used for Logger
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#            print(f"{cls._instances[cls]} not in Singleton")
#        else:
#            print(f"{cls._instances[cls]} is in Singleton")
        return cls._instances[cls]
