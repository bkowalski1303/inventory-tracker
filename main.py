import item_class
from inventory_tracker import load_inventory, print_inventory, add_new_item, record_sale, generate_restock_report, add_stock
import sys


def main():
    inventory = load_inventory("inventory.json")

    while True:
        print("\n=== Inventory Tracker ===")
        print("1. View Inventory")
        print("2. Add New Item")
        print("3. Record Sale")
        print("4. Produce Restock Report")
        print("5. Add stock")
        print("6. Quit")

        choice = input("Choose an option: ")
        print(choice)

        match choice:
            case "1":
                print_inventory(inventory)
            case "2":
                pass
                add_new_item(inventory)
            case "3":
                record_sale(inventory)
            case "4":
                generate_restock_report(inventory)
            case "5":
                add_stock(inventory)
            case "6":
                sys.exit()
            case _:
                print("Please try again")

if __name__ == "__main__":
    main()