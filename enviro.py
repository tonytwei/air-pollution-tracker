#########################################################################
#########################################################################

# Configuration
run_background = False
run_flask = True

# sample is taken every <> seconds
data_read_interval = 10

# data aggregation size
# 60 = 1 minute, 3600 = 1 hour
seconds_per_aggreate = 60
data_aggregate_size = int(seconds_per_aggreate / data_read_interval)

#########################################################################
# Sensors
import time
from enviroplus import gas
from bme280 import BME280
from flask.helpers import send_from_directory
from pms5003 import PMS5003

# Processing
import os
from time import strftime, localtime, sleep, time, asctime
from flask import Flask, render_template, jsonify
import json
from math import floor
import threading

app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

bme280 = BME280()
pms5003 = PMS5003()

run_flag = True

curr_data = []
hist_data = []

def filename(t):
    # add minute to filename
    return strftime("enviro-data/%Y_%j_%H_%M", localtime(t))

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

def print_data(d):
    for key, value in d.items():
        print(f'{key}: {value}')

def sum_data(data):
    totals = {"time": data[0]["time"]}
    keys = list(data[0].keys())
    keys.remove("time")
    for key in keys:
        totals[key] = 0
    for record in data:
        for key in keys:
            totals[key] += record[key]
    num_records = float(len(data))
    for key in keys:
        totals[key] = round(totals[key] / num_records, 1)
    return totals


# TODO change to save to file
def save_data_to_json(d, file_path):
    file_path += ".json"
    with open(file_path, 'w') as json_file:
        json.dump(d, json_file, indent=4)


def read_hist_data(fname):
    d = []
    print("reading " + fname)
    with open(fname, 'r') as f:
        d = json.load(f)
        # TODO delete old line by line reading since changed from .txt to .json
        '''
        for line in f.readlines():
            try:
                record = json.loads(line)
                d.append(record)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        '''
    return d

# data collection thread
def background(script_dir):
    global record, curr_data
    while (run_flag):
        t = int(floor(time()))
        record = read_data(t)

        # we want to save the last hour of data and append new record
        curr_data = curr_data[-(data_aggregate_size - 1):]
        curr_data.append(record)

        # should we save the data?
        if (t % data_aggregate_size == 0 and len(curr_data) >= data_aggregate_size/2):
            totals = sum_data(curr_data)

            os.system('clear')
            print_data(totals)
            print(totals["time"])
            file_path = os.path.join(script_dir, filename(t))

            print("filename(t): " + filename(t))
            print("file_path: " + file_path)
            save_data_to_json(totals, file_path)


        # temp save to json
        # print(filename(t - (data_aggregate_size - 1)))
        # print_data(record)
        # file_path = os.path.join(script_dir, 'data.json')  # Absolute file path
        # save_data_to_json(record, file_path)

        sleep(data_read_interval)


# TODO fix flask routes
@app.route('/')
def index():
    return render_template('index.html', hist_data=json.dumps(hist_data))

@app.route('/say_hello')
def say_hello():
    return jsonify({"message": "Hello, world!"})

if __name__ == '__main__':
    # makes directory for data storage
    if not os.path.isdir('enviro-data'):
        os.makedirs('enviro-data')
    
    # opens directory and reads historical data
    files =  sorted(os.listdir('enviro-data'))
    for f in files:
        hist_data.append(read_hist_data("enviro-data/" + f))

    # TODO remove run_background after testing
    if run_background:
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
    
    if (run_background):
        print("Closing background thread")
        background_thread.join()