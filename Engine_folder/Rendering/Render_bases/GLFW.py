import glfw

from glfw.GLFW import glfwWindowHint, GLFW_CONTEXT_VERSION_MAJOR, GLFW_CONTEXT_VERSION_MINOR, GLFW_OPENGL_PROFILE, \
    GLFW_OPENGL_CORE_PROFILE, GLFW_OPENGL_FORWARD_COMPAT

from Engine_folder.Logger import log


class GLFWBase:
    _key_list = {96: '`', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 48: '0',
                 45: '-', 61: '=', 92: '\\', 81: 'q', 87: 'w', 69: 'e', 82: 'r', 84: 't', 89: 'y', 85: 'u', 73: 'i',
                 79: 'o', 80: 'p', 91: '[', 93: ']', 65: 'a', 83: 's', 68: 'd', 70: 'f', 71: 'g', 72: 'h', 74: 'j',
                 75: 'k', 76: 'l', 59: ';', 39: "'", 90: 'z', 88: 'x', 67: 'c', 86: 'v', 66: 'b', 78: 'n', 77: 'm',
                 44: ',', 46: '.', 47: '/', 258: 'tab', 340: 'l_shift', 280: 'caps_lock', 341: 'l_control',
                 342: 'l_alt', 343: 'l_win', 32: 'space', 346: 'r_alt', 347: 'r_win', 345: 'r_control', 348: 'menu',
                 265: 'up_arrow', 263: 'left_arrow', 264: 'down_arrow', 262: 'right_arrow', 260: 'insert',
                 261: 'delete', 268: 'home', 269: 'end', 266: 'pg_up', 267: 'pg_down', 290: 'f1', 256: 'escape',
                 344: 'r_shift', 257: 'enter', 259: 'return', 291: 'f2', 292: 'f3', 293: 'f4', 294: 'f5', 295: 'f6',
                 296: 'f7', 297: 'f8', 298: 'f9', 299: 'f10', 300: 'f11', 301: 'f12', 283: 'prnt_scr',
                 281: 'scroll_lock', 284: 'pause_break', 331: 'num_/', 332: 'num_*', 333: 'num_-', 334: 'num_+',
                 335: 'num_enter', 320: 'num_0', 330: 'num_.', 321: 'num_1', 322: 'num_2', 323: 'num_3', 326: 'num_6',
                 325: 'num_5', 324: 'num_4', 327: 'num_7', 328: 'num_8', 329: 'num_9', 282: 'num_lock'}

    # backup
    key_states_list = {'`': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '0': 0,
                       '-': 0, '=': 0, '\\': 0, 'q': 0, 'w': 0, 'e': 0, 'r': 0, 't': 0, 'y': 0, 'u': 0, 'i': 0,
                       'o': 0, 'p': 0, '[': 0, ']': 0, 'a': 0, 's': 0, 'd': 0, 'f': 0, 'g': 0, 'h': 0, 'j': 0,
                       'k': 0, 'l': 0, ';': 0, "'": 0, 'z': 0, 'x': 0, 'c': 0, 'v': 0, 'b': 0, 'n': 0, 'm': 0,
                       ',': 0, '.': 0, '/': 0, 'tab': 0, 'shift': 0, 'caps_lock': 0, 'control': 0, 'alt': 0,
                       'win': 0, 'space': 0, 'r_alt': 0, 'r_win': 0, 'r_control': 0, 'menu': 0, 'up_arrow': 0,
                       'left_arrow': 0, 'down_arrow': 0, 'right_arrow': 0, 'insert': 0, 'delete': 0, 'home': 0,
                       'end': 0, 'pg_up': 0, 'pg_down': 0, 'f1': 0, 'escape': 0, 'r_shift': 0, 'enter': 0,
                       'return': 0, 'f2': 0, 'f3': 0, 'f4': 0, 'f5': 0, 'f6': 0, 'f7': 0, 'f8': 0, 'f9': 0, 'f10': 0,
                       'f11': 0, 'f12': 0, 'prnt_scr': 0, 'scroll_lock': 0, 'pause_break': 0, 'num_/': 0, 'num_*': 0,
                       'num_-': 0, 'num_+': 0, 'num_enter': 0, 'num_0': 0, 'num_.': 0, 'num_1': 0, 'num_2': 0,
                       'num_3': 0, 'num_6': 0, 'num_5': 0, 'num_4': 0, 'num_7': 0, 'num_8': 0, 'num_9': 0,
                       'num_lock': 0}

    """
    Basic GLFW loop
    objects list can be changed with scene
    """

    def __init__(self):
        self.window = None
        self.context = None
        self._set_key_state_func = None

    def prepare(self, key_state_func):
        # Initialize the library
        if not glfw.init():
            return

        # Force OpenGL 4.6 'core' context.
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, True)

        self._set_key_state_func = key_state_func

        log("Using GLFW Render Base", "Renderer")

    def create_window(self, width=800, height=600, name="OpenGL demo", render_api=None):
        # Create a windowed mode window
        self.window = glfw.create_window(width, height, name, None, None)
        if not self.window:
            log("Failed to create GLFW window", "Renderer", "Critical")
            self.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        render_api.set_viewport(None, width, height)

        # set callbacks
        glfw.set_framebuffer_size_callback(self.window, render_api.set_viewport)
        glfw.set_key_callback(self.window, self.input_callback)

    def close_window(self):
        glfw.set_window_should_close(self.window, True)

    def input_callback(self, window, key, scancode, action, mods):
        if key not in self._key_list:
            if action == glfw.PRESS:
                log(f'Unknown key {key} with scancode {scancode}', 'Input Manager', 'Warn')
            return -1
        # window - useless
        # key - idn
        # scancode - idn
        # action - 0 - release
        #          1 - press
        #          2 - hold
        # mods - shift = 1
        #        ctrl = 2
        #        alt = 4
        #        win = 8
        if action == glfw.PRESS:
            self._set_key_state_func(self._key_list[key], 1)
        elif action == glfw.RELEASE:
            self._set_key_state_func(self._key_list[key], 0)

    def swap_buffers(self):
        # processes events
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def should_close(self):
        # name speaks about itself
        return glfw.window_should_close(self.window)

    @staticmethod
    def terminate():
        glfw.terminate()
