import asyncore
from bluetooth import *
from bthandler import BTClientHandler
from historical import HistoricalProcessor

class BTServer(asyncore.dispatcher):
    """Asynchronous Bluetooth  Server"""

    def __init__(self, uuid, service_name, port=PORT_ANY):
        asyncore.dispatcher.__init__(self)

        if not is_valid_uuid(uuid):
            raise ValueError("uuid %s is not valid" % uuid)

        self.uuid = uuid
        self.service_name = service_name
        self.port = port

        # Create the server-side BT socket
        self.set_socket(BluetoothSocket(RFCOMM))
        self.bind(("", self.port))
        self.listen(1)

        # Track the client-side handlers with a set
        self.active_client_handlers = set()

        advertise_service(
            self.socket,
            self.service_name,
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE]
        )
        self.port = self.socket.getsockname()[1]

        # start storing sensor data
        self.saver = None
        self.saving = False

        self.start_saving()

        print "Server initiated..."
        print "[DB] Start storing sensor data"
        print "Waiting for android device to be connected on port %d" %self.port


    def handle_accept(self):
        # This method is called when an incoming connection request from a client is accept.

        if self.saving:
            self.saver.stop()
            self.saver.join()
            self.saving = False
            print "[DB] Storing sensor data stopped"

        # Get the client-side BT socket
        pair = self.socket.accept()

        if pair is not None:
            client_sock, client_addr = pair
            client_handler = BTClientHandler(socket=client_sock, server=self)
            self.active_client_handlers.add(client_handler)

            print "Connected to %s," % repr(client_addr[0]) + \
                  " number of active connections is %d" % len(self.active_client_handlers)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def start_saving(self):
        if not self.saving:
            self.saving = True
            self.saver = HistoricalProcessor()
            self.saver.start()

    def stop_saving(self):
        if self.saving:
            self.saver.stop()
            self.saver.join()
            self.saving = False