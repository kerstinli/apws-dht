import time
import adafruit_dht
import board


def main() -> None:
    # DHT11 DATA -> BCM GPIO 4 (physischer Pin 7)
    sensor = adafruit_dht.DHT11(board.D4)
    try:
        while True:
            try:
                temperature = sensor.temperature
                humidity = sensor.humidity
                print(f"Temperatur: {temperature:.1f} °C")
                print(f"Luftfeuchtigkeit: {humidity:.1f} %")
                print("-" * 30)
            except RuntimeError as error:
                # DHT11 kann gelegentlich eine fehlerhafte Messung liefern.
                print(f"Messfehler: {error}")
            # DHT11 sollte nicht häufiger als etwa alle 2 Sekunden
            # ausgelesen werden.
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nProgramm beendet.")
    finally:
        sensor.exit()


if __name__ == "__main__":
    main()
