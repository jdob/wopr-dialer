import os
import pika

from wopr import *


class BusConnector(object):

    def __init__(self, hostname=None, port=None) -> None:
        super().__init__()

        self.connection = None
        self.channel = None  # https://pika.readthedocs.io/en/stable/modules/channel.html

        self.hostname = hostname or os.environ.get(ENV_BUS_HOST, None) or "localhost"
        self.port = port or os.environ.get(ENV_BUS_PORT, None) or 5672

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.hostname, port=self.port))
        self.channel = self.connection.channel()

    def disconnect(self):
        self.connection.close()

    def __str__(self):
        return 'bus_host[%s], bus_port[%s]' % (self.hostname, self.port)
