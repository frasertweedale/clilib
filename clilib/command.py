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

"""
CLI command classes.
"""

import argparse
import textwrap

from . import util


class Command(object):
    """A command object.

    Subclasses must implement ``__call__``, which takes no arguments.

    The short help is the first non-empty paragraph of the docstring
    of the command, and the epilog is the whole docstring excluding
    the first paragraph.
    """

    args = []
    """
    An array of (args, kwargs) tuples that will be used as arguments to
    ArgumentParser.add_argument().
    """

    @classmethod
    def add_parser(cls, subparsers):
        """Add a subparser for this command to a subparsers object."""
        name = cls.__name__.lower()
        parser = subparsers.add_parser(
            name,
            help=cls.help(),
            epilog=cls.epilog(),
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        for arg in cls.args:
            util.add_arg_to_parser(arg, parser)
        parser.set_defaults(command=cls)

    @classmethod
    def help(cls):
        return textwrap.dedent(cls.__doc__).split('\n\n')[0].strip()

    @classmethod
    def epilog(cls):
        return '\n\n'.join(
            textwrap.dedent(cls.__doc__).split('\n\n')[1:]
        ).strip()

    def __init__(self, args, parser, commands, aliases, config=None):
        """
        Initialse the command.

        ``args``
            an ``argparse.Namespace``
        ``parser``
            the ``argparse.ArgumentParser``
        ``commands``
            a mapping of all Command classes keyed by __name__.lower()
        ``aliases``
            a dict of aliases keyed by alias
        ``config``
            a ``ConfigParser.SafeConfigParser`` or ``None`` (the default)
        """
        self._args = args
        self._parser = parser
        self._commands = commands
        self._aliases = aliases
        self._config = config


class Config(Command):
    """Show or update configuration."""
    args = Command.args + [
        lambda x: x.add_argument(
            '--list', '-l', action='store_true',
            help='list all configuration options'),
        lambda x: x.add_argument(
            'name', nargs='?',
            help='name of option to show, set or remove'),
        lambda x: x.add_argument(
            '--remove', action='store_true',
            help='remove the specified option'),
        lambda x: x.add_argument(
            'value', nargs='?',
            help='set value of given option'),
    ]

    def __call__(self):
        if not self._config:
            raise UserWarning('Configuration not available.')
        args = self._args
        if args.list:
            for section in self._config.sections():
                for option, value in self._config.items(section):
                    print '{}={}'.format('.'.join((section, option)), value)
        elif not args.name:
            raise UserWarning('No configuration option given.')
        else:
            try:
                section, option = args.name.rsplit('.', 1)
            except ValueError:
                raise UserWarning('Invalid configuration option.')
            if not section or not option:
                raise UserWarning('Invalid configuration option.')

            if args.remove:
                # remove the option
                self._config.remove_option(section, option)
                if not self._config.items(section):
                    self._config.remove_section(section)
                self._config.write()
            elif args.value:
                # set new value
                if not self._config.has_section(section):
                    self._config.add_section(section)
                oldvalue = self._config.get(section, option) \
                    if self._config.has_option(section, option) else None
                self._config.set(section, option, args.value)
                self._config.write()
                print '{}: {} => {}'.format(args.name, oldvalue, args.value)
            else:
                curvalue = self._config.get(section, option)
                print '{}: {}'.format(args.name, curvalue)


class Help(Command):
    """Show help."""
    args = Command.args + [
        lambda x: x.add_argument(
            'subcommand', metavar='SUBCOMMAND', nargs='?',
            help='show help for subcommand'),
    ]

    def __call__(self):
        if not self._args.subcommand:
            self._parser.parse_args(['--help'])
        else:
            if self._args.subcommand in self._aliases:
                print "'{}': alias for {}".format(
                    self._args.subcommand,
                    self._aliases[self._args.subcommand]
                )
            elif self._args.subcommand not in self._commands:
                print "unknown subcommand: '{}'".format(self._args.subcommand)
            else:
                self._parser.parse_args([self._args.subcommand, '--help'])
