# Home Automation
A modular collection of scripts and helpers for building a **DIY home automation system**. This project ties together scheduling, sensor monitoring, Raspberry Pi utilities, and automation scripts to run tasks on a schedule or based on sensor input. It provides a foundation for experimenting with IoT and smart-home style automation using Python and shell scripts.

> 📊 View the [Home Temperature Chart](http://iot-temperature-project.s3-website-us-west-2.amazonaws.com/highchartSimple.html)

## What It Does
- **Temperature Monitoring:** `temperature_sensors/` contains scripts to read sensor data (e.g., DHT sensors) and log/report results.
- **Automation Rules & Scripts:** `smart/`, `scripts/`, and `activities/` provide logic for automating tasks or triggering actions (lights, relays, notifications, etc.).
- **Scheduling:** `cronJob.txt` shows examples of scheduled tasks (via cron) for recurring automations.
- **Indexing:** `indexing/` modules for searching providers such as Google and Bing.
- **Pi Helpers:** `pi_helper/` includes Raspberry Pi–specific utilities to simplify system commands.
- **Learning & Notes:** `ponderizing/` contains scriptures and sending email script to be used by automated cronjob.

## Project Structure
    .
    ├── activities/            # automation activity scripts
    ├── cronJob.txt            # sample cron jobs for scheduling
    ├── indexing/              # indexing modules
    ├── pi_helper/             # Raspberry Pi helper utilities
    ├── ponderizing/           # emailing scriptures modules
    ├── scripts/               # general scripts for automation
    ├── smart/                 # "smart" automation logic
    ├── temperature_sensors/   # temperature sensor readers
    ├── LICENSE
    └── README.md

## Tech Stack
- **Languages:** Python 3.x (primary), Shell scripts, Arduino (C++), Node.js
- **Hardware:** Raspberry Pi, ESP8266, `DHT22/11` (temperature/humidity) sensors
- **Cloud:** AWS (IoT, DynamoDB, Lambdas, S3)
- **Tools:** system **cron** (scheduling).

## Getting Started
**Prerequisites**
- Python 3.x
- Raspberry Pi (running MQTT)
- Install needed Python libraries & virtualenv
- follow steps.txt for better instructions on each folder

**Clone & Setup**
git clone https://github.com/ylehilds/home_automation.git
cd home_automation

## Run Scripts
**Temperature Sensor Reader**
Take a look at the cron jobs by running this command:
```bash
crontab -l
```
Then run the script yourself just like the cronjob would run

## Scheduled via cron:
Use the provided cron template found in cronJob.txt

## Potential Use Cases
- Periodically log and graph home temperature/humidity.
- Automate GPIO-connected devices (lights, fans, relays).
- Run recurring activities (backups, notifications) with cron.
- Expand to more sensors and add cloud integrations (MQTT, Home Assistant).

## Roadmap
- [ ] Add MQTT broker integration for real-time events.
- [ ] Expand visualization with charts/dashboards.
- [ ] Use other microcontrollers such as ESP32.
- [ ] Support additional sensors (motion, light, etc.).
- [ ] Package as a long-running service/daemon.
- [ ] Optional Dockerization for easier deployment.

## License
MIT License — see `LICENSE`.

## Author
**Lehi Alcantara** • https://www.lehi.dev • lehi@lehi.dev