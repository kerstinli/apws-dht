import os
import time
import adafruit_dht
import board
import requests

# The API endpoint
opensearch_url = "https://192.168.8.168:9200/posts"

# 5 Minuten in Sekunden
ticktack = 5 * 60

opensearch_ca_cert = os.environ["OPENSEARCH_CA_CERT"]  # z.B. "/certs/ca.pem"
opensearch_auth = (os.environ["OPENSEARCH_USER"], os.environ["OPENSEARCH_PASSWORD"])

def main() -> None:
    # DHT11 DATA -> BCM GPIO 4 (physischer Pin 7)
    sensor = adafruit_dht.DHT11(board.D4)
    try:
        while True:
            try:
                weather_data = {
                    "temperature": sensor.temperature,
                    "humidity": sensor.humidity,
                    #"date": sensor.humidity,
                    #print(f"Temperatur: {temperature:.1f} °C")
                    #print(f"Luftfeuchtigkeit: {humidity:.1f} %")
                    #print("-" * 30)
                }
                # A POST request to the API
                #response = requests.post(opensearch_url, json=weather_data)
                response = requests.post(
                    opensearch_url,
                    json=weather_data,
                    auth=opensearch_auth,
                    verify=opensearch_ca_cert,
                    timeout=10,
                )
            except RuntimeError as error:
                # DHT11 kann gelegentlich eine fehlerhafte Messung liefern.
                print(f"Messfehler: {error}")
            except requests.exceptions.RequestException as error:
                # Netzwerk-/TLS-/Auth-Fehler beim POST an OpenSearch.
                print(f"Übertragungsfehler: {error}")
            # DHT11 sollte nicht häufiger als etwa alle 2 Sekunden
            # ausgelesen werden.
            # Programm für 5 Minuten anhalten
            time.sleep(ticktack)
    except KeyboardInterrupt:
        print("\nProgramm beendet.")
    finally:
        sensor.exit()


if __name__ == "__main__":
    main()
