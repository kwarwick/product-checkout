import pandas as pd

pricing_standard_file = "pricing_standard.csv"
pricing_rules_file = "pricing_rules.csv"


# Checkout class is used to add items to a transaction. When called, will determine the total value of the
# transaction. This will take into account any special pricing considerations based on the selected customer.
class Checkout:
    def __init__(self, pricing_rules):
        self.items = []
        self.pricing_rules = pd.read_csv("data\\" + pricing_rules)
        self.customer = "default"

    # Adds an item to the checkout
    def add(self, item):
        self.items.append(item)

    # Sets the currently selected customer
    def set_customer(self, customer):
        self.customer = customer

    # Calculates and displays the order total based on any special pricing rules for the current customer, returning
    # base retail pricing otherwise.
    # TODO: Currently only implementing base retail pricing logic
    def total(self):
        total = 0
        for item in self.items:
            total += item.retail_price
        print("Total:", total)


# Item class is used to define each item that can be added to a checkout, along with its name, price, and description.
class Item:
    def __init__(self, name, description, retail_price):
        self.name = name
        self.description = description
        self.retail_price = retail_price


dummy_item = Item("Fries", "Yes, I would like fries with that", 5.99)

co = Checkout(pricing_rules_file)
co.add(dummy_item)
co.add(dummy_item)
co.total()
