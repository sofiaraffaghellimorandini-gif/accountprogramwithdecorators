import os
from ast import literal_eval


class Manager:

    def __init__(self):
        self.account_balance = 0
        self.warehouse = {}
        self.operations_history = []

    def assign(operation_name):
        def decorator(func):
            def wrapper(self, *args):
                result = func(self, *args)
                self.operations_history.append(result)
                return result
            return wrapper
        return decorator

    @assign("BALANCE")
    def update_balance(self, amount):
        self.account_balance += amount
        return f"BALANCE: {amount:+.2f}, New balance: {self.account_balance:.2f}"

    @assign("SALE")
    def record_sale(self, product_name, price, quantity):
        total_sale = price * quantity
        self.account_balance += total_sale

        if product_name in self.warehouse:
            self.warehouse[product_name]['quantity'] -= quantity
            if self.warehouse[product_name]['quantity'] <= 0:
                del self.warehouse[product_name]

        return f"SALE: {product_name}, Price: {price:.2f}, Quantity: {quantity}, Total: {total_sale:.2f}"

    @assign("PURCHASE")
    def record_purchase(self, product_name, price, quantity):
        total_cost = price * quantity
        self.account_balance -= total_cost

        if product_name in self.warehouse:
            self.warehouse[product_name]['quantity'] += quantity
            self.warehouse[product_name]['price'] = price
        else:
            self.warehouse[product_name] = {'price': price, 'quantity': quantity}

        return f"PURCHASE: {product_name}, Price: {price:.2f}, Quantity: {quantity}, Total: {total_cost:.2f}"

    def get_balance(self):
        return self.account_balance

    def get_warehouse(self):
        return self.warehouse

    def get_history(self):
        return self.operations_history

    def save_data(self):
        file = open(balance_file, "w")
        file.write(str(self.account_balance))
        file.close()

        file = open(warehouse_file, "w")
        file.write(str(self.warehouse))
        file.close()

        file = open(history_file, "w")
        for operation in self.operations_history:
            file.write(operation + "\n")
        file.close()


balance_file = "account_balance.txt"
warehouse_file = "../packageloading/warehouse_inventory.txt"
history_file = "../packageloading/operations_history.txt"

manager = Manager()

print("Loading previous data...")

if os.path.exists(balance_file):
    file = open(balance_file, "r")
    content = file.read()
    manager.account_balance = float(content)
    file.close()
    print(f"Account balance loaded: {manager.account_balance:.2f}")
else:
    print("No previous balance found. Starting with 0.")

if os.path.exists(warehouse_file):
    file = open(warehouse_file, "r")
    content = file.read()
    if content == "":
        manager.warehouse = {}
    else:
        manager.warehouse = literal_eval(content)
    file.close()
    print(f"Warehouse inventory loaded: {len(manager.warehouse)} products")
else:
    print("No previous warehouse data found. Starting with empty warehouse.")

if os.path.exists(history_file):
    file = open(history_file, "r")
    for line in file:
        line = line.rstrip("\n")
        if line != "":
            manager.operations_history.append(line)
    file.close()
    print(f"Operations history loaded: {len(manager.operations_history)} operations")
else:
    print("No previous history found. Starting with empty history.")

print("\nWelcome to the Company Account and Warehouse Management System!")
print("=" * 60)

while True:

    print("\nAvailable commands:")
    print("- balance")
    print("- sale")
    print("- purchase")
    print("- account")
    print("- list")
    print("- warehouse")
    print("- review")
    print("- end")

    command = input("\nEnter command: ").lower()

    if command == "balance":
        amount_input = input("Enter amount to add (positive) or subtract (negative): ")

        if amount_input.replace(".", "", 1).replace("-", "", 1).isdigit():
            amount = float(amount_input)
            result = manager.update_balance(amount)
            print(f"Balance updated! Current balance: {manager.get_balance():.2f}")
        else:
            print("ERROR: Please enter a valid number!")

    elif command == "sale":
        product_name = input("Enter product name: ")
        price_input = input("Enter product price: ")
        quantity_input = input("Enter quantity sold: ")

        if price_input.replace(".", "", 1).isdigit() and quantity_input.isdigit():
            price = float(price_input)
            quantity = int(quantity_input)

            if price <= 0 or quantity <= 0:
                print("ERROR: Price and quantity must be positive!")
                continue

            total_sale = price * quantity
            result = manager.record_sale(product_name, price, quantity)
            print(f"Sale recorded! Total: {total_sale:.2f}, New balance: {manager.get_balance():.2f}")
        else:
            print("ERROR: Please enter valid numbers for price and quantity!")

    elif command == "purchase":
        product_name = input("Enter product name: ")
        price_input = input("Enter product price: ")
        quantity_input = input("Enter quantity to purchase: ")

        if price_input.replace(".", "", 1).isdigit() and quantity_input.isdigit():
            price = float(price_input)
            quantity = int(quantity_input)

            if price <= 0 or quantity <= 0:
                print("ERROR: Price and quantity must be positive!")
                continue

            total_cost = price * quantity

            if manager.get_balance() - total_cost < 0:
                print(
                    f"ERROR: Insufficient funds! Purchase cost: {total_cost:.2f}, Current balance: {manager.get_balance():.2f}")
                continue

            result = manager.record_purchase(product_name, price, quantity)
            print(f"Purchase recorded! Total cost: {total_cost:.2f}, New balance: {manager.get_balance():.2f}")
        else:
            print("ERROR: Please enter valid numbers for price and quantity!")

    elif command == "account":
        print(f"\nCurrent account balance: {manager.get_balance():.2f}")

    elif command == "list":
        print("\n" + "=" * 60)
        print("WAREHOUSE INVENTORY")
        print("=" * 60)

        if len(manager.get_warehouse()) == 0:
            print("Warehouse is empty!")
        else:
            for product_name, details in manager.get_warehouse().items():
                print(f"Product: {product_name}")
                print(f"  Price: {details['price']:.2f}")
                print(f"  Quantity: {details['quantity']}")
                print(f"  Total value: {details['price'] * details['quantity']:.2f}")
                print("-" * 60)

    elif command == "warehouse":
        product_name = input("Enter product name to check: ")

        if product_name in manager.get_warehouse():
            details = manager.get_warehouse()[product_name]
            print(f"\nProduct: {product_name}")
            print(f"  Price: {details['price']:.2f}")
            print(f"  Quantity: {details['quantity']}")
            print(f"  Total value: {details['price'] * details['quantity']:.2f}")
        else:
            print(f"Product '{product_name}' not found in warehouse!")

    elif command == "review":
        from_input = input("Enter 'from' index (or press Enter for beginning): ")
        to_input = input("Enter 'to' index (or press Enter for end): ")

        history = manager.get_history()

        if from_input == "" and to_input == "":
            from_index = 0
            to_index = len(history)
        else:
            if (from_input == "" or from_input.isdigit()) and (to_input == "" or to_input.isdigit()):
                from_index = 0 if from_input == "" else int(from_input)
                to_index = len(history) if to_input == "" else int(to_input)

                if from_index < 0 or to_index < 0:
                    print("ERROR: Indices cannot be negative!")
                    continue

                if from_index > len(history) or to_index > len(history):
                    print(f"ERROR: Indices out of range! Valid range: 0 to {len(history)}")
                    continue

                if from_index > to_index:
                    print("ERROR: 'from' index cannot be greater than 'to' index!")
                    continue
            else:
                print("ERROR: Please enter valid numbers for indices!")
                continue

        print("\n" + "=" * 60)
        print("OPERATIONS HISTORY")
        print("=" * 60)

        if len(history) == 0:
            print("No operations recorded yet!")
        elif from_index >= len(history):
            print("No operations in this range!")
        else:
            for i in range(from_index, min(to_index, len(history))):
                print(f"[{i}] {history[i]}")

    elif command == "end":
        print("\nSaving data before exit...")

        manager.save_data()

        print("Account balance saved successfully!")
        print("Warehouse inventory saved successfully!")
        print("Operations history saved successfully!")
        print("\nThank you for using the Company Account and Warehouse Management System!")
        print("Goodbye!")
        break

    else:
        print(f"ERROR: '{command}' is not a valid command. Please try again.")
