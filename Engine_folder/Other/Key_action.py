from Engine_folder.Logger import log


class KeyAction:
    def __init__(self, key, action, needed_state=1, args=()):
        self.id = 0
        self.key = key
        self.args = args
        self.action = action
        self.key_state = -1
        self.needed_state = needed_state

    def call(self, get_key_state, get_ref_state):
        # Checks key state
        key_state = get_ref_state(ref_name=self.key, test_check=True)

        if key_state == -1:
            key_state = get_key_state(key_name=self.key)

        if key_state == 1:
            if self.key_state == -1:
                self.key_state = 0
            if self.key_state <= 2:
                self.key_state += 1
        elif key_state == 0:
            if self.key_state == 0:
                self.key_state = -1
            self.key_state = 0

        # calls action if sey_state == needed_state
        if self.key_state == self.needed_state:
            self.action(*self.args)

