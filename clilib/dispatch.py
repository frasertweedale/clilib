# This file is part of clilib
# Copyright (C) 2011, 2012 Fraser Tweedale
# Copyright (C) 2011, 2012 Benon Technologies Pty Ltd
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


import argparse

from . import command
from . import util


class Dispatcher(object):
    """Dispatcher class."""
    __slots__ = ['_commands', '_config', '_global_args']

    def __init__(
        self,
        config=None,
        global_args=(),
        with_help=True,
        with_config=False,
    ):
        """Initialise the dispatcher.

        ``config``
          A ConfigParser.SafeConfigParser.  The "alias" section is used
          by the dispatcher.
        ``global_args``
          Iterable of global argument specifications.
        ``with_help``
          Whether to provide the built-in "help" command.  Defaults
          to ``True``.
        ``with_config``
          Whether to provide the built-in "config" command.
          Defaults to ``False``.
        """
        self._config = config
        self._global_args = global_args
        self._commands = set()

        if with_help:
            self.add_command(command.Help)
        if with_config:
            self.add_command(command.Config)

    def add_command(self, cmd):
        """Add the given ``Command`` to this ``Dispatcher``."""
        if not issubclass(cmd, command.Command):
            raise TypeError(
                '{} is not an instance of {}'.format(cmd, command.Command)
            )
        self._commands.add(cmd)

    def aliases(self):
        return dict(self._config.items('alias')) \
            if self._config and self._config.has_section('alias') else {}

    def epilog(self):
        """Format an epilog showing the aliases."""
        lines = [
            "    {:20}{}".format(alias, target)
            for alias, target in sorted(self.aliases().viewitems())
        ]
        return 'user-defined aliases:\n' + '\n'.join(lines) if lines else None

    def dispatch(self):
        # create an argument parser
        parser_1 = argparse.ArgumentParser(add_help=False)

        # add global arguments
        for arg in self._global_args:
            util.add_arg_to_parser(arg, parser_1)

        # parse known args
        args, argv = parser_1.parse_known_args()

        # add subcommands
        parser_2 = argparse.ArgumentParser(
            parents=[parser_1],
            description='Perform evidence based scheduling.',
            epilog=self.epilog(),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        subparsers = parser_2.add_subparsers(title='subcommands')
        commands = {x.__name__.lower(): x for x in self._commands}
        for name in sorted(commands):
            commands[name].add_parser(subparsers)

        # process user-defined aliases
        aliases = self.aliases()
        for i, arg in enumerate(argv):
            if arg in aliases:
                # an alias; replace and stop processing
                argv[i:i + 1] = aliases[arg].split()
                break
            if arg in commands:
                # a valid command; stop processing
                break

        # parse remaining args
        args = parser_2.parse_args(args=argv, namespace=args)

        # execute command
        args.command(
            args=args,
            parser=parser_2,
            commands=commands,
            aliases=aliases,
            config=self._config
        )()
