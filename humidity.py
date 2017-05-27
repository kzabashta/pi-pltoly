import plotly.plotly as py
import json
import time
import datetime
import dht11
import RPi.GPIO as GPIO

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=4)

with open('/home/pi/scripts/plotly-temp/config.json') as config_file:
    plotly_user_config = json.load(config_file)

py.sign_in(plotly_user_config["plotly_username"], plotly_user_config["plotly_api_key"])

SECONDS_IN_DAY = 84400

SAMPLE_FREQUENCY = 1
EMIT_FREQUENCY = 60

url = py.plot([
    {
        'x': [], 'y': [], 'type': 'scatter',
        'stream': {
            'token': plotly_user_config['plotly_streaming_tokens'][0],
            'maxpoints': SECONDS_IN_DAY / EMIT_FREQUENCY
        }
    }], filename='Humidity')

stream = py.Stream(plotly_user_config['plotly_streaming_tokens'][0])
stream.open()

i = 0
total_sum = 0
while True:
    time.sleep(SAMPLE_FREQUENCY)
    result = instance.read()
    if result.is_valid():
       	humidity = result.humidity
	stream.write({'x': datetime.datetime.now(), 'y': humidity})

        if i > EMIT_FREQUENCY:
            stream.write({'x': datetime.datetime.now(), 'y': total_sum / i}) 
            total_sum = 0
            i = 0
        else:
            total_sum += humidity
            i+=1
