# geminiAPI


Simple API to link account, view order history, and make orders on Gemini Sandbox Exchange.


This is currently running on gemini sandbox only.

 
How to use API:

1. Start server (python3 manage.py runserver) on port 8000
2. Go to localhost/8000/create/account
3. Grant access
4. Remember your account ID that is returned in response


To view order history:
1. Go to localhost:8000/history/{insert id here}

To make an order:
1. endpoint is localhost:8000/order/{insert id here}
2. Make a post request with the following fields:
	symbol, amount, price, side(buy or sell), type(exchange or stop limit)




ex.
curl -X POST localhost:8000/order/01cd9c0e-f025-11ec-9089-1e003902ca29 -H 'Content-Type: application/json' -d '{"symbol": "ethusd",
    "amount": "1",
    "price": "2000.00",
    "side": "buy",
    "type": "exchange limit"}'
