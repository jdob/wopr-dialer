import argparse
import sys

from wopr.dialer import Dialer


def handle(commands):

    # Message bus location
    d = Dialer(hostname=commands.hostname, port=commands.port)
    d.connect()

    # Commands; the order is intentional for command precedence
    if commands.purge:
        print('Purging all message queues')
        d.purge_all()
    elif commands.purge_numbers:
        print('Purging numbers message queue')
        d.purge_numbers()
    elif commands.purge_results:
        print('Purging results message queue')
        d.purge_results()

    if commands.populate:
        print('Populating the numbers queue')
        d.populate()

    if commands.listen_numbers:
        print('Listening on the numbers queue')

        try:
            d.start_reading_numbers(print_callback)
        except KeyboardInterrupt:
            pass  # User aborted

    if commands.listen_results:
        print('Listening on the results queue')

        try:
            d.start_reading_results(print_callback)
        except KeyboardInterrupt:
            pass  # User aborted

    d.disconnect()


def print_callback(ch, method, properties, body):
    print(body.decode('utf-8'))


def parse(args):
    parser = argparse.ArgumentParser(
        description='Command line interface to the WOPR Dialer',
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

    parser.add_argument('--listen_numbers',
                        dest='listen_numbers',
                        action='store_true',
                        help='listens on the numbers queue and prints new messages')

    parser.add_argument('--listen_results',
                        dest='listen_results',
                        action='store_true',
                        help='listens on the results queue and prints new messages')

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
    handle(parsed)
