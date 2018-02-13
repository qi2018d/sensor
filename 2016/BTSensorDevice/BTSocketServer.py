from bluetooth import *
import threading

class BTSocketServer:
    def __init__(self,
                 name="BTSocketServer",
                 protocol=RFCOMM,
                 backlog=1,
                 server_addr="",
                 server_port=PORT_ANY,
                 uuid="94f39d29-7d6d-437d-973b-fba39e49d4ee",
                 buff_size=1024):
        self.name = name                    # server name
        self.protocol = protocol            # protocol to be used
        self.backlog = backlog              # max number of connections
        self.server_sock = None
        self.server_addr = server_addr      # server address
        self.server_port = server_port      # server port (might change later)
        self.client_sock = None
        self.client_addr = None             # client address
        self.client_port = None             # client port
        self.uuid = uuid                    #
        self.buff_size = buff_size          # receiving buffer
        self.sendLock = threading.Lock()    # send lock
        self.recvLock = threading.Lock()    # receive lock

    def start(self):
        self.server_sock = BluetoothSocket(self.protocol)
        self.server_sock.bind((self.server_addr, self.server_port))
        self.server_sock.listen(self.backlog)

        # update server info
        self.server_addr = self.server_sock.getsockname()[0]
        self.server_port = self.server_sock.getsockname()[1]

        advertise_service(self.server_sock,
                          self.name,
                          service_id=self.uuid,
                          service_classes=[self.uuid, SERIAL_PORT_CLASS],
                          profiles=[SERIAL_PORT_PROFILE],
                          #                   protocols = [ OBEX_UUID ]
                          )
        print("Started server at ({}, {})".format(
            self.server_addr, self.server_port))

    def wait(self):
        
        print("wwwWaiting for connection on channel {}...".format(
            self.server_port))

        # Keep waiting until a client connects to the server
        print "testaaaaaa"
        self.client_sock, tmp = self.server_sock.accept()
        print "exit?"
        self.client_addr = tmp[0]
        self.client_port = tmp[1]
        print("Accepted connection from ({}, {})".format(
            self.client_addr, self.client_port))

    def stop(self):
        print("Closing socket connections...")
        self.client_sock.close()
        self.server_sock.close()
        print("Socket connections closed")

    def send(self, msg):
        with self.sendLock:
            return self.client_sock.send(msg + '\n')

    def recv(self):
        with self.recvLock:
            return self.client_sock.recv(self.buff_size)

