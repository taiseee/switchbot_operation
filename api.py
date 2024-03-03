from switchbot import Auth, DoorClient

import json


def unlock_handler(event, context):
    token = event["headers"]["token"]
    secret = event["headers"]["secret"]
    device_id = event["headers"]["deviceid"]
    auth = Auth(token, secret)
    door = DoorClient(auth, device_id)
    door.unlock()
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "unlock success"}),
    }
