import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
import json
import os
import re
import hashlib
from models import User, Meal, Table

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEALS_FILE = os.path.join(BASE_DIR, "meals.json")

DEFAULT_MEALS = [
    {"id": "m1", "name": "Taco Salad",  "host": "John Miller",       "desc": "Fresh taco salad with homemade salsa.",      "seats": 3},
    {"id": "m2", "name": "Hamburgers",  "host": "James Washington",   "desc": "Classic backyard burgers, all the fixings.", "seats": 5},
    {"id": "m3", "name": "Pasta Bake",  "host": "George Mason",       "desc": "Cheesy baked penne with Italian sausage.",  "seats": 2},
]

def load_meals():
    if not os.path.exists(MEALS_FILE):
        return DEFAULT_MEALS.copy()
    try:
        with open(MEALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_MEALS.copy()

def save_meals():
    with open(MEALS_FILE, "w", encoding="utf-8") as f:
        json.dump(MEALS, f, indent=2)

MEALS = load_meals()
RESERVATIONS = []
CONNECTIONS_FILE = os.path.join(BASE_DIR, "connections.json")

DEFAULT_CONNECTIONS = [
    {"username": "sarahmitchell", "name": "Sarah Mitchell", "role": "Host"},
    {"username": "tombradley", "name": "Tom Bradley", "role": "Guest"},
]


def load_connections():
    if not os.path.exists(CONNECTIONS_FILE):
        return DEFAULT_CONNECTIONS.copy()
    try:
        with open(CONNECTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONNECTIONS.copy()


def save_connections():
    with open(CONNECTIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(CONNECTIONS, f, indent=2)


CONNECTIONS = load_connections()

USER_DB_FILE = os.path.join(BASE_DIR, "users.json")

# Colour palette — warm, dark, earthy
BG_MAIN   = "#022801"
BG_CARD   = "#60442e"
BG_NAV    = "#60442e"
BG_INPUT  = "#c7d3bf"
ACCENT    = "#E8631A"
BTN_EARTH = "#C4956A"
TXT_CREAM = "#c7d3bf"
TXT_SAGE  = "#4f7543"
TXT_GREEN = "#4f7543"
TXT_WHITE = "#FFFFFF"

# Fonts
F = "DejaVu Sans"
FONT_TITLE  = (F, 24, "bold")
FONT_HEAD   = (F, 18, "bold")
FONT_BODY   = (F, 14)
FONT_SMALL  = (F, 10)
FONT_NAV    = (F, 16, "bold")

FONT_BTN    = (F, 16, "bold")

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

DAYS_OF_MONTH = [str(day) for day in range(1, 32)]

TIME_OPTIONS = []
for hour in range(1, 13):
    for minute in ("00", "15", "30", "45"):
        TIME_OPTIONS.append(f"{hour}:{minute}")


def get_default_meal_date_values():
    tomorrow = date.today() + timedelta(days=1)
    return MONTH_NAMES[tomorrow.month - 1], str(tomorrow.day)


def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}
    try:
        with open(USER_DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users):
    with open(USER_DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


# For a school project, SHA-256 is acceptable. In production, use bcrypt or argon2.
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validate_phone(phone):
    if not re.fullmatch(r"\d+", phone or ""):
        return False, "Cell number must contain digits only with no spaces, dashes, or parentheses."
    return True, ""


def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not password.isalnum():
        return False, "Password must be alphanumeric only."
    if not re.search(r"[A-Z]", password):
        return False, "Password must include at least 1 uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must include at least 1 lowercase letter."
    if not re.search(r"\d", password):
        return False, "Password must include at least 1 number."
    return True, ""


def validate_meal_datetime(month_name, day_value, time_value, am_pm, time_is_tbd):
    if month_name not in MONTH_NAMES:
        return False, "Please select a valid meal month.", "", ""

    if not day_value.isdigit():
        return False, "Please select a valid meal day.", "", ""

    month_num = MONTH_NAMES.index(month_name) + 1
    day_num = int(day_value)
    today = date.today()
    selected_year = today.year

    try:
        selected_date = date(selected_year, month_num, day_num)
    except ValueError:
        return False, "Please select a real calendar date.", "", ""

    if selected_date < today:
        try:
            selected_date = date(selected_year + 1, month_num, day_num)
        except ValueError:
            return False, "Please select a real calendar date.", "", ""

    days_away = (selected_date - today).days
    if days_away < 1:
        return False, "Meal date must be at least tomorrow.", "", ""
    if days_away > 90:
        return False, "Meal date cannot be more than 90 days away.", "", ""

    if time_is_tbd:
        return True, "", selected_date.strftime("%Y-%m-%d"), "TBD"

    if time_value not in TIME_OPTIONS:
        return False, "Please select a valid meal time.", "", ""

    if am_pm not in ("AM", "PM"):
        return False, "Please select AM or PM.", "", ""

    return True, "", selected_date.strftime("%Y-%m-%d"), f"{time_value} {am_pm}"


def format_meal_date_for_display(meal_date):
    try:
        parsed_date = datetime.strptime(meal_date, "%Y-%m-%d")
        return parsed_date.strftime("%B %d").replace(" 0", " ")
    except (ValueError, TypeError):
        return meal_date or "Date TBD"
    
def short_description(text, limit=105):
    if not text:
        return ""
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "..."


# Helper functions for meal sorting and connection matching
def meal_sort_key(meal):
    raw_date = meal.get("date", "9999-12-31")
    raw_time = meal.get("time", "TBD")

    try:
        parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        parsed_date = date.max

    if raw_time == "TBD":
        parsed_time = datetime.strptime("11:59 PM", "%I:%M %p").time()
    else:
        try:
            parsed_time = datetime.strptime(raw_time, "%I:%M %p").time()
        except (ValueError, TypeError):
            parsed_time = datetime.strptime("11:59 PM", "%I:%M %p").time()

    return (parsed_date, parsed_time, meal.get("name", "").lower())


def meal_hosted_by_connection(meal):
    meal_host_name = meal.get("host", "").lower()
    meal_host_username = meal.get("host_username", "").lower()

    for connection in CONNECTIONS:
        connection_name = connection.get("name", "").lower()
        connection_username = connection.get("username", "").lower()
        if meal_host_name and meal_host_name == connection_name:
            return True
        if meal_host_username and meal_host_username == connection_username:
            return True

    return False

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class Card(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_CARD, relief="flat",
                         highlightbackground=TXT_CREAM, highlightthickness=2, **kw)


class PrimaryBtn(tk.Button):
    def __init__(self, parent, text, command, **kw):
        super().__init__(parent, text=text, command=command,
                         bg=BTN_EARTH, fg=TXT_GREEN, font=FONT_BTN,
                         relief="flat", cursor="hand2",
                         highlightbackground=TXT_CREAM, highlightthickness=1,
                         padx=6, pady=2, **kw)
        self.bind("<Enter>", lambda e: self.config(bg="#D4A87A", fg=ACCENT))
        self.bind("<Leave>", lambda e: self.config(bg=BTN_EARTH, fg=TXT_GREEN))


class SecondaryBtn(tk.Button):
    def __init__(self, parent, text, command, **kw):
        super().__init__(parent, text=text, command=command,
                         bg=BG_CARD, fg=TXT_CREAM, font=FONT_BTN,
                         relief="flat", cursor="hand2",
                         highlightbackground=ACCENT, highlightthickness=1,
                         padx=6, pady=2, **kw)
        self.bind("<Enter>", lambda e: self.config(bg="#2F4430"))
        self.bind("<Leave>", lambda e: self.config(bg=BG_CARD))


class KinTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KinTable")
        self.geometry("800x1000")
        self.minsize(640, 480)
        self.configure(bg=BG_MAIN)
        self.resizable(True, True)
        self.current_user = None

        self._container = tk.Frame(self, bg=BG_MAIN)
        self._container.pack(fill="both", expand=True)

        self._screens = {}
        for ScreenClass in (LoginScreen, HomeScreen, ReservationsScreen,
                            HostScreen, ConnectionsScreen, ProfileScreen):
            screen = ScreenClass(self._container, self)
            self._screens[ScreenClass.NAME] = screen
            screen.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.show("login")

    def show(self, name):
        screen = self._screens[name]
        if hasattr(screen, "refresh"):
            screen.refresh()
        screen.lift()


class NavBar(tk.Frame):
    TABS = [
        ("Home",         "home"),
        ("Meals",        "reservations"),
        ("Host a Meal",  "host"),
        ("Connections",  "connections"),
        ("Profile",      "profile"),
    ]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_NAV)
        self._app = app
        self._btns = {}

        tk.Label(self, text="KinTable", font=(F, 13, "bold"),
                 bg=BG_NAV, fg=ACCENT, padx=14).pack(side="left")
        tk.Frame(self, bg=ACCENT, width=2).pack(side="left", fill="y", pady=6)

        for label, name in self.TABS:
            btn = tk.Button(self, text=label, font=FONT_NAV,
                            bg=BG_NAV, fg=TXT_GREEN,
                            relief="flat", cursor="hand2",
                            padx=12, pady=10,
                            command=lambda n=name: self._app.show(n))
            btn.pack(side="left", fill="y")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1F301F", fg=ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_NAV, fg=TXT_GREEN))
            self._btns[name] = btn


class LoginScreen(tk.Frame):
    NAME = "login"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        self._mode = "welcome"
        self._build()

    def refresh(self):
        self._render_mode()

    def _build(self):
        self._scroll = ScrollFrame(self)
        self._scroll.pack(fill="both", expand=True)

        self._outer = tk.Frame(self._scroll.inner, bg=BG_MAIN)
        self._outer.pack(fill="both", expand=True, padx=30, pady=40)

        tk.Label(self._outer, text="KinTable", font=(F, 38, "bold"),
                 bg=BG_MAIN, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(self._outer, text="Hyper-local meal sharing for families",
                 font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM).pack(pady=(0, 30))

        self._card = Card(self._outer, padx=36, pady=30)
        self._card.pack()
        self._render_mode()

    def _clear_card(self):
        for widget in self._card.winfo_children():
            widget.destroy()

    def _render_mode(self):
        self._clear_card()
        if self._mode == "welcome":
            self._build_welcome()
        elif self._mode == "signup":
            self._build_signup()
        elif self._mode == "login_form":
            self._build_login()
        elif self._mode == "forgot":
            self._build_forgot()

    def _build_welcome(self):
        tk.Label(self._card, text="Welcome to KinTable", font=FONT_HEAD,
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 10))
        tk.Label(self._card,
                 text="Choose an option below to create an account or log in.",
                 font=FONT_BODY, bg=BG_CARD, fg=TXT_CREAM,
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 18))
        PrimaryBtn(self._card, "Sign Up", lambda: self._set_mode("signup")).pack(fill="x", pady=(0, 10))
        PrimaryBtn(self._card, "Login", lambda: self._set_mode("login_form")).pack(fill="x")

    def _build_signup(self):
        tk.Label(self._card, text="Create your account", font=FONT_HEAD,
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))
        tk.Label(self._card,
                 text="Use the scroll bar if the full sign-up form is not visible.",
                 font=FONT_SMALL, bg=BG_CARD, fg=TXT_CREAM,
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 18))

        self._first = self._field(self._card, "First Name")
        self._last  = self._field(self._card, "Last Name")
        self._uname = self._field(self._card, "Username")
        self._phone = self._field(self._card, "Cell Number")
        tk.Label(self._card,
                 text="Your cell number is used to verify your identity if you ever forget your login information.",
                 font=FONT_SMALL, bg=BG_CARD, fg=TXT_CREAM,
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 20))
        self._pw_signup = self._field(self._card, "Create Password", show="*")
        self._pw_confirm = self._field(self._card, "Confirm Password", show="*")
        tk.Label(self._card,
                 text="Password must be at least 6 characters, alphanumeric only, case sensitive, and include 1 uppercase, 1 lowercase, and 1 number.",
                 font=FONT_SMALL, bg=BG_CARD, fg=TXT_CREAM,
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 12))

        btn_row = tk.Frame(self._card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(8, 0))
        PrimaryBtn(btn_row, "Back", lambda: self._set_mode("welcome")).pack(side="left")
        PrimaryBtn(btn_row, "Create Account", self._register).pack(side="right")



    def _build_login(self):
        tk.Label(self._card, text="Login", font=FONT_HEAD,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(0, 18))

        self._login_uname = self._field(self._card, "Username")
        self._login_pw = self._field(self._card, "Password", show="*")

        btn_row = tk.Frame(self._card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(8, 0))
        PrimaryBtn(btn_row, "Back", lambda: self._set_mode("welcome")).pack(side="left")
        PrimaryBtn(btn_row, "Login", self._login).pack(side="right")

        PrimaryBtn(self._card, "Forgot Login Info", lambda: self._set_mode("forgot")).pack(fill="x", pady=(14, 0))

    def _build_forgot(self):
        tk.Label(self._card, text="Forgot Login Info", font=FONT_HEAD,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(0, 10))
        tk.Label(self._card,
                 text="Enter the cell number tied to your account. Use digits only with no spaces, dashes, or parentheses.",
                 font=FONT_BODY, bg=BG_CARD, fg=TXT_CREAM,
                 wraplength=340, justify="left").pack(anchor="w", pady=(0, 16))

        self._forgot_phone = self._field(self._card, "Cell Number")

        btn_row = tk.Frame(self._card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(8, 0))
        PrimaryBtn(btn_row, "Back", lambda: self._set_mode("login_form")).pack(side="left")
        PrimaryBtn(btn_row, "Verify", self._forgot_login_info).pack(side="right")

    def _set_mode(self, mode):
        self._mode = mode
        self._render_mode()

    def _field(self, parent, label, show=None):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                     bg=BG_INPUT, fg=BG_MAIN, insertbackground=BG_MAIN,
                     relief="flat",
                     highlightbackground=TXT_GREEN, highlightthickness=2,
                     width=30, show=show)
        e.pack(fill="x", pady=(2, 10), ipady=6)
        return var

    def _register(self):
        first = self._first.get().strip()
        last  = self._last.get().strip()
        uname = self._uname.get().strip()
        phone = self._phone.get().strip()
        password = self._pw_signup.get().strip()
        confirm = self._pw_confirm.get().strip()

        if not first or not last or not uname or not phone or not password or not confirm:
            messagebox.showwarning("Missing info", "Please fill in all fields.")
            return

        valid_phone, phone_msg = validate_phone(phone)
        if not valid_phone:
            messagebox.showwarning("Invalid phone number", phone_msg)
            return

        valid_pw, pw_msg = validate_password(password)
        if not valid_pw:
            messagebox.showwarning("Invalid password", pw_msg)
            return

        if password != confirm:
            messagebox.showwarning("Password mismatch", "Password and Confirm Password must match.")
            return

        users = load_users()
        if uname in users:
            messagebox.showwarning("Username unavailable", "That username already exists. Please choose another.")
            return

        users[uname] = {
            "full_name": f"{first} {last}",
            "phone": phone,
            "password_hash": hash_password(password),
            "role": "guest",
            "active": True,
        }
        save_users(users)

        self._app.current_user = User(uname, f"{first} {last}", "guest", True)
        messagebox.showinfo("Account Created", "Your account has been created successfully.")
        self._app.show("home")

    def _login(self):
        uname = self._login_uname.get().strip()
        password = self._login_pw.get().strip()

        if not uname or not password:
            messagebox.showwarning("Missing info", "Please enter your username and password.")
            return

        users = load_users()
        record = users.get(uname)
        if not record:
            messagebox.showwarning("Login failed", "Username was not found.")
            return

        if record.get("password_hash") != hash_password(password):
            messagebox.showwarning("Login failed", "Incorrect password.")
            return

        self._app.current_user = User(uname,
                                      record.get("full_name", uname),
                                      record.get("role", "guest"),
                                      record.get("active", True))
        self._app.show("home")

    def _forgot_login_info(self):
        phone = self._forgot_phone.get().strip()
        valid_phone, phone_msg = validate_phone(phone)
        if not valid_phone:
            messagebox.showwarning("Invalid phone number", phone_msg)
            return

        users = load_users()
        matches = [uname for uname, info in users.items() if info.get("phone") == phone]
        if not matches:
            messagebox.showwarning("No Match Found", "No account was found with that cell number.")
            return

        usernames = ", ".join(matches)
        messagebox.showinfo("Verification Successful",
                            f"Account match found for cell number ending in {phone[-4:]}.\nUsername(s): {usernames}")
        self._set_mode("login_form")


class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_MAIN, **kw)
        self.canvas = tk.Canvas(self, bg=BG_MAIN, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=BG_MAIN)

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._resize_inner)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _resize_inner(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class HomeScreen(tk.Frame):
    NAME = "home"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True, padx=30, pady=20)

    def refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        user = self._app.current_user
        greeting = f"Good evening, {user.name.split()[0]}!" if user else "Good evening!"

        tk.Label(self._content, text="Discover Meals Near You",
                 font=FONT_TITLE, bg=BG_MAIN, fg=ACCENT).pack(anchor="w")
        tk.Label(self._content, text=greeting,
                 font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w", pady=(2, 16))

        available_meals = sorted(
            [meal for meal in MEALS if meal.get("seats", 0) > 0],
            key=meal_sort_key
        )

        if not available_meals:
            tk.Label(self._content,
                     text="No meals are currently available. Check back soon for new KinTable listings!",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM,
                     justify="left").pack(anchor="w", pady=8)
            return

        connection_meals = [meal for meal in available_meals if meal_hosted_by_connection(meal)]

        top_section = tk.Frame(self._content, bg=BG_MAIN, height=210)
        top_section.pack(fill="x", pady=(0, 12))
        top_section.pack_propagate(False)

        tk.Label(top_section, text="Your Connections' Meals", font=FONT_HEAD,
                 bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(0, 6))

        connection_scroll = ScrollFrame(top_section)
        connection_scroll.pack(fill="both", expand=True)

        if connection_meals:
            for meal in connection_meals:
                self._meal_card(connection_scroll.inner, meal)
        else:
            tk.Label(connection_scroll.inner,
                     text="No meals from your connections are currently available.",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM,
                     justify="left").pack(anchor="w", pady=8)

        bottom_section = tk.Frame(self._content, bg=BG_MAIN)
        bottom_section.pack(fill="both", expand=True)

        tk.Label(bottom_section, text="All Available Meals", font=FONT_HEAD,
                 bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(0, 6))

        all_scroll = ScrollFrame(bottom_section)
        all_scroll.pack(fill="both", expand=True)

        for meal in available_meals:
            self._meal_card(all_scroll.inner, meal)

    def _meal_card(self, parent, meal):
        card = Card(parent, padx=10, pady=5)
        card.pack(fill="x", pady=3, padx=2)

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x")
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, minsize=210)
        top.grid_columnconfigure(2, minsize=165)

        left_info = tk.Frame(top, bg=BG_CARD)
        left_info.grid(row=0, column=0, sticky="nw")
        tk.Label(left_info, text=meal["name"], font=FONT_HEAD,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
        tk.Label(left_info, text=short_description(meal.get("desc", "")), font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_CREAM, wraplength=360, justify="left").pack(anchor="w")

        meal_date = format_meal_date_for_display(meal.get("date", "Date TBD"))
        meal_time = meal.get("time", "TBD")
        center_info = tk.Frame(top, bg=BG_CARD, width=210)
        center_info.grid(row=0, column=1, sticky="ne", padx=(8, 10))
        center_info.grid_propagate(False)
        tk.Label(center_info, text=f"When: {meal_date} at {meal_time}", font=(F, 10, "bold"),
                 bg=BG_CARD, fg=ACCENT, anchor="e", width=28).pack(anchor="e")

        user = self._app.current_user
        is_own_meal = user and (meal.get("host_username") == user.id or meal.get("host") == user.name)
        if not is_own_meal:
            tk.Label(center_info, text=f"Hosted by {meal['host']}", font=FONT_SMALL,
                     bg=BG_CARD, fg=TXT_CREAM, anchor="e", width=28).pack(anchor="e")

        action_area = tk.Frame(top, bg=BG_CARD, width=165)
        action_area.grid(row=0, column=2, sticky="ne")
        action_area.grid_propagate(False)

        existing_reservation = next((r for r in RESERVATIONS if r["id"] == meal["id"]), None)
        if is_own_meal:
            PrimaryBtn(action_area, "Your Meal", lambda: None, state="disabled").pack(anchor="e")
        elif existing_reservation:
            reserved_seats = existing_reservation.get("reserved_seats", 1)
            seat_word = "Seat" if reserved_seats == 1 else "Seats"
            PrimaryBtn(action_area, f"Leave My {seat_word}", lambda m=meal: self._leave_seat(m)).pack(anchor="e")
        else:
            PrimaryBtn(action_area, "Reserve a Seat", lambda m=meal: self._reserve(m)).pack(anchor="e")

        tk.Label(action_area, text=f"{meal['seats']} seats available", font=(F, 14),
                 bg=BG_CARD, fg=ACCENT).pack(anchor="e", pady=(1, 0))
    
    def _reserve(self, meal):
        if meal["seats"] <= 0:
            messagebox.showwarning("No servings available", f"Sorry, there are no servings left for {meal['name']}.")
            return

        user = self._app.current_user
        if user and (meal.get("host_username") == user.id or meal.get("host") == user.name):
            messagebox.showwarning("Own listing", "You cannot reserve a meal that you listed yourself.")
            return

        existing = [r for r in RESERVATIONS if r["id"] == meal["id"]]
        if existing:
            messagebox.showinfo("Already reserved", f"You already have a reservation for {meal['name']}.")
            return

        requested = self._ask_servings(meal)
        if requested is None:
            return

        if requested > meal["seats"]:
            messagebox.showwarning(
                "Not enough servings",
                "Sorry, we don't have that many servings. But if your guests want to share, you could all have slightly less of a portion and save room for dessert!"
            )
            return

        meal["seats"] -= requested
        reservation = meal.copy()
        reservation["reserved_seats"] = requested
        RESERVATIONS.append(reservation)
        save_meals()

        serving_word = "serving" if requested == 1 else "servings"
        messagebox.showinfo("Reserved!", f"You've reserved {requested} {serving_word} at {meal['host']}'s {meal['name']}. Enjoy!")
        self.refresh()

    def _ask_servings(self, meal):
        dialog = tk.Toplevel(self.winfo_toplevel())
        dialog.title("Reserve Servings")
        dialog.configure(bg=BG_MAIN)
        dialog.resizable(False, False)
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        dialog.lift()
        dialog.attributes("-topmost", True)
        dialog.after(200, lambda: dialog.attributes("-topmost", False))

        result = {"value": None}

        card = Card(dialog, padx=24, pady=20)
        card.pack(padx=20, pady=20)

        tk.Label(
            card,
            text="Reserve Servings",
            font=FONT_HEAD,
            bg=BG_CARD,
            fg=ACCENT
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            card,
            text=f"{meal['name']} has {meal['seats']} servings available. How many would you like to reserve?",
            font=FONT_BODY,
            bg=BG_CARD,
            fg=TXT_CREAM,
            wraplength=360,
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        servings_var = tk.StringVar(value="1")
        entry = tk.Entry(
            card,
            textvariable=servings_var,
            font=FONT_BODY,
            bg=BG_INPUT,
            fg=BG_MAIN,
            insertbackground=BG_MAIN,
            relief="flat",
            highlightbackground=TXT_GREEN,
            highlightthickness=2,
            width=12
        )
        entry.pack(anchor="w", ipady=6, pady=(0, 16))
        dialog.update_idletasks()
        dialog.geometry(f"+{self.winfo_toplevel().winfo_x() + 120}+{self.winfo_toplevel().winfo_y() + 120}")
        entry.focus_force()
        entry.select_range(0, tk.END)

        def submit():
            value = servings_var.get().strip()
            try:
                servings = int(value)
            except ValueError:
                messagebox.showwarning("Invalid number", "Please enter a whole number of servings.")
                return

            if servings <= 0:
                messagebox.showwarning("Invalid number", "Please request at least 1 serving.")
                return

            result["value"] = servings
            dialog.destroy()

        def cancel():
            result["value"] = None
            dialog.destroy()

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x")
        SecondaryBtn(btn_row, "Cancel", cancel).pack(side="left")
        PrimaryBtn(btn_row, "Reserve", submit).pack(side="right")

        dialog.bind("<Return>", lambda event: submit())
        dialog.bind("<Escape>", lambda event: cancel())
        dialog.wait_window()
        return result["value"]
    
    def _leave_seat(self, meal):
        reservation = next((r for r in RESERVATIONS if r["id"] == meal["id"]), None)
        if not reservation:
            messagebox.showinfo("No Meal Reservation", f"You do not currently have a reservation for {meal['name']}.")
            self.refresh()
            return

        reserved_seats = reservation.get("reserved_seats", 1)
        RESERVATIONS.remove(reservation)

        for listed_meal in MEALS:
            if listed_meal["id"] == meal["id"]:
                listed_meal["seats"] += reserved_seats
                break

        save_meals()
        serving_word = "serving" if reserved_seats == 1 else "servings"
        messagebox.showinfo("Meal Reservation Removed", f"You left your seat for {meal['name']}. {reserved_seats} {serving_word} are now available again.")
        self.refresh()


class ReservationsScreen(tk.Frame):
    NAME = "reservations"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True, padx=30, pady=20)

    def refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        tk.Label(self._content, text="My Meals",
                 font=FONT_TITLE, bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(0, 16))

        user = self._app.current_user
        hosted_meals = []
        if user:
            hosted_meals = sorted(
                [meal for meal in MEALS if meal.get("host_username") == user.id or meal.get("host") == user.name],
                key=meal_sort_key
            )

        if not RESERVATIONS and not hosted_meals:
            tk.Label(self._content,
                     text="You have no reserved or hosted meals yet.\nHead to Home to find a meal, or Host a Meal to create one!",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM, justify="left").pack(anchor="w")
            return

        sf = ScrollFrame(self._content)
        sf.pack(fill="both", expand=True)

        sorted_reservations = sorted(RESERVATIONS, key=meal_sort_key)

        combined_meals = []
        for meal in sorted_reservations:
            meal["meal_type"] = "reserved"
            combined_meals.append(meal)
        for meal in hosted_meals:
            meal["meal_type"] = "hosted"
            combined_meals.append(meal)

        combined_meals = sorted(combined_meals, key=meal_sort_key)

        for meal in combined_meals:
            card = Card(sf.inner, padx=10, pady=5)
            card.pack(fill="x", pady=3, padx=2)

            meal_date = format_meal_date_for_display(meal.get("date", "Date TBD"))
            meal_time = meal.get("time", "TBD")
            meal_type = meal.get("meal_type")

            top = tk.Frame(card, bg=BG_CARD)
            top.pack(fill="x")
            top.grid_columnconfigure(0, weight=1)
            top.grid_columnconfigure(1, minsize=210)
            top.grid_columnconfigure(2, minsize=165)

            left_info = tk.Frame(top, bg=BG_CARD)
            left_info.grid(row=0, column=0, sticky="nw")

            title_text = meal["name"]
            if meal_type == "hosted":
                title_text = f"🍽️ {meal['name']} — Your Meal"

            tk.Label(left_info, text=title_text, font=FONT_HEAD,
                     bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
            tk.Label(left_info, text=short_description(meal.get("desc", "")), font=FONT_SMALL,
                     bg=BG_CARD, fg=TXT_CREAM, wraplength=360, justify="left").pack(anchor="w")

            center_info = tk.Frame(top, bg=BG_CARD, width=210)
            center_info.grid(row=0, column=1, sticky="ne", padx=(8, 10))
            center_info.grid_propagate(False)
            tk.Label(center_info, text=f"When: {meal_date} at {meal_time}", font=(F, 10, "bold"),
                     bg=BG_CARD, fg=ACCENT, anchor="e", width=28).pack(anchor="e")

            if meal_type == "reserved":
                tk.Label(center_info, text=f"Hosted by {meal['host']}", font=FONT_SMALL,
                         bg=BG_CARD, fg=TXT_CREAM, anchor="e", width=28).pack(anchor="e")

            action_area = tk.Frame(top, bg=BG_CARD, width=165)
            action_area.grid(row=0, column=2, sticky="ne")
            action_area.grid_propagate(False)

            if meal_type == "reserved":
                reserved_seats = meal.get("reserved_seats", 1)
                seat_word = "Seat" if reserved_seats == 1 else "Seats"
                PrimaryBtn(action_area, f"Leave My {seat_word}", lambda m=meal: self._cancel(m)).pack(anchor="e")
                tk.Label(action_area, text=f"{reserved_seats} reserved", font=(F, 14),
                         bg=BG_CARD, fg=ACCENT).pack(anchor="e", pady=(1, 0))
            else:
                PrimaryBtn(action_area, "Cancel Hosted Meal", lambda m=meal: self._cancel_hosted_meal(m)).pack(anchor="e")
                tk.Label(action_area, text=f"{meal['seats']} seats available", font=(F, 14),
                         bg=BG_CARD, fg=ACCENT).pack(anchor="e", pady=(1, 0))

    def _cancel(self, meal):
        matching_reservation = next((r for r in RESERVATIONS if r["id"] == meal["id"]), None)
        if matching_reservation:
            meal = matching_reservation
            RESERVATIONS.remove(meal)

            reserved_seats = meal.get("reserved_seats", 1)
            for listed_meal in MEALS:
                if listed_meal["id"] == meal["id"]:
                    listed_meal["seats"] += reserved_seats
                    save_meals()
                    break
        messagebox.showinfo("Meal Cancelled", f"Your meal reservation for {meal['name']} has been cancelled.")
        self.refresh()


    def _cancel_hosted_meal(self, meal):
        if messagebox.askyesno("Cancel Hosted Meal", f"Remove your hosted meal listing for {meal['name']}?"):
            matching_meal = next((m for m in MEALS if m["id"] == meal["id"]), None)
            if matching_meal:
                MEALS.remove(matching_meal)
                save_meals()
                messagebox.showinfo("Hosted Meal Cancelled", f"Your hosted meal listing for {meal['name']} was removed.")
                self.refresh()


class HostScreen(tk.Frame):
    NAME = "host"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(outer, text="Host a Meal", font=FONT_TITLE,
                 bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(0, 16))

        card = Card(outer, padx=28, pady=24)
        card.pack(fill="x")

        self._title_var = self._field(card, "Meal Title", "e.g. Beef Stew")
        self._desc_var  = self._text_field(card, "Description")

        default_month, default_day = get_default_meal_date_values()
        self._month_var = tk.StringVar(value=default_month)
        self._day_var = tk.StringVar(value=default_day)

        tk.Label(card, text="Meal Date", font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(10, 0))
        date_row = tk.Frame(card, bg=BG_CARD)
        date_row.pack(fill="x", pady=(2, 0))
        self._month_box = ttk.Combobox(date_row, textvariable=self._month_var,
                                       values=MONTH_NAMES, state="readonly",
                                       font=FONT_BODY, width=12)
        self._month_box.pack(side="left", ipady=4)
        self._day_box = ttk.Combobox(date_row, textvariable=self._day_var,
                                     values=DAYS_OF_MONTH, state="readonly",
                                     font=FONT_BODY, width=12)
        self._day_box.pack(side="left", padx=(8, 0), ipady=4)

        self._time_tbd_var = tk.BooleanVar(value=True)
        self._time_var = tk.StringVar(value=TIME_OPTIONS[0])
        self._ampm_var = tk.StringVar(value="PM")

        tk.Checkbutton(card, text="Time TBD", variable=self._time_tbd_var,
                       command=self._toggle_time_fields,
                       bg=BG_CARD, fg=TXT_CREAM, selectcolor=BG_CARD,
                       activebackground=BG_CARD, activeforeground=TXT_CREAM,
                       font=FONT_SMALL).pack(anchor="w", pady=(10, 0))

        time_row = tk.Frame(card, bg=BG_CARD)
        time_row.pack(fill="x", pady=(2, 0))
        self._time_box = ttk.Combobox(time_row, textvariable=self._time_var,
                                      values=TIME_OPTIONS, state="disabled",
                                      font=FONT_BODY, width=12)
        self._time_box.pack(side="left", ipady=4)
        self._ampm_box = ttk.Combobox(time_row, textvariable=self._ampm_var,
                                      values=["AM", "PM"], state="disabled",
                                      font=FONT_BODY, width=12)
        self._ampm_box.pack(side="left", padx=(8, 0), ipady=4)

        self._seats_var = self._field(card, "Number of Extra Servings", "e.g. 4")
        self._invite_var = self._field(card, "Invite Users (comma-separated usernames)", "optional")

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(20, 0))
        PrimaryBtn(btn_row, "Create Meal Listing", self._submit).pack(side="right")
        PrimaryBtn(btn_row, "Clear", self._clear).pack(side="right", padx=(0, 8))

        tk.Label(outer, text="Your Meal Listings", font=FONT_TITLE,
                 bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(22, 10))
        self._listings_area = tk.Frame(outer, bg=BG_MAIN)
        self._listings_area.pack(fill="both", expand=True)
        self._refresh_my_listings()

    def _field(self, parent, label, placeholder=""):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(10, 0))
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                     bg=BG_INPUT, fg=TXT_GREEN, insertbackground=TXT_GREEN,
                     relief="flat",
                     highlightbackground=TXT_GREEN, highlightthickness=1)
        e.pack(fill="x", ipady=6, pady=(2, 0))
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=TXT_SAGE)
            e.bind("<FocusIn>",  lambda ev, en=e, ph=placeholder, v=var:
                   (en.delete(0, "end"), en.config(fg=TXT_GREEN)) if v.get() == ph else None)
            e.bind("<FocusOut>", lambda ev, en=e, ph=placeholder, v=var:
                   (en.insert(0, ph), en.config(fg=TXT_GREEN)) if not v.get() else None)
        return var

    def _text_field(self, parent, label):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(10, 0))
        t = tk.Text(parent, font=FONT_BODY, height=4,
                    bg=BG_INPUT, fg=TXT_GREEN, insertbackground=TXT_GREEN,
                    relief="flat",
                    highlightbackground=TXT_GREEN, highlightthickness=1)
        t.pack(fill="x", pady=(2, 0))
        return t

    def _toggle_time_fields(self):
        if self._time_tbd_var.get():
            self._time_box.config(state="disabled")
            self._ampm_box.config(state="disabled")
        else:
            self._time_box.config(state="readonly")
            self._ampm_box.config(state="readonly")

    def _clear(self):
        default_month, default_day = get_default_meal_date_values()
        self._title_var.set("e.g. Beef Stew")
        self._desc_var.delete("1.0", "end")
        self._month_var.set(default_month)
        self._day_var.set(default_day)
        self._time_tbd_var.set(True)
        self._time_var.set(TIME_OPTIONS[0])
        self._ampm_var.set("PM")
        self._toggle_time_fields()
        self._seats_var.set("e.g. 4")
        self._invite_var.set("optional")

    def _submit(self):
        title = self._title_var.get().strip()
        desc = self._desc_var.get("1.0", "end").strip()
        month_name = self._month_var.get().strip()
        day_value = self._day_var.get().strip()
        time_value = self._time_var.get().strip()
        am_pm = self._ampm_var.get().strip()
        time_is_tbd = self._time_tbd_var.get()
        seats = self._seats_var.get().strip()

        if not title or not desc or not month_name or not day_value or not seats:
            messagebox.showwarning("Missing info", "Please fill in Meal Title, Description, Date, and Servings.")
            return

        valid_dt, dt_msg, meal_date, meal_time = validate_meal_datetime(month_name, day_value, time_value, am_pm, time_is_tbd)
        if not valid_dt:
            messagebox.showwarning("Invalid date or time", dt_msg)
            return

        if title.lower() == "e.g. beef stew":
            messagebox.showwarning("Invalid input", "Please enter a real meal title.")
            return

        if len(title) < 5 or not re.search(r"[A-Za-z]", title):
            messagebox.showwarning("Invalid meal title", "Meal title must be at least 5 characters and include letters.")
            return

        if not re.fullmatch(r"[A-Za-z0-9 '&,-]+", title):
            messagebox.showwarning("Invalid meal title", "Meal title can only include letters, numbers, spaces, apostrophes, ampersands, commas, and hyphens.")
            return

        if len(desc) < 10 or not re.search(r"[A-Za-z]", desc):
            messagebox.showwarning("Invalid description", "Please enter a real meal description of at least 10 characters.")
            return

        try:
            seats = int(seats)
            if seats < 1:
                messagebox.showwarning("Invalid input", "Number of servings must be greater than 0.")
                return
        except ValueError:
            messagebox.showwarning("Invalid input", "Number of servings must be a whole number.")
            return

        user = self._app.current_user
        new_meal = {
            "id": f"m{len(MEALS)+1}",
            "name": title,
            "host": user.name if user else "You",
            "host_username": user.id if user else "",
            "desc": desc,
            "date": meal_date,
            "time": meal_time,
            "seats": seats,
        }

        MEALS.append(new_meal)
        save_meals()
        self._clear()
        self._refresh_my_listings()
        messagebox.showinfo("Meal Listed!", f'"{title}" has been listed. Other families can now discover it!')


    def _refresh_my_listings(self):
        for widget in self._listings_area.winfo_children():
            widget.destroy()

        user = self._app.current_user
        if not user:
            tk.Label(self._listings_area,
                     text="Host your first meal and fill out the information above!",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w")
            return

        my_meals = [meal for meal in MEALS if meal.get("host_username") == user.id or meal.get("host") == user.name]

        if not my_meals:
            tk.Label(self._listings_area,
                     text="Host your first meal and fill out the information above!",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w")
            return

        sf = ScrollFrame(self._listings_area)
        sf.pack(fill="both", expand=True)

        for meal in my_meals:
            card = Card(sf.inner, padx=18, pady=14)
            card.pack(fill="x", pady=8, padx=2)
            tk.Label(card, text=meal["name"], font=FONT_HEAD,
                     bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
            meal_date = format_meal_date_for_display(meal.get("date", "Date TBD"))
            meal_time = meal.get("time", "TBD")
            tk.Label(card, text=f"When: {meal_date} at {meal_time}", font=FONT_SMALL,
                     bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(2, 2))
            tk.Label(card, text=f"{meal['seats']} servings available", font=FONT_SMALL,
                     bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 6))
            tk.Label(card, text=meal["desc"], font=FONT_BODY,
                     bg=BG_CARD, fg=TXT_CREAM, wraplength=600, justify="left").pack(anchor="w")
            PrimaryBtn(card, "Cancel Listing", lambda m=meal: self._cancel_listing(m)).pack(anchor="e", pady=(12, 0))

    def _cancel_listing(self, meal):
        if messagebox.askyesno("Cancel Listing", f"Remove your listing for {meal['name']}?"):
            if meal in MEALS:
                MEALS.remove(meal)
                save_meals()
                self._refresh_my_listings()
                messagebox.showinfo("Listing Cancelled", f"Your listing for {meal['name']} was removed.")



class ConnectionsScreen(tk.Frame):
    NAME = "connections"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True, padx=30, pady=20)
        self._search_var = tk.StringVar()

    def refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        tk.Label(
            self._content,
            text="Connections",
            font=FONT_TITLE,
            bg=BG_MAIN,
            fg=ACCENT
        ).pack(anchor="w", pady=(0, 16))

        search_card = Card(self._content, padx=18, pady=14)
        search_card.pack(fill="x", pady=(0, 12))

        tk.Label(
            search_card,
            text="Find Users",
            font=FONT_HEAD,
            bg=BG_CARD,
            fg=ACCENT
        ).pack(anchor="w", pady=(0, 6))

        tk.Label(
            search_card,
            text="Search by username or full name, then add users as connections.",
            font=FONT_SMALL,
            bg=BG_CARD,
            fg=TXT_CREAM,
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(0, 10))

        search_row = tk.Frame(search_card, bg=BG_CARD)
        search_row.pack(fill="x")

        entry = tk.Entry(
            search_row,
            textvariable=self._search_var,
            font=FONT_BODY,
            bg=BG_INPUT,
            fg=TXT_GREEN,
            insertbackground=TXT_GREEN,
            relief="flat",
            highlightbackground=TXT_GREEN,
            highlightthickness=1
        )
        entry.pack(side="left", fill="x", expand=True, ipady=6)
        entry.bind("<Return>", lambda event: self.refresh())

        PrimaryBtn(search_row, "Search", self.refresh).pack(side="left", padx=(8, 0))
        PrimaryBtn(search_row, "Clear", self._clear_search).pack(side="left", padx=(8, 0))

        results_label = tk.Label(
            self._content,
            text="User Search Results",
            font=FONT_HEAD,
            bg=BG_MAIN,
            fg=ACCENT
        )
        results_label.pack(anchor="w", pady=(8, 8))

        results_frame = ScrollFrame(self._content)
        results_frame.pack(fill="both", expand=True)

        users = self._get_filtered_users()
        if not users:
            tk.Label(
                results_frame.inner,
                text="No matching users found.",
                font=FONT_BODY,
                bg=BG_MAIN,
                fg=TXT_CREAM
            ).pack(anchor="w", pady=8)
        else:
            for username, info in users:
                self._user_result_card(results_frame.inner, username, info)

        tk.Label(
            self._content,
            text="Current Connections",
            font=FONT_HEAD,
            bg=BG_MAIN,
            fg=ACCENT
        ).pack(anchor="w", pady=(14, 8))

        current_frame = ScrollFrame(self._content)
        current_frame.pack(fill="both", expand=True)

        if not CONNECTIONS:
            tk.Label(
                current_frame.inner,
                text="No connections added yet.",
                font=FONT_BODY,
                bg=BG_MAIN,
                fg=TXT_CREAM
            ).pack(anchor="w", pady=8)
        else:
            for conn in CONNECTIONS:
                self._connection_card(current_frame.inner, conn)

    def _clear_search(self):
        self._search_var.set("")
        self.refresh()

    def _get_filtered_users(self):
        users = load_users()
        query = self._search_var.get().strip().lower()
        current_user = self._app.current_user
        results = []

        if not users:
            return []

        for username, info in users.items():
            full_name = info.get("full_name", username)

            if current_user and username.lower() == current_user.id.lower():
                continue

            username_lower = username.lower()
            name_parts = full_name.lower().split()
            if query and query not in username_lower and not any(part.startswith(query) for part in name_parts):
                continue

            results.append((username, info))

        results.sort(key=lambda item: item[1].get("full_name", item[0]).lower())
        return results

    def _user_result_card(self, parent, username, info):
        full_name = info.get("full_name", username)
        already_connected = any(conn.get("username", conn.get("name", "")).lower() == username.lower() for conn in CONNECTIONS)
        card = Card(parent, padx=18, pady=14)
        card.pack(fill="x", pady=8, padx=2)

        initials = "".join(p[0].upper() for p in full_name.split()[:2]) or username[:2].upper()
        avatar = tk.Label(
            card,
            text=initials,
            font=(F, 13, "bold"),
            bg=TXT_CREAM,
            fg=TXT_GREEN,
            width=3,
            relief="flat"
        )
        avatar.pack(side="left", padx=(0, 14))

        info_frame = tk.Frame(card, bg=BG_CARD)
        info_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            info_frame,
            text=full_name,
            font=FONT_HEAD,
            bg=BG_CARD,
            fg=TXT_CREAM
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Username: {username}",
            font=FONT_SMALL,
            bg=BG_CARD,
            fg=TXT_CREAM
        ).pack(anchor="w")

        if already_connected:
            tk.Label(
                card,
                text="Added",
                font=FONT_SMALL,
                bg=BG_CARD,
                fg=ACCENT
            ).pack(side="right")
        else:
            PrimaryBtn(
                card,
                "Add",
                lambda u=username, n=full_name: self._add_connection(u, n)
            ).pack(side="right")

    def _connection_card(self, parent, conn):
        display_name = conn.get("name", conn.get("username", "Unknown User"))
        username = conn.get("username", display_name)

        card = Card(parent, padx=18, pady=14)
        card.pack(fill="x", pady=8, padx=2)

        initials = "".join(p[0].upper() for p in display_name.split()[:2]) or username[:2].upper()
        avatar = tk.Label(
            card,
            text=initials,
            font=(F, 13, "bold"),
            bg=TXT_CREAM,
            fg=TXT_GREEN,
            width=3,
            relief="flat"
        )
        avatar.pack(side="left", padx=(0, 14))

        info_frame = tk.Frame(card, bg=BG_CARD)
        info_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            info_frame,
            text=display_name,
            font=FONT_HEAD,
            bg=BG_CARD,
            fg=TXT_CREAM
        ).pack(anchor="w")

        tk.Label(
            info_frame,
            text=f"Username: {username}",
            font=FONT_SMALL,
            bg=BG_CARD,
            fg=TXT_CREAM
        ).pack(anchor="w")

        PrimaryBtn(
            card,
            "Remove",
            lambda c=conn: self._remove_connection(c)
        ).pack(side="right")

    def _add_connection(self, username, full_name):
        current_user = self._app.current_user
        if current_user and username.lower() == current_user.id.lower():
            messagebox.showwarning("Invalid connection", "You cannot add yourself as a connection.")
            return

        for conn in CONNECTIONS:
            if conn.get("username", conn.get("name", "")).lower() == username.lower():
                messagebox.showwarning("Duplicate connection", "That connection already exists.")
                return

        CONNECTIONS.append({
            "username": username,
            "name": full_name,
            "role": "Connection"
        })
        save_connections()

        messagebox.showinfo("Connection Added", f"{full_name} was added to your connections.")
        self.refresh()

    def _remove_connection(self, connection):
        if connection in CONNECTIONS:
            CONNECTIONS.remove(connection)
            save_connections()
            messagebox.showinfo("Connection Removed", f"{connection.get('name', 'Connection')} was removed.")
            self.refresh()


class ProfileScreen(tk.Frame):
    NAME = "profile"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True, padx=30, pady=20)

    def refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        user = self._app.current_user

        tk.Label(self._content, text="Profile",
                 font=FONT_TITLE, bg=BG_MAIN, fg=ACCENT).pack(anchor="w", pady=(0, 16))

        card = Card(self._content, padx=28, pady=24)
        card.pack(fill="x")

        if user:
            initials = "".join(p[0].upper() for p in user.name.split()[:2])
            av = tk.Label(card, text=initials, font=(F, 28, "bold"),
                          bg=TXT_CREAM, fg=TXT_GREEN, width=3, relief="flat")
            av.pack(pady=(0, 16))

            for label, val in [("Full Name",    user.name),
                                ("Username",     user.id),
                                ("Status",       "Active" if user.active else "Inactive"),
                                ("Member Since", str(date.today()))]:
                row = tk.Frame(card, bg=BG_CARD)
                row.pack(fill="x", pady=5)
                tk.Label(row, text=label + ":", font=FONT_SMALL,
                         bg=BG_CARD, fg=TXT_CREAM, width=14, anchor="w").pack(side="left")
                tk.Label(row, text=val, font=FONT_BODY,
                         bg=BG_CARD, fg=TXT_CREAM, anchor="w").pack(side="left")

            PrimaryBtn(card, "Sign Out", self._signout).pack(anchor="e", pady=(20, 0))

    def _signout(self):
        RESERVATIONS.clear()
        self._app.current_user = None
        login_screen = self._app._screens.get("login")
        if login_screen:
            login_screen._set_mode("welcome")
        self._app.show("login")


if __name__ == "__main__":
    app = KinTableApp()
    app.mainloop()
