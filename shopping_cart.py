# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:12:55 2020

@author: danca_000
"""

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

def print_receipt(receipt_strings, subtotal, tax, total, discount = False):
    print("#> ---------------------------------")
    print("#> GREEN FOODS GROCERY")
    print("#> WWW.GREEN-FOODS-GROCERY.COM")
    print("#> ---------------------------------")
    print("#> CHECKOUT AT: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("#> ---------------------------------")
    print("#> SELECTED PRODUCTS:")
    for item in receipt_strings:
        print(item)
    if(discount == True):
        print("#> ... DISCOUNT " + " (-$3.00)")
    print("#> ---------------------------------")
    print(f"#> SUBTOTAL: ${subtotal:.2f}")
    print(f"#> TAX: ${tax:.2f}")
    print(f"#> TOTAL: ${total:.2f}")
    print("#> Please come again!")

receipt_strings = []
subtotal = 0
product_totals = {} 
for i in range(1, data.shape[0] + 1):
    product_totals[i] = 0

#loop for user input, stores the number of each product purchase
while(True):
    prodID = input("Please input a product identifier, or DONE if finsihed: ")
    if (prodID == "DONE"):
        break
    if (prodID.isdigit() and int(prodID) in data.index):
        prodID = int(prodID)
        product_totals[prodID] += 1
    else:
        print("It doesn't look like that was a valid product identifier, please try again.")

#formats and stores a string for each product that was purchased
for key in product_totals.keys():
    if(product_totals[key] > 0):
        receipt_strings.append("#> ... " + str(product_totals[key]) + "x " + data.loc[product_totals[key]]['name'] +
                               " ($" + "{:,.2f}".format(data.loc[key]['price'] * product_totals[key]) + ")" )
        subtotal += data.loc[key]["price"] * product_totals[key]
#Loop for the rewards program prompt, 
while True:
    total = subtotal*1.0875
    tax = total-subtotal
    rewards = input("Are you a member of our rewards program? (y/n)\n")
    if (rewards.lower() != "y" and rewards.lower() != "n"):
        print("Sorry, please answer \"y\" for yes or \"n\" for no")
    elif (rewards.lower() == "y"):
        while True:
            email = input("What is your email? (Or CANCEL to continue without using rewards)\n")
            if(email == "CANCEL"):
                print_receipt(receipt_strings,  subtotal, tax, total)
                break
            try:
                name = members.loc[members['Email'] == email].Name.iloc[0]
                points = members.loc[members['Email'] == email].Points.iloc[0]
                points += subtotal
                print(f"Thank you for you purchase,{name}")
                print("With this purchase, you have {:,.0f} points.".format(points))
                members['Points'][members['Email'] == email] = points
                if(points > 100):
                    print("You have over 100 points, so you'll be getting $3 off your bill!")
                    subtotal -= 3
                    members['Points'][members['Email'] == email] -= 100
                    members.to_csv("members.csv",index=False)
                    print_receipt(receipt_strings, subtotal, tax, total, discount=True)
                    break
                else:
                    members.to_csv("members.csv", index=False)
                    print_receipt(receipt_strings, subtotal, tax, total)
                    break
                    
            except:
                print("I'm sorry, that email isn't in our records.")
        break
    else:
        answer = input(("Would you like to join?\nYou get a point for every dollar"
        " you spend with us, \nand once you have over 100 points you get $2 off your total! (y/n)\n"))
        if (answer.lower() == "y"):
            while True:
                email = input("What is your email?\n")
                name = input("what is your first name?\n")
                if (email in set(members['Email'])):
                    print("Sorry, that email is already taken. Please try again")
                else:
                    break
            total = subtotal * 1.0875
            new_member = pd.DataFrame(data={'Email':email, 'Name':name, 'Points':total}, index=[0])
            new_member.set_index('Email', drop=True)
            members = members.append(new_member, sort=True)
            members.to_csv("members.csv", index=False)
            print("Your information has been saved!")
            print("You now have {:,.0f} points!".format(subtotal))
            print_receipt(receipt_strings, subtotal, tax, total)
            break
        else:
            print_receipt(receipt_strings, subtotal, tax, total) 
            break