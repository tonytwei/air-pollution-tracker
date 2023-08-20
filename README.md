# Live Environment Monitor

<p align="center">
    <img src="https://cdn.discordapp.com/attachments/1084642204590559242/1142727628747452436/image.png" alt="Web App Screenshot">
</p>

## Overview

The Live Enviroment Monitor project aims to create a real-time air quality monitoring system using a Raspberry Pi and environmental sensors. The system collects data on various environmental parameters, such as temperature, humidity, pressure, gas levels, and particulate matter, and displays this information on a web-based dashboard.

## Features

- Real-time data collection of important environmental parameters.
- Web-based dashboard for visualizing live air quality metrics.
- Efficient multi-threading for continuous data collection and presentation.
- JSON data storage for historical analysis and visualization.

## Components

- Raspberry Pi
- Environmental sensors: Enviro+, PMS5003
- Python libraries: `enviroplus`, `bme280`, `pms5003`, `flask`
- HTML/CSS/JavaScript for the web dashboard

## How It Works

1. Environmental sensor data including temperature, humidity, pressure, gas levels, and particulate matter are collected using the Raspberry Pi.
2. The collected data is processed and stored in JSON format.
3. A Flask-based web application serves as a dashboard to visualize real-time air quality metrics.
4. Multi-threading is employed to ensure continuous data collection without interrupting the web interface.

## Setup and Usage

1. Clone this repository to your Raspberry Pi.
2. Install the required Python libraries.
3. Run the main script to start data collection and the Flask server: `python enviro.py`.
4. Access the dashboard by opening a web browser and navigating to `http://raspberry_pi_ip:5000`.

![Project Image](https://i.imgur.com/hspH5oy.jpg)
