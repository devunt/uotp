from binascii import unhexlify
from struct import unpack

from .base import Packet, Opcode


class IssueRequest(Packet):
    def __init__(self):
        super().__init__()
        self.opcode = Opcode.Issue
        self.shared_key = self.generate_shared_key()

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        oid = ''
        ver1, ver2 = data['version']

        return '{: <3}{: <11}{: <16}{: <4}{:0>4}{:0>4}'.format(
            data['mno'], oid, data['hw_model'], data['hw_id'], ver1, ver2
        ).encode()

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
