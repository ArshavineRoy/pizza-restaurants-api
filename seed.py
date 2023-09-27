from server.app import app
from server.models import db, Restaurant, Pizza, RestaurantPizza
from faker import Faker
import random


ke_restaurants = [
    "Java House",
    "Artcaffe",
    "Cafe Deli",
    "Kilimanjaro Jamia",
    "Villa Rosa Kempinski",
    "Carnivore Restaurant",
    "Talisman Restaurant",
    "Mama Oliech Restaurant",
    "Nyama Mama",
    "Habesha Restaurant",
    "The Talisman",
    "Mama Rocks Gourmet Burgers",
    "About Thyme Restaurant",
    "Cafe Maghreb",
    "Lord Erroll Gourmet Restaurant",
    "Que Pasa Bar & Bistro",
    "Sankara Nairobi, Sarabi Rooftop Bar",
    "Anghiti Restaurant",
    "Seven Seafood & Grill",
    "Zen Garden",
    "Hashmi BBQ",
    "Le Palanka"
]

pizza_flavors = [
    "Margherita",
    "Pepperoni",
    "Hawaiian",
    "Supreme",
    "BBQ Chicken",
    "Veggie Supreme",
    "Meat Lovers",
    "Buffalo Chicken",
    "Mushroom and Swiss",
    "White Garlic",
    "Pesto and Tomato",
    "Four Cheese",
    "Spinach and Feta",
    "Sausage and Peppers",
    "Mediterranean",
    "BBQ Pulled Pork",
    "Shrimp Scampi",
    "Taco Pizza",
    "Alfredo Chicken",
    "BLT Pizza",
    "Philly Cheesesteak",
    "Caprese",
    "Greek Pizza",
    "Breakfast Pizza",
    "Truffle and Mushroom"
]

pizza_ingredients = [
    "Tomato Sauce",
    "Mozzarella Cheese",
    "Pepperoni Slices",
    "Ham",
    "Pineapple Chunks",
    "Green Bell Pepper",
    "Onion",
    "Olives",
    "Mushrooms",
    "BBQ Sauce",
    "Grilled Chicken",
    "Red Onion",
    "Bacon",
    "Ranch Dressing",
    "Garlic Sauce",
    "Parmesan Cheese",
    "Pesto Sauce",
    "Tomato Slices",
    "Cheddar Cheese",
    "Sausage",
    "Jalapeno Peppers",
    "Feta Cheese",
    "Shrimp",
    "Taco Seasoning",
    "Alfredo Sauce",
    "Lettuce",
    "Tomato",
    "Beef",
    "Mayonnaise",
    "Ketchup",
    "Philly Steak",
    "Fresh Basil",
    "Mozzarella Pearls",
    "Kalamata Olives",
    "Eggs",
    "Béchamel Sauce",
    "Truffle Oil",
]


fake = Faker()


if __name__ == '__main__':
    with app.app_context():

        Restaurant.query.delete()
        Pizza.query.delete()
        RestaurantPizza.query.delete()

        restaurants = []
        for res in ke_restaurants:
            restaurant = Restaurant(
                name=res,
                address=f"{fake.street_address()}, Nairobi"
            )

            restaurants.append(restaurant)
            
        db.session.add_all(restaurants)

        pizzas = []
        for pz in pizza_flavors:

            all_ingredients = {
                f"{random.choice(pizza_ingredients)}, " +\
                f"{random.choice(pizza_ingredients)}, " +\
                f"{random.choice(pizza_ingredients)}, " +\
                f"{random.choice(pizza_ingredients)}, " +\
                f"{random.choice(pizza_ingredients)}"
            }

            pizza = Pizza(
                name=pz,
                ingredients=', '.join(all_ingredients)
            )

            pizzas.append(pizza)
            
        db.session.add_all(pizzas)

        restaurant_pizzas = []
        for restaurant in restaurants:
            for i in range(random.randint(1, 4)):
                restaurant_pizza=RestaurantPizza(
                    price=random.randint(1, 30),
                    restaurant=restaurant,
                    pizza=random.choice(pizzas)
                )

                restaurant_pizzas.append(restaurant_pizza)

        db.session.add_all(restaurant_pizzas)

        db.session.commit()

        print("Db seeded successfully.")
