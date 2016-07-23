# encoding=utf8

""" The elastic setup script
    Author: lipixun
    Created Time : 三  1/20 20:11:05 2016

    File Name: setup.py
    Description:

"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from setuptools import setup, find_packages

requirements = [ x.strip() for x in open('requirements.txt').readlines() ]

setup(
    name = 'pyelastic',
    author = 'lipixun',
    author_email = 'lipixun@outlook.com',
    url = 'https://github.com/lipixun/pyelastic',
    packages = find_packages(),
    package_data = {
        'elastic': [
            'VERSION'
        ] },
    install_requires = requirements,
    description = 'The elastic lib',
    long_description = open('README.md').read(),
)

