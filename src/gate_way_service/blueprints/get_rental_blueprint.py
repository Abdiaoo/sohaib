import os
import json

from quart import Blueprint, Response, request
from .service_requests import get_data_from_service

get_rental_blueprint = Blueprint('get_rental', __name__, )


def car_simplify(car: dict) -> dict:
    return {
        "carUid": car['carUid'],
        "brand": car['brand'],
        "model": car['model'],
        "registrationNumber": car['registrationNumber']
    }


@get_rental_blueprint.route('/api/v1/rental/<string:rentalUid>', methods=['GET'])
async def get_rental(rentalUid: str) -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(
            status=400,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Request has not X-User-Name header!']
            })
        )

    response = get_data_from_service(
        'http://' + os.environ['RENTAL_SERVICE_HOST'] + ':' + os.environ['RENTAL_SERVICE_PORT']
        + '/api/v1/rental/'+rentalUid, timeout=5, headers={'X-User-Name': request.headers['X-User-Name']})
    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Rental Service is Unavailable']
            })
        )

    rental = response.json()
    response = get_data_from_service(
        'http://' + os.environ['CARS_SERVICE_HOST'] + ':' + os.environ['CARS_SERVICE_PORT']
        + '/api/v1/cars/' + rental['carUid'], timeout=5)
    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Car Service is Unavailable']
            })
        )
    del rental['carUid']
    rental['car'] = car_simplify(response.json())

    response = get_data_from_service(
        'http://' + os.environ['PAYMENT_SERVICE_HOST'] + ':' + os.environ['PAYMENT_SERVICE_PORT']
        + '/api/v1/payment/' + rental['paymentUid'], timeout=5)
    if response is None:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Car Service is Unavailable']
            })
        )
    rental['payment'] = response.json()
    del rental['paymentUid']

    return Response(
        status=200,
        content_type='application/json',
        response=json.dumps(rental)
    )