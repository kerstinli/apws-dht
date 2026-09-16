import time

import adafruit_dht
import board
import requests

# The API endpoint
logstash_url = "http://logstash:5044"

# 5 Minuten in Sekunden
ticktack = 5 * 60

def main() -> None:
    # DHT11 DATA -> BCM GPIO 4 (physischer Pin 7)
    sensor = adafruit_dht.DHT11(board.D4)
    try:
        while True:
            try:
                dht_data = {
                    "temperature": sensor.temperature,
                    "humidity": sensor.humidity,
                    "name": "dht",
                }
                # A POST request to the API
                response = requests.post(
                    logstash_url,
                    json=dht_data,
                    timeout=10,
                )
                print(
                    f"Übertragen: {dht_data['temperature']} °C, "
                    f"{dht_data['humidity']} %, Status {response.status_code}"
                )
            except RuntimeError as error:
                # DHT11 kann gelegentlich eine fehlerhafte Messung liefern.
                print(f"Messfehler: {error}")
            except requests.exceptions.RequestException as error:
                # Netzwerk-/TLS-/Auth-Fehler beim POST an OpenSearch.
                print(f"Übertragungsfehler: {error}")
            # Programm für 5 Minuten anhalten
            time.sleep(ticktack)
    except KeyboardInterrupt:
        print("\nProgramm beendet.")
    finally:
        sensor.exit()


if __name__ == "__main__":
    main()
