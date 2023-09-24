#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

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
            response_dict = [restaurant.to_dict() for restaurant in restaurants]

            response = make_response(
                response_dict,
                200
            )
            return response
        


api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):
    def get(self):
        pass


api.add_resource(RestaurantByID, '/restaurants/<int:id>')


class Pizzas(Resource):
    def get(self):
        pass

api.add_resource(Pizzas, '/pizzas')


if __name__ == '__main__':
    app.run(port=5555, debug=True)