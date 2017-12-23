from .packet import IssueRequest, ResetErrorCountRequest, TimeRequest, UseHistoryRequest
from .token import OTPTokenGenerator, OTPUtil


class UOTP:
    def __init__(self, _id: str = '', oid: int = None, seed: bytes = None, serial_number: str = None):
        self.__account = {
            'id': _id.encode(),
            'oid': oid,
            'seed': seed,
            'serial_number': serial_number,
        }
        self.__generator = OTPTokenGenerator(self.account_oid, self.account_seed)
        self.__timediff = 0

    def generate_token(self) -> str:
        self.__generator.compensate_time_deviation(self.__timediff)
        return self.__generator.generate_token()

    def sync_time(self, timediff=None) -> bool:
        try:
            if timediff is None:
                time = TimeRequest()()['time']
                timediff = time - OTPUtil.now()
        except RuntimeError:
            return False
        else:
            self.__timediff = timediff
            return True

    def issue_account(self) -> bool:
        try:
            resp = IssueRequest()()
            self.__account = {
                'id': resp['user_hash'],
                'oid': resp['oid'],
                'seed': resp['seed'],
                'serial_number': OTPUtil.humanize(resp['serial_number'], char='-', each=4)
            }
        except RuntimeError:
            return False
        else:
            self.__generator = OTPTokenGenerator(self.account_oid, self.account_seed)
            return True

    def reset_error(self) -> bool:
        try:
            req = ResetErrorCountRequest()
            req.set_oid(self.account_oid)
            req.set_encryption_info(self.__account['id'], self.generate_token())
            req()
        except RuntimeError:
            return False
        else:
            return True

    def get_history(self, page=1) -> dict:
        req = UseHistoryRequest()
        req.set_oid(self.account_oid)
        req.set_encryption_info(self.__account['id'], self.generate_token())
        req['page'] = page
        req['period'] = 3
        return req().params

    @property
    def account_id(self):
        return self.__account['id'].decode()

    @property
    def account_oid(self):
        return self.__account['oid']

    @property
    def account_seed(self):
        return self.__account['seed']

    @property
    def account_serial_number(self):
        return self.__account['serial_number']
