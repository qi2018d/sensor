import asyncore
from bterror import BTError
from realtime import RealtimeProcessor

class BTClientHandler(asyncore.dispatcher):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher.__init__(self, socket)
        self.server = server
        self.sender = RealtimeProcessor(self)
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