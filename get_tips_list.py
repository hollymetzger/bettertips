from square.client import Client
import requests
import json
import os
import time
import datetime

def get_square_payments():
    # Set up Square API access credentials
    headers = {
        'Authorization': 'Bearer ' + os.environ['SQUARE_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    # Define the start and end times in EST timezone
    start_time = datetime.datetime(2023, 5, 12, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
    end_time = datetime.datetime(2023, 5, 13, 0, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))
    
    # Set up the request URL and parameters
    url = 'https://connect.squareup.com/v2/payments'
    params = {
        'begin_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
    }

    # Send the request to Square API and parse the response
    response = requests.get(url, headers=headers, params=params)
    payments = json.loads(response.text)['payments']

    # Extract the payment details from the response
    payment_list = []
    for payment in payments:

        payment_time = payment['created_at']
        
        if 'device_details' in payment:
            device_details = payment['device_details']
        
        if 'tip_money' in payment:
            tip_money = payment['tip_money']
            tip_amount = float(tip_money['amount']) / 100.0
        else:
            tip_amount = '0.0'
        
        payment_list.append({'time': payment_time, 'tip_amount': tip_amount, 'device_details': device_details})

    return payment_list



# get list of payments
list = get_square_payments()


# calculate total server and sushi tips
servertips = 0
sushitips = 0
for p in list:
    if (p['device_details']['device_installation_id']) == '778C7517-2B72-4EEE-8041-F1B024304390':
        servertips += float(p['tip_amount'])
    else:
        sushitips += float(p['tip_amount'])
twelve = servertips *0.12
servertips -= twelve
sushitips += twelve

print("Server tips: ${:0.2f} Sushi tips: ${:0.2f}".format(servertips, sushitips))



"""

******************** tried to get ticket name but it's not working, insert at line 44 ****************

        if 'order_id' in payment:
            order_id = payment['order_id']
            order_url = 'https://connect.squareup.com/v2/orders/' + order_id
            response = requests.get(order_url, headers=headers)
            try:
                order = json.loads(response.text)['order']
                if 'ticket_name' in order:
                    table_name = order['ticket_name']
                else:
                    table_name = 'no ticket name'
            except KeyError:
                table_name = 'error'
        else:
            table_name = 'no order id'
"""
