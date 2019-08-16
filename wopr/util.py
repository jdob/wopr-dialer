import argparse
import os
import pika
import sys

from wopr import *
from wopr.base import BusConnector


class Util(BusConnector):

    def connect(self):
        super().connect()

        self.channel.queue_declare(queue=self.QUEUE_NUMBERS)
        self.channel.queue_declare(queue=self.QUEUE_RESULTS)

    def purge_all(self):
        self.purge_numbers()
        self.purge_results()

    def purge_numbers(self):
        self.channel.queue_purge(self.QUEUE_NUMBERS)

    def purge_results(self):
        self.channel.queue_purge(self.QUEUE_RESULTS)

    def populate(self):
        for i in range(0, 10000):
            number = '555-%s' % str(i).zfill(4)
            self._send_number(number)

    def _send_number(self, number):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.QUEUE_NUMBERS,
                                   body=number)


def parse(args):
    parser = argparse.ArgumentParser(
        description='Command line interface to the WOPR utilities',
        add_help=False
    )

    # Commands
    parser.add_argument('--populate',
                        dest='populate',
                        action='store_true',
                        help='populates the numbers message queue')

    parser.add_argument('--purge',
                        dest='purge',
                        action='store_true',
                        help='purges messages from all of the message queues')

    parser.add_argument('--purge_numbers',
                        dest='purge_numbers',
                        action='store_true',
                        help='purges messages from the numbers message queue')

    parser.add_argument('--purge_results',
                        dest='purge_results',
                        action='store_true',
                        help='purges messages from the results message queue')

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

    u = Util(hostname=parsed.hostname, port=parsed.port)
    u.connect()

    if parsed.purge:
        print('Purging all message queues')
        u.purge_all()
    elif parsed.purge_numbers:
        print('Purging numbers message queue')
        u.purge_numbers()
    elif parsed.purge_results:
        print('Purging results message queue')
        u.purge_results()

    if parsed.populate:
        print('Populating the numbers queue')
        u.populate()
