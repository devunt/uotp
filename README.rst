*****
μOTP+
*****

μOTP+ is the next generation OTP toolkit.


Installation
============

You will need Python 3.4 or higher in order to run ``uotp``.

.. code-block:: console

  $ pip install -U uotp


How to use μOTP+ as GUI application
===================================

Run ``uotp gui``.

.. code-block:: console

  $ uotp gui


How to use μOTP+ as CLI application
===================================

Just run ``uotp``.

.. code-block:: console

  $ uotp

μOTP+ will automatically issue a new account and sync time with the server for you.

Once you have successfully issued the new account, running ``uotp`` again will start giving you the OTP token.

For more information, see ``uotp --help``.


Configuration file
------------------

By default, a new configuration file will be automatically generated on ``~/.config/uotp/config.yml``.

This behaviour however can be overriden by passing ``--conf=/path/to/config.yml`` to ``uotp`` command or setting ``UOTP_CONF=/path/to/config.yml`` environment variable.

.. code-block:: console

  $ uotp --conf=uotp.yml new
  $ UOTP_CONF=uotp.yml uotp new


How to develop an application using μOTP+
=========================================

.. code-block:: python

  # Import everything
  from uotp import UOTP


  # Create an instance of UOTP
  uotp = UOTP


  # Issue a new account
  uotp.issue_account()
  print('S/N: ', uotp.account_serial_number)


  # Sync time with the server
  uotp.sync_time()


  # Get a new OTP token
  token = uotp.generate_token()
  print('Token: ', token)


License
=======

All proprietary materials are intellectual property of (C) 2004 - 2017 ATsolutions
