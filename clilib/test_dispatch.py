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

import collections
import re
import unittest

from . import command
from . import dispatch


class DispatchTestCase(unittest.TestCase):

    def test_epilog_no_aliases(self):
        class BogoDispatcher(dispatch.Dispatcher):
            def aliases(self):
                return {}

        disp = BogoDispatcher()
        self.assertIsNone(disp.epilog())

    def test_epilog_two_aliases(self):
        class BogoDispatcher(dispatch.Dispatcher):
            def aliases(self):
                # OrderedDict to make sure that sorting happens
                return collections.OrderedDict(
                    reop='update --status REOPENED',
                    close='update --status CLOSED',
                )

        disp = BogoDispatcher()
        regexp = re.compile(
            r'''
                user-defined \s aliases: \n
                \s* close \s* update \s --status \s CLOSED \n
                \s* reop \s* update \s --status \s REOPENED
            ''',
            re.VERBOSE
        )
        self.assertRegexpMatches(disp.epilog(), regexp)

    def test_init_default_command(self):
        """With no args, only Help command is initially present."""
        disp = dispatch.Dispatcher()
        self.assertSetEqual(disp._commands, set([command.Help]))

    def test_init_with_help(self):
        """Test that ``with_help`` adds the help command."""
        disp = dispatch.Dispatcher(with_help=True)
        self.assertIn(command.Help, disp._commands)

    def test_init_without_help(self):
        disp = dispatch.Dispatcher(with_help=False)
        self.assertNotIn(command.Help, disp._commands)

    def test_init_with_config(self):
        disp = dispatch.Dispatcher(with_config=True)
        self.assertIn(command.Config, disp._commands)

    def test_init_without_config(self):
        disp = dispatch.Dispatcher(with_config=False)
        self.assertNotIn(command.Config, disp._commands)

    def test_init_empty_command_set(self):
        disp = dispatch.Dispatcher(with_help=False, with_config=False)
        self.assertSetEqual(disp._commands, set())

    def test_add_command(self):
        class Command1(command.Command):
            pass

        class Command2(command.Command):
            pass

        class NotACommand(object):
            pass

        disp = dispatch.Dispatcher(with_help=False, with_config=False)

        disp.add_command(Command1)
        self.assertSetEqual(disp._commands, set([Command1]))

        # add same command = idempotent
        disp.add_command(Command1)
        self.assertSetEqual(disp._commands, set([Command1]))

        disp.add_command(Command2)
        self.assertSetEqual(disp._commands, set([Command1, Command2]))

        with self.assertRaises(TypeError):
            disp.add_command(NotACommand)
