# fake data
def get_meals():
    return [
        {"name": "Taco Salad", "host": "John Miller"},
        {"name": "Hamburgers", "host": "James Washington"},
        {"name": "Pasta Bake", "host": "George Mason"}
    ]

# navigation
class App:
    def __init__(self):
        self.current_screen = "home"
    def navigate(self, screen):
        self.current_screen = screen
        self.render()
    def render(self):
        if self.current_screen == "home":
            show_home_screen(self)
        elif self.current_screen == "reservations":
            show_reservations_screen(self)
        elif self.current_screen == "host":
            show_host_screen(self)
        elif self.current_screen == "connections":
            show_connections_screen(self)
        elif self.current_screen == "profile":
            show_profile_screen(self)

# home/discover screen
def show_home_screen(app):
    print("\n--- HOME / DISCOVER ---")
    print("Good evening User!")
    meals = get_meals()
    print(f"{len(meals)} meals currently available in your area\n")
    for meal in meals:
        print(f"{meal['name']} by {meal['host']}")
    print("\nChoose where to go next:")
    print("1. Reservations")
    print("2. Host a Meal")
    print("3. Connections")
    print("4. Profile")
    print("5. Exit")

    choice = input("Enter choice: ")
    if choice == "1":
        app.navigate("reservations")
    elif choice == "2":
        app.navigate("host")
    elif choice == "3":
        app.navigate("connections")
    elif choice == "4":
        app.navigate("profile")
    elif choice == "5":
        print("Goodbye!")
    else:
        print("Invalid choice. Returning to home.")
        app.navigate("home")

def show_reservations_screen(app):
    print("\n--- RESERVATIONS ---")
    print("You have no reservations yet.")
    input("Press enter to return to home...")
    app.navigate("home")
def show_host_screen(app):
    print("\n--- HOST A MEAL ---")
    print("Host meal form will go here.")
    input("Press Enter to return to home...")
    app.navigate("home")

def show_connections_screen(app):
    print("\n--- CONNECTIONS ---")
    print("Your saved connections will appear here.")
    input("Press Enter to return to home...")
    app.navigate("home")

def show_profile_screen(app):
    print("\n--- PROFILE ---")
    print("User profile details will appear here.")
    input("Press Enter to return to home...")
    app.navigate("home")
if __name__ == "__main__":
    app = App()
    app.render()
