import asyncore
from btserver import BTServer

if __name__ == '__main__':
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "AsynchronousBTServer"

    server = BTServer(uuid, service_name)
    asyncore.loop()