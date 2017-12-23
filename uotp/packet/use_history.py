from datetime import datetime
from struct import unpack_from

from .base import Packet, Opcode


class UseHistoryRequest(Packet):
    OPCODE = Opcode.UseHistory

    @classmethod
    def _encode_payload(cls, data: dict) -> bytes:
        # [period] 1: 3 days / 2: 1 week / 3: 1 month
        return '{:0>4}{: <1}'.format(
            data['page'], data['period']
        ).encode()

    @classmethod
    def _decode_payload(cls, payload: bytes) -> dict:
        date_start, date_end, = map(lambda x: datetime.strptime(x.decode(), '%Y-%m-%d'), unpack_from('!10s10s', payload, 0))
        page_total, page_current, data_count = map(lambda x: int(x), unpack_from('!4s4s2s', payload, 20))

        entries = []
        offset = 30
        for i in range(data_count):
            date, time, typ, name = unpack_from('!10s8s40s40s', payload, offset)
            entries.append({
                'datetime': datetime.strptime((date + time).decode(), '%Y-%m-%d%H:%M:%S'),
                'type': typ.decode('cp949').strip(),
                'name': name.decode('cp949').strip(),
            })

            offset += 98

        return {
            'period': {
                'start': date_start,
                'end': date_end,
            },
            'page': {
                'total': page_total,
                'current': page_current,
            },
            'entries': entries,
        }
