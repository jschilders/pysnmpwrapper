#!/usr/bin/env python
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pysnmpwrapper',
    version='0.0.1',
    description='Wrapper for pysnmp, to make life a little easier.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jos Schilders',
    author_email='jschilders@groomlake.nl',
    url='http://github.com/jschiilders/pysnmpwrapper/',
    license='LICENSE.txt',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords=['python', 'pysnmp', 'wrapper', 'snmp'],
    packages=['pysnmpwrapper'],
    python_requires='>=3.6, <4',
    install_requires=['pysnmp'],
)