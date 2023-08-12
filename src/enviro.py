#########################################################################
#########################################################################

# Configuration
run_background = True
run_flask = False
data_read_interval = 5 # in seconds


#########################################################################
# Sensors
import time
from enviroplus import gas
from bme280 import BME280
from pms5003 import PMS5003

# Processing
import os
from time import strftime, localtime, sleep, time, asctime
from flask import Flask, render_template
import json
from math import floor
import threading


app = Flask(__name__)

bme280 = BME280()
pms5003 = PMS5003()


hours = []
run_flag = True
samples_in_data = 600 ### check source

def filename(t):
    return strftime("enviro-data/%Y_%j_%H", localtime(t))

def read_data(time):
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
    
    record = {
        'time' : asctime(localtime(time)),
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
    return record

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



# data collection thread
def background(script_dir):
    global record, data
    while (run_flag):
        t = int(floor(time()))
        record = read_data(t)

        print(filename(t))
        print_data(record)

        # temp save to json
        file_path = os.path.join(script_dir, 'data.json')  # Absolute file path
        save_data_to_json(record, file_path)

        sleep(data_read_interval)
        os.system('clear')


def read_hour(fname):
    hour = []
    print("reading " + fname)
    with open(fname, 'r') as f:
        for line in f.readlines():
            record = json.loads(line)
            # TODO implement to prevent first record of the day being inaccurate
            # add_record(hour, record)
            hour.append(record)
    return hour


if __name__ == '__main__':
    # makes directory for data storage
    if not os.path.isdir('enviro-data'):
        os.makedirs('enviro-data')
    
    # opens directory and reads hourly data
    files =  sorted(os.listdir('enviro-data'))
    for f in files:
        hours.append(read_hour('enviro-data/' + f))

    script_directory = os.path.dirname(os.path.abspath(__file__))
    background_thread = threading.Thread(target=background, args=(script_directory,))
    background_thread.start()

    # TODO remove run_flask after testing
    if run_flask:
        try:
            app.run(debug=True, port=5000, host='0.0.0.0')
        except Exception as e:
            print(e)
        run_flag = False
        print("Closing background thread")
        background_thread.join()