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


class PizzasSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Pizza
        ordered=True
    
    id = ma.auto_field()
    name = ma.auto_field()
    ingredients = ma.auto_field()

pizza_schema = PizzasSchema()
pizzas_schema = PizzasSchema(many=True)

class RestaurantPizzaSchema(ma.SQLAlchemySchema):

    class Meta:
        model = RestaurantPizza
        ordered=True
    
    id = ma.auto_field()
    price = ma.auto_field()

restaurant_pizza_schema = RestaurantPizzaSchema()


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
                "error": "Restaurant not found"
            }

            response = make_response(
                response_body,
                404
            )

            return response
        
        else:

            pizzas = Pizza.query.join(RestaurantPizza).filter(RestaurantPizza.restaurant_id == id).all()

            response_body = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": []
            }

            for pizza in pizzas:
                pizza_data = {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients
                }
                response_body["pizzas"].append(pizza_data)

            response = make_response(
                response_body,
                200
            )
            return response
        
    def delete(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        
        if not restaurant:
            response_body = {
                "error": "Restaurant not found"
            }

            response = make_response(
                response_body,
                404
            )

            return response
        
        else:
        
            db.session.delete(restaurant)
            db.session.commit()

            response_body ={}

            response = make_response(
                response_body,
                204
            )

            return response

api.add_resource(RestaurantByID, '/restaurants/<int:id>')


class Pizzas(Resource):

    def get(self):
        pizzas = Pizza.query.all()

        if not pizzas:
            response_body = {
                "error": "Pizza not found"
            }

            response = make_response(
                response_body,
                404
            )
            return response
        else:

            response = make_response(
                pizzas_schema.dump(pizzas),
                200
            )
            return response

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):


    def post(self):
        restaurant_pizza = RestaurantPizza(
            price=int(request.form["price"]),
            restaurant_id=int(request.form["restaurant_id"]),
            pizza_id=int(request.form["pizza_id"])
        )

        pizza = Pizza.query.filter(Pizza.id == int(request.form["pizza_id"])).first()

        db.session.add(restaurant_pizza)
        db.session.commit()        
        
        response=make_response(
            pizza_schema.dump(pizza),
            201
        )

        return response

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')
