from square.client import Client
import requests
import json
import os

def get_square_payments():
    # Set up Square API access credentials
    headers = {
        'Authorization': 'Bearer ' + os.environ['SQUARE_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }

    # Set up the request URL and parameters
    url = 'https://connect.squareup.com/v2/payments'
    params = {
        'begin_time': '2023-04-01T00:00:00Z',
        'end_time': '2023-04-01T23:59:59Z'
    }

    # Send the request to Square API and parse the response
    response = requests.get(url, headers=headers, params=params)
    payments = json.loads(response.text)['payments']

    # Extract the payment details from the response
    payment_list = []
    for payment in payments:
        payment_time = payment['created_at']
        if 'tip_money' in payment:
            tip_money = payment['tip_money']
            tip_amount = float(tip_money['amount']) / 100.0
        else:
            tip_amount = 0.0
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
            table_name = ''
        payment_list.append({'time': payment_time, 'tip_amount': tip_amount, 'table_name': table_name})

    return payment_list

list = get_square_payments()

for payment in list:
    print(payment)