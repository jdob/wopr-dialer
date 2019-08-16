import argparse
import os
import sys

import pika

from wopr import *
from wopr.base import BusConnector


class Dialer(BusConnector):

    def connect(self):
        super().connect()
        self.channel.queue_declare(queue=QUEUE_NUMBERS)

    def start_reading_numbers(self, callback):
        self.channel.basic_consume(queue=QUEUE_NUMBERS,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def send_result(self, result):
        self.channel.basic_publish(exchange='',
                                   routing_key=QUEUE_RESULTS,
                                   body=result)


def parse(args):
    parser = argparse.ArgumentParser(
        description='Command line interface to the WOPR Dialer',
        add_help=False
    )

    # Arguments
    parser.add_argument('-h', '--hostname',
                        dest='hostname',
                        action='store',
                        help='hostname of the message bus')

    parser.add_argument('--port', '-p',
                        dest='port',
                        action='store',
                        type=int,
                        help='port of the message bus')

    return parser.parse_args(args)


if __name__ == '__main__':
    parsed = parse(sys.argv[1:])

    d = Dialer(hostname=parsed.hostname, port=parsed.port)
    d.connect()

    print('Reading numbers on [%s]' % d)
    d.start_reading_numbers(print_callback)
