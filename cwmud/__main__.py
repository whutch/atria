# -*- coding: utf-8 -*-
"""The main entry point for server."""
# Part of Clockwork MUD Server (https://github.com/whutch/cwmud)
# :copyright: (c) 2018 Will Hutcheson
# :license: MIT (https://github.com/whutch/cwmud/blob/master/LICENSE.txt)

import asyncio

###from .nanny import start_listeners, start_nanny
from .core.logs import get_logger

LOG = get_logger()
LOOP = asyncio.get_event_loop()


'''

SERVER STRUCTURE



[ TELNET SERVERS (Client) ] <--------------> [ SESSION SERVERS (Session) ] <-------> [ INSTANCE SERVER (Character/RegionInstance) ] <-----> [ WORLD SERVER (World/Region) ]
                                     |                                                                                                                      |
[ WEBSOCKET SERVERS (Client) ] <-----/                                                                                                           [ GENERATION SERVER ]


package should be structured so that you point the server to a
game module/working directory and that is where all config is loaded
and where logs and data are kept so no settings/state need to be
edited in the actual cwmud package

dump "game" package, can maintain an example game as a separate project with settings file and everything



TIME MANAGER THING

- "flex" tasks, have a specified amount of time, but prior tasks that finish early/late will add/take time from the next flex task
    - marking a task done before its due time (outside a small grace period) moves all subsequent static tasks up in the schedule until the next flex task, which adds time to the start
    - marking a task done after its due time (again, outside the grace period) moves all subsequent static tasks down in the schedule until the next flex task, which takes time from the start


'''


'''
import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
'''


''' SHARDING

- Any number of login/client servers.
    - Login servers pass oauth sessions around to the game servers?
- Any number of game servers.
- A client can be moved seamlessly from one game server to another.
    - Their connection stays with the client server and their messages get sent to a different game server.
- Controller server keep a registry of regions and which game servers contain which regions.


'''


class Client:
    pass


class ClientManager:
    pass


class ClientServer:

    protocol = None

    def __init__(self):
        pass


class Protocol:

    def read():
        pass

    def write():
        pass


class TelnetProtocol(ClientProtocol):
    pass


class TelnetServer(ClientServer):
    
    protocol = TelnetProtocol


class UDPProtocol(asyncio.DatagramProtocol):

    def __init__(self, message_handler):
        self.message_handler = message_handler

    def datagram_received(self, data, addr):
        msg = data.decode()
        LOOP.create_task(self.message_handler(msg))

    @classmethod
    def create(cls):
        return cls(handle_message)


def handle_exception(loop, context):
    print(context)


def run():
    # Start the event loop.
    try:
        LOOP.set_exception_handler(handle_exception)
        LOOP.run_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    ###start_listeners()
    ###start_nanny()
    run()
