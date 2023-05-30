import os
import json
from quart import Blueprint, Response, request, render_template_string
from .service_requests import post_data_from_service
from quart import Quart, render_template
from quart import url_for

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/api/v1/login', methods=['GET'])
async def login() -> Response:
    return await render_template('login.html')

# @handlelogin.route('/api/v1/logeeeein', methods=['GET'])
# async def get_cars() -> Response:
#     response = post_data_from_service('http://' + os.environ['PROVIDER_SERVICE_HOST'] + ':' +
#                                     os.environ['PROVIDER_SERVICE_PORT'] + '/' + 'api/v1/session/login', timeout=5)
#     if response:
#         cars_data = response.json()['items']
#         user_avatar = url_for('static', filename='images/avatars/non.jpg')
#         user_name = 'John Doe'
#         return await render_template_string(open('templates/cars.html').read(), cars_data=cars_data,
#                                             user_avatar=user_avatar, user_name=user_name)
#     else:
#         return Response(
#             status=500,
#             content_type='application/json',
#             response=json.dumps({
#                 'errors': ['Cars Service is Unavailable']
#             })
#         )