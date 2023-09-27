#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource, Namespace, fields

from server.models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JSON_SORT_KEYS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)

api = Api()
api.init_app(app)

ns = Namespace("api")
api.add_namespace(ns)

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


# restx swagger input
restaurant_pizza_model = api.model(
    "RestaurantPizza Input", {
        "price": fields.Integer,
        "restaurant_id": fields.Integer,
        "pizza_id": fields.Integer,
    }
)

@ns.route("/restaurants")
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

@ns.route("/restaurants/<int:id>")
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
                "error": "Restaurant not found."
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

@ns.route("/pizzas")
class Pizzas(Resource):

    def get(self):
        pizzas = Pizza.query.all()

        if not pizzas:
            response_body = {
                "error": "Pizza not found."
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

@ns.route("/restaurant_pizzas")
class RestaurantPizzas(Resource):

    @ns.expect(restaurant_pizza_model)
    def post(self):
        restaurant_pizza = RestaurantPizza(
            price=ns.payload["price"],
            restaurant_id=ns.payload["restaurant_id"],
            pizza_id=ns.payload["pizza_id"]
        )
        # price = ns.payload["price"]
        restaurant = Restaurant.query.filter(Restaurant.id == int(ns.payload["restaurant_id"])).first()
        pizza = Pizza.query.filter(Pizza.id == int(ns.payload["pizza_id"])).first()


        if not pizza and not restaurant:
            return make_response(
                {"error": "Restaurant and Pizza not found."},
                404
            )
        elif not restaurant:
            return make_response(
                {"error": "Restaurant not found."},
                404
            )
        elif not pizza:
            return make_response(
                {"error": "Pizza not found."},
                404
            )
        elif 1 < ns.payload["price"] > 30:
            return make_response(
                {
                    "error": "Validation Error",
                    "message": "Price must be between 1 and 30"
                },
                422
            )
        else:
            db.session.add(restaurant_pizza)
            db.session.commit()        
            
            response=make_response(
                pizza_schema.dump(pizza),
                201
            )

            return response
