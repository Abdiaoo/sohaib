import json 
from quart import Blueprint, Response, request
from .models.cars_model import CarsModel

delete_car_order_blueprint = Blueprint('delete_car_order',__name__, )

@delete_car_order_blueprint.route('/api/v1/cars/<string:carUid>/order', methods=['DELETE'])

async def delete_car_order(carUid: str) -> Response:
    try:
        car = CarsModel.select().where(
            CarsModel.car_uid == carUid
        ).get()

        if car.availability is True:
            return Response(
                status=403,
                content_type='application/json',
                response=json.dumps({
                    'errors': ['Car Not Order it']
                })
            )
        car.availability = True
        car.save()

        return Response(
                status=200,
                content_type='application/json',
                response=json.dumps({
                    'Message': ['Car Order Deleted Successfully']
                })
        )
    except:
        return Response(
            status=404,
            content_type='application/json',
            response=json.dumps({
                'errors': ['There is No such this Uid in the Database']
            })
        )