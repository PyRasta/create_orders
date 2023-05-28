import logging
import random
import time

from binance import Client
from binance.enums import *
from binance.exceptions import *

from config import API_KEY, API_SECRET


client = Client(API_KEY, API_SECRET)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    
def generate_params_for_orders(data):
    params_for_orders = []
    symbol = data.symbol
    volume = data.volume
    side = data.side
    number = data.number
    price_min = data.price_min
    price_max = data.price_max
    amount_dif = data.amount_dif
    initial_amount = volume / number
    remaining_volume = volume
    for i in range(number):
        if remaining_volume <= 0:
            break
        price = random.uniform(price_min, price_max)
        if i != number-1:
            order_volume = random.uniform(initial_amount - amount_dif, initial_amount + amount_dif)
        else:
            order_volume = remaining_volume
        order_volume = round(order_volume, 2)
        order = {
            'symbol': symbol,
            'side': side,
            'price': price,
            'qty': price / order_volume,
            'volume': order_volume
        }
        remaining_volume -= order_volume
        params_for_orders.append(order)
    return params_for_orders


def create_order(params_for_order, count_try=0):
    try:
        precision = False
        exchange_info = client.futures_exchange_info()['symbols']
        for i in exchange_info:
            if i['symbol'] == params_for_order['symbol']:
                precision = i['quantityPrecision']
                break
        if not precision:
            return False, {'message': 'not find symbol'}
        qty = round(params_for_order['qty'], precision)
        order_id = client.futures_create_order(
            symbol=params_for_order['symbol'],
            side=params_for_order['side'],
            type=FUTURE_ORDER_TYPE_MARKET,
            quantity=str(qty)
        )
        return params_for_order, order_id
    except BinanceAPIException as error:
        if count_try != 5:
            logging.info('No create order')
            logging.info(error)
            time.sleep(1)
            count_try += 1
            return create_order(params_for_order, count_try)
        else:
            return False, {'message': 'not create order', 'error': error.args[2]}
        

def run(data):
    params_for_orders = generate_params_for_orders(data)
    results = []
    for params_for_order in params_for_orders:
        result = create_order(params_for_order)
        if not result[0]:
            print(result)
            return result
        results.append(result)
    return results
