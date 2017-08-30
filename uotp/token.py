from functools import reduce
from hashlib import sha1

from .util import OTPUtil


class OTPTokenGenerator:
    def __init__(self, oid: int, seed: bytes):
        self.__oid = oid
        self.__seed = seed
        self.__timediff = 0

    def compensate_time_deviation(self, timediff: int):
        self.__timediff = timediff

    def generate_token(self) -> str:
        now = OTPUtil.now()
        now += self.__timediff

        time = now // 10
        oid = self.__oid

        acc_seed = bytearray(11)
        time_seed = bytearray(11)

        for i in reversed(range(11)):
            acc_seed[i] = int(oid) & 255
            time_seed[i] = int(time) & 255

            oid >>= 8
            time >>= 8

        acc_seed += self.__seed

        acc_seed_0 = bytearray(64)
        acc_seed_0[:20] = sha1(acc_seed).digest()

        acc_seed_1 = acc_seed_0[:]
        acc_seed_2 = acc_seed_0[:]

        for i in range(64):
            acc_seed_1[i] ^= 54
            acc_seed_2[i] ^= 92

        digest = sha1(acc_seed_1 + time_seed).digest()
        digest = sha1(acc_seed_2 + digest).digest()

        digit = digest[-1] & 0xf

        # noinspection PyShadowingNames
        token = reduce(lambda r, i: (r << 8) | digest[digit + i], range(4))
        token &= 0xffffdb

        rem = now % 30
        if 10 <= rem < 20:
            token |= 4
        elif 20 <= rem < 30:
            token |= 32

        token = token % 10000000
        token = str(token).zfill(7)

        return token
