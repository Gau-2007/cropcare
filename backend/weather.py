import requests


def get_forecast(lat, lon):
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "hourly": "relative_humidity_2m",
        "forecast_days": 3, "timezone": "auto",
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=8)
    r.raise_for_status()
    d = r.json()

    hum = d["hourly"]["relative_humidity_2m"]
    days = []
    for i, date in enumerate(d["daily"]["time"]):
        hours = [h for h in hum[i * 24:(i + 1) * 24] if h is not None]
        days.append({
            "date": date,
            "tmax": d["daily"]["temperature_2m_max"][i],
            "tmin": d["daily"]["temperature_2m_min"][i],
            "rain": d["daily"]["precipitation_sum"][i],
            "humidity": round(sum(hours) / len(hours)) if hours else None,
        })
    return days