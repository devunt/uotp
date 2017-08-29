from functools import reduce
from hashlib import sha1

from .util import Util


class OTPTokenGenerator:
    def __init__(self, oid, seed):
        self.__oid = oid
        self.__seed = seed
        self.__timediff = 0

    def compensate_time_deviation(self, timediff):
        self.__timediff = timediff

    @property
    def generate_token(self):
        now = Util.now()
        now += self.__timediff

        time = now // 10
        oid = self.__oid

        seed_oid = bytearray(11)
        seed_time = bytearray(11)

        for i in reversed(range(0, 11)):
            seed_time[i] = int(time) & 255
            seed_oid[i] = int(oid) & 255

            oid >>= 8
            time >>= 8

        seed_oid += self.__seed

        seed = bytearray(64)
        seed[:20] = sha1(seed_oid).digest()

        seed_1 = seed[:]
        seed_2 = seed[:]

        for i in range(0, 64):
            seed_1[i] ^= 54
            seed_2[i] ^= 92

        digest = sha1(seed_1 + seed_time).digest()
        digest = sha1(seed_2 + digest).digest()

        digit = digest[-1] & 0xf

        # noinspection PyShadowingNames
        token = reduce(lambda r, i: (r << 8) | digest[digit + i], range(0, 4))
        token &= 0xffffdb

        rem = now % 30
        if 10 <= rem < 20:
            token |= 4
        elif 20 <= rem < 30:
            token |= 32

        token = token % 10000000
        token = str(token).zfill(7)

        return token
