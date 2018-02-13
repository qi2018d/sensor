import asyncore
import logging
import adc
import led
from bterror import BTError

logger = logging.getLogger(__name__)

led_pin = 42

class BTClientHandler(asyncore.dispatcher_with_send):
    """BT handler for client-side socket"""

    def __init__(self, socket, server):
        asyncore.dispatcher_with_send.__init__(self, socket)
        self.server = server
        self.data = ""

    def handle_read(self):
        try:
            data = self.recv(1024)
            if not data:
                return

            lf_char_index = data.find('\n')

            if lf_char_index == -1:
                # No new line character in data, so we append all.
                self.data += data
            else:
                # We see a new line character in data, so append rest and handle.
                self.data += data[:lf_char_index]

                if self.data == "blink":
                    print "blink start"
                    led.blink(led_pin, 1, 1, 5)
                    print "blink end"

                elif self.data == "turn LED on":
                    print "turning on LED"
                    self.send("turning on LED")
                    led.on(led_pin)

                elif self.data == "turn LED off":
                    print "turning off LED"
                    self.send("turning off LED")
                    led.off(led_pin)

                elif self.data == "read adc":
                    read_value = adc.read0()
                    print "ADC 0 value read: " + str(read_value)
                    self.send(str(read_value) + '\n')

                else:
                    print "received [%s]" % self.data
                    self.send(self.data + '\n')

                # Clear the buffer
                self.data = ""
        except Exception as e:
            BTError.print_error(handler=self, error=BTError.ERR_READ, error_message=repr(e))
            self.data = ""
            self.handle_close()

    def handle_close(self):
        # flush the buffer
        while self.writable():
            self.handle_write()

        self.server.active_client_handlers.remove(self)
        self.close()