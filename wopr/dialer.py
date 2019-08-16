import argparse
import os
import random
import sys
import time

import pika

from wopr import *
from wopr.base import BusConnector


DEFAULT_SLEEP = 2


class Dialer(BusConnector):

    def connect(self):
        super().connect()
        self.channel.queue_declare(queue=self.QUEUE_NUMBERS)
        self.channel.queue_declare(queue=self.QUEUE_RESULTS)

        self.sleep_time = os.environ.get('SLEEP_TIME', DEFAULT_SLEEP)

    def start_reading_numbers(self, callback=None):
        callback = callback or self.process_number

        self.channel.basic_consume(queue=self.QUEUE_NUMBERS,
                                   on_message_callback=callback,
                                   auto_ack=False)
        self.channel.start_consuming()

    def send_result(self, result):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.QUEUE_RESULTS,
                                   body=result)

    def process_number(self, ch, method, properties, body):

        body = body.decode('utf-8')
        print('Processing %s' % body)

        time.sleep(self.sleep_time)

        result = '%s - No Connection' % body
        if random.randrange(0, 10) == 0:
            result = '%s - Connection Found' % body

        self.send_result(result)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)


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

    try:
        d.start_reading_numbers()
    except KeyboardInterrupt:
        print('Disconnecting from the message bus')
        d.disconnect()
