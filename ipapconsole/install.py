#!/usr/bin/env python

# ----------------------------------------------------------------------------
# An IPython profile that provides a CLI to access an Icepap system.
# Copyright (C) 2016  MaxIV Laboratory.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------


from __future__ import with_statement

import os
import sys

import IPython

from IPython.core.profiledir import ProfileDirError, ProfileDir
from IPython.utils.io import ask_yes_no

try:
    from IPython.paths import get_ipython_dir
except ImportError:
    try:
        from IPython.utils.path import get_ipython_dir
    except ImportError:
        from IPython.genutils import get_ipython_dir

__PROFILE = """
#!/usr/bin/env python
\"\"\"An automaticaly generated IPython profile useful to configure an
Icepap system.
\"\"\"

# Protected block
{protected_block}

"""

__PROTECTED_BLOCK = """
import ipapconsole
config = get_config()
ipapconsole.load_config(config)
"""

__CONFIG_FILE_NAME = 'ipython_config.py'


def is_installed(ipydir=None, profile='ipapconsole'):
    ipython_dir = ipydir or get_ipython_dir()
    try:
        p_dir = ProfileDir.find_profile_dir_by_name(ipython_dir, profile)
    except ProfileDirError:
        return False
    abs_config_file_name = os.path.join(p_dir.location, __CONFIG_FILE_NAME)
    if not os.path.isfile(abs_config_file_name):
        return False
    with open(abs_config_file_name) as f:
        return __PROTECTED_BLOCK in f.read()


def install(ipydir=None, verbose=True, profile='ipapconsole'):
    if verbose:
        def out(msg):
            sys.stdout.write(msg)
            sys.stdout.flush()
    else:
        out = lambda x: None

    ipython_dir = ipydir or get_ipython_dir()
    try:
        p_dir = ProfileDir.find_profile_dir_by_name(ipython_dir, profile)
    except ProfileDirError:
        p_dir = ProfileDir.create_profile_dir_by_name(ipython_dir, profile)
    abs_config_file_name = os.path.join(p_dir.location, __CONFIG_FILE_NAME)
    create_config = True
    if os.path.isfile(abs_config_file_name):
        msg = "Ipapconsole configuration file {0} already exists.\n"
        msg += "Do you wish to replace it (y/n)?"
        msg = msg.format(abs_config_file_name)
        create_config = ask_yes_no(msg, default='y')

    if not create_config:
        return

    out("Installing ipapconsole extension to ipython... ")

    profile = __PROFILE.format(protected_block=__PROTECTED_BLOCK)

    with open(abs_config_file_name, "w") as f:
        f.write(profile)
        f.close()
    out("[DONE]\n\n")
    out("""\
To start ipython with ipapconsole interface simply type on the command line:
%% ipython --profile=ipapconsole
""")


def main():
    d = None
    if len(sys.argv) > 1:
        d = sys.argv[1]
    install(d)


if __name__ == "__main__":
    main()
