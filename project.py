#CLINICAL MANAGEMENT SYSTEM 

import os

# File paths
PATIENT_FILE = "patients.txt"
MEDICINE_FILE = "medicines.txt"

# Admin credentials
ADMIN_USERNAME = "Shiv"
ADMIN_PASSWORD = "Shiv@2006"

# Main Menu
def main_menu():
    while True:
        print("\n--- Clinical Management System ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            login_user()
        elif choice == "2":
            register_patient()
        elif choice == "3":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Registration
def register_patient():
    print("\n--- Registration ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if check_user_exists(PATIENT_FILE, username):
        print("Patient already registered with this username.")
        return

    with open(PATIENT_FILE, "a") as file:
        file.write(f"{username},{password}\n")
    print("Registered successfully! Please log in to continue.")

# Check if user exists
def check_user_exists(filename, username):
    if not os.path.exists(filename):
        return False
    with open(filename, "r") as file:
        for line in file:
            stored_username, _ = line.strip().split(",")
            if stored_username == username:
                return True
    return False

# Login
def login_user():
    print("\n--- Login ---")
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful.")
        admin_menu()
    elif validate_user(PATIENT_FILE, username, password):
        print("Login successful.")
        patient_menu(username)
    else:
        print("Invalid credentials.")

# Validate user credentials
def validate_user(filename, username, password):
    if not os.path.exists(filename):
        return False
    with open(filename, "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if stored_username == username and stored_password == password:
                return True
    return False

# Admin Menu
def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. View Patients")
        print("2. Add Medicine")
        print("3. View Medicines")
        print("4. Update Medicine")
        print("5. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            view_patients()
        elif choice == "2":
            add_medicine()
        elif choice == "3":
            view_medicines()
        elif choice == "4":
            update_medicine()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

# View patients
def view_patients():
    if not os.path.exists(PATIENT_FILE):
        print("No patients found.")
        return

    print("\n--- Registered Patients ---")
    with open(PATIENT_FILE, "r") as file:
        for idx, line in enumerate(file, start=1):
            username, _ = line.strip().split(",")
            print(f"{idx}. {username}")

# Add medicine
def add_medicine():
    print("\n--- Add Medicine ---")
    name = input("Enter medicine name: ")
    quantity = input("Enter quantity: ")
    price = input("Enter price: ")
    details = input("Enter details: ")

    with open(MEDICINE_FILE, "a") as file:
        file.write(f"{name},{quantity},{price},{details}\n")
    print("Medicine added successfully!")

# View medicines
def view_medicines():
    print("\n--- Medicines List ---")
    if not os.path.exists(MEDICINE_FILE):
        print("No medicines available.")
        return

    print(f"{'Name':<20} {'Quantity':<10} {'Price':<10} {'Details':<30}")
    print("-" * 75)
    with open(MEDICINE_FILE, "r") as file:
        for line in file:
            name, quantity, price, details = line.strip().split(",", 3)
            print(f"{name:<20} {quantity:<10} {price:<10} {details:<30}")

# Update medicine
def update_medicine():
    print("\n--- Update Medicine ---")
    if not os.path.exists(MEDICINE_FILE):
        print("No medicines available.")
        return

    with open(MEDICINE_FILE, "r") as file:
        medicines = file.readlines()

    print(f"{'ID':<5} {'Name':<20} {'Quantity':<10} {'Price':<10} {'Details':<30}")
    print("-" * 75)
    for idx, line in enumerate(medicines, start=1):
        name, quantity, price, details = line.strip().split(",", 3)
        print(f"{idx:<5} {name:<20} {quantity:<10} {price:<10} {details:<30}")

    try:
        choice = int(input("Enter the ID of the medicine to update: "))
        if 1 <= choice <= len(medicines):
            name, quantity, price, details = medicines[choice - 1].strip().split(",", 3)
            name = input(f"Enter new name (current: {name}): ") or name
            quantity = input(f"Enter new quantity (current: {quantity}): ") or quantity
            price = input(f"Enter new price (current: {price}): ") or price
            details = input(f"Enter new details (current: {details}): ") or details
            medicines[choice - 1] = f"{name},{quantity},{price},{details}\n"
            with open(MEDICINE_FILE, "w") as file:
                file.writelines(medicines)
            print("Medicine updated successfully!")
        else:
            print("Invalid ID.")
    except ValueError:
        print("Invalid input. Please try again.")

# Patient Menu
def patient_menu(username):
    while True:
        print(f"\n--- Welcome, Patient {username} ---")
        print("1. View Medicines")
        print("2. Buy Medicines")
        print("3. Logout")
        choice = input("Select an option: ")

        if choice == "1":
            view_medicines()
        elif choice == "2":
            buy_medicines(username)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

# Buy medicines
def buy_medicines(username):
    print("\n--- Buy Medicines ---")
    if not os.path.exists(MEDICINE_FILE):
        print("No medicines available.")
        return

    with open(MEDICINE_FILE, "r") as file:
        medicines = file.readlines()

    print(f"{'ID':<5} {'Name':<20} {'Quantity':<10} {'Price':<10} {'Details':<30}")
    print("-" * 75)
    for idx, line in enumerate(medicines, start=1):
        name, quantity, price, details = line.strip().split(",", 3)
        print(f"{idx:<5} {name:<20} {quantity:<10} {price:<10} {details:<30}")

    try:
        choice = int(input("Enter the ID of the medicine to buy: "))
        if 1 <= choice <= len(medicines):
            name, quantity, price, details = medicines[choice - 1].strip().split(",", 3)
            quantity = int(quantity)
            if quantity > 0:
                qty_to_buy = int(input(f"Enter quantity to buy (available: {quantity}): "))
                if 0 < qty_to_buy <= quantity:
                    total_cost = qty_to_buy * float(price)
                    updated_quantity = quantity - qty_to_buy
                    medicines[choice - 1] = f"{name},{updated_quantity},{price},{details}\n"
                    with open(MEDICINE_FILE, "w") as file:
                        file.writelines(medicines)
                    print(f"Purchase successful! Total cost: ₹{total_cost:.2f}")
                else:
                    print("Invalid quantity. Please try again.")
            else:
                print("Out of stock.")
        else:
            print("Invalid ID.")
    except ValueError:
        print("Invalid input. Please try again.")

# Run the system
if __name__ == "__main__":
    main_menu()
