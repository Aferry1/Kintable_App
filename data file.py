from models import User, Meal

hostfamily1 = User("User1", "John Miller", "host", True)
hostfamily2 = User("User2", "James Washington", "host", True)
hostfamily3 = User("User3", "George Mason", "host", True)

meal1 = Meal("Meal1", "Taco Salad", "Taco salad with fresh toppings and crunchy tortilla chips", "April 5")
meal2 = Meal("Meal2", "Hamburgers", "Homemade grilled burgers with toppings and waffle fries", "April 6")
meal3 = Meal("Meal3", "Pasta Bake", "Baked pasta in alfredo sauce with chicken", "April 7")

meal_records = [
    {"meal": meal1, "host": hostfamily1},
    {"meal": meal2, "host": hostfamily2},
    {"meal": meal3, "host": hostfamily3}
]

def meal_info_data():
    return [
        {
            "name": record["meal"].title,
            "host": record["host"].name,
            "date": record["meal"].date_prepared,
            "description": record["meal"].description
        }
        for record in meal_records
    ]

for meal in meal_info_data():
    print(meal)