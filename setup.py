#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import join, dirname
import gearmanadmin

setup(
    name='gearman-admin',
    version=gearmanadmin.__version__,
    description='Gearman admin command line interface',
    author='Vladimir Glafirov',
    author_email='vglafirov@gmail.com',
    url='https://github.com/vglafirov/gearman-admin',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            ['gearman-admin = gearmanadmin.shell:main']
    },
    install_requires=[
        'prettytable',
        'gearman'
    ],
    test_suite='tests',
)
