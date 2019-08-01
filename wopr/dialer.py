import os
import pika


QUEUE_NUMBERS = 'wopr_numbers'
QUEUE_RESULTS = 'wopr_results'

ENV_BUS_HOST = 'BUS_HOST'
ENV_BUS_PORT = 'BUS_PORT'


class Dialer(object):

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

        # Declaring a queue is idempotent, so it's safe to do each connect
        self.channel.queue_declare(queue=QUEUE_NUMBERS)
        self.channel.queue_declare(queue=QUEUE_RESULTS)

    def disconnect(self):
        self.connection.close()

    def start_reading_numbers(self, callback):
        self.channel.basic_consume(queue=QUEUE_NUMBERS,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def start_reading_results(self, callback):
        self.channel.basic_consume(queue=QUEUE_RESULTS,
                                   on_message_callback=callback,
                                   auto_ack=True)
        self.channel.start_consuming()

    def send_number(self, number):
        self.channel.basic_publish(exchange='',
                                   routing_key=QUEUE_NUMBERS,
                                   body=number)

    def send_result(self, result):
        self.channel.basic_publish(exchange='',
                                   routing_key=QUEUE_RESULTS,
                                   body=result)

    def purge_all(self):
        self.purge_numbers()
        self.purge_results()

    def purge_numbers(self):
        self.channel.queue_purge(QUEUE_NUMBERS)

    def purge_results(self):
        self.channel.queue_purge(QUEUE_RESULTS)

    def populate(self):
        for i in range(0, 10000):
            number = '555-%s' % str(i).zfill(4)
            self.send_number(number)

    def __str__(self):
        return 'bus_host[%s], bus_port[%s]' % (self.hostname, self.port)


if __name__ == '__main__':
    d = Dialer()
    print(d.hostname)
    print(d.port)
