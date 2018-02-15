import asyncore

from btserver import BTServer

if __name__ == '__main__':
    uuid = "00001101-0000-1000-8000-00805F9B34FB"
    service_name = "AsynchronousBTServer"

    server = BTServer(uuid, service_name)
    asyncore.loop()