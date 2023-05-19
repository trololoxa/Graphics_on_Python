import numpy as np


# same ndarray, but with xyz bindings
class Vector(np.ndarray):
    """
    ndarray, but with vector bindings
    """
    size = 3

    def __new__(cls, *args):
        data = tuple(args)
        arr = np.array(data, dtype=np.float32, copy=True)
        # noinspection PyTypeChecker
        arr.resize(cls.size)
        return np.ndarray.__new__(cls, shape=(cls.size,), buffer=arr)


class Vec2(Vector):
    size = 2

    @property
    def x(self):
        return self[0]

    @x.setter
    def x(self, other):
        self[0] = other

    @property
    def y(self):
        return self[1]

    @y.setter
    def y(self, other):
        self[1] = other


class Vec3(Vec2):
    size = 3

    @property
    def z(self):
        return self[2]

    @z.setter
    def z(self, other):
        self[2] = other


class Vec4(Vec3):
    size = 4

    @property
    def w(self):
        return self[3]

    @w.setter
    def w(self, other):
        self[3] = other
