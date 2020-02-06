# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 11:07:43 2020

@author: DCagney
"""
import pytest
import pandas as pd
from datetime import datetime

# products = [
#     {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
#     {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
#     {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
#     {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
#     {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
#     {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
#     {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
#     {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
#     {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
#     {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
#     {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
#     {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
#     {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
#     {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
#     {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
#     {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
#     {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
#     {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
#     {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
#     {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
# ] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


data = pd.read_csv("products.txt", index_col = "id")
members= pd.read_csv("members.csv")
members.set_index('Email', drop=True)

receipt_strings = []
subtotal = 0
print(members.columns)
print(members)
product_totals = {} 
for i in range(1, data.shape[0] + 1):
    product_totals[i] = 0
 
while(True):
    prodID = input("Please input a product identifier, or DONE if finsihed: ")
    if (prodID == "DONE"):
        break
    if (prodID.isdigit() and int(prodID) in data.index):
        prodID = int(prodID)
        product_totals[prodID] += 1
    else:
        print("It doesn't look like that was a valid product identifier, please try again.")

for key in product_totals.keys():
    if(product_totals[key] > 0):
        receipt_strings.append("#> ... " + str(product_totals[key]) + "x " + data.loc[product_totals[key]]['name'] +
                               " ($" + "{:,.2f}".format(data.loc[key]['price'] * product_totals[key]) + ")" )
        subtotal += data.loc[key]["price"] * product_totals[key]
while True:
    rewards = input("Are you a member of our rewards program? (y/n)")
    if (rewards.lower() != "y" and rewards.lower() != "n"):
        print("Sorry, please answer \"y\" for yes or \"n\" for no")
    elif (rewards.lower() == "y"):
        print("heya member")
        break
    else:
        answer = input("Would you like to join? You receive $3 off for every $100 you spend with us! (y/n)")
        if (answer.lower() == "y"):
            email = input("What is your email?")
            name = input("what is your first name?")
            total = subtotal * 1.0875
            new_member = pd.DataFrame(data={'Email':email, 'Name':name, 'Points':total}, index=[0])
            new_member.set_index('Email', drop=True)
            members = members.append(new_member, sort=True)
            print(members)
            members.to_csv("members.csv", index=False)
            print("Your information has been saved!")
            print(members.columns)
            break
        else:
            total = subtotal * 1.0875
            tax = total-subtotal
            print("#> ---------------------------------")
            print("#> GREEN FOODS GROCERY")
            print("#> WWW.GREEN-FOODS-GROCERY.COM")
            print("#> ---------------------------------")
            print("#> CHECKOUT AT: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("#> ---------------------------------")
            print("#> SELECTED PRODUCTS:")
            for item in receipt_strings:
                print(item)
            print("#> ---------------------------------")
            print(f"#> SUBTOTAL: ${subtotal:.2f}")
            print(f"#> TAX: ${tax:.2f}")
            print(f"#> TOTAL: ${total:.2f}")
            print("#> Please come again!")
            break