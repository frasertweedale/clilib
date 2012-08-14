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

import unittest

from . import command


class CommandTestCase(unittest.TestCase):
    """Test Command base class methods."""

    def test_one_line(self):
        class Bogo(command.Command):
            """Simple"""

        instance = Bogo('fake', 'fake', 'fake', 'fake')
        self.assertEqual(instance.help(), "Simple")
        self.assertEqual(instance.epilog(), "")

    def test_paras_dedent_first(self):
        """Indent-to-newline should not cause problems."""
        class Bogo(command.Command):
            """No newline.
            
            <--- There is whitespace to here on previous line.
            """

        instance = Bogo('fake', 'fake', 'fake', 'fake')
        self.assertEqual(instance.help(), "No newline.")
        self.assertEqual(
            instance.epilog(),
            "<--- There is whitespace to here on previous line."
        )

    def test_paras_inline_summary(self):
        class Bogo(command.Command):
            """No newline.

            Second para.
            """

        instance = Bogo('fake', 'fake', 'fake', 'fake')
        self.assertEqual(instance.help(), "No newline.")
        self.assertEqual(instance.epilog(), "Second para.")

    def test_paras_newline_summary(self):
        class Bogo(command.Command):
            """
            Newline.

            Second para.

            Third para."""

        instance = Bogo('fake', 'fake', 'fake', 'fake')
        self.assertEqual(instance.help(), "Newline.")
        self.assertEqual(instance.epilog(), "Second para.\n\nThird para.")
