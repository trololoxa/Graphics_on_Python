import time

# from pynput import mouse, keyboard
from Engine_folder.Other.Singleton import Singleton
from Engine_folder.Other.Key_action import KeyAction
from Engine_folder.Logger import log


class InputManager:
    """
    Holds key lists and processes all actions \n
    key_list: all keys with they_re states \n
    actions: list of actions, that contain needed key, action, needed state and args for action
    """
    def __init__(self):
        self._key_list = {'`': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '0': 0,
                          '-': 0, '=': 0, '\\': 0, 'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0,
                          'o': 0, 'p': 0, '[': 0, ']': 0, 'a': 0, 's': 0, 'd': 0, 'f': 0, 'g': 0, 'h': 0, 'j': 0,
                          'k': 0, 'l': 0, ';': 0, "'": 0, 'z': 0, 'x': 0, 'c': 0, 'v': 0, 'b': 0, 'n': 0, 'm': 0,
                          ',': 0, '.': 0, '/': 0, 'tab': 0, 'l_shift': 0, 'caps_lock': 0, 'l_control': 0, 'l_alt': 0,
                          'l_win': 0, 'space': 0, 'r_alt': 0, 'r_win': 0, 'r_control': 0, 'menu': 0, 'up_arrow': 0,
                          'left_arrow': 0, 'down_arrow': 0, 'right_arrow': 0, 'insert': 0, 'delete': 0, 'home': 0,
                          'end': 0, 'pg_up': 0, 'pg_down': 0, 'f1': 0, 'escape': 0, 'r_shift': 0, 'enter': 0,
                          'return': 0, 'f2': 0, 'f3': 0, 'f4': 0, 'f5': 0, 'f6': 0, 'f7': 0, 'f8': 0, 'f9': 0, 'f10': 0,
                          'f11': 0, 'f12': 0, 'prnt_scr': 0, 'scroll_lock': 0, 'pause_break': 0, 'num_/': 0, 'num_*': 0,
                          'num_-': 0, 'num_+': 0, 'num_enter': 0, 'num_0': 0, 'num_.': 0, 'num_1': 0, 'num_2': 0,
                          'num_3': 0, 'num_6': 0, 'num_5': 0, 'num_4': 0, 'num_7': 0, 'num_8': 0, 'num_9': 0,
                          'num_lock': 0}

        self.actions = []

        self.references = {}

    @property
    def key_list(self):
        return self._key_list

    def add_action(self, key, action, needed_state=1, *args):
        # adds action to actions list
        self.actions.append(KeyAction(key=key, action=action, needed_state=needed_state,
                                      args=args))

    def do_actions(self):
        # calls all actions every frame
        for action in self.actions:
            action.call(self.get_key_state, self.get_reference_state)

    # TODO: delete action normally

    def set_key_state(self, key_name, key_state):
        # Later_TODO: Make it editable only inside engine (Only if bugs, it's free country (I'm just lazy))
        # Sets key state if key is real and state is 0 or 1
        if key_name not in self._key_list:
            log("Unknown key name", "Input Manager", "Warn")
            return -1

        if key_state not in [0, 1]:
            log("Unknown key state", "Input Manager", "Warn")
            return -1

        self._key_list[key_name] = key_state

    def get_key_state(self, key_name):
        # returns key state
        if key_name not in self._key_list:
            log("Unknown key name", "Input Manager", "Warn")
            return -1

        return self._key_list[key_name]

    def add_key_reference(self, ref_name, *key_names):
        if ref_name not in self.references:
            self.references[ref_name] = []

        for key_name in key_names:
            if key_name not in self._key_list:
                log(f'Unknown key {key_name} for reference {ref_name}', 'Input Manager', 'Error')
            else:
                self.references[ref_name].append(key_name)

    def remove_key_reference(self, ref_name, *key_names):
        if ref_name not in self.references:
            log(f'Unknown reference {ref_name}', 'Input Manager', 'Error')
            return -1

        for key_name in key_names:
            if key_names not in self._key_list:
                log(f'Unknown key {key_names} for reference {ref_name}', 'Input Manager', 'Error')
                continue

            if key_name not in self.references[ref_name]:
                log(f'Key {key_name} not in reference {ref_name}', 'Input Manager', 'Warn')
            else:
                self.references[ref_name].remove(key_name)

    def get_reference_state(self, ref_name, test_check=False):
        if ref_name not in self.references:
            if not test_check:
                log(f'Unknown reference {ref_name}', 'Input Manager', 'Error')
            return -1

        for key in self.references[ref_name]:
            if self.get_key_state(key):
                return 1

        return 0
