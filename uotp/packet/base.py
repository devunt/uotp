from binascii import unhexlify
from enum import Enum, unique
from hashlib import sha1, sha256
from random import choice
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
    Information = 402
    Time = 407
    Issue = 451
    ResetErrorCount = 452
    UseHistory = 453
    Help = 454


class Packet:
    OPCODE = None
    SIMPLE = False

    def __init__(self):
        self.status = Status.OK
        self.params = {}

        self.oid = ''

        self.shared_crypto_key = b''
        self.extra_token = b''

    def __call__(self):
        crypto_key = self.__get_crypto_key()

        s = socket()
        s.connect(('211.49.97.230', 20004))
        s.send(self.__to_bytes(crypto_key))

        s.recv(1)
        size = int(s.recv(5))
        data = s.recv(size)

        s.close()

        return self.__from_bytes(data, crypto_key)

    def __getitem__(self, item):
        return self.params[item]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __repr__(self):
        return '<Packet: {}>'.format(self.OPCODE)

    def set_oid(self, oid):
        self.oid = oid

    def set_encryption_info(self, shared_crypto_key: bytes = b'', extra_token: str = b''):
        if shared_crypto_key:
            self.shared_crypto_key = shared_crypto_key
        if extra_token:
            self.extra_token = '{:0>7} '.format(extra_token).encode()

    def __get_crypto_key(self) -> bytes:
        if self.shared_crypto_key:
            if self.extra_token:
                hasher = sha1()
                hasher.update(unhexlify(self.shared_crypto_key))
                hasher.update(self.extra_token)
                return hasher.digest()
            else:
                return self.shared_crypto_key
        else:
            return b''

    def __generate_payload_common_header(self) -> bytes:
        return '{: <3}{: <11}{: <16}{: <4}{:0>4}{:0>4}'.format(
            choice(('KTF', 'SKT', 'LGT')), self.oid,
            choice(('SM-G950S', 'SM-G955L', 'SM-G920K')), 'GA15', 2, 0
        ).encode()

    def __to_bytes(self, crypto_key: bytes = b'') -> bytes:
        payload = self._encode_payload(self.params)

        if not self.SIMPLE:
            payload = self.__generate_payload_common_header() + payload

        payload += self.extra_token

        if crypto_key and payload:
            payload = SEED.encrypt(crypto_key, payload)

        shared_key = self.shared_crypto_key.rjust(64, b' ')
        codes = '{:0>4}{:0>3}'.format(self.status.value, self.OPCODE.value).encode()

        body = shared_key + codes + payload
        header = 'S{:0>5}'.format(len(body)).encode()

        return header + body

    @classmethod
    def __from_bytes(cls, data: bytes, crypto_key: bytes = b'') -> 'Packet':
        self = Packet()

        shared_key, status, opcode = unpack('64s4s3s', data[:71])

        self.shared_crypto_key = unhexlify(shared_key.decode().rstrip(' '))

        try:
            self.status = Status(status.decode())
        except ValueError:
            self.status = Status.Error

        try:
            self.OPCODE = Opcode(int(opcode.decode()))
        except ValueError:
            self.OPCODE = Opcode.Error

        payload = data[71:]

        if self.shared_crypto_key or crypto_key:
            payload = SEED.decrypt(self.shared_crypto_key or crypto_key, payload)

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
