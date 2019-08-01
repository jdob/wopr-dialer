import pika


def send():
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")


def receive():
    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)
    channel.start_consuming()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')

    send()
    receive()

    connection.close()
