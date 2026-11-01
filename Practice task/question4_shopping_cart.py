VAT_RATE = 0.13
PRODUCTS = {
    "P101": {"name": "Notebook", "price": 250.0, "stock": 40},
    "P102": {"name": "Backpack", "price": 2200.0, "stock": 15},
    "P103": {"name": "Calculator", "price": 1200.0, "stock": 20},
    "P104": {"name": "Desk lamp", "price": 1800.0, "stock": 12},
}


def read_integer(prompt, minimum=1):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print("Value must be at least {}.".format(minimum))
            else:
                return value
        except ValueError:
            print("Please enter a whole number.")


def display_products(products):
    print("\nAVAILABLE PRODUCTS")
    found = False
    for product_id, product in products.items():
        if product["stock"] > 0:
            found = True
            print("{} | {} | Rs. {:.2f} | Stock: {}".format(
                product_id, product["name"], product["price"], product["stock"]
            ))
    if not found:
        print("No products are currently in stock.")


def add_to_cart(products, cart):
    product_id = input("Product ID: ").strip().upper()
    if product_id not in products:
        print("Product not found.")
        return
    quantity = read_integer("Quantity to add: ")
    existing_quantity = cart.get(product_id, 0)
    if existing_quantity + quantity > products[product_id]["stock"]:
        print("Not enough stock. Available quantity: {}".format(
            products[product_id]["stock"]
        ))
        return
    cart[product_id] = existing_quantity + quantity
    print("Product added to cart.")


def remove_from_cart(cart):
    product_id = input("Product ID to remove: ").strip().upper()
    if product_id not in cart:
        print("That product is not in the cart.")
        return
    del cart[product_id]
    print("Product removed from cart.")


def update_cart_quantity(products, cart):
    product_id = input("Product ID to update: ").strip().upper()
    if product_id not in cart:
        print("That product is not in the cart.")
        return
    quantity = read_integer("New quantity: ")
    if quantity > products[product_id]["stock"]:
        print("Not enough stock. Available quantity: {}".format(
            products[product_id]["stock"]
        ))
        return
    cart[product_id] = quantity
    print("Cart quantity updated.")


def calculate_subtotal(products, cart):
    subtotal = 0.0
    for product_id, quantity in cart.items():
        subtotal += products[product_id]["price"] * quantity
    return subtotal


def discount_rate(subtotal):
    if subtotal >= 20000:
        return 0.15
    if subtotal >= 10000:
        return 0.10
    if subtotal >= 5000:
        return 0.05
    return 0.0


def display_cart(products, cart):
    if not cart:
        print("Your cart is empty.")
        return
    for product_id, quantity in cart.items():
        product = products[product_id]
        print("{} | {} | Quantity: {} | Line total: Rs. {:.2f}".format(
            product_id, product["name"], quantity,
            product["price"] * quantity
        ))
    print("Subtotal: Rs. {:.2f}".format(calculate_subtotal(products, cart)))


def checkout(products, cart):
    if not cart:
        print("Cannot checkout: your cart is empty.")
        return

    subtotal = calculate_subtotal(products, cart)
    rate = discount_rate(subtotal)
    discount = subtotal * rate
    discounted_subtotal = subtotal - discount
    vat = discounted_subtotal * VAT_RATE
    final_total = discounted_subtotal + vat

    print("\n============== INVOICE ==============")
    print("{:<18} {:>5} {:>12} {:>14}".format(
        "Product", "Qty", "Unit price", "Line total"
    ))
    for product_id, quantity in cart.items():
        product = products[product_id]
        print("{:<18} {:>5} {:>12.2f} {:>14.2f}".format(
            product["name"], quantity, product["price"],
            product["price"] * quantity
        ))
    print("-------------------------------------")
    print("Subtotal:          Rs. {:.2f}".format(subtotal))
    print("Discount ({:.0f}%):    Rs. {:.2f}".format(rate * 100, discount))
    print("VAT (13%):         Rs. {:.2f}".format(vat))
    print("Final bill:        Rs. {:.2f}".format(final_total))
    print("=====================================")

    for product_id, quantity in cart.items():
        products[product_id]["stock"] -= quantity
    cart.clear()
    print("Purchase completed; stock has been updated.")


def main():
    products = {}
    for product_id, product in PRODUCTS.items():
        products[product_id] = product.copy()
    cart = {}
    while True:
        print("\nSHOPPING CART")
        print("1. Display products\n2. Add product to cart")
        print("3. Remove product\n4. Update cart quantity")
        print("5. Display cart\n6. Checkout\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            display_products(products)
        elif choice == "2":
            add_to_cart(products, cart)
        elif choice == "3":
            remove_from_cart(cart)
        elif choice == "4":
            update_cart_quantity(products, cart)
        elif choice == "5":
            display_cart(products, cart)
        elif choice == "6":
            checkout(products, cart)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
