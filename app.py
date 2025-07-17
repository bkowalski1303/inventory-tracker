from flask import Flask, render_template, request, redirect, url_for
from inventory_tracker import load_inventory, save_inventory, add_new_item, generate_restock_report
from item_class import Item

app = Flask(__name__)
DATA_FILE = "inventory.json"

@app.route("/")
def index():
    inventory = load_inventory(DATA_FILE)
    return render_template("index.html", inventory=inventory)

@app.route("/add", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        stock = int(request.form["stock"])
        threshold = int(request.form["threshold"])

        inventory = load_inventory(DATA_FILE)
        inventory[name] = Item(name, stock, threshold)
        inventory[name].sales_history = []
        save_inventory(inventory, DATA_FILE)

        return redirect(url_for("index"))
    return render_template("add_item.html")

@app.route("/restock")
def restock_report():
    inventory = load_inventory(DATA_FILE)
    # Generate a restock report priority list
    restock_list = []
    for name, item in inventory.items():
        if item.stock < item.restock_threshold:
            gap = item.restock_threshold - item.stock
            restock_list.append((gap, name, item))
    # Sort highest gap first
    restock_list.sort(reverse=True)
    return render_template("restock_report.html", restock_list=restock_list)

if __name__ == "__main__":
    app.run(debug=True)
