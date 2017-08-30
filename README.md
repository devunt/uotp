# μOTP+
μOTP+ is the next generation OTP toolkit.

## Installation
```shell
$ pip install -U uotp
```

## How to use as cli application
### Issue a new OTP account
```
$ uotp new
Time synchronized with the remote server (offset: -2sec).
A new account has been issued successfully.

Serial Number: 1734-9041-9316
```

### Get a new OTP token
```
$ uotp get
OTP Token: 364 8913
```

### Sync the time with server
```
$ uotp sync
Time synchronized with the remote server (offset: 1sec).
```

### Configuration file
By default, a new configuration file will be generated on `~/.config/uotp/config.yml`.
This behaviour can be overriden by passing `--conf=/path/to/config.yml` to `uotp` commands or setting `UOTP_CONF=/path/to/config.yml` environment variable.
```
$ uotp --conf=uotp.yml new
$ UOTP_CONF=uotp.yml uotp new
```

## How to use as python module
### Import everything
```python
from uotp import OTPTokenGenerator, OTPUtil
from uotp.packet import IssueRequest, TimeRequest
```

### Issue a new OTP account
```python
req = IssueRequest()
req['mno'] = 'KTF'
req['hw_id'] = 'GA15'
req['hw_model'] = 'SM-N900P'
req['version'] = (2, 0)

resp = req()
oid = resp['oid']
seed = resp['seed']
serial_number = resp['serial_number']

print(Util.humanize(serial_number, char='-', each=4))
```

### Sync the time with server
```python
remote_now = TimeRequest()()['time']
local_now = Util.now()

timediff = remote_now - local_now
```


### Get a new OTP token
```python
generator = OTPTokenGenerator(oid, seed)
generator.compensate_time_deviation(timediff)
token = generator.generate_token()

print(Util.humanize(token, char=' ', each=3, maxgroup=2)
```
