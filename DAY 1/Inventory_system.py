class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, name, quantity):
        if name in self.products:
            self.products[name] += quantity   ## Add the quantity to existing product if it already exists in the system
        else:
            self.products[name] = quantity  ## Add new product to the inventory if it does not exist
        print(f"Added {quantity} of {name}. Total: {self.products[name]}")

    def remove_product(self, name, quantity):
        if name in self.products and self.products[name] >= quantity:     ## Condition to check the availability of the product and quantity in the inventory
            self.products[name] -= quantity       ## Remove the specified quantity from the inventory if it exists and is sufficient
            print(f"Removed {quantity} of {name}. Remaining: {self.products[name]}")
        else:
            print(f"Cannot remove {quantity} of {name}. Not enough stock or product does not exist.")

    def view_inventory(self):

        if not self.products or all(qty == 0 for qty in self.products.values()):
            print("Inventory is empty.")

        else:
            print("Current Inventory:")
            for name, quantity in self.products.items():
                print(f"{name}: {quantity}")


def main():
    inventory = Inventory()
    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. View Inventory")
        print("4. Exit")
        choice = input("Enter your choice: ")
        match choice:
            case '1':
                name = input("Enter product name: ")
                quantity = int(input("Enter quantity to add: "))
                inventory.add_product(name, quantity)
            case '2':
                name = input("Enter product name: ")
                quantity = int(input("Enter quantity to remove: "))
                inventory.remove_product(name, quantity)
            case '3':
                inventory.view_inventory()
            case '4':
                print("Exiting Inventory Management System.")
                break
            case _:
                print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    main()

