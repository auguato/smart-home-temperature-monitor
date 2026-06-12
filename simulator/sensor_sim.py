"""
sensor_sim.py
Simulates a DHT22 temperature and humidity sensor.
Generates realistic readings using sine wave daily cycles + random noise.
"""

import math
import random
import time
from datetime import datetime


def get_simulated_reading() -> dict:
    """
    Returns a simulated temperature and humidity reading.
    Temperature follows a daily sine wave (cooler at night, warmer midday).
    Humidity is inversely correlated with temperature.
    """
    now = datetime.now()
    hour = now.hour + now.minute / 60.0

    # Sine wave: coldest at 4am (~22°C), warmest at 2pm (~32°C)
    base_temp = 27.0
    amplitude = 5.0
    phase = (hour - 14) * (2 * math.pi / 24)
    temperature = base_temp + amplitude * math.sin(phase) + random.uniform(-0.5, 0.5)

    # Humidity inversely correlated with temperature
    base_humidity = 70.0
    humidity = base_humidity - (temperature - base_temp) * 1.5 + random.uniform(-2, 2)
    humidity = max(30.0, min(95.0, humidity))

    return {
        "timestamp": now.isoformat(),
        "temperature_c": round(temperature, 2),
        "humidity_pct": round(humidity, 2),
        "sensor": "DHT22-SIM"
    }


if __name__ == "__main__":
    print("Running sensor simulator... Press Ctrl+C to stop.\n")
    while True:
        reading = get_simulated_reading()
        print(f"[{reading['timestamp']}] Temp: {reading['temperature_c']}°C | "
              f"Humidity: {reading['humidity_pct']}%")
        time.sleep(5)
