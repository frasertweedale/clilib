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
Simple command line interface library.

Commands
========

Command classes inherit from ``clilib.Command``, and must be
implemented to conform to the following protocol:

Arguments
---------

Arguments are specified but the ``args`` attribute of the command
class, which is a sequence of:

- callables that take an ``argparse.ArgumentParser`` as their sole
  argument and perform some action on that parser (e.g., adding
  an argument), or,
- pairs that contain a sequence of positional args followed by a
  mapping of keyword args that will be used as the arguments to
  ``argparse.ArgumentParser.add_argument``.

The sequence may contain a mix of callables and tuples.

``__call__``
------------

The ``__call__`` method must be implemented and must take no
arguments (apart from the invocant).  The command object is called
to invoke its functionality.

Pre-set attributes
------------------

The following attributes are set on a command object prior to the
object being called to invoke its functionality:

``_args``
  The ``argparse.Namespace`` corresponding to the arguments to the
  command.  There are either the arguments given on the command
  line or default arguments.
``_parser``
  The ``argparse.ArgumentParser``.
``_commands``
  A mapping of all command classes keyed by (lower case) name.
``aliases``
  A mapping of command aliases keyed by alias.
``config``
  A ``ConfigParser.SafeConfigParser`` object or ``None`` (the default).

In most circumstances, only the ``_args`` attribute will be
required.  The others are mainly used in the implementations of
advanced commands like the built-in ``Help`` and ``Config``
commands.


Dispatcher
==========

Commands are registered to a ``Dispatcher`` instance.  The command
line parsing and dispatching is accomplished by calling the
dispatcher's ``dispatch`` method, which takes no arguments.

Global arguments (arguments to be applied to every command) are
given as a sequence of command arguments (see above) to the
``global_args`` keyword parameter of the ``Dispatcher`` constructor.

A ``Config`` object may also be given via the ``config`` keyword
argument.


Config
======

A class defining and providing read and write access to a
configuration file can be defined by extending ``clilib.Config``

The following methods are required to be implemented by subclasses:

``check_section``
  Given a section name (the only argument), return the input
  if the section is valid, otherwise raise ``UserWarning``.


Caveats and limitations
=======================

CLI commands are the names of command classes lower-cased.  The
behavoiur when there are two or more classes with the same name
(when lower-cased) on the same dispatcher is undefined.  Don't do
that.


Examples
========

The following program is a basic calculator program providing
the commands "add" and "sub", and a "--radix" argument for
doing arithmetic in bases other than 10 (e.g. binary)::

    import clilib


    class CalculatorCommand(clilib.Command):
        args = [
            (['--radix'], dict(type=int)),
            (['inputs'], dict(type=int, nargs='+')),
        ]

        def __call__(self):
            if self._args.radix:
                mapper = lambda x: int(str(x), self._args.radix)
            else:
                mapper = lambda x: int(x)
            inputs = (mapper(x) for x in self._args.inputs)
            print reduce(self._reduce, inputs)


    class Add(CalculatorCommand):
        \"\"\"Add values.\"\"\"
        def _reduce(self, a, b):
            return a + b


    class Sub(CalculatorCommand):
        \"\"\"Subtract values.\"\"\"
        def _reduce(self, a, b):
            return a - b


    dispatcher = clilib.Dispatcher()
    dispatcher.add_command(Add)
    dispatcher.add_command(Sub)
    dispatcher.dispatch()

"""

from .clilib import *

version_info = (0, 0, 1, 'dev', 0)

version_fmt = '{0}.{1}'
if version_info[2]:
    version_fmt += '.{2}'
if version_info[3] != 'final':
    version_fmt += '{3}{4}'
version = version_fmt.format(*version_info)
