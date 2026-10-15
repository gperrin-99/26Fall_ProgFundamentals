cafe_name = "Python Café"
tax_rate = 0.08

menu = {
    "espresso": 3.00,
    "latte": 4.50,
    "matcha": 4.25,
    "mocha": 5.00,
    "muffin": 2.50,
    "croissant": 3.25,
}

order = []


def greet(name):
    print(f"Welcome to {cafe_name}, {name}!")


def show_menu(menu):
    print("\n--- MENU ---")
    for item, price in menu.items():
        print(f"{item.title()}: ${price:.2f}")


def show_order(order, menu):
    if not order:
        print("Your order is empty.")
        return

    print("\n--- YOUR ORDER ---")
    for item in order:
        print(f"{item.title()}: ${menu[item]:.2f}")
    print(f"Number of items: {len(order)}")


def calculate_subtotal(order, menu):
    subtotal = 0.0
    for item in order:
        subtotal += menu[item]
    return subtotal


def get_discount(subtotal, is_member):
    if is_member and subtotal >= 20:
        return subtotal * 0.15
    elif is_member and subtotal >= 10:
        return subtotal * 0.10
    elif not is_member and subtotal >= 25:
        return subtotal * 0.05
    else:
        return 0.0


def print_receipt(name, order, menu, is_member):
    subtotal = calculate_subtotal(order, menu)
    discount = get_discount(subtotal, is_member)
    discounted_subtotal = subtotal - discount
    tax = tax_rate * discounted_subtotal
    total = discounted_subtotal + tax

    print(f"\n==== {cafe_name} Receipt ====")
    print(f"Customer: {name}")
    for item in order:
        print(f"{item.title()}: ${menu[item]:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")
    print(f"Discount: -${discount:.2f}")
    print(f"Tax: ${tax:.2f}")
    print(f"Total: ${total:.2f}")

    if not is_member:
        print("Join our rewards club to save on a future visit!")

    print(f"Thank you, {name}!")


print(f"Welcome to {cafe_name}!")
customer_name = input("What is your name? ")
greet(customer_name)

member_answer = input("Are you a rewards member? (yes/no) ").lower()
is_member = member_answer == "yes"

while True:
    print(
        "\n1. View menu\n"
        "2. Add an item\n"
        "3. Remove an item\n"
        "4. View my order\n"
        "5. Checkout"
    )
    selection = input("Choose an option (1-5): ")

    if selection == "1":
        show_menu(menu)
    elif selection == "2":
        show_menu(menu)
        item = input("What would you like to add? ").lower()
        if item in menu:
            quantity_text = input("How many? ")
            if quantity_text.isdigit():
                quantity = int(quantity_text)
                if quantity == 0:
                    raise ValueError("Quantity must be greater than zero.")
                order.extend([item] * quantity)
                print(f"Added {quantity} {item}(s) to your order.")
            else:
                print("Please enter a positive whole-number quantity.")
        else:
            print("That item is not on the menu.")
    elif selection == "3":
        item = input("Which item should I remove? ").lower()
        if item in order:
            order.remove(item)
            print(f"Removed one {item} from your order.")
        else:
            print(f"{item.title()} is not in your order.")
    elif selection == "4":
        show_order(order, menu)
    elif selection == "5":
        if not order:
            print("Your order is empty. Please add something before checking out.")
        else:
            print_receipt(customer_name, order, menu, is_member)
            break
    else:
        print("Please choose a number from 1 to 5.")
