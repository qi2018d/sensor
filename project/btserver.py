import asyncore
import time

from bluetooth import *

from aqi_thread import AQIThread
from bthandler import BTClientHandler
from reader_thread import ReaderThread
from sender import Sender


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
        self.disconnected_time = time.time()

        advertise_service(
            self.socket,
            self.service_name,
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE]
        )

        self.port = self.socket.getsockname()[1]
        self.sender = Sender(self.active_client_handlers)

        # start thread that read sensor, save to db and send it to app
        self.reader_thread = ReaderThread(self.sender)
        self.reader_thread.start()
        print "Starts reading, storing air data from sensors"

        # start thread that calculate aqi from stored data and send it to app
        self.aqi_thread = AQIThread(self.sender)
        self.aqi_thread.start()
        print "Starts calculating aqi from db"

        print "Server initiated... Waiting for android device to be connected on port %d" %self.port

    def handle_accept(self):

        # Get the client-side BT socket
        pair = self.socket.accept()

        if pair is not None:

            client_sock, client_addr = pair
            client_handler = BTClientHandler(socket=client_sock, server=self)

            # if this is the only connection made, send stored historical data
            if len(self.active_client_handlers) is 0:
                self.active_client_handlers.add(client_handler)
                self.sender.send_air_history_from(self.disconnected_time)

            else:
                self.active_client_handlers.add(client_handler)


            print "Connected to %s," % repr(client_addr[0]) + \
                  " number of active connections is %d" % len(self.active_client_handlers)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

