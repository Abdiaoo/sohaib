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
