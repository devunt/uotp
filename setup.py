#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import with_statement


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='μOTP+',
    packages=['uotp'],
    version='0.0.1',
    description='The next generation OTP toolkit',
    url='https://github.com/devunt/uotp',
    download_url='',
    author='Bae Junehyeon',
    author_email='devunt' '@' 'gmail.com',
    license='Public Domain',
    py_modules=['uotp'],
    keywords=['otp'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: Korean',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
)
