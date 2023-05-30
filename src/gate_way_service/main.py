from quart import Quart
import os
from blueprints.get_cars_blueprint import get_cars_blueprint
from blueprints.get_rentals_blueprint import get_rentals_blueprint
from blueprints.get_rental_blueprint import get_rental_blueprint
from blueprints.post_rental_blueprint import post_rentals_blueprint
from blueprints.delete_rental_blueprint import delete_rental_blueprint
from blueprints.post_rental_finish_blueprint import post_rental_finish_blueprint
from blueprints.login_blueprint import login_blueprint
from quart import url_for
from playhouse.db_url import connect
from peewee import SqliteDatabase

app = Quart(__name__,static_folder='static')

os.environ['CARS_SERVICE_HOST'] = "localhost"
os.environ['CARS_SERVICE_PORT'] = "8070"
os.environ['PAYMENT_SERVICE_HOST'] = "localhost"
os.environ['PAYMENT_SERVICE_PORT'] = "8050"
os.environ['RENTAL_SERVICE_HOST'] = "localhost"
os.environ['RENTAL_SERVICE_PORT'] = "8060"
os.environ['PROVIDER_SERVICE_HOST'] = "localhost"
os.environ['PROVIDER_SERVICE_PORT'] = "8040"
db_path = os.path.join(os.getcwd(), 'database.db')

database = SqliteDatabase(db_path)

database.connect()

app.database = database

app.register_blueprint(get_cars_blueprint)
app.register_blueprint(get_rentals_blueprint)
app.register_blueprint(post_rentals_blueprint)
app.register_blueprint(delete_rental_blueprint)
app.register_blueprint(post_rental_finish_blueprint)
app.register_blueprint(get_rental_blueprint)
app.register_blueprint(login_blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
