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

        # id = payment['id']
        # order_id = payment['order_id']
        payment_time = payment['created_at']
        updated_at = payment['updated_at']
        
        if 'tip_money' in payment:
            tip_money = payment['tip_money']
            tip_amount = float(tip_money['amount']) / 100.0
        else:
            tip_amount = '0.0'
        
        payment_list.append({'time': payment_time, 'tip_amount': tip_amount})

    return payment_list




list = get_square_payments()

for p in list:
    print(p)