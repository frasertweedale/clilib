# This file is part of clilib
# Copyright (C) 2012 Fraser Tweedale
#
# clilib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
clilib utility functions.
"""


def add_arg_to_parser(arg, parser):
    """Add the argument to the given parser.

    An argument may be a callable that takes as its argument the parser
    and mutates it in some fashion, or a tuple of length two containing
    a sequence and a mapping which will be used as the ``args`` and
    ``kwargs`` to an invocation of the parser's ``add_argument`` method.
    """
    if callable(arg):
        arg(parser)
    else:
        parser.add_argument(*arg[0], **arg[1])
