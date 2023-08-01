# Sensors
from enviroplus import gas
from bme280 import BME280

# Processing
import os
import time

bme280 = BME280()

def read_data():
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()

    gases = gas.read_all()
    
    
    curr_data = {
        'temp' : round(temperature, 1),
        'humi' : round(humidity, 1),
        'pres' : round(pressure, 1),
        'oxi'  : round(gases.oxidising / 1000, 1),
        'red'  : round(gases.reducing / 1000),
        'nh3'  : round(gases.nh3 / 1000)
    }
    return curr_data

def print_data(curr_data):
    for key, value in curr_data.items():
        print(f'{key}: {value}')


while (True):

    data = read_data()
    print_data(data)

    time.sleep(1)
    os.system('clear')