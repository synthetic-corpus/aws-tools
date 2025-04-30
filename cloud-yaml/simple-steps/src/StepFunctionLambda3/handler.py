import os

def lambda_handler(event, context):
    env = os.getenv("ENVIRONMENT", "undefined")
    input_str = event.get("output", "")
    return {
        "environment": env,
        "output": input_str + "_Step3"
    }
