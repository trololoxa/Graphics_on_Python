"""
Manages own assets, like other managers (or don't, and send this to main.py)
Saves own path, custom assets path and custom assets scriptable objects
"""
import json
import os
import pathlib
from Engine_folder.Logger import log
import sys


class AssetManager:
    def __init__(self):
        self._engine_dict = None
        self._custom_asset_dict = None
        self._scriptable_objects_paths = []
        self._settings_file = ""
        self._settings = None
        self._settings_file_path = None
        self._data_folder = None
        self.is_frozen = getattr(sys, 'frozen', False)

        self.logs_dict = ""
        self.shader_dict = ""
        self.texture_dict = ""

    @property
    def settings(self):
        return self._settings['Settings']

    def init_custom_dict(self, directory):
        # Initializes asset dict and loads all scriptable objects
        self._custom_asset_dict = pathlib.Path(directory).absolute()
        self._check_scriptable_objects(self._custom_asset_dict)
        log(f'Using {str(self._custom_asset_dict)} for assets', 'Asset Manager')

    def init_settings(self):
        # Opens settings file and loads all settings
        self._settings_file = open(str(self._settings_file_path), "r", encoding="utf-8")
        self._settings = json.load(self._settings_file)
        log(f'Initialized settings file at path {str(self._settings_file_path)}', 'Asset Manager')
        # TODO: save _settings file after end

    def _check_scriptable_objects(self, directory):
        # searches for all scriptable objects in asset dictionary
        directories = self.get_subfolders(directory)
        files = self.get_subfiles(directory, 'py')

        # Checks through all files
        for file in files:
            with open(file, 'r') as inp_file:
                line = inp_file.read()
                if '(ScriptableObject)' in line:
                    self._scriptable_objects_paths.append(file)

        # Checks directories inside given directory using simple recursion
        for inside_directory in directories:
            self._check_scriptable_objects(inside_directory)

    def execute_scripts(self):
        for script_path in self._scriptable_objects_paths:
            script_file = open(str(script_path), 'r', encoding='utf-8')
            script = script_file.read()
            script_file.close()
            # TODO: transfer scriptable object to components

    def initialize_dictionaries(self, program_name="EngineTest"):
        if self.is_frozen:
            # TODO: custom path if compiled
            self._engine_dict = pathlib.Path(sys.executable).absolute().joinpath('Engine_folder')
        else:
            self._engine_dict = pathlib.Path(__file__).absolute().parent.parent

        # initializes all folders needed for other managers
        log('Initializing dictionaries', 'Asset Manager')
        self.shader_dict = self._engine_dict.joinpath("Shaders")
        self.texture_dict = self._engine_dict.joinpath("Textures")
        # loads folder for engine data
        self._data_folder = pathlib.WindowsPath(os.getenv('APPDATA')).joinpath(program_name)
        log(f'Using {str(self._data_folder)} for data', 'Asset Manager')
        self.logs_dict = self._data_folder.joinpath(pathlib.Path('Logs'))
        self._settings_file_path = self._data_folder.joinpath('settings.json')

        # id some folders or files don't exist - it creates them
        if not self._data_folder.exists():
            pathlib.Path.mkdir(self._data_folder)
            log(f'Created data folder in {str(self._data_folder)}', 'Asset Manager')
        if not self.logs_dict.exists():
            pathlib.Path.mkdir(self.logs_dict)
            log(f'Created logs folder in {str(self.logs_dict)}', 'Asset Manager')
        if not self._settings_file_path.exists():
            file = open(str(self._settings_file_path), 'w', encoding='utf-8')
            json.dump({"Settings": {"base": "GLFW", "api": "OpenGL"}}, file)
            file.close()
            log(f'Created settings file in {str(self._settings_file_path)}', 'Asset Manager')

        log('Initialization complete', 'Asset Manager')

    @staticmethod
    def get_subfolders(directory):
        # checks for directories in given directory and returns them
        directory = pathlib.Path(directory)
        return [x for x in directory.iterdir() if x.is_dir()]

    @staticmethod
    def get_subfiles(directory, file_extension="*"):
        # checks for files in given directory and with given extension and returns them
        directory = pathlib.Path(directory)
        return [x for x in directory.glob(f'*.{file_extension}')]
