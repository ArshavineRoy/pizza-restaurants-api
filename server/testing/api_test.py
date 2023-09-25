import json
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

class TestFlaskAPI:
    '''Flask RESTful API'''

    def test_restaurants_endpoint(self):
        '''has a resource available at "/restaurants".'''
        response = app.test_client().get('/restaurants')
        assert(response.status_code == 200)

    def test_restaurants_endpoint_returns_json(self):
        '''provides a response content type of application/json at "/restaurants".'''
        response = app.test_client().get('/restaurants')
        assert response.content_type == 'application/json'

    def test_restaurants_endpoint_returns_list_of_restaurant_objects(self):
        '''returns JSON representing models.Restaurant objects.'''
        with app.app_context():
            res = Restaurant(name="Villa Rosa Kempinski", address="4801 Charles Falls, Nairobi")
            db.session.add(res)
            db.session.commit()

            response = app.test_client().get('/restaurants')
            data = json.loads(response.data.decode())
            assert(type(data) == list)
            for record in data:
                assert(type(record) == dict)
                assert(record['id'])
                assert(record['name'])
                assert(record['address'])

            db.session.delete(res)
            db.session.commit()

    def test_get_restaurant_by_id(self):
        '''has a resource available at "/restaurants/:id".'''
        response = app.test_client().get('/restaurants/1')
        assert(response.status_code == 200)

    def test_get_restaurant_by_id_returns_one_restaurant(self):
        '''returns JSON representing one Restaurant object at "/restaurants/:id".'''
        response = app.test_client().get('/restaurants/1')
        data = json.loads(response.data.decode())

        assert(type(data) == dict)
        assert(data["id"])
        assert(data["name"])
        assert(data["address"])
        assert(data["pizzas"])

    def test_delete_restaurant_by_id_deletes_restaurant(self):
        '''can DELETE restaurants through "/restaurants/:id".'''
        with app.app_context():
            vk = Restaurant(
                name="Villa Rosa Kempinski", 
                address="4801 Charles Falls, Nairobi"
            )

            db.session.add(vk)
            db.session.commit()
            
            response = app.test_client().delete(f'/restaurants/{vk.id}')
            data = response.data.decode()

            assert(not data)

    def test_pizzas_endpoint(self):
        '''has a resource available at "/pizzas".'''
        response = app.test_client().get('/pizzas')
        assert(response.status_code == 200)

    def test_pizzas_endpoint_returns_json(self):
        '''provides a response content type of application/json at "/pizzas".'''
        response = app.test_client().get('/pizzas')
        assert response.content_type == 'application/json'

    def test_pizzas_endpoint_returns_list_of_pizza_objects(self):
        '''returns JSON representing models.Pizza objects.'''
        with app.app_context():
            pizza = Pizza(name="Supreme", ingredients="Shrimp, Ham, Eggs")
            db.session.add(pizza)
            db.session.commit()

            response = app.test_client().get('/pizzas')
            data = json.loads(response.data.decode())
            assert(type(data) == list)
            for record in data:
                assert(type(record) == dict)
                assert(record['id'])
                assert(record['name'])
                assert(record['ingredients'])

            db.session.delete(pizza)
            db.session.commit()

    def test_creates_restaurant_pizzas(self):
        '''can POST new restaurant_pizzas through "/restaurant_pizzas".'''

        with app.app_context():

            last = RestaurantPizza.query.order_by(RestaurantPizza.id.desc()).first()

            db.session.delete(last)
            db.session.commit()

            response = app.test_client().post(
                '/restaurant_pizzas',
                data={
                    "price": 23,
                    "restaurant_id": 1,
                    "pizza_id": 1,
                }
            )

            last = RestaurantPizza.query.order_by(RestaurantPizza.id.desc()).first()

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            assert last.price == 23
