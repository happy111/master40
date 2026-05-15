from aws_lambda_powertools.event_handler import APIGatewayRestResolver

app = APIGatewayRestResolver()


@app.get("/hello")
def hello():
    return {
        "message": "Hello from AWS Lambda Powertools"
    }


@app.get("/user/<user_id>")
def get_user(user_id):
    return {
        "user_id": user_id,
        "status": "success"
    }


@app.post("/add")
def add_numbers():
    body = app.current_event.json_body

    number1 = body.get("number1", 0)
    number2 = body.get("number2", 0)

    return {
        "sum": number1 + number2
    }


def lambda_handler(event, context):
    return app.resolve(event, context)
