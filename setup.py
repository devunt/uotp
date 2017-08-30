from setuptools import setup, find_packages


with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='uotp',
    version='0.1.1',
    description='μOTP+: The next generation OTP toolkit',
    long_description=long_description,

    packages=find_packages(),

    author='Bae Junehyeon',
    author_email='devunt' '@' 'gmail.com',
    url='https://github.com/devunt/uotp',
    download_url='',
    license='Public Domain',

    python_requires='~=3.6',
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
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: Korean',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities',
    ],
)
