from datetime import datetime
from math import ceil


class Util:
    @staticmethod
    def now() -> int:
        now = datetime.now()
        return (now.year - 2000) * 31536000 \
            + (now.month - 1) * 2592000 \
            + (now.day - 1) * 86400 \
            + now.hour * 3600 \
            + now.minute * 60 \
            + now.second

    @staticmethod
    def humanize(text: str, char: str, each: int, maxgroup: int = -1) -> str:
        if maxgroup == -1:
            maxgroup = ceil(len(text) / each)
        r = char.join(text[i:i + each] for i in range(0, len(text), each) if i / each < maxgroup)
        r += text[each * maxgroup:]
        return r


class Int32:
    MAX = 0x7fffffff
    MIN = -0x7fffffff

    def __init__(self, value):
        value = int(value)
        if not (self.MIN <= value <= self.MAX):
            value = (value + self.MAX + 1) % (2 * (self.MAX + 1)) - self.MAX - 1
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f'<Int32: {self.value}>'

    def __format__(self, format_spec):
        return format(self.value, format_spec)

    def __int__(self):
        return self.value

    def __add__(self, other):
        return Int32(self.value + other)

    def __sub__(self, other):
        return Int32(self.value - other)

    def __and__(self, other):
        return Int32(self.value & other)

    def __lshift__(self, other):
        return Int32(self.value << other)

    def __rshift__(self, other):
        return Int32(self.value >> other)

    def __xor__(self, other):
        return Int32(self.value ^ other)

    def __radd__(self, other):
        return Int32(other + self.value)

    def __rsub__(self, other):
        return Int32(other - self.value)

    def __rxor__(self, other):
        return Int32(other ^ self.value)

    def to_bytes(self, length=4, byteorder='little', signed=True):
        return self.value.to_bytes(length, byteorder, signed=signed)

