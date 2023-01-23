import json
import pika

connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq"))

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
