# -*- coding: utf-8 -*-
"""Configuration for testing through py.test."""
# Part of Clockwork MUD Server (https://github.com/whutch/cwmud)
# :copyright: (c) 2008 - 2016 Will Hutcheson
# :license: MIT (https://github.com/whutch/cwmud/blob/master/LICENSE.txt)

from os.path import abspath, dirname, join
import sys
import time

import redis

# Until Clockwork is an installable package, we need to add it to our Python
# path so that we can do "from cwmud" imports in the tests.
TEST_ROOT = dirname(abspath(__file__))
sys.path.insert(0, dirname(TEST_ROOT))

from cwmud import ROOT_DIR, settings


# Change the log path during testing.
settings.LOG_PATH = join(ROOT_DIR, "logs", "test.log")

# Change the data path during testing.
settings.DATA_DIR = join(ROOT_DIR, ".cache", "data")

settings.BIND_ADDRESS = "localhost"
# Use a different listen port, in case the tests are run while a
# real server is running on the same system.
settings.BIND_PORT = 4445

# Make sure the idle times are defaults
settings.IDLE_TIME = 180
settings.IDLE_TIME_MAX = 600

# Clear out the contrib modules
settings.INCLUDE_MODULES = []

from cwmud.core.logs import get_logger

log = get_logger("tests")


# Send out a message to signal the starts of a test run.
rdb = redis.StrictRedis(decode_responses=True)
rdb.publish("tests-start", time.time())
log.debug("====== TESTS START ======")
