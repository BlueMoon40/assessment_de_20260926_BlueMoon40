CREATE TABLE IF NOT EXISTS raw.weather_daily (
    city TEXT NOT NULL,
    date DATE NOT NULL,
    temperature_2m_mean DECIMAL(10, 2),
    temperature_2m_max DECIMAL(10, 2),
    temperature_2m_min DECIMAL(10, 2),
    precipitation_sum DECIMAL(10, 2),
    PRIMARY KEY (city, date)
);
