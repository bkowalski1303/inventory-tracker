from flask import Flask, render_template, request, redirect, url_for
from inventory_tracker import load_inventory, save_inventory
from item_class import Item  # ensure this exists

app = Flask(__name__)
INVENTORY_FILE = "inventory.json"


@app.route("/")
def index():
    inventory = load_inventory(INVENTORY_FILE)
    return render_template("index.html", inventory=inventory)


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    inventory = load_inventory(INVENTORY_FILE)

    if request.method == "POST":
        name = request.form["name"].strip()
        stock = int(request.form["stock"])
        threshold = int(request.form["threshold"])

        if name in inventory:
            return render_template(
                "add_item.html",
                error="Item already exists!",
                inventory=inventory
            )

        # Create new Item object
        new_item = Item(name=name, stock=stock, restock_threshold=threshold)
        new_item.sales_history = []  # initialize empty history

        # Save to inventory
        inventory[name] = new_item
        save_inventory(inventory, INVENTORY_FILE)

        return redirect(url_for("index"))

    return render_template("add_item.html")


@app.route("/add_stock/<item_name>", methods=["GET", "POST"])
def add_stock(item_name):
    inventory = load_inventory(INVENTORY_FILE)

    if item_name not in inventory:
        return "Item not found!", 404

    if request.method == "POST":
        try:
            amount = int(request.form["amount"])
        except ValueError:
            return render_template(
                "add_stock.html",
                item_name=item_name,
                error="Please enter a valid number."
            )

        # Increase stock
        inventory[item_name].stock += amount
        save_inventory(inventory, INVENTORY_FILE)
        return redirect(url_for("index"))

    return render_template("add_stock.html", item_name=item_name)


@app.route("/delete_item/<item_name>")
def delete_item(item_name):
    inventory = load_inventory(INVENTORY_FILE)

    if item_name not in inventory:
        return "Item not found!", 404

    # Delete item
    del inventory[item_name]
    save_inventory(inventory, INVENTORY_FILE)

    return redirect(url_for("index"))


@app.route("/restock_report")
def restock_report():
    inventory = load_inventory(INVENTORY_FILE)

    # Find items below threshold
    low_stock_items = {
        name: item for name, item in inventory.items()
        if item.stock < item.restock_threshold
    }

    return render_template("restock_report.html", low_stock_items=low_stock_items)

if __name__ == "__main__":
    app.run(debug=True)

