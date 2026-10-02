PROFILES = {
    "Potato___Late_blight": "cool_wet",
    "Tomato___Late_blight": "cool_wet",
    "Potato___Early_blight": "warm_humid",
    "Tomato___Early_blight": "warm_humid",
    "Tomato___Septoria_leaf_spot": "warm_humid",
    "Tomato___Target_Spot": "warm_humid",
    "Tomato___Bacterial_spot": "warm_humid",
    "Tomato___Leaf_Mold": "very_humid",
    "Tomato___Spider_mites Two-spotted_spider_mite": "hot_dry",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "whitefly",
    "Tomato___Tomato_mosaic_virus": "contact",
}

WATER = {
    "cool_wet": "Avoid overhead watering. Water at the base in the morning so leaves dry before night. Skip watering if rain is expected.",
    "warm_humid": "Water at the base in the morning, not on the leaves. Avoid watering late in the day.",
    "very_humid": "Water lightly at the base and keep air moving. Avoid wetting leaves and avoid watering in the evening.",
    "hot_dry": "Keep soil evenly moist and do not let plants dry out. Water at the base, and check the underside of leaves often.",
    "whitefly": "Water regularly at the base to reduce plant stress. Watering does not control the virus, so focus on whitefly control and removing infected plants.",
    "contact": "Water at the base. Avoid touching wet plants, and clean hands and tools between plants.",
}


def assess_risk(class_name, days):
    """Return (risk dict, water advice) using simple rules and the 3-day forecast."""
    if "healthy" in class_name:
        return {"level": "None", "reason": "The plant looks healthy. Keep monitoring."}, \
               "Normal watering at the base, in the morning."

    profile = PROFILES.get(class_name, "warm_humid")
    water = WATER[profile]

    if profile == "contact":
        return {"level": "Medium",
                "reason": "This virus spreads by hands, tools and sap, not by weather. Remove infected plants early."}, water
    if not days:
        return {"level": "Unknown", "reason": "Weather forecast is not available right now."}, water

    temps = [(d["tmax"] + d["tmin"]) / 2 for d in days if d["tmax"] is not None and d["tmin"] is not None]
    hums = [d["humidity"] for d in days if d["humidity"] is not None]
    temp = sum(temps) / len(temps) if temps else 25
    hum = sum(hums) / len(hums) if hums else 60
    rain = sum(d["rain"] or 0 for d in days)

    level = "Low"
    if profile == "cool_wet":
        if 10 <= temp <= 25 and (hum >= 85 or rain >= 5):
            level = "High"
        elif hum >= 70 or rain >= 2:
            level = "Medium"
    elif profile == "warm_humid":
        if 20 <= temp <= 32 and (hum >= 80 or rain >= 5):
            level = "High"
        elif hum >= 65 or rain >= 2:
            level = "Medium"
    elif profile == "very_humid":
        level = "High" if hum >= 85 else "Medium" if hum >= 70 else "Low"
    elif profile == "hot_dry":
        if temp >= 30 and hum < 50 and rain < 1:
            level = "High"
        elif temp >= 25 and hum < 65:
            level = "Medium"
    elif profile == "whitefly":
        if temp >= 25 and rain < 3:
            level = "High"
        elif temp >= 20:
            level = "Medium"

    reason = (f"Next 3 days: average {temp:.0f} C, humidity {hum:.0f}%, "
              f"total rain {rain:.0f} mm. ")
    if level == "High":
        reason += "This weather strongly favors spread. Act today."
    elif level == "Medium":
        reason += "Spread is possible. Inspect plants daily."
    else:
        reason += "This weather does not favor fast spread."
    return {"level": level, "reason": reason}, water