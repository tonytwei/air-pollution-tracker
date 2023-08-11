#########################################################################
#########################################################################

# Configuration
run_background = True
run_flask = True
data_read_interval = 5 # in seconds


#########################################################################
# Sensors
from enviroplus import gas
from bme280 import BME280
from pms5003 import PMS5003

# Processing
import os
import time
from flask import Flask, render_template
import json
from math import floor
import threading


app = Flask(__name__)

bme280 = BME280()
pms5003 = PMS5003()

def read_data():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()

    gases = gas.read_all()
    particles = pms5003.read()
    
    pm100 = particles.pm_per_1l_air(10.0)
    pm50 = particles.pm_per_1l_air(5.0)
    pm25 = particles.pm_per_1l_air(2.5)
    pm10 = particles.pm_per_1l_air(1.0)
    pm5 = particles.pm_per_1l_air(0.5)
    pm3 = particles.pm_per_1l_air(0.3)
    
    curr_data = {
        'time' : 0,
        'temp' : round(temperature, 1),
        'humi' : round(humidity, 1),
        'pres' : round(pressure, 1),
        'oxi'  : round(gases.oxidising / 1000, 1),
        'red'  : round(gases.reducing / 1000),
        'nh3'  : round(gases.nh3 / 1000),
        'pm03' : pm3,
        'pm05' : pm5,
        'pm10' : pm10,
        'pm25' : pm25,
        'pm50' : pm50,
        'pm100': pm100,
    }
    return curr_data

def print_data(curr_data):
    for key, value in curr_data.items():
        print(f'{key}: {value}')

def save_data_to_json(curr_data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(curr_data, json_file, indent=4)



@app.route('/')
def index():
    data = read_data()
    return render_template('sensor_data.html', data=data)



# multi threading
def background(script_dir):
    while (True):
        # t = int(floor(time()))
        data = read_data()
        print_data(data)
        file_path = os.path.join(script_dir, 'data.json')  # Absolute file path
        save_data_to_json(data, file_path)
        time.sleep(data_read_interval)
        os.system('clear')

if __name__ == '__main__':
    script_directory = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
    background_thread = threading.Thread(target=background, args=(script_directory,))
    background_thread.start()


if run_flask and __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
    
'''
while (True):
    data = read_data(t)
    print_data(data)
    save_data_to_json(data, 'data.json')
    time.sleep(data_read_interval)
    os.system('clear')
'''
