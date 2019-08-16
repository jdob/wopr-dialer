import os
import pika

from wopr import *


ENV_BUS_HOST = 'BUS_HOST'
ENV_BUS_PORT = 'BUS_PORT'


class BusConnector(object):

    QUEUE_NUMBERS = 'wopr_numbers'
    QUEUE_RESULTS = 'wopr_results'

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
        self.channel.basic_qos(prefetch_count=1)

    def disconnect(self):
        self.connection.close()


    def print_callback(self, ch, method, properties, body):
        print(body.decode('utf-8'))

    def __str__(self):
        return 'bus_host[%s], bus_port[%s]' % (self.hostname, self.port)
