from rest_framework.utils import json


def errors_serializer(exception: Exception) -> str:
    try:
        json.loads(exception.args[0])
    except ValueError:
        response = json.dumps({'detail': str(exception.args[0])})
    else:
        response = str(exception.args[0])

    return response
