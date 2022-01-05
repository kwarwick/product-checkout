# Product Checkout Assignment
This exercise deals with programming the required logic to apply special offers and promotions to various customers of 
Bepoz.

## Installation
The only required package to run this code is Pandas. The specific process to do this will depend on your environment,
with full instructions available from [Pandas](https://pandas.pydata.org/docs/getting_started/install.html).

## Usage
The script can be run by following the template in the provided test examples. This matches the pseudocode provided
and can be executed as follows:
```python
co = Checkout(pricing_rules_file)
co.add(item1)
co.add(item2)
co.total()
```

Pricing rules and standard pricing are stored as csv files in the data directory. They can be edited to change the
behaviour of the checkout.

Direct discount pricing rules are stored by simply specifying the promotional price for a given customer and item
combination.

Multi-deal discount pricing expects input of the form 4->3, meaning that for every 4 of a matching item added, only
3 are paid for. This works with any combination of numbers where the rightmost number is smaller than the leftmost
number.

If a customer is eligible for multiple multi-deals, only the one that gives them the greatest discount will be applied.

If a customer is eligible for multiple direct discounts, only the best one will be applied.

It is assumed that multiple pricing rules can be applied in the same transaction, and direct discount pricing can 
also be utilised in multi-deals if a customer is eligible for both on the same item.