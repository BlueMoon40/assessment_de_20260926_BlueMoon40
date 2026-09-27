from pathlib import Path

import openmeteo_requests
import requests_cache
import yaml
from retry_requests import retry


API_URL = "https://archive-api.open-meteo.com/v1/archive"

# Cache API responses and retry failed requests
cache_session = requests_cache.CachedSession(
    ".cache",
    expire_after=-1
)

retry_session = retry(
    cache_session,
    retries=5,
    backoff_factor=0.2
)

openmeteo = openmeteo_requests.Client(
    session=retry_session
)


def load_cities():
    """Load city configuration from config/cities.yml."""

    config_path = Path(__file__).resolve().parents[1] / "config" / "cities.yml"

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config["cities"]


def fetch_daily(logical_date):
    """
    Fetch daily weather data for all configured cities
    for the supplied logical date.
    """

    cities = load_cities()

    results = []

    for city in cities:

        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "start_date": logical_date,
            "end_date": logical_date,
            "daily": [
                "temperature_2m_mean",
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum"
            ],
            "timezone": city["timezone"]
        }

        responses = openmeteo.weather_api(
            API_URL,
            params=params
        )

        response = responses[0]
        daily = response.Daily()

        results.append({
    "city": city["name"],
    "date": logical_date,
    "temperature_2m_mean": float(daily.Variables(0).ValuesAsNumpy()[0]),
    "temperature_2m_max": float(daily.Variables(1).ValuesAsNumpy()[0]),
    "temperature_2m_min": float(daily.Variables(2).ValuesAsNumpy()[0]),
    "precipitation_sum": float(daily.Variables(3).ValuesAsNumpy()[0])
})

    return results


if __name__ == "__main__":

    data = fetch_daily("2026-09-26")

    for row in data:
        print(row)