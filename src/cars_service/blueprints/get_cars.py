import json 
from quart import Blueprint, Response, request
from .models.cars_model import CarsModel

#http://0.0.0.0:8070/api/v1/cars/?page=1&size=10

get_cars_blueprint = Blueprint('get_cars', __name__, )

def validate_args(args):
    errors = []
    if 'page' in args.keys():
        try:
            page = int(args['page'])
            if page <= 0:
                errors.append('Page Must Be Greater Than Zero')
        except ValueError:
            errors.append('Page Must Be A Number')
            page = None
    
    else:
        errors.append('Page Must Be Define')
        page = None

    if 'size' in args.keys():
        try:
            size = int(args['size'])
            if size <= 0:
                errors.append('Size Must Be Greater Than Zero')
        except ValueError:
            size = None
            errors.append('Size Must Be A Number')
    else:
        errors.append('Size Must Be Define')
        size = None

    if 'showAll' in args.keys():
        if args['showAll'].lower() == 'true':
            show_all = True
        elif args['showAll'].lower() == 'false':
            show_all = False
        else:
            errors.append('showAll Must Be True or False')
            show_all = None
    else:
        show_all = False

    return page, size, show_all, errors


@get_cars_blueprint.route('/api/v1/cars/', methods=['GET'])
async def get_cars() -> Response:
    page, size, show_all, errors = validate_args(request.args)

    if len(errors) > 0:
        return Response(
            status=400,
            content_type='application/json',
            response=json.dumps({
                'errors': errors
            })
        )
    
    if not show_all:
        query = CarsModel.select().where(CarsModel.availability == True)
        count_total = query.count()
        cars = [car.to_dict() for car in query.paginate(page, size)]
    else:
        count_total = CarsModel.select().count()
        cars = [car.to_dict() for car in CarsModel.select().paginate(page, size)]

    return Response(
        status=200,
        content_type='application/json',
        response=json.dumps({
            "page": page,
            "pageSize": size,
            "totalElements": count_total,
            "items": cars
        })
    ) 