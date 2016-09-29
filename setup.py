"""Setup file for ipapconsole."""

import os
from setuptools import setup, find_packages


def get_entry_points():
    return {"console_scripts": ["ipapconsole = ipapconsole:run"]}


def safe_read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except IOError:
        return ""

CLASSIFIERS = """\
Framework :: IPython
Intended Audience :: Developers
Intended Audience :: Science/Research
Programming Language :: Python
Topic :: System :: Shells
""".splitlines()

name = 'ipapconsole'
version = '0.0.1b1'
packages = find_packages()
entry_points = get_entry_points()
# TODO: ensure dependencies
# install_requires = ['pyIcePAP']
license = 'GPLv3'
classifiers = CLASSIFIERS
author = 'Guifre Cuni, Antonio Milan Otero'
author_email = 'gcuni@cells.es, antonio.milan_otero@maxiv.lu.se'
description = 'An interactive Icepap console'
long_description = safe_read('README.md')
# url = 'http://www.maxiv.lu.se'


setup(
    name=name,
    version=version,
    packages=packages,
    entry_points=entry_points,
    # install_requires=install_requires,
    license=license,
    classifiers=classifiers,
    author=author,
    author_email=author_email,
    description=description
)
