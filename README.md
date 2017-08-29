# μOTP+
μOTP+ is the next generation OTP toolkit.

## How to use
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
local_now = Util.now()
remote_now = TimeRequest()()['time']

timediff = remote_now - local_now
```


### Generate a new OTP token
```python
generator = OTPTokenGenerator(oid, seed)
generator.compensate_time_deviation(timediff)
token = generator.generate_token()

print(Util.humanize(token, char=' ', each=3, maxgroup=2)
```
