from setuptools import setup, find_packages


setup(
    name='uotp',
    version='0.0.1',
    packages=find_packages(),

    description='μOTP+: The next generation OTP toolkit',
    author='Bae Junehyeon',
    author_email='devunt' '@' 'gmail.com',
    url='https://github.com/devunt/uotp',
    download_url='',
    license='Public Domain',

    install_requires=[
        'click',
        'PyYAML'
    ],
    entry_points={
        'console_scripts': [
            'uotp = uotp.cli:cli',
        ]
    },

    keywords=['otp'],
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
