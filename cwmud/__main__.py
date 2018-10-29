# -*- coding: utf-8 -*-
"""The main entry point for server."""
# Part of Clockwork MUD Server (https://github.com/whutch/cwmud)
# :copyright: (c) 2018 Will Hutcheson
# :license: MIT (https://github.com/whutch/cwmud/blob/master/LICENSE.txt)

from .nanny import start_nanny

if __name__ == "__main__":  # pragma: no cover
    start_nanny()
