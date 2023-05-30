import os
import json
from quart import Blueprint, Response, request, render_template_string
from .service_requests import get_data_from_service
from quart import Quart, render_template
from quart import url_for

get_cars_blueprint = Blueprint('get_cars', __name__)

@get_cars_blueprint.route('/api/v1/cars/', methods=['GET'])
async def get_cars() -> Response:
    response = get_data_from_service('http://' + os.environ['CARS_SERVICE_HOST'] + ':' +
                                    os.environ['CARS_SERVICE_PORT'] + '/' + 'api/v1/cars?' +
                                    request.full_path.split('?')[-1], timeout=5)
    if response:
        cars_data = response.json()['items']
        user_avatar = url_for('static', filename='images/avatars/non.jpg')
        user_name = 'John Doe'
        return await render_template_string(open('templates/cars.html').read(), cars_data=cars_data,
                                            user_avatar=user_avatar, user_name=user_name)
    else:
        return Response(
            status=500,
            content_type='application/json',
            response=json.dumps({
                'errors': ['Cars Service is Unavailable']
            })
        )
