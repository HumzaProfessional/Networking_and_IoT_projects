import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CropConditions')

def lambda_handler(event, context):

    crop = event.get("crop")
    zone = event.get("zone")
    humidity = event.get("humidity")
    temperature = event.get("temperature_c")

    result = {
        "crop": crop,
        "zone": zone,
        "humidity": humidity,
        "temperature_c": temperature,
        "humidity_status": "unknown",
        "temperature_status": "unknown",
        "overall_status": "unknown"
    }

    if crop == "tomato":

        if 60 <= humidity <= 70:
            result["humidity_status"] = "good"
        elif humidity < 60:
            result["humidity_status"] = "too low"
        else:
            result["humidity_status"] = "too high"

        if 21 <= temperature <= 27:
            result["temperature_status"] = "good"
        elif temperature < 21:
            result["temperature_status"] = "too low"
        else:
            result["temperature_status"] = "too high"

    elif crop == "corn":

        if 40 <= humidity <= 60:
            result["humidity_status"] = "good"
        elif humidity < 40:
            result["humidity_status"] = "too low"
        else:
            result["humidity_status"] = "too high"

        if 25 <= temperature <= 33:
            result["temperature_status"] = "good"
        elif temperature < 25:
            result["temperature_status"] = "too low"
        else:
            result["temperature_status"] = "too high"

    if (
        result["humidity_status"] == "good"
        and result["temperature_status"] == "good"
    ):
        result["overall_status"] = "optimal"
    else:
        result["overall_status"] = "needs adjustment"

    table.put_item(
        Item={
            "zone": zone,
            "timestamp": datetime.utcnow().isoformat(),
            **result
        }
    )

    print("Saved to DynamoDB:", result)

    return result
