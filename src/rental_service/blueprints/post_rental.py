import datetime
import json
import uuid
from quart import Blueprint, Response, request
from .models.rental_model import RentalModel


post_rental_blueprint = Blueprint('post_rental', __name__,)


def validate_body(body):
    try:
        body = json.loads(body)
    except:
        return None, ['Can not deserialize body!']

    errors = []
    if 'carUid' not in body or type(body['carUid']) is not str or\
            'dateFrom' not in body or type(body['dateFrom']) is not str or\
            'dateTo' not in body or type(body['dateTo']) is not str or\
            'paymentUid' not in body or type(body['paymentUid']) is not str:
        return None, ['Bad structure body!']

    return body, errors


@post_rental_blueprint.route('/api/v1/rental/', methods=['POST'])
async def post_rental() -> Response:
    if 'X-User-Name' not in request.headers.keys():
        return Response(
            status=400,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Request has not X-User-Name header!']
            })
        )

    user = request.headers['X-User-Name']

    body, errors = validate_body(await request.body)
    if len(errors) > 0:
        return Response(
            status=400,
            content_type='application/json',
            response=json.dumps(errors)
        )

    rental = RentalModel.create(
        rental_uid=uuid.uuid4(),
        username=user,
        car_uid=uuid.UUID(body['carUid']),
        date_from=datetime.datetime.strptime(body['dateFrom'], "%Y-%m-%d").date(),
        date_to=datetime.datetime.strptime(body['dateTo'], "%Y-%m-%d").date(),
        payment_uid=uuid.UUID(body['paymentUid']),
        status='IN_PROGRESS'
    )

    return Response(
        status=200,
        content_type='application/json',
        response=json.dumps(rental.to_dict())
    )



'''

{
  "carUid": "109b42f3-198d-4c89-9276-a7520a7120ab",
  "dateFrom": "2023-06-01",
  "dateTo": "2023-06-05",
  "paymentUid": "3a7f54d6-2513-4bdc-986a-3e04a47d3d20"
}

For Header:

key
X-User-Name

value
anyname


rental uid:

7aaf7a68-dfd4-4d9e-bba9-401c9d752ada

'''