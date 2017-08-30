from binascii import unhexlify
from enum import Enum, unique
from hashlib import sha256
from socket import socket
from struct import pack, unpack

from ..seed import SEED
from ..util import OTPUtil


@unique
class Status(Enum):
    OK = '0000'
    C002 = 'C002'
    S003 = 'S003'
    Error = -1


@unique
class Opcode(Enum):
    Error = -1
    Time = 407
    Issue = 451
    ResetErrorCount = 452


class Packet:
    def __init__(self):
        self.opcode = None
        self.status = Status.OK
        self.shared_key = b''
        self.params = {}

    def __call__(self):
        crypt_key = self.shared_key

        s = socket()
        s.connect(('211.49.97.230', 20004))
        s.send(self.__to_bytes(crypt_key))

        s.recv(1)
        size = int(s.recv(5))
        data = s.recv(size)

        s.close()

        return self.__from_bytes(data, crypt_key)

    def __getitem__(self, item):
        return self.params[item]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __repr__(self):
        return '<Packet: {}>'.format(self.opcode)

    def __to_bytes(self, crypt_key: bytes = b'') -> bytes:
        payload = self._encode_payload(self.params)

        if crypt_key and payload:
            payload = SEED.encrypt(crypt_key, payload)

        shared_key = self.shared_key.rjust(64, b' ')
        codes = '{:0>4}{:0>3}'.format(self.status.value, self.opcode.value).encode()

        body = shared_key + codes + payload
        header = 'S{:0>5}'.format(len(body)).encode()

        return header + body

    @classmethod
    def __from_bytes(cls, data: bytes, crypt_key: bytes = b'') -> 'Packet':
        self = Packet()

        shared_key, status, opcode = unpack('64s4s3s', data[:71])

        self.shared_key = unhexlify(shared_key.decode().rstrip(' '))

        try:
            self.status = Status(status.decode())
        except ValueError:
            self.status = Status.Error

        try:
            self.opcode = Opcode(int(opcode.decode()))
        except ValueError:
            self.opcode = Opcode.Error

        payload = data[71:]

        if self.shared_key or crypt_key:
            payload = SEED.decrypt(self.shared_key or crypt_key, payload)

        if self.status is not Status.OK:
            raise RuntimeError(self.status, payload.decode('euc-kr'))

        self.params = cls._decode_payload(payload)

        return self

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        raise NotImplementedError

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        raise NotImplementedError

    @staticmethod
    def generate_shared_key() -> bytes:
        return sha256(pack('!I', OTPUtil.now())).hexdigest().encode()
