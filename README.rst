*****
μOTP+
*****

μOTP+ is the next generation OTP toolkit.


Installation
============

.. code-block:: console

  $ pip install -U uotp


How to use μOTP+ as cli application
===================================

Just run ``utop``.

.. code-block:: console

  $ uotp

μOTP+ will automatically issue a new account and sync time with the server for you.

Once you have successfully issued the new account, running ``uotp`` again will start giving you the OTP token.

For more information, see ``uotp --help``


Configuration file
------------------

By default, a new configuration file will be automatically generated on ``~/.config/uotp/config.yml``.

This behaviour however can be overriden by passing ``--conf=/path/to/config.yml`` to ``uotp`` command or setting `UOTP_CONF=/path/to/config.yml` environment variable.

.. code-block:: console

  $ uotp --conf=uotp.yml new
  $ UOTP_CONF=uotp.yml uotp new


How to develop an application using μOTP+
=========================================

.. code-block:: python

  # Import everything
  from uotp import OTPTokenGenerator, OTPUtil
  from uotp.packet import IssueRequest, TimeRequest


  # Issue a new account
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


  # Sync time with the server
  remote_now = TimeRequest()()['time']
  local_now = Util.now()

  timediff = remote_now - local_now


  # Get a new OTP token
  generator = OTPTokenGenerator(oid, seed)
  generator.compensate_time_deviation(timediff)
  token = generator.generate_token()

  print(Util.humanize(token, char=' ', each=3, maxgroup=2)


License
=======

All proprietary materials are intellectual property of (C) 2004 - 2017 ATsolutions