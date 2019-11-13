import json

from flask import Response


def generate_response(status, data):
    return Response(
        mimetype='application/json',
        response=json.dumps(data),
        status=status
    )
