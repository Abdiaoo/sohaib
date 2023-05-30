from quart import Quart
from blueprints.models.cars_model import CarsModel
from blueprints.get_cars import get_cars_blueprint
from blueprints.get_car import get_car_blueprint
from blueprints.post_car_order import post_car_order_blueprint
from blueprints.delete_car_order import delete_car_order_blueprint

app = Quart(__name__)
app.register_blueprint(get_cars_blueprint)
app.register_blueprint(get_car_blueprint)
app.register_blueprint(post_car_order_blueprint)
app.register_blueprint(delete_car_order_blueprint)

def create_tables():
    CarsModel.drop_table()
    CarsModel.create_table()

    CarsModel.get_or_create(
        id=1,
        car_uid="109b42f3-198d-4c89-9276-a7520a7120ab",
        brand="Mercedes Benz",
        model="GLA 250",
        registration_number="ЛО777Х799",
        power=249,
        type="SEDAN",
        price=3500,
        availability=True
    )

    CarsModel.get_or_create(
        id=2,
        car_uid="2b251ea7-3c22-4a78-b56c-4fbf4fe9a8b2",
        brand="BMW",
        model="X5",
        registration_number="ABC123",
        power=300,
        type="SUV",
        price=5000,
        availability=True
    )

if __name__ == '__main__':
    database = 'database.db'

    CarsModel._meta.database.init(database)

    create_tables()
    app.run(host='0.0.0.0', port=8070)