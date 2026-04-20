
import json
import os
from models import User

USER_FILE = 'users.json'
MEAL_FILE = 'meals.json'

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as file:
        data = json.load(file)

    users = {}
    for username, info in data.items():
        users[username] = User(
            id=info["id"], 
            name=info["name"], 
            role=info["role"], 
            active=info["active"]
        )
    return users

def save_user(new_user):
    users = load_users()
    data = {}
    

    for u_id, uobj in users.items():
        data[u_id] = {
            "id": uobj.id,
            "name": uobj.name,
            "role": uobj.role,
            "active": uobj.active
        }
        
    data[new_user.id] = {
        "id": new_user.id,
        "name": new_user.name,
        "role": new_user.role,
        "active": new_user.active
    }
    
  
    with open(USER_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def load_meals():
    if not os.path.exists(MEAL_FILE):
        return [] 
        
    with open(MEAL_FILE, 'r') as file:
        return json.load(file)

def save_meal(new_meal):
    meals = load_meals()
    meals.append(new_meal)
    
    with open(MEAL_FILE, "w") as file:
        json.dump(meals, file, indent=4)
        

    ## import data management 
    
 
