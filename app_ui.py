##navigation
class App:
    def __init__(self):
        self.current_screen = "home"
    def navigate(self, screen):
        self.current_screen = screen
        self.render()
    def render(self):
        if self.current_screen == "home":
            show_home_screen()
        elif self.current_screen == "reservations":
            show_reservations_screen()
        elif self.current_screen == "host":
            show_host_screen()
        elif self.current_screen == "connections":
            show_connections_screen()
        elif self.current_screen == "profile":
            show_profile_screen()
#home/discover screen
def show_home_screen():
    print("\n--- HOME / DISCOVER ---")
    print("Good evening, User!")
    print("4 meals currently available in your area\n")

    meals = get_meals()
    for meal in meals:
        print(f"{meal['name']} by {meal['host']}")

  #fake data
  def get_meals():
    return [
        {"name": "Taco Salad", "host": "John Miller"},
        {"name": "Hamburgers", "host": "James Washington"},
        {"name": "Pasta Bake", "host": "George Mason"}
    ]

#other screens
def show_reservations_screen():
    print("\n--- RESERVATIONS ---")

def show_host_screen():
    print("\n--- HOST A MEAL ---")

def show_connections_screen():
    print("\n--- CONNECTIONS ---")

def show_profile_screen():
    print("\n--- PROFILE ---")


#run
if __name__ == "__main__":
    app = App()
    app.render()

    # test navigation
    app.navigate("reservations")
    app.navigate("host")
