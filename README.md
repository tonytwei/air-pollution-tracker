# Live Air Pollution Tracker

## Overview

This project aims to create a live air pollution tracker using a Raspberry Pi and environmental sensors. The system collects real-time data on temperature, humidity, pressure, gas levels, and particulate matter, displaying the information on a web page.

## Features

- Real-time data collection of environmental parameters.
- Web-based dashboard to visualize live air quality metrics.
- Multi-threading for efficient data collection and presentation.
- JSON data storage for historical analysis.

## Components

- Raspberry Pi
- Environmental sensors: BME280, PMS5003
- Python libraries: `enviroplus`, `bme280`, `pms5003`, `flask`
- HTML/CSS for web dashboard

## How It Works

1. Environmental sensor data (temperature, humidity, pressure, gas levels, particulate matter) is collected using the Raspberry Pi.
2. The collected data is processed and stored in JSON format.
3. A Flask web application serves as a dashboard to display the real-time air quality metrics.
4. Multi-threading is employed to ensure continuous data collection without blocking the web interface.

## Project Status

The project is currently in progress. Real-time data collection and web dashboard functionality have been implemented. Future enhancements include refining the web interface design and adding historical data analysis.

## Setup and Usage

1. Clone this repository to your Raspberry Pi.
2. Install required Python libraries.
3. Run the main script to start data collection and the Flask server: `python my_app.py`.
4. Access the dashboard by opening a web browser and navigating to `http://raspberry_pi_ip:5000`.

## Future Enhancements

- Historical data analysis and visualization.
- Integration with external APIs for location-based air quality data.
- Customized alerts based on air quality thresholds.


<img src="https://i.imgur.com/hspH5oy.jpg" alt="Project Image" width="50%">
