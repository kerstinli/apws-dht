# apws-dht

A small Python service that reads temperature and humidity from a DHT11 sensor connected to a Raspberry Pi (or similar GPIO-capable board) and periodically posts the readings to a Logstash HTTP endpoint.

## How it works

`src/main.py` polls a DHT11 sensor every 5 minutes and sends a JSON payload via HTTP POST:

```json
{
  "temperature": 21.0,
  "humidity": 45,
  "name": "near_the_plant"
}
```

Sensor read errors and request failures are logged but do not stop the loop.

## Configuration

The target endpoint and GPIO pin can be set via environment variables or command-line flags (flags take precedence):

| Setting        | Env var        | CLI flag           | Default                  |
|----------------|----------------|---------------------|---------------------------|
| Logstash URL   | `LOGSTASH_URL` | `--logstash-url`    | `http://logstash:5044`   |
| GPIO pin       | `GPIO_PIN`     | `--pin`             | `D4`                      |

## Running locally

Requires Python 3.12+ and a board supported by [Adafruit Blinka](https://github.com/adafruit/Adafruit_Blinka) (e.g. Raspberry Pi), since the DHT11 sensor library needs real GPIO access.

```bash
cd src
pip install adafruit-circuitpython-dht lgpio requests
python main.py --logstash-url http://localhost:5044 --pin D4
```

## Running with Docker

```bash
cd src
docker build -t apws-dht .
docker run --device /dev/gpiomem -e LOGSTASH_URL=http://logstash:5044 -e GPIO_PIN=D4 apws-dht
```

GPIO device access must be passed through to the container (e.g. `--device /dev/gpiomem` or `--privileged`, depending on your setup).

## License

MIT — see [LICENSE](LICENSE).
