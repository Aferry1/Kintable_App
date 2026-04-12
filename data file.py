#Rida Data Table of app
from models import User, Meal, Home, Table, Seat, Dependent, CuisineStyle, ConversationTopic
# --- USERS ---
hostfamily1 = User("User1", "John Miller", "host", True)
hostfamily2 = User("User2", "James Washington", "host", True)
hostfamily3 = User("User3", "George Mason", "host", True)

# --- HOMES ---
home1 = Home("Home1", "123 Oak Street", "St. Louis, MO", "Miller Home")
home2 = Home("Home2", "456 Elm Avenue", "St. Louis, MO", "Washington Home")
home3 = Home("Home3", "789 Pine Road", "St. Louis, MO", "Mason Home")

# --- TABLES ---
table1 = Table("Table1", "Miller Dining Table", 6)
table2 = Table("Table2", "Washington Dining Table", 8)
table3 = Table("Table3", "Mason Dining Table", 4)

# --- SEATS ---
seats_table1 = [Seat(f"Seat1_{i}", True) for i in range(1, 7)]
seats_table2 = [Seat(f"Seat2_{i}", True) for i in range(1, 9)]
seats_table3 = [Seat(f"Seat3_{i}", True) for i in range(1, 5)]

# --- MEALS ---
meal1 = Meal("Meal1", "Taco Salad", "Taco salad with fresh toppings and crunchy tortilla chips", "April 5")
meal2 = Meal("Meal2", "Hamburgers", "Homemade grilled burgers with toppings and waffle fries", "April 6")
meal3 = Meal("Meal3", "Pasta Bake", "Baked pasta in alfredo sauce with chicken", "April 7")

# --- CUISINE STYLES ---
cuisine1 = CuisineStyle("Cuisine1", "Mexican", "Latin America")
cuisine2 = CuisineStyle("Cuisine2", "American", "North America")
cuisine3 = CuisineStyle("Cuisine3", "Italian", "Europe")

# --- CONVERSATION TOPICS ---
topic1 = ConversationTopic("Topic1", "Military Life", "Community")
topic2 = ConversationTopic("Topic2", "Parenting Tips", "Family")
topic3 = ConversationTopic("Topic3", "Neighborhood Events", "Local")

# --- RELATIONSHIPS ---

# Users -> Homes
hostfamily1.hosted_home = home1
hostfamily2.hosted_home = home2
hostfamily3.hosted_home = home3

# Homes -> Tables (bidirectional)
home1.table = table1
home2.table = table2
home3.table = table3

table1.home = home1
table2.home = home2
table3.home = home3

# Tables -> Seats
table1.seats = seats_table1
table2.seats = seats_table2
table3.seats = seats_table3

for seat in seats_table1:
    seat.table = table1
for seat in seats_table2:
    seat.table = table2
for seat in seats_table3:
    seat.table = table3

# Tables -> Meals (bidirectional)
table1.meals.append(meal1)
table2.meals.append(meal2)
table3.meals.append(meal3)

meal1.table = table1
meal2.table = table2
meal3.table = table3

# Meals -> Cuisine Styles (bidirectional)
meal1.cuisine_styles.append(cuisine1)
meal2.cuisine_styles.append(cuisine2)
meal3.cuisine_styles.append(cuisine3)

cuisine1.meals.append(meal1)
cuisine2.meals.append(meal2)
cuisine3.meals.append(meal3)

# Meals -> Conversation Topics (bidirectional)
meal1.conversation_topics.append(topic1)
meal2.conversation_topics.append(topic2)
meal3.conversation_topics.append(topic3)

topic1.meals.append(meal1)
topic2.meals.append(meal2)
topic3.meals.append(meal3)

# --- MEAL RECORDS ---
meal_records = [
    {"meal": meal1, "host": hostfamily1, "home": home1, "table": table1},
    {"meal": meal2, "host": hostfamily2, "home": home2, "table": table2},
    {"meal": meal3, "host": hostfamily3, "home": home3, "table": table3},
]

# --- MEAL INFO FUNCTION ---
def meal_info_data():
    return [
        {
            "name": record["meal"].title,
            "host": record["host"].name,
            "date": record["meal"].date_prepared,
            "description": record["meal"].description,
            "location": record["home"].name,
            "seats_available": sum(1 for s in record["table"].seats if s.is_available),
            "cuisine": record["meal"].cuisine_styles[0].name if record["meal"].cuisine_styles else "N/A",
            "topic": record["meal"].conversation_topics[0].topic if record["meal"].conversation_topics else "N/A"
        }
        for record in meal_records
    ]


if __name__ == "__main__":
    for meal in meal_info_data():
        print(meal)

     #Done by Rida Akhter
