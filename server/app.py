#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_marshmallow import Marshmallow


from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_SORT_KEYS"] = False
app.json.compact = False



 

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)

api = Api(app)


class RestaurantSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Restaurant
        ordered=True

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()

restaurants_schema = RestaurantSchema(many=True)

class RestaurantByIDSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Restaurant
        ordered=True

    id = ma.auto_field()
    name = ma.auto_field()
    address = ma.auto_field()



restaurant_by_id_schema = RestaurantByIDSchema()

class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the RestaurantPizza RESTful API"
        }
        response = make_response(
            response_dict,
            200
        )

        return response
api.add_resource(Home, '/')

class Restaurants(Resource):

    def get(self):
        restaurants = Restaurant.query.all()

        if not restaurants:
            response_body = {
                "message": "This record does not exist in our database. Please try again."
            }

            response = make_response(
                response_body,
                404
            )
            return response
        else:

            response = make_response(
                restaurants_schema.dump(restaurants),
                200
            )
            return response

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):

        restaurant = Restaurant.query.filter(Restaurant.id == id).first()

        if not restaurant:
            response_body = {
                "message": "This record does not exist in our database. Please try again."
            }

            response = make_response(
                response_body,
                404
            )

            return response
        
        else:

            response = make_response(
                restaurant_by_id_schema.dump(restaurant),
                200
            )
            return response


api.add_resource(RestaurantByID, '/restaurants/<int:id>')


class Pizzas(Resource):
    def get(self):
        pass

api.add_resource(Pizzas, '/pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)