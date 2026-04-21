def lambda_handler(event, context):
    print("Incoming event:", event)

    crop = event.get("crop")
    humidity = event.get("humidity")
    temperature = event.get("temperature_c")

    result = {
        "crop": crop,
        "humidity": humidity,
        "temperature_c": temperature,
        "humidity_status": "unknown",
        "temperature_status": "unknown",
        "overall_status": "unknown"
    }

    if crop == "tomato":

        # Humidity check
        if humidity is None:
            result["humidity_status"] = "missing"
        elif 60 <= humidity <= 70:
            result["humidity_status"] = "good"
        elif humidity < 60:
            result["humidity_status"] = "too low"
        else:
            result["humidity_status"] = "too high"

        # Temperature check
        if temperature is None:
            result["temperature_status"] = "missing"
        elif 21 <= temperature <= 27:
            result["temperature_status"] = "good"
        elif temperature < 21:
            result["temperature_status"] = "too low"
        else:
            result["temperature_status"] = "too high"

        # Overall decision logic
        if (
            result["humidity_status"] == "good"
            and result["temperature_status"] == "good"
        ):
            result["overall_status"] = "optimal"
        else:
            result["overall_status"] = "needs adjustment"

    return result
