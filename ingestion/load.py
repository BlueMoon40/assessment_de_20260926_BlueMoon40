import os
import psycopg2
from dotenv import load_dotenv

from weather_api import fetch_daily


load_dotenv()


def load_data(data_records):
    # 1. Convert API records into tuples matching the database columns
    insert_data = [
        (
            item["city"],
            item["date"],
            item["temperature_2m_mean"],
            item["temperature_2m_max"],
            item["temperature_2m_min"],
            item["precipitation_sum"]
        )
        for item in data_records
    ]

    # 2. Connect to PostgreSQL and insert data
    print(f"Connecting to DB and inserting {len(insert_data)} records...")

    with psycopg2.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO raw.weather_daily (
                    city,
                    date,
                    temperature_2m_mean,
                    temperature_2m_max,
                    temperature_2m_min,
                    precipitation_sum
                )
                VALUES (%s, %s, %s, %s, %s, %s)

                ON CONFLICT (city, date)
                DO UPDATE SET
                    temperature_2m_mean = EXCLUDED.temperature_2m_mean,
                    temperature_2m_max = EXCLUDED.temperature_2m_max,
                    temperature_2m_min = EXCLUDED.temperature_2m_min,
                    precipitation_sum = EXCLUDED.precipitation_sum;
                """,
                insert_data
            )

    print("Load complete!")


def ingest_data(logical_date):
    print(f"Fetching weather data for {logical_date}...")

    data_records = fetch_daily(logical_date=logical_date)

    load_data(data_records)


if __name__ == "__main__":
    ingest_data("2026-09-24")