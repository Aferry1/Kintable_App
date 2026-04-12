import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models import User, Meal, Table

# Sample data
MEALS = [
    {"id": "m1", "name": "Taco Salad",  "host": "John Miller",       "desc": "Fresh taco salad with homemade salsa.",      "seats": 3},
    {"id": "m2", "name": "Hamburgers",  "host": "James Washington",   "desc": "Classic backyard burgers, all the fixings.", "seats": 5},
    {"id": "m3", "name": "Pasta Bake",  "host": "George Mason",       "desc": "Cheesy baked penne with Italian sausage.",  "seats": 2},
]

RESERVATIONS = []
CONNECTIONS  = [
    {"name": "Sarah Mitchell", "role": "Host"},
    {"name": "Tom Bradley",    "role": "Guest"},
]

# Colour palette — warm, dark, earthy
BG_MAIN   = "#1E2D1E"
BG_CARD   = "#253525"
BG_NAV    = "#152015"
BG_INPUT  = "#2D3F2D"
ACCENT    = "#E8631A"
BTN_EARTH = "#C4956A"
TXT_CREAM = "#F2E8D9"
TXT_SAGE  = "#9DB89D"
TXT_GREEN = "#1B2B1B"
TXT_WHITE = "#FFFFFF"

# Fonts
F = "DejaVu Sans"
FONT_TITLE  = (F, 22, "bold")
FONT_HEAD   = (F, 14, "bold")
FONT_BODY   = (F, 11)
FONT_SMALL  = (F, 9)
FONT_NAV    = (F, 10, "bold")
FONT_BTN    = (F, 11, "bold")


class Card(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_CARD, relief="flat",
                         highlightbackground=ACCENT, highlightthickness=1, **kw)


class PrimaryBtn(tk.Button):
    def __init__(self, parent, text, command, **kw):
        super().__init__(parent, text=text, command=command,
                         bg=BTN_EARTH, fg=TXT_GREEN, font=FONT_BTN,
                         relief="flat", cursor="hand2",
                         highlightbackground=ACCENT, highlightthickness=2,
                         padx=14, pady=6, **kw)
        self.bind("<Enter>", lambda e: self.config(bg="#D4A87A"))
        self.bind("<Leave>", lambda e: self.config(bg=BTN_EARTH))


class SecondaryBtn(tk.Button):
    def __init__(self, parent, text, command, **kw):
        super().__init__(parent, text=text, command=command,
                         bg=BG_CARD, fg=TXT_CREAM, font=FONT_BTN,
                         relief="flat", cursor="hand2",
                         highlightbackground=ACCENT, highlightthickness=1,
                         padx=14, pady=6, **kw)
        self.bind("<Enter>", lambda e: self.config(bg="#2F4430"))
        self.bind("<Leave>", lambda e: self.config(bg=BG_CARD))


class KinTableApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KinTable")
        self.geometry("900x640")
        self.minsize(750, 540)
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
        ("Reservations", "reservations"),
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
                            bg=BG_NAV, fg=TXT_WHITE,
                            relief="flat", cursor="hand2",
                            padx=12, pady=10,
                            command=lambda n=name: self._app.show(n))
            btn.pack(side="left", fill="y")
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1F301F", fg=ACCENT))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BG_NAV, fg=TXT_WHITE))
            self._btns[name] = btn


class LoginScreen(tk.Frame):
    NAME = "login"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        self._build()

    def _build(self):
        outer = tk.Frame(self, bg=BG_MAIN)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(outer, text="KinTable", font=(F, 38, "bold"),
                 bg=BG_MAIN, fg=ACCENT).pack(pady=(0, 4))
        tk.Label(outer, text="Hyper-local meal sharing for families",
                 font=FONT_BODY, bg=BG_MAIN, fg=TXT_SAGE).pack(pady=(0, 30))

        card = Card(outer, padx=36, pady=30)
        card.pack()

        tk.Label(card, text="Create your account", font=FONT_HEAD,
                 bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w", pady=(0, 18))

        self._first = self._field(card, "First Name")
        self._last  = self._field(card, "Last Name")
        self._uname = self._field(card, "Username")

        PrimaryBtn(card, "Get Started", self._register).pack(fill="x", pady=(18, 0))

    def _field(self, parent, label):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_SAGE).pack(anchor="w")
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                     bg=BG_INPUT, fg=TXT_CREAM, insertbackground=TXT_CREAM,
                     relief="flat",
                     highlightbackground=ACCENT, highlightthickness=1,
                     width=30)
        e.pack(fill="x", pady=(2, 10), ipady=6)
        return var

    def _register(self):
        first = self._first.get().strip()
        last  = self._last.get().strip()
        uname = self._uname.get().strip()
        if not first or not last or not uname:
            messagebox.showwarning("Missing info", "Please fill in all fields.")
            return
        self._app.current_user = User(uname, f"{first} {last}", "guest", True)
        self._app.show("home")


class ScrollFrame(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_MAIN, **kw)
        canvas = tk.Canvas(self, bg=BG_MAIN, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg=BG_MAIN)
        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")


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
                 font=FONT_TITLE, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w")
        tk.Label(self._content, text=greeting,
                 font=FONT_BODY, bg=BG_MAIN, fg=TXT_SAGE).pack(anchor="w", pady=(2, 16))

        sf = ScrollFrame(self._content)
        sf.pack(fill="both", expand=True)

        for meal in MEALS:
            self._meal_card(sf.inner, meal)

    def _meal_card(self, parent, meal):
        card = Card(parent, padx=18, pady=14)
        card.pack(fill="x", pady=8, padx=2)

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x")

        tk.Label(top, text=meal["name"], font=FONT_HEAD,
                 bg=BG_CARD, fg=TXT_CREAM).pack(side="left")
        tk.Label(top, text=f"{meal['seats']} seats available", font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_SAGE).pack(side="right")

        tk.Label(card, text=f"Hosted by {meal['host']}", font=FONT_SMALL,
                 bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(2, 6))
        tk.Label(card, text=meal["desc"], font=FONT_BODY,
                 bg=BG_CARD, fg=TXT_SAGE, wraplength=600, justify="left").pack(anchor="w")

        PrimaryBtn(card, "Reserve a Seat", lambda m=meal: self._reserve(m)).pack(
            anchor="e", pady=(12, 0))

    def _reserve(self, meal):
        existing = [r for r in RESERVATIONS if r["id"] == meal["id"]]
        if existing:
            messagebox.showinfo("Already reserved", f"You already have a reservation for {meal['name']}.")
            return
        RESERVATIONS.append(meal.copy())
        messagebox.showinfo("Reserved!", f"You've reserved a seat at {meal['host']}'s {meal['name']}. Enjoy!")


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

        tk.Label(self._content, text="Your Reservations",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w", pady=(0, 16))

        if not RESERVATIONS:
            tk.Label(self._content,
                     text="You have no upcoming reservations.\nHead to Discover to find a meal near you!",
                     font=FONT_BODY, bg=BG_MAIN, fg=TXT_SAGE, justify="left").pack(anchor="w")
            return

        sf = ScrollFrame(self._content)
        sf.pack(fill="both", expand=True)

        for meal in RESERVATIONS:
            card = Card(sf.inner, padx=18, pady=14)
            card.pack(fill="x", pady=8, padx=2)
            tk.Label(card, text=meal["name"], font=FONT_HEAD,
                     bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
            tk.Label(card, text=f"Hosted by {meal['host']}", font=FONT_SMALL,
                     bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(2, 6))
            tk.Label(card, text=meal["desc"], font=FONT_BODY,
                     bg=BG_CARD, fg=TXT_SAGE, wraplength=600, justify="left").pack(anchor="w")
            SecondaryBtn(card, "Cancel Reservation",
                         lambda m=meal: self._cancel(m)).pack(anchor="e", pady=(12, 0))

    def _cancel(self, meal):
        if meal in RESERVATIONS:
            RESERVATIONS.remove(meal)
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
                 bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w", pady=(0, 16))

        card = Card(outer, padx=28, pady=24)
        card.pack(fill="x")

        self._title_var = self._field(card, "Meal Title", "e.g. Beef Stew")
        self._desc_var  = self._text_field(card, "Description")
        self._seats_var = self._field(card, "Number of Extra Servings", "e.g. 4")
        self._invite_var = self._field(card, "Invite Users (comma-separated usernames)", "optional")

        btn_row = tk.Frame(card, bg=BG_CARD)
        btn_row.pack(fill="x", pady=(20, 0))
        PrimaryBtn(btn_row, "Create Meal Listing", self._submit).pack(side="right")
        SecondaryBtn(btn_row, "Clear", self._clear).pack(side="right", padx=(0, 8))

    def _field(self, parent, label, placeholder=""):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_SAGE).pack(anchor="w", pady=(10, 0))
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=FONT_BODY,
                     bg=BG_INPUT, fg=TXT_CREAM, insertbackground=TXT_CREAM,
                     relief="flat",
                     highlightbackground=ACCENT, highlightthickness=1)
        e.pack(fill="x", ipady=6, pady=(2, 0))
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=TXT_SAGE)
            e.bind("<FocusIn>",  lambda ev, en=e, ph=placeholder, v=var:
                   (en.delete(0, "end"), en.config(fg=TXT_CREAM)) if v.get() == ph else None)
            e.bind("<FocusOut>", lambda ev, en=e, ph=placeholder, v=var:
                   (en.insert(0, ph), en.config(fg=TXT_SAGE)) if not v.get() else None)
        return var

    def _text_field(self, parent, label):
        tk.Label(parent, text=label, font=FONT_SMALL,
                 bg=BG_CARD, fg=TXT_SAGE).pack(anchor="w", pady=(10, 0))
        t = tk.Text(parent, font=FONT_BODY, height=4,
                    bg=BG_INPUT, fg=TXT_CREAM, insertbackground=TXT_CREAM,
                    relief="flat",
                    highlightbackground=ACCENT, highlightthickness=1)
        t.pack(fill="x", pady=(2, 0))
        return t

    def _clear(self):
        self._title_var.set("")
        self._desc_var.delete("1.0", "end")
        self._seats_var.set("")
        self._invite_var.set("")

    def _submit(self):
        title  = self._title_var.get().strip()
        desc   = self._desc_var.get("1.0", "end").strip()
        seats  = self._seats_var.get().strip()
        if not title or not desc or not seats:
            messagebox.showwarning("Missing info", "Please fill in Meal Title, Description, and Servings.")
            return
        try:
            int(seats)
        except ValueError:
            messagebox.showwarning("Invalid input", "Number of servings must be a whole number.")
            return

        user = self._app.current_user
        new_meal = {
            "id":    f"m{len(MEALS)+1}",
            "name":  title,
            "host":  user.name if user else "You",
            "desc":  desc,
            "seats": int(seats),
        }
        MEALS.append(new_meal)
        self._clear()
        messagebox.showinfo("Meal Listed!", f'"{title}" has been listed. Other families can now discover it!')


class ConnectionsScreen(tk.Frame):
    NAME = "connections"

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG_MAIN)
        self._app = app
        NavBar(self, app).pack(side="top", fill="x")
        self._content = tk.Frame(self, bg=BG_MAIN)
        self._content.pack(fill="both", expand=True, padx=30, pady=20)

    def refresh(self):
        for w in self._content.winfo_children():
            w.destroy()

        tk.Label(self._content, text="Connections",
                 font=FONT_TITLE, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w", pady=(0, 16))

        sf = ScrollFrame(self._content)
        sf.pack(fill="both", expand=True)

        for conn in CONNECTIONS:
            card = Card(sf.inner, padx=18, pady=14)
            card.pack(fill="x", pady=8, padx=2)

            initials = "".join(p[0].upper() for p in conn["name"].split()[:2])
            avatar = tk.Label(card, text=initials, font=(F, 13, "bold"),
                              bg=BTN_EARTH, fg=TXT_GREEN, width=3, relief="flat")
            avatar.pack(side="left", padx=(0, 14))

            info = tk.Frame(card, bg=BG_CARD)
            info.pack(side="left", fill="x", expand=True)
            tk.Label(info, text=conn["name"], font=FONT_HEAD,
                     bg=BG_CARD, fg=TXT_CREAM).pack(anchor="w")
            tk.Label(info, text=conn["role"], font=FONT_SMALL,
                     bg=BG_CARD, fg=ACCENT).pack(anchor="w")


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
                 font=FONT_TITLE, bg=BG_MAIN, fg=TXT_CREAM).pack(anchor="w", pady=(0, 16))

        card = Card(self._content, padx=28, pady=24)
        card.pack(fill="x")

        if user:
            initials = "".join(p[0].upper() for p in user.name.split()[:2])
            av = tk.Label(card, text=initials, font=(F, 28, "bold"),
                          bg=BTN_EARTH, fg=TXT_GREEN, width=3, relief="flat")
            av.pack(pady=(0, 16))

            for label, val in [("Full Name",    user.name),
                                ("Username",     user.id),
                                ("Status",       "Active" if user.active else "Inactive"),
                                ("Member Since", str(date.today()))]:
                row = tk.Frame(card, bg=BG_CARD)
                row.pack(fill="x", pady=5)
                tk.Label(row, text=label + ":", font=FONT_SMALL,
                         bg=BG_CARD, fg=TXT_SAGE, width=14, anchor="w").pack(side="left")
                tk.Label(row, text=val, font=FONT_BODY,
                         bg=BG_CARD, fg=TXT_CREAM, anchor="w").pack(side="left")

            PrimaryBtn(card, "Sign Out", self._signout).pack(anchor="e", pady=(20, 0))

    def _signout(self):
        RESERVATIONS.clear()
        self._app.current_user = None
        self._app.show("login")


if __name__ == "__main__":
    app = KinTableApp()
    app.mainloop()
