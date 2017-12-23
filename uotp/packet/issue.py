from binascii import unhexlify
from struct import unpack

from .base import Packet, Opcode


class IssueRequest(Packet):
    OPCODE = Opcode.Issue

    def __init__(self):
        super().__init__()
        self.set_encryption_info(self.generate_shared_key())

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        return b''

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        serial_number, oid, seed, user_hash, issue_info = map(lambda x: x.strip(), unpack('!20s11s40s64s80s', payload))

        return {
            'oid': int(oid),
            'seed': unhexlify(seed),
            'serial_number': serial_number.decode(),
            'user_hash': user_hash,
            'issue_info': issue_info,
        }
