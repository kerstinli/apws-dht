# Basis-Image
FROM ghcr.io/astral-sh/uv:0.12-python3.12-trixie-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    pipx swig python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /dht11

RUN uv init

RUN uv add adafruit-circuitpython-dht lgpio

COPY main.py .

CMD ["uv", "run", "main.py"]
