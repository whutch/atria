# -*- coding: utf-8 -*-
"""Tests for the server's main entry point."""
# Part of Clockwork MUD Server (https://github.com/whutch/cwmud)
# :copyright: (c) 2018 Will Hutcheson
# :license: MIT (https://github.com/whutch/cwmud/blob/master/LICENSE.txt)

import cwmud.nanny as nanny


class TestMain:

    """A collection of tests for the server's nanny process."""

    def test_main(self):
        """There's nothing to test yet."""
        nanny.start_nanny()
