from datetime import datetime
from Engine_folder.Other.Singleton import Singleton
import os


class Logger(metaclass=Singleton):
    def __init__(self):
        self.file = None
        self.real_time_logging = True
        self.delayed_logs = []
        self.directory = "G:\\Programming\\Python\\graphic_nigger\\Logs"
        self.base_name = "test_{}_{}.log"
        self.filename = ""

    def initialize(self, asset_manager):
        self.directory = asset_manager.logs_dict
        self.create_file(asset_manager)

    def create_file(self, asset_manager):
        # initializes logger file and saves in into var

        # gets all files from the directory
        files = asset_manager.get_subfiles(self.directory)

        index = 0
        while True:
            if self.base_name.format(datetime.date(datetime.now()), index) not in [file.name for file in files]:
                break
            index += 1

        # creates file name and opens this file
        self.filename = self.base_name.format(datetime.date(datetime.now()), index)
        self.file = open(str(self.directory) + "\\" + self.filename, "w", encoding="utf-8")

        self.log("Initialization complete", "Logger", "Info")

    def log(self, message=None, origin=None, log_type="Info"):
        # logs given message to file and mb to console
        log_message = f'[{datetime.time(datetime.today()).replace(microsecond=0)}] [{log_type}] [{origin}]: {message}\n'
        self.delayed_logs.append(log_message)

        if self.file is not None:
            for delayed_log in self.delayed_logs:
                self.file.write(delayed_log)

            self.delayed_logs = []

        if self.real_time_logging:
            print(f'[{datetime.time(datetime.today()).replace(microsecond=0)}] [{log_type}] [{origin}]: {message}')


def log(message=None, origin=None, log_type="Info"):
    Logger().log(message=message, origin=origin, log_type=log_type)
