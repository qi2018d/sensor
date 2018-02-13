import asyncore
from bterror import BTError
from realtime import RealtimeManager
import json

from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.2f')


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

class BTClientHandler(asyncore.dispatcher):
    """BT handler for client-side socket"""

    def __init__(self, socket, server, history):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server

        # send historical data if exists
        if history is not None:
            chunk_size = 5
            history_chunks = [history[i:i + chunk_size] for i in xrange(0, len(history), chunk_size)]

            for chunk in history_chunks:
                self.send(json.dumps({'type': 'historical', 'data': chunk}, sort_keys=True))

        # start to send real-time data
        self.sender = RealtimeManager(self)
        self.sender.start()

    def handle_read(self):

        try:
            data = self.recv(1024)

            if not data:
                return

        except Exception as e:
            # BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.handle_close()

    def handle_close(self):

        # request stop realtime thread and join it
        print "handle close"
        self.sender.stop()
        self.sender.join()

        # remove this handler from server
        self.server.active_client_handlers.remove(self)

        # if this handler is the final, start storing data
        if len(self.server.active_client_handlers) is 0:
            print "[DB] Final connection lost, start storing data to database"
            self.server.start_saving()

        self.close()