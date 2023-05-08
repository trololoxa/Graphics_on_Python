from datetime import datetime
from Engine.Other.Singleton import Singleton
import os


class Logger(metaclass=Singleton):
    def __init__(self):
        self.file = None
        self.real_time_logging = True
        self.directory = "G:\\Programming\\Python\\graphic_nigger\\Logs"
        self.base_name = "test_{}_{}.log"
        self.filename = ""

    def create_file(self):
        after_log = False
        if not os.path.exists(self.directory):
            after_log = ("Specified path don't exist, using User\\Documents\\Engine_Logs path", "Logger", "Warn")
            self.directory = os.path.expanduser(os.getenv('USERPROFILE')) + "\\Documents\\Engine_Logs"
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)

        files = os.fsencode(self.directory)
        files = os.listdir(files)
        files = [os.fsdecode(file) for file in files]

        index = 0
        while True:
            if self.base_name.format(datetime.date(datetime.now()), index) not in files:
                break
            index += 1

        self.filename = self.base_name.format(datetime.date(datetime.now()), index)
        self.file = open(self.directory + "\\" + self.filename, "w", encoding="utf-8")
        if after_log:
            self.log(*after_log)

        self.log("Initialization complete", "Logger", "Info")

    def log(self, message=None, origin=None, log_type="Info"):
        log = f'[{datetime.time(datetime.today()).replace(microsecond=0)}] [{log_type}] [{origin}]: {message}\n'
        self.file.write(log)
        if self.real_time_logging:
            print(f'[{datetime.time(datetime.today()).replace(microsecond=0)}] [{log_type}] [{origin}]: {message}')
