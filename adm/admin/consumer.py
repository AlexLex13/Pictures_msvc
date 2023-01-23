import django
import json
import os
import pika

from products.models import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
