from tkinter.ttk import Separator
from item_class import Item
import json
import heapq


def load_inventory(filename):
    # open the invenotry file and load it into a dict calles data
    with open(filename, "r") as f:
        data = json.load(f)
        
        # data is currently a python dict. We need to make it an Object

        # initialize a dict where the key will be the name and the value will be an object in memory
        # The objects are the item class which has been created speficically to represent the data from the json
        inventory = {}
        
        # Loop through data.items(). This allows us to see every key and value in the data dictionary
        for key, values in data.items():

            # This sets the key of the inventory dict to the name of the dict in data
            # it sets the value to an Item object that emcompases the rest of the data
            inventory[key] = Item(name = key, stock = values["stock"], restock_threshold = values["restock_threshold"])

            # Since the sales history is not a part of the Item constructor, we have to add it manually later. 
            # This adds the sales history to the item
            inventory[key].sales_history = values["sales_history"]

        # Returns the inventory dict containing the objects
        return inventory
    
def save_inventory(inventory, filename):
        
    # Sets up a empty dict for us to transform the objects into
    data = {}

    # loops through the objects in the inventory and transforms them into python dicts
    for key,value in inventory.items():
        data[key] = {
            "stock" : value.stock,
            "restock_threshold" : value.restock_threshold,
            "sales_history" : value.sales_history
        }
        
    # Transforms the python dict we have created into JSON
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def add_new_item(inventory):
    name = input("Enter item name: ")
    if name in inventory:
        print("This item already exists")
        return
    stock = int(input("Enter the stock amount: "))
    restock_threshold = int(input("Enter the restock threshold: "))
    inventory[name] = Item(name,stock,restock_threshold)
    inventory[name].sales_history = []
    print(f"{name} added to inventory.")
    save_inventory(inventory,"inventory.json")

def print_inventory(inventory):
    for x in inventory:
        print(inventory[x])

def record_sale(inventory):
   
    item_check = False
    while item_check == False:
        item = input("Which item would you like to buy? ")
        for x in inventory:
            if(item == x):
                item_check = True
            
        if item_check == False:
            print("Please Try Again")


                
    amount = int(input("What is the quantity you would like? "))

    instock = False
    while instock == False:
            if amount > inventory[item].stock:
                print("We do not have that many items, please try again")
            else:
                inventory[item].stock -= amount
                instock = True
    save_inventory(inventory,"inventory.json")




def generate_restock_report(inventory):
    # Create an empty priority queue
    pq = []

    # Build priority list
    for name, item in inventory.items():
        if item.stock < item.restock_threshold:
            # How badly we need it
            gap = item.restock_threshold - item.stock
            # Push into heap with NEGATIVE gap (so largest gap comes first)
            heapq.heappush(pq, (-gap, name, item))

    if not pq:
        print("\n All items are sufficiently stocked!")
        return

    print("\n=== Restock Report ===")
    # Pop from priority queue in order
    rank = 1
    while pq:
        neg_gap, name, item = heapq.heappop(pq)
        gap = -neg_gap  # convert back to positive
        print(f"{rank}. {name} (stock: {item.stock} / threshold: {item.restock_threshold}) → NEED {gap} more")
        rank += 1


def add_stock(inventory):
    
    flag = False
    while flag == False:
        item = input("Which item would you like to add? ")
        if item in inventory:
            flag = True
        else:
            print("Please try again")
            
    inventory[item].stock += int(input("How many " + item + "'s would you like to add? "))
    
    save_inventory(inventory, "inventory.json")