"""
Test custom Django management commands.
"""
from unittest.mock import patch

"""
Mock behaviour of database because we need to stimulate
When the database is returning or not
"""
from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db if db ready"""
        patched_check.return_value = True

        # execute code and check
        call_command('wait_for_db')
        # check that check function has been called with database=[..] parameter
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationError."""
        # This for raise exeption
        # side_effect allow to pass in various different items that get handle # depend on that type
        # if pass E => mock lib raise that E, if pass boolean,  it return boolean value
        # this allow to define various different values that happen each time call it in the order that it'scalled
        patched_check.side_effect = [Psycopg2Error] * 2 + \
                                    [OperationalError] * 3 + [True]
        # get True back after 6 times
        call_command('wait_for_db')
        self.assertEquals(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
