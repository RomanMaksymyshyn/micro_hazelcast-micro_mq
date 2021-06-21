import threading

import pika
from flask import Flask

app = Flask(__name__)


@app.route('/messages',  methods=['GET'])
def messages():
    print(ALL_TIME_MESSAGES_11)
    return str(ALL_TIME_MESSAGES_11)


def threaded(fn):
    def run(*args, **kwargs):
        t = threading.Thread(target=fn, args=args, kwargs=kwargs)
        t.start()
        return t
    return run

@threaded
def consuming(messages_list):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1')
    )
    channel = connection.channel()
    channel.queue_declare(queue='mq_for_messages_service')
    def callback(ch, method, properties, body):    
        print(" [x] Received %r" % body.decode())
        messages_list.append(body.decode())
        print(messages_list)
    channel.basic_consume(queue='mq_for_messages_service', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    ALL_TIME_MESSAGES_11 = []
    consuming(ALL_TIME_MESSAGES_11)
    print('LETS GO 1')
    app.run(host='0.0.0.0', port=1122, debug=False)
