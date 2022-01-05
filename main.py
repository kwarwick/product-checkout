import pandas as pd

pricing_standard_file = "pricing_standard.csv"
pricing_rules_file = "pricing_rules.csv"


# Checkout class is used to add items to a transaction. When called, will determine the total value of the
# transaction. This will take into account any special pricing considerations based on the selected customer.
class Checkout:
    def __init__(self, pricing_rules):
        self.items = []
        self.pricing_rules = pd.read_csv("data\\" + pricing_rules)
        # print(self.pricing_rules)
        self.customer = "default"

    # Adds an item to the checkout
    def add(self, item):
        self.items.append(item)

    # Sets the currently selected customer
    def set_customer(self, customer):
        self.customer = customer

    # Calculates and displays the order total based on any special pricing rules for the current customer, returning
    # base retail pricing otherwise. Currently assuming that direct discounts and multi-deals can stack. Prevents
    # several multi-deals from stacking. Also applies the best direct discount available for each product. Also assumes
    # there is no limit to the number of special pricing options that can be applied outside of these restrictions.
    def total(self):
        added_item_prices = {}
        added_item_counts = {}
        # Add standard retail price to a dict for reference for each item in transaction, and count quantities.
        for item in self.items:
            if item.name not in added_item_prices.keys():
                added_item_prices[item.name] = item.retail_price
            if item.name in added_item_counts.keys():
                added_item_counts[item.name] += 1
            else:
                added_item_counts[item.name] = 1

        # Determine any special pricing rules that apply to the selected customer
        special_pricing = []

        for index, pricing_rule in self.pricing_rules.iterrows():
            if pricing_rule['Customer'] == self.customer:
                special_pricing.append((pricing_rule['Product Name'],pricing_rule['Pricing']))

        # We will need a copy of the item counts dict in case of conflicting multi-deals - need to apply the best one.
        offer_item_counts = {}
        for offer in special_pricing:
            offer_product = offer[0]
            offer_pricing = offer[1]
            if offer_product in added_item_counts.keys():
                # Handle multi-deals
                if "->" in offer_pricing:
                    added_item_count = added_item_counts[offer_product]
                    high, low = offer_pricing.split("->")
                    deal_stacks = added_item_count // int(high)
                    remainder = added_item_count % int(high)
                    offer_item_count = deal_stacks * int(low) + remainder
                    if offer_product in offer_item_counts.keys():
                        if offer_item_counts[offer_product] > offer_item_count:
                            offer_item_counts[offer_product] = offer_item_count
                    else:
                        offer_item_counts[offer_product] = offer_item_count

                # Handle direct discounts
                elif added_item_prices[offer_product] > float(offer_pricing):
                    added_item_prices[offer_product] = float(offer_pricing)

        # Update the item counts based on the best available offer
        for offer_item in offer_item_counts.keys():
            if offer_item_counts[offer_item] < added_item_counts[offer_item]:
                added_item_counts[offer_item] = offer_item_counts[offer_item]

        total = 0

        for item in added_item_counts.keys():
            total += added_item_counts[item] * added_item_prices[item]

        print("Total: $", total, sep='')


# Item class is used to define each item that can be added to a checkout, along with its name, price, and description.
class Item:
    def __init__(self, name, description, retail_price):
        self.name = name
        self.description = description
        self.retail_price = retail_price

    def __str__(self):
        return self.name + " ($" + str(self.retail_price) + "): " + self.description


# Load in item database
items_df = pd.read_csv("data\\" + pricing_standard_file)
items = []
for index, row in items_df.iterrows():
    items.append(Item(row['Name'], row['Description'], row['Retail Price']))

# This is purely to aid in testing - would be simplified with a GUI
small = items[0]
medium = items[1]
large = items[2]

# Case 1
print("Case 1 (expecting $49.97)")
co = Checkout(pricing_rules_file)
co.add(small)
co.add(medium)
co.add(large)
co.total()
print("")

# Case 2
print("Case 2 (expecting $45.97)")
co = Checkout(pricing_rules_file)
co.set_customer('Microsoft')
co.add(small)
co.add(small)
co.add(small)
co.add(large)
co.total()
print("")

# Case 3
print("Case 3 (expecting $67.96)")
co = Checkout(pricing_rules_file)
co.set_customer('Amazon')
co.add(medium)
co.add(medium)
co.add(medium)
co.add(large)
co.total()
print("")

# Case 4
print("Case 4 (expecting $131.92)")
co = Checkout(pricing_rules_file)
co.set_customer('Facebook')
co.add(small)
co.add(medium)
co.add(small)
co.add(large)
co.add(medium)
co.add(medium)
co.add(large)
co.add(medium)
co.add(medium)
co.total()
print("")
