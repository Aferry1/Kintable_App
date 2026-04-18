# Written by Adam Ferry
from models import User, Meal, Table
from datetime import date

# Account setup
def user_registration():
    print("\nWelcome to Kintable! Please enter your login credentials.\n")

    first_name = input("First name: ")
    last_name = input("Last name: ")
    user_id = input("Username: ")

    name = first_name + " " + last_name
    # User.role is defined based on user activity
    test_user = User(user_id, name, None, True)

    print("\nHi " + test_user.id + "! \n" 
          + "We're getting everything ready for you... \n")
    
    return test_user

# Menu actions
# This is a temporary way to simulate functionality without a GUI
def user_actions():
    print("Please select an option from the list below: \n" +
        "0 - Quit \n" +
        "1 - Host a meal")
    user_choice = int(input())
    # Consider match statements
    if (user_choice == 0):
        print("\nOkay. See you later!")
    elif (user_choice == 1):
        host_meal()
    else:
        print("\nPlease choose a valid option.")
        user_actions()

# Host meal
def host_meal():
    print("\nWhat are you making today?")
    meal_title = input()
    
    print("\nCould you give a short description of the dish?")
    # Impose string limit?
    meal_description = input()
    
    print("\nHow many extra servings are there?")
    table_capacity = int(input())
    
    print("\nIs there anyone you want to invite?\n" +
          "(Please seperate multiple users with commas.)")
    # Functionality to invite users not included
    invitees = input()
    notified_users = invitees.split(",")
    
    # Define other variables independent of user input (Functionality not yet implemented)
    unique_meal_id = "MyMeal"
    meal_date = date.today()
    unique_table_id = "MyTable"
    table_name = test_user.name + "'s table"

    test_meal = Meal(unique_meal_id, meal_title, meal_description, meal_date)
    test_table = Table(unique_table_id, table_name, table_capacity)
    
    print("\nYour meal has successfully been created!" +
          "\n Returning home...")
    user_actions()
    

# User path
test_user = user_registration()
user_actions()