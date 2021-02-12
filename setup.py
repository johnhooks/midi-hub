"""Setup tool for the midi-hub
Created by John Hooks
Febuary 2021
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='midi-hub',
    version='0.1.1',
    license='GNU',
    url='https://github.com/johnhooks/midi-hub',
    author='John Hooks',
    author_email='bitmachina@outlook.com',
    description='A script to connect all USB MIDI devices on a Raspberry Pi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    install_requires=[],
)
