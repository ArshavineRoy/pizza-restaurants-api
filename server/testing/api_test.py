import json
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

class TestPlant:
    '''Flask RESTful API'''

    def test_restaurants_endpoint(self):
        '''has a resource available at "/restaurants".'''
        response = app.test_client().get('/restaurants')
        assert(response.status_code == 200)

    def test_restaurants_endpoint_returns_json(self):
        '''provides a response content type of application/json at "/restaurants"'''
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

    # def test_get_restaurants(self):
    #     '''has a resource available at "/plants/<int:id>".'''
    #     response = app.test_client().get('/plants/1')
    #     assert(response.status_code == 200)

    # def test_plant_by_id_get_route_returns_one_plant(self):
    #     '''returns JSON representing one Plant object at "/plants/<int:id>".'''
    #     response = app.test_client().get('/plants/1')
    #     data = json.loads(response.data.decode())

    #     assert(type(data) == dict)
    #     assert(data["id"])
    #     assert(data["name"])

    # def test_plant_by_id_patch_route_updates_is_in_stock(self):
    #     '''returns JSON representing updated Plant object with "is_in_stock" = False at "/plants/<int:id>".'''
    #     with app.app_context():
    #         plant_1 = Plant.query.filter_by(id=1).first()
    #         plant_1.is_in_stock = True
    #         db.session.add(plant_1)
    #         db.session.commit()
            
    #     response = app.test_client().patch(
    #         '/plants/1',
    #         json = {
    #             "is_in_stock": False,
    #         }
    #     )
    #     data = json.loads(response.data.decode())

    #     assert(type(data) == dict)
    #     assert(data["id"])
    #     assert(data["is_in_stock"] == False)

    # def test_plant_by_id_delete_route_deletes_plant(self):
    #     '''returns JSON representing updated Plant object at "/plants/<int:id>".'''
    #     with app.app_context():
    #         lo = Plant(
    #             name="Live Oak",
    #             image="https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
    #             price=250.00,
    #             is_in_stock=False,
    #         )

    #         db.session.add(lo)
    #         db.session.commit()
            
    #         response = app.test_client().delete(f'/plants/{lo.id}')
    #         data = response.data.decode()

    #         assert(not data)