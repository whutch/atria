# -*- coding: utf-8 -*-
"""Rooms and areas, the virtual space of the MUD."""
# Part of Atria MUD Server (https://github.com/whutch/atria)
# :copyright: (c) 2008 - 2016 Will Hutcheson
# :license: MIT (https://github.com/whutch/atria/blob/master/LICENSE.txt)

import re
from weakref import WeakSet

from .entities import Attribute, ENTITIES, Entity, Unset
from .logs import get_logger
from .pickle import PickleStore
from .storage import STORES
from .utils.funcs import joins


log = get_logger("world")


@ENTITIES.register
class Room(Entity):

    """A MUD room.  Where the magic happens."""

    _store = STORES.register("rooms", PickleStore("rooms"))
    # _store_key moved below due to referenced functions.
    _uid_code = "R"

    def __init__(self, data=None, active=False, savable=True):
        super().__init__(data, active, savable)
        self._chars = WeakSet()  # The Characters currently in this room.

    def __repr__(self):
        name = self.name if self.name else "(unnamed)"
        return joins("Room<", name, ":", self.get_coord_str(), ">", sep="")

    @property
    def chars(self):
        """Return this room's character set.

        You shouldn't need to add or remove Characters from this set directly,
        it is done automatically when the Character.room attribute is changed.

        """
        return self._chars

    @property
    def coords(self):
        """Return a tuple of this room's x,y,z coordinates."""
        return self.x, self.y, self.z

    def get_coord_str(self):
        """Return a string representing the coordinates for this room.

        :returns str: The coordinate string

        """
        if self.x is Unset or self.y is Unset or self.z is Unset:
            return Unset
        return "{},{},{}".format(self.x, self.y, self.z)

    def set_coord_from_str(self, coord_str):
        """Set this room's coordinates given a string.

        :param str coord_str: A string of coordinates in the form "x,y,z"
        :returns None:

        """
        # noinspection PyAttributeOutsideInit
        self.x, self.y, self.z = map(int, coord_str.split(","))

    _store_key = ("coords", get_coord_str, set_coord_from_str)

    def get_exits(self):
        """Return the rooms this room connects to.

        :returns dict: The connecting rooms, keyed by direction name

        """
        # This is an inefficient placeholder until an Exit type is in.
        found = {}
        for change, (dir_name, rev_name) in _movement_strings.items():
            x, y, z = map(sum, zip(self.coords, change))
            room = Room.find("x", x, "y", y, "z", z, n=1)
            if room:
                found[dir_name] = room
        return found


@Room.register_attr("name")
class RoomName(Attribute):

    """The name of a room."""

    _min_len = 1
    _max_len = 60
    _valid_chars = re.compile(r"^[a-zA-Z ]+$")
    default = "An Unnamed Room"

    @classmethod
    def _validate(cls, new_value):
        if (not isinstance(new_value, str) or
                not cls._valid_chars.match(new_value)):
            raise ValueError("Room names can only contain letters and spaces.")
        name_len = len(new_value)
        if name_len < cls._min_len or name_len > cls._max_len:
            raise ValueError(joins("Room names must be between",
                                   cls._min_len, "and", cls._max_len,
                                   "characters in length."))
        new_value = new_value.title()
        return new_value


@Room.register_attr("description")
class RoomDescription(Attribute):

    """The description of a room."""

    default = "A nondescript room."

    @classmethod
    def _validate(cls, new_value):
        if not isinstance(new_value, str):
            raise ValueError("Room descriptions must be strings.")
        return new_value


@Room.register_attr("x")
class RoomX(Attribute):

    """The X coordinate of a room."""

    _min_val = -1000
    _max_val = 1000

    @classmethod
    def _validate(cls, new_value):
        if not isinstance(new_value, int):
            raise ValueError("Room coordinates must be integers.")
        return new_value


@Room.register_attr("y")
class RoomY(Attribute):

    """The Y coordinate of a room."""

    _min_val = -1000
    _max_val = 1000

    @classmethod
    def _validate(cls, new_value):
        if not isinstance(new_value, int):
            raise ValueError("Room coordinates must be integers.")
        return new_value


@Room.register_attr("z")
class RoomZ(Attribute):

    """The Z coordinate of a room."""

    _min_val = -1000
    _max_val = 1000

    @classmethod
    def _validate(cls, new_value):
        if not isinstance(new_value, int):
            raise ValueError("Room coordinates must be integers.")
        return new_value


# These are used to generate Character.act messages.
_movement_strings = {
    (1, 0, 0): ("east", "the west"),
    (-1, 0, 0): ("west", "the east"),
    (0, 1, 0): ("north", "the south"),
    (0, -1, 0): ("south", "the north"),
    (0, 0, 1): ("up", "below"),
    (0, 0, -1): ("down", "above"),
    (1, 1, 0): ("northeast", "the southwest"),
    (-1, 1, 0): ("northwest", "the southeast"),
    (1, -1, 0): ("southeast", "the northwest"),
    (-1, -1, 0): ("southwest", "the northeast"),
}


def get_movement_strings(change):
    """Return a pair of strings to describe bi-directional character movement.

    :param tuple<int,int,int> change: A tuple of the (x,y,z) change
    :returns tuple<str,str>: The relevant to and from strings

    """
    return _movement_strings.get(change, ("nowhere", "nowhere"))
