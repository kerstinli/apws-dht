import argparse
import logging
import os
import sys
import time

import adafruit_dht
import board
import requests

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

# 60 minutes
ticktack = 60 * 60

def execute(logstash_url: str, pin_name: str) -> None:
    """
    Method to execute the main logic of the script.
    :param logstash_url: the target logstash to send data to
    :param pin_name: the pin where the sensor is connected to
    """
    # DHT11 sensor on specified GPIO pin
    pin = getattr(board, pin_name)
    sensor = adafruit_dht.DHT11(pin)
    logging.info(f"Using GPIO pin: {pin_name}")
    try:
        while True:
            try:
                dht_data = {
                    "temperature": sensor.temperature,
                    "humidity": sensor.humidity,
                    "name": "near_the_plant",
                }
                # A POST request to the API
                response = requests.post(
                    logstash_url,
                    json=dht_data,
                    timeout=10,
                )
                logging.info(
                    f"Sent: {dht_data['temperature']} °C, "
                    f"{dht_data['humidity']} % with status {response.status_code}"
                )
            except RuntimeError as error:
                logging.error(f"Error getting values from sensor: {error}")
            except requests.exceptions.RequestException as error:
                logging.error(f"Error sending data to Logstash: {error}")
            time.sleep(ticktack)
    except KeyboardInterrupt:
        logging.info("Cancel execution...")
    finally:
        sensor.exit()


if __name__ == "__main__":
    # The API endpoint - can be overridden by environment variable or command-line argument
    logstash_url: str = os.getenv("LOGSTASH_URL", "http://logstash:5044")

    # GPIO pin - can be overridden by environment variable or command-line argument
    pin_name = os.getenv("GPIO_PIN", "D4")

    parser = argparse.ArgumentParser(description="DHT11 Sensor to Logstash")
    parser.add_argument(
        "--logstash-url",
        help="Logstash endpoint URL (overrides LOGSTASH_URL environment variable)",
    )
    parser.add_argument(
        "--pin",
        help="GPIO pin (e.g., D4, D18, overrides GPIO_PIN environment variable)",
    )
    args = parser.parse_args()
    if args.logstash_url:
        logstash_url = args.logstash_url
    if args.pin:
        pin_name = args.pin

    execute(logstash_url, pin_name)
