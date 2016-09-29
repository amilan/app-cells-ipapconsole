"""Setup file for ipapconsole"""

from setuptools import setup, find_packages


def get_entry_points():
    return {"console_scripts": ["ipapconsole = ipapconsole:run"]}

CLASSIFIERS = """\
Framework :: IPython
Intended Audience :: Developers
Intended Audience :: Science/Research
Programming Language :: Python
Topic :: System :: Shells
""".splitlines()

name = 'ipapconsole'
version = '0.0.1'
packages = find_packages()
entry_points = get_entry_points()
# TODO: ensure dependencies
# install_requires = ['pyIcePAP']
license = 'GPLv3'
classifiers = CLASSIFIERS
author = 'Guifre Cuni, Antonio Milan Otero'
author_email = 'gcuni@cells.es, antonio.milan_otero@maxiv.lu.se'
description = 'An interactive Icepap console'
long_description = open('README.md').read()
# url = 'http://maxiv.lu.se'


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
