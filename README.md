# Pizza Restaurants Flask API

## Phase 4 Week 1 : Flask Code Challenge

[![license](https://img.shields.io/badge/license-%20MIT%20-green.svg)](./LICENSE)
![python version](https://img.shields.io/badge/python-3.10.12-blue.svg)
![Flask version](https://img.shields.io/badge/flask-2.3.3-red.svg)
![Flask-RESTX version](https://img.shields.io/badge/Flask_RESTX-1.1.0-cyan.svg)
![Gunicorn version](https://img.shields.io/badge/gunicorn-21.2.0-orange.svg)
![Pytest version](https://img.shields.io/badge/pytest-7.4.2-white.svg)

## Introduction

This is a Flask API that simulates a Pizza Restaurant domain.

![API Image](image.png)

## Features

- Find all restaurants
- Find a restaurant by ID
- Delete a restaurant by ID
- Find all pizzas
- Create a new RestaurantPizza that is associated with an existing Pizza and Restaurant

## Installation

### 1. Clone the repository

```txt
git clone https://github.com/ArshavineRoy/pizza-restaurants-api
```

### 2. Navigate to the project's directory

```txt
cd pizza-restaurants-api
```

### 3. Install required dependencies

```python
pipenv install
```

- If `pipenv` is not already installed, you can do so using `pip`:

  ```python
  pip install pipenv
  ```

### 4. Activate the virtual environment

```python
pipenv shell
```

### 5. If needed, seed the database with

```python
python3 seed.py
```

### 6. Run the Flask server from the root directory

```python
python3 run.py
```

### 7. Use an API management tool e.g., `Postman` / `Insomnia` to make requests

## Usage

1. **GET/restaurants**

   Returns JSON data for restaurants in the format below:

   ```JSON
    [
      {
        "id": 1,
        "name": "Dominion Pizza",
        "address": "Good Italian, Ngong Road, 5th Avenue"
      },
      {
        "id": 2,
        "name": "Pizza Hut",
        "address": "Westgate Mall, Mwanzi Road, Nrb 100"
      }
    ]
   ```

1. **GET/restaurants/:id**

   Returns JSON data for the restaurant in the format below:

   ```JSON
     {
      "id": 1,
      "name": "Dominion Pizza",
      "address": "Good Italian, Ngong Road, 5th Avenue",
      "pizzas": [
        {
          "id": 1,
          "name": "Cheese",
          "ingredients": "Dough, Tomato Sauce, Cheese"
        },
        {
          "id": 2,
          "name": "Pepperoni",
          "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
        }
       ]
     }
   ```

1. **DELETE /restaurants/:id**

   Removes a restaurant from the database along with any RestaurantPizzas that are associated with it and returns an empty dictionary.

1. **GET /pizzas**

   Return JSON data for pizzas in the format below:

   ```JSON
   [
      {
        "id": 1,
        "name": "Hawaiian",
        "ingredients": "Dough, Tomato Sauce, Cheese"
      },
      {
        "id": 2,
        "name": "Pepperoni",
        "ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
      }
    ]
   ```

1. **POST /restaurant_pizzas**

   Creates a new RestaurantPizza that is associated with an existing Pizza and Restaurant and returns JSON data for the pizza.

   ```JSON
   [
     {
       "id": 10,
       "name": "Hawaiian",
       "ingredients": "Dough, Tomato Sauce, Cheese"
     }
   ]
   ```

## Author & License

Authored by [Arshavine Waema](https://github.com/ArshavineRoy).

Licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
