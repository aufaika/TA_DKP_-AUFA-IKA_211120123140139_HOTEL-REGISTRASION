import tkinter as tk
from tkinter import messagebox
from collections import deque
from tkcalendar import DateEntry
from datetime import datetime

# Dictionary to store registered user information
registered_users = {
    "user1": "password1",
    "user2": "password2"
}

# Dictionary to store reservation information
reservations = {}

# Dictionary to store hotel information
hotel_data = {
    "available_rooms": ["Standard", "Deluxe", "Suite"],
    "room_prices": {"Standard": 500000, "Deluxe": 1500000, "Suite": 2000000},
    "breakfast_price": 50000
}

# Queue to store check-in and check-out dates
date_queue = deque()

# Global variable to indicate whether the user has successfully logged in or registered
logged_in = False

class HotelReservation:
    def __init__(self):
        self._check_in = None
        self._check_out = None
        self._room_type = None
        self._breakfast = False
        self.room_prices = {
            'Standard': 500000,
            'Deluxe': 1500000,
            'Suite': 2000000
        }

    def get_check_in(self):
        return self._check_in

    def set_check_in(self, check_in):
        self._check_in = check_in

    def get_check_out(self):
        return self._check_out

    def set_check_out(self, check_out):
        self._check_out = check_out

    def get_room_type(self):
        return self._room_type

    def set_room_type(self, room_type):
        self._room_type = room_type

    def get_breakfast(self):
        return self._breakfast

    def set_breakfast(self, breakfast):
        self._breakfast = breakfast

    def calculate_total(self):
        total_price = self.room_prices[self._room_type]
        if self._breakfast:
            total_price += 50000
        return total_price

def login():
    global logged_in
    username = entry_username.get()
    password = entry_password.get()

    if username in registered_users and registered_users[username] == password:
        label_result.config(text="Login successful!", bg="saddlebrown")
        logged_in = True
    else:
        label_result.config(text="Incorrect username or password.", bg="saddlebrown")
        logged_in = False

def register():
    global logged_in
    username = entry_username.get()
    password = entry_password.get()

    if username in registered_users:
        label_result.config(text="Username already taken.", bg="saddlebrown")
        logged_in = False
    else:
        registered_users[username] = password
        label_result.config(text="Registration successful!", bg="saddlebrown")
        logged_in = True

def show_room_price(*args):
    room_type = variable_room_type.get()
    price = hotel_data["room_prices"][room_type]
    label_room_price.config(text="Room Price: Rp {}".format(price))

def choose_dates():
    if not logged_in:
        label_result.config(text="Please log in or register first.", bg="saddlebrown")
        return

    checkin_date = entry_checkin_date.get_date().strftime("%Y-%m-%d")
    checkout_date = entry_checkout_date.get_date().strftime("%Y-%m-%d")
    date_queue.append((checkin_date, checkout_date))
    label_result.config(text="Check-in Date: {}\nCheck-out Date: {}".format(checkin_date, checkout_date), bg="saddlebrown")

def calculate_total():
    if not logged_in:
        label_total.config(text="Silakan login atau daftar terlebih dahulu.", bg="burlywood")
        return

    room_type = variable_room_type.get()
    breakfast = variable_breakfast.get()

    # Ambil data reservasi dari antrian
    reservation = date_queue.popleft()

    # Ubah tanggal check-in dan check-out menjadi objek datetime
    checkin_date = datetime.strptime(reservation[0], "%Y-%m-%d")
    checkout_date = datetime.strptime(reservation[1], "%Y-%m-%d")

    # Hitung selisih hari antara check-in dan check-out
    duration = (checkout_date - checkin_date).days

    # Buat objek reservasi
    reservation = HotelReservation()
    reservation.set_room_type(room_type)
    reservation.set_breakfast(breakfast)

    # Hitung total pembayaran
    total_price = reservation.calculate_total() * duration
    
    # Hitung total pembayaran untuk harga sarapan
    breakfast_price = hotel_data["breakfast_price"] * duration if breakfast else 0

    label_total.config(text="Total Pembayaran: Rp {}".format(total_price), bg="burlywood")

window = tk.Tk()
window.title("Hotel Reservation")
window.geometry("400x580")
window.configure(bg="saddlebrown")

label_title = tk.Label(window, text="Welcome to Hotel Satu", bg="saddlebrown", fg="wheat", font=("Arial", 16, "bold"))
label_title.pack(pady=10)

label_username = tk.Label(window, text="Username:", bg="saddlebrown", fg="wheat")
label_username.pack()
entry_username = tk.Entry(window)
entry_username.pack()

label_password = tk.Label(window, text="Password:", bg="saddlebrown", fg="wheat")
label_password.pack()
entry_password = tk.Entry(window, show="*")
entry_password.pack()

button_login = tk.Button(window, text="Login", command=login, bg="wheat", fg="saddlebrown")
button_login.pack(pady=5)
button_register = tk.Button(window, text="Register", command=register, bg="wheat", fg="saddlebrown")
button_register.pack()

label_result = tk.Label(window, text="", bg="saddlebrown", fg="wheat")
label_result.pack(pady=10)

label_checkin_date = tk.Label(window, text="Check-in Date:", bg="saddlebrown", fg="wheat")
label_checkin_date.pack()
entry_checkin_date = DateEntry(window, date_pattern='dd mm yyyy')
entry_checkin_date.pack()

label_checkout_date = tk.Label(window, text="Check-out Date:", bg="saddlebrown", fg="wheat")
label_checkout_date.pack()
entry_checkout_date = DateEntry(window, date_pattern='dd mm yyyy')
entry_checkout_date.pack()

label_room_type = tk.Label(window, text="Room Type:", bg="saddlebrown", fg="wheat")
label_room_type.pack()

variable_room_type = tk.StringVar(window)
variable_room_type.set(hotel_data["available_rooms"][0])
option_menu_room_type = tk.OptionMenu(window, variable_room_type, *hotel_data["available_rooms"], command=show_room_price)
option_menu_room_type.pack()

label_room_price = tk.Label(window, text="", bg="saddlebrown", fg="wheat")
label_room_price.pack()

label_breakfast = tk.Label(window, text="Add Breakfast:", bg="saddlebrown", fg="wheat")
label_breakfast.pack()

label_breakfast_price = tk.Label(window, text="Breakfast Price: Rp {}".format(hotel_data["breakfast_price"]), bg="saddlebrown", fg="wheat")
label_breakfast_price.pack()

variable_breakfast = tk.IntVar()
check_button_breakfast = tk.Checkbutton(window, text="Yes", variable=variable_breakfast, onvalue=1, offvalue=0, bg="saddlebrown", fg="saddlebrown")
check_button_breakfast.pack()

button_choose_dates = tk.Button(window, text="Choose Dates", command=choose_dates, bg="wheat", fg="saddlebrown")
button_choose_dates.pack(pady=5)

button_calculate_total = tk.Button(window, text="Calculate Total", command=calculate_total, bg="wheat", fg="saddlebrown")
button_calculate_total.pack()

label_total = tk.Label(window, text="Total Payment: Rp 0", bg="wheat", fg="saddlebrown")
label_total.pack(pady=10)

window.mainloop()
