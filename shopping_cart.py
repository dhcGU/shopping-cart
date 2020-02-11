


"""
@author: dhc38
"""

import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

pd.options.mode.chained_assignment = None

load_dotenv()
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "You need an env var named SENDGRID_API_KEY.")
SENDING_EMAIL = os.environ.get("SENDING_EMAIL", "You need an env var named SENDING_EMAIL.")
print(SENDGRID_API_KEY)

data = pd.read_csv("products.txt", index_col = "id")
members= pd.read_csv("members.csv")
members.set_index('Email', drop=True)

#function that prints receipt to the terminal 
def print_receipt(receipt_strings, subtotal, tax, total, discount = False):
    print("#> ---------------------------------")
    print("#> GREEN FOODS GROCERY")
    print("#> WWW.GREEN-FOODS-GROCERY.COM")
    print("#> ---------------------------------")
    print("#> CHECKOUT AT: " + datetime.now().strftime("%Y-%m-%d %I:%M:%p"))
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

#function that returns the html content for emails
def render_email(receipt_strings, subtotal, tax, total, discount=False):
    html = ""
    html +="#> ---------------------------------<br>"
    html +="#> GREEN FOODS GROCERY<br>"
    html +="#> WWW.GREEN-FOODS-GROCERY.COM<br>"
    html +="#> ---------------------------------<br>"
    html +="#> CHECKOUT AT: " + datetime.now().strftime("%Y-%m-%d %I:%M:%p")
    html +="#> ---------------------------------<br>"
    html +="#> SELECTED PRODUCTS:<br>"
    for item in receipt_strings:
        html += str(item) + "<br>"
    if(discount == True):
        html +="#> ... DISCOUNT " + " (-$3.00)<br>"
    html +="#> ---------------------------------<br>"
    html +=f"#> SUBTOTAL: ${subtotal:.2f}<br>"
    html +=f"#> TAX: ${tax:.2f}<br>"
    html +=f"#> TOTAL: ${total:.2f}<br>"
    html +="#> Please come again!<br>"
    return html

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
        receipt_strings.append("#> ... " + str(product_totals[key]) + "x " + data.loc[key]['name'] +
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
            canceled = False
            if(email == "CANCEL"):
                print_receipt(receipt_strings,  subtotal, tax, total)
                canceled = True
                break
            try:
                name = members.loc[members['Email'] == email].Name.iloc[0]
                points = members.loc[members['Email'] == email].Points.iloc[0]
                break
            except:
                print("I'm sorry, that email isn't in our records.")
        if(canceled == True):
            break
        points += subtotal
        print(f"Thank you for you purchase,{name}")
        print("With this purchase, you have {:,.0f} points.".format(points))
        members['Points'][members['Email'] == email] = points
        while True:
            emailReceipt = input("Would you like your receipt emailed to you? (y/n)\n")
            if(emailReceipt.lower() == 'y' or emailReceipt.lower() == 'n'):
                break
            else:
                print("Sorry, please respond \"y\" to email your receipt or \"n\" to print it.")
        if(points > 100):
            print("You have over 100 points, so you'll be getting $3 off your bill!")
            subtotal -= 3
            members['Points'][members['Email'] == email] -= 100
            members.to_csv("members.csv",index=False)
            if(emailReceipt == 'n'):
                print_receipt(receipt_strings, subtotal, tax, total, discount=True)
                break
            else:
                client = SendGridAPIClient(SENDGRID_API_KEY)
                subject = "Your receipt from Green Grocery Store"
                content = render_email(receipt_strings, subtotal, tax, total, discount=True)
                message = Mail(from_email=SENDING_EMAIL, to_emails=email, subject=subject, html_content=content)
                try:
                    response = client.send(message)
                    if(response.status_code != 202):  
                        raise
                    print("Your receipt has been emailed. Have a great day!")
                    break
                except:
                    print("Sorry, we couldn't email your receipt.")
                    print_receipt(receipt_strings, subtotal, tax, total, discount=True)
                    break
            break
        else:
            members.to_csv("members.csv", index=False)
            if(emailReceipt == 'n'):
                print_receipt(receipt_strings, subtotal, tax, total)
                break
            else:
                client = SendGridAPIClient(SENDGRID_API_KEY) 
                subject = "Your receipt from Green Grocery Store"
                content = render_email(receipt_strings, subtotal, tax, total)
                message = Mail(from_email=SENDING_EMAIL, to_emails=email, subject=subject, html_content=content)
                try:
                    response = client.send(message)
                    if(response.status_code != 202):  
                        raise
                    print("Your receipt has been emailed. Have a great day!")
                    break
                except:
                    print("Sorry, we couldn't email your receipt.")
                    print_receipt(receipt_strings, subtotal, tax, total)
                    break  
            break
        break
    else:
        while True:
            answer = input(("Would you like to join?\nYou get a point for every dollar"
                            " you spend with us, \nand once you have over 100 points you get $3 off your total! (y/n)\n"))
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
            elif (answer.lower() == "n"):
                print_receipt(receipt_strings, subtotal, tax, total) 
                break
            else:
                print("Sorry, please answer \"y\" for yes or \"n\" for no")
                continue
            break
        break