import asyncore
from bterror import BTError
import time


class BTClientHandler(asyncore.dispatcher):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server

    def handle_read(self):

        try:
            data = self.recv(1024)
            if not data:
                return

        except Exception as e:
            print "[Connection Lost]",
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.handle_close()

    def handle_close(self):

        # remove this handler from server
        self.server.active_client_handlers.remove(self)

        # if this was the last connection, update disconnected time
        if len(self.server.active_client_handlers) is 0:
            self.server.disconnected_time = time.time()

        self.close()