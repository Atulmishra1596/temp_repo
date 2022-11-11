import logging
from http import HTTPStatus

from flask import json, jsonify, request
from prometheus_client import Summary

from utility.database import PostGres

summary_ping = Summary(
    'ping_requests',
    'Ping requests check')


log = logging.getLogger(__name__)

@summary_ping.time()
def get():
    """
    Output:
        message: string
        statuscode: int
    """
    message = {
        "data": {
            "message": "Server up and running",
            "statuscode": HTTPStatus.OK.value
        }
    }

    return jsonify(message), HTTPStatus.OK
