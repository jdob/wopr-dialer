import argparse
import os
import pika
import sys

from wopr import *
from wopr.base import BusConnector


class Listener(BusConnector):

    def connect(self):
        super().connect()

        self.channel.queue_declare(queue=self.QUEUE_RESULTS)

    def start_reading_results(self, callback):
        self.channel.basic_consume(queue=self.QUEUE_RESULTS,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()


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

    l = Listener(hostname=parsed.hostname, port=parsed.port)
    l.connect()

    print('Listening for results on [%s]' % l)

    try:
        l.start_reading_results(l.print_callback)
    except KeyboardInterrupt:
        print('Disconnecting from the message bus')
        l.disconnect()