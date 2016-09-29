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


__all__ = ["install",
           "load_ipython_extension",
           "load_config",
           "run"]

from install import install
from ipapconsole import load_ipython_extension
from ipapconsole import load_config, run
