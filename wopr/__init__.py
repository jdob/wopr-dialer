QUEUE_NUMBERS = 'wopr_numbers'
QUEUE_RESULTS = 'wopr_results'

ENV_BUS_HOST = 'BUS_HOST'
ENV_BUS_PORT = 'BUS_PORT'


def print_callback(ch, method, properties, body):
    print(body.decode('utf-8'))
