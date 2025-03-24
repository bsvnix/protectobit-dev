from flask import Flask, render_template
from kafka import KafkaConsumer
import json
from threading import Thread

app = Flask(__name__)
connections = []

def consume_kafka():
    consumer = KafkaConsumer('adfs_logs', bootstrap_servers=['kafka:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    for message in consumer:
        connections.append(message.value)

Thread(target=consume_kafka, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', connections=connections)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
