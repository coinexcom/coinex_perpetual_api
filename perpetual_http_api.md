# Authorization

* The authorization process is as described in the example.

> Example:

```
1. The input parameter string of http message is as follows:
market=BTCUSD&type=buy&price=680&amount=1.0&timestamp=1550743431000

2. At the end of the above message, splice the secret_key to get the following:
market=BTCUSD&type=buy&price=680&amount=1.0&timestamp=1550743431000&secret_key=B51068CF10B34E7789C374AB932696A05E0A629BE7BFC62F
Note: The secret_key parameter is not required when sending http message. This step is only used to calculate sha256 signature.

3. Perform sha256 signature to the above string, convert it to hexadecimal lowercase with a length of 64 bits, and add this signature to the header of http as follows:
Authorization: 3e9e58c40d18358bb129c98139eec99af781275708895e522f572a87dc8d9137

4. Add AccessId to the header of http, and the server will search the corresponding user information according to the AccessId.
AccessId: 4DA36FFC61334695A66F8D29020EB589

5. After receiving the http message, the server will find the user's secret key according to AccessId, conduct the same operation as above and judge whether the received signature is equal to the one calculated by itself. If they are equal, the authorization is successful, otherwise it fails.

```

# Timestamp Verification

When the server receives the request, it will judge the timestamp in the request. The request will be considered invalid if it was sent 5000 milliseconds ago. This window time value can be defined by sending the optional parameter recvWindow.

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| timestamp | Integer | Y | Timestamp in milliseconds |
| windowtime | Integer | N | Window time in milliseconds |

# Request

### GET

```
http://api.coinex.com/perpetual/v1/market/depth?market=BTCUSD&merge=1
```

### POST

```
http://api.coinex.com/perpetual/v1/order/put_limit

Request parameters are put into http body in the form of application/x-www-form-urlencoded
```

# RESPONSE

* result: Json object, null for failure
* error: Json object, null for success, non-null for failure
   1. code: error code
   2. message: error message
* id: Request id, Integer
* example

```
// success
{
    "message": "OK",
    "data": {
      ....
    },
    "code": 0
}

// error
{
    "message": "error message",
    "data": {},
    "code": 11
}
```

# System Api

### Ping

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/ping
* Params: none
* Data:

```
"data": "pong"
```

### System Time

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/time
* Params: none
* Data:

```
"data": 11111123455 // millisecond
```
# Market Api

### Market List

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/list
* Params: none
* Data:

```
'data': [
  {
    'name': 'BTCUSD',
    'type': 1, // 1: USDT-M Contracts, 2: Coin-M Contracts
    'stock': 'BTC',
    'money': 'USD',
    'fee_prec': 4,
    'stock_prec': 8,
    'money_prec': 8,
    'multiplier': 1,
    'amount_prec': 0,
    'amount_min': '10',
    'tick_size': '0.5', // Min. Price Increment
    'leverages': ["3", "5", "8", "10", "15", "20", "30", "50", "100"]
  }
]
```

### Market Limit config

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/limit_config
* Params: none
* Data:

```
'data': {
  'BTCUSD': [
    ["1000", "100", "0.005"], // amount, leverage, mainten_margin
    ["10000", "50", "0.01"],
    ["15000", "30", "0.015"],
    ["25000", "20", "0.02"],
    ["50000", "15", "0.025"],
    ["75000", "10", "0.03"],
    ["80000", "6", "0.035"],
    ["110000", "6", "0.04"],
    ["120000", "5", "0.045"],
    ["130000", "5", "0.05"],
    ["140000", "5", "0.055"],
    ["150000", "3", "0.06"]
  ]
}
```

### Market Ticker

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/ticker
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes |  |

* Data:

```
"data": {
  "ticker": {
    "period": 86400,
    "funding_time": 10,
    "position_amount": "100",
    "funding_rate_last": "0.01",
    "funding_rate_next": "0.02",
    "insurance": "100"
    "last": "7000.00",
    "sign_price": "7100", // sign price
    "index_price": "7111", // index price
    "sell_total": "700",
    "buy_total": "600
    "open": "0",
    "close": "0",
    "high": "0",
    "low": "0",
    "volume": "0",
    "buy": "110.1", // first buy price
    "buy_amount": "100", // first buy amount
    "sell": "110.1", // first sell price
    "sell_amount": "100" // first sell amount
  },
  "date": 11111111 //timestamp
}
```

### Market Ticker All

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/ticker/all
* Params: none
* Data:

```
"data": {
  "ticker":{
    "BTCUSD": {
      "period": 86400,
      "funding_time": 10,
      "position_amount": "100",
      "funding_rate_last": "0.01",
      "funding_rate_next": "0.02",
      "insurance": "100",
      "last": "7000.00",
      "sign_price": "7100",
      "index_price": "7111",
      "sell_total": "700",
      "buy_total": "600"
      "open": "0",
      "close": "0",
      "high": "0",
      "low": "0",
      "volume": "0",
      "buy": "110.1", // first buy price
      "buy_amount": "100", // first buy amount
      "sell": "110.1", // first sell price
      "sell_amount": "100" // first sell amount
    }
      ...
  },
  "date": 11111111 //timestamp
}
```

### Market Depth

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/depth
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market, e.g. "BTCUSD" Perpetual Market |
| merge | String | Y | Merge precision, take one of the value among "10", "1", "0", "0.1" and "0.01". |
| limit | Integer | Y | The number of entries obtained, take one of the value among 5, 10, 20, 50 and 100. |

* Data:

```
"data": {
  "asks": [
    ["3750", "39"],
    ["3800", "305"],
    ["3900", "22"]
  ],
  "bids": [
    ["3700", "35"],
    ["3650", "80"],
    ["3600", "305"],
    ["3599", "20"],
    ["3598", "10"],
    ["3597", "20"]
  ],
  "last": "3740",
  "time": 111111,
  "sign_price": "3750",
  "index_price": "3750"
}
```

### Market deals

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/deals
* Request:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y |  |
| last_id | Integer |  N |  |
| limit | Integer | N | |

* Data:

```
"data": [
  {
    "id": 11,
    "type": "buy", // buy or sell
    "price": "100.1"
    "amount": "100",
    "date": 111111,
    "date_ms": 1111111.111
  }
   ...
]
```

### Market Funding History

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/funding_history
* Request:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | |
| start_time | Integer | N | |
| end_time | Integer | N | |
| offset | Integer | Y | |
| limit | Integer | Y | |

* Data:

```
"data": {
  "offset": 10,
  "limit": 100,
  "records": [
    {
      'time': 1615233600.7274661,
      'market': 'BTCUSD',
      'asset': BTC,
      'funding_rate': 0.00175,
      'funding_rate_real': 0.00175
    }
       ...
  ]
}
```

### User deals

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/user_deals
* Request:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | |
| side | Integer | Y | 0 for no limit, 1 for sell, 2 for buy |
| start_time | Integer | N | |
| end_time | Integer | N | |
| offset | Integer | Y | |
| limit | Integer | Y | |

* Data:

```
"data": {
  "offset": 10,
  "limit": 100,
  "records": [
    {
      'id': 1,
      'time': 102001.123,
      'deal_type': 1, //1 open position, 2 add position, 3 sub position, 4 close position, 5 sys close, 6 position liq, 7 position adl
      'market': 'BTCUSD',
      'user_id': 11,
      'order_id': 13,
      'position_id': 12,
      'side': 1,  //1: sell, 2: buy
      'role': 1,  //1: maker, 2: taker
      'position_type': 1,
      'price': '110.1',
      'open_price': '120.1',
      'amount': '110',
      'position_amount': '220',
      'margin_amount': '220',  // Position Margin after execution
      'leverage': '10',
      'deal_stock': '0.222',
      'deal_fee': '0.001',
      'deal_margin': '20',  // Margin of transaction
      'fee_rate': '0.02',
      'deal_profit': '100',
      'deal_insurance': '0.004' // Consumed or increased Insurance Fund
    }
      ...
  ]
}
```

### Market Kline

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/kline
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| limit | Integer | N | The number of candlesticks obtained must not be greater than 1000 (1000 by default)|
| type | String | Y | Supported candlestick parameters: 1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week|

* Data:

```
"data": [
  [
    1440308700,    # Time
    233.37,        # Opening Price
    233.48,        # Closing Price
    243.37,        # Highest Price
    223.48,        # Lowest Price
    52，           # Trading Volume
    22.2810015     # Trading Value
    "BTCUSD"     # Market Name
  ],
  [
    1440308701,   # Time
    233.31,       # Opening Price
    233.41,       # Closing Price
    243.31,       # Highest Price
    223.41,       # Lowest Price
    51，          # Trading Volume
    21.2810015    # Trading Value
    "BTCUSD"    # Market Name
  ]
]
```

### Ajust leverage

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/market/adjust_leverage
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| leverage | String | Y | leverage |
| position_type | Integer | Y | 1 Isolated Margin 2 Cross Margin |
| timestamp | Integer | Y | Timestamp in milliseconds |
| windowtime | Integer | N | Window time in milliseconds |

* Data:

```
"data": {
  "position_type": 1, // Position Type
  "leverage": "10"    // Leverage
}
```

### Get position amount

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/market/position_expect
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| price | String | Y | Price |
| side | Integer | Y | 1 Sell 2 Buy |
| timestamp | Integer | Y | Timestamp in milliseconds |
| windowtime | Integer | N | Window time in milliseconds |

* Data:

```
"data": {
  "position_expect": "10"    // Expected Amount of Opening
}
```


# Asset Api

### asset query

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/asset/query
* Params: None
* Data:

```
"data": {
  "BTC": {
    "available": "250", // Available Balance
    "frozen": "10",    // Frozen
    "tranfer": "10",   // Available Transfer
    "balance_total": "11", // Balance
    "margin", "10", // Margin
    "profit_unreal": "100" // Unrealized PNL
  },
  "ETH": {
    "available": "250", // Available Balance
    "frozen": "10",    // Frozen
    "tranfer": "10",   // Available Transfer
    "balance_total": "11", // Balance
    "margin", "10",// Margin
    "profit_unreal": "100" // Unrealized PNL
  }
}
```


# Order Api

### Put limit order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y |  |
| side | Integer | Y | 1 sell, 2 buy |
| amount | String | Y | Delegation Amount |
| price | String | Y | Delegated Price |
| effect_type | Integer | N | Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. GTC Order is set by default.  |
| option | Integer | N | Option, 1: Maker Only. The default is "O". |
| client_id | String | N | You can customize order IDs to identify your orders. The system supports alphabets + numbers(case-sensitive，e.g:A123、a123), or alphabets (case-sensitive，e.g:Abc、abc) only|
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,    // Position Type 1: Isolated Margin 2: Cross Margin
  'stop_id': 0         // Stop Order ID
}
```

### Put market order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_market
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| side | Integer | Y | Side, 1: Sell, 2: Buy|
| amount | String | Y | Amount |
| client_id | String | N | You can customize order IDs to identify your orders. The system supports alphabets + numbers(case-sensitive，e.g:A123、a123), or alphabets (case-sensitive，e.g:Abc、abc) only|
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds |

* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,    // Position Type 1: Isolated Margin, 2: Cross Margin
  'stop_id': 0         // Stop Order ID
}
```

### Put limit close order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/close_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | Perpetual Market |
| position_id | Integer | Yes | Position ID |
| amount | String | Yes | Closing Amount|  |
| price | String | Yes | Price |
| effect_type | Integer | No |  Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. "GTC Order" is set by default. |
| option | Integer | N | Option, 1: Maker Only. The default is "0".  |
| timestamp | Integer | Yes | Timestamp in milliseconds|
| windowtime | Integer | No | Window time in milliseconds|


* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,    // Position Type 1: Isolated Margin 2: Cross Margin
  'stop_id': 0          // Stop Order ID
}
```

### Put market close order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/close_market
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | Perpetual Market |
| position_id | Integer | Yes | Position ID |
| timestamp | Integer | Yes | Timestamp in milliseconds|
| windowtime | Integer | No | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,   // Position Type 1: Isolated Margin 2: Cross Margin
  'stop_id': 0         // Stop Order ID
}
```

### Put stop limit order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_stop_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| side | Integer | Y | Side, 1: Sell for Short, 2: Buy for Long |
| stop_type | Integer | Y | Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at the index price |
| amount | String | Y | Delegation Amount |
| stop_price | String | Y | Stop Price |
| price | String | Y | Delegated Price |
| effect_type | Integer | N | Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. "GTC Order" is set by default. |
| option | Integer | N | Option, 1: Maker Only. The default is "0". |
| client_id | String | N | You can customize order IDs to identify your orders. The system supports alphabets + numbers(case-sensitive，e.g:A123、a123), or alphabets (case-sensitive，e.g:Abc、abc) only|
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": "success"
```

### Put stop market order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_stop_market
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| side | Integer | Y | Side, 1: Sell for Short, 2: Buy for Long|
| stop_type | Integer | Y | Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at the index price|
| amount | String | Y | Delegation Amount |
| stop_price | String | Y | Stop Price |
| client_id | String | N | You can customize order IDs to identify your orders. The system supports alphabets + numbers(case-sensitive，e.g:A123、a123), or alphabets (case-sensitive，e.g:Abc、abc) only|
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | No | Window time in milliseconds|

* Data:

```
"data": "success"
```

### Cancel pending order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| order_id | Integer | Y | Unexecuted Order ID |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,   // Position Type 1: Isolated Margin 2: Cross Margin
  'stop_id': 0         // Stop Order ID
}
```

### Cancel all pending order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_all
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market  |
| side | Integer | N | Side, 0: all, 1: Sell, 2: Buy |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": "success"
```

### Cancel pending stop order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_stop
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market  |
| order_id | Integer | Y | Unexecuted Order ID |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'effect_type': 1, // Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. "GTC Order" is set by default.
  'stop_type': 1,   // Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at the index price
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'web',
  'state': 1,
  'stop_price': '9200',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
}
```

### Cancel all pending stop order

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_stop_all
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market |
| side | Integer | N | Side, 0: all, 1: Sell, 2: Buy |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": "success"
```

### Query pending order

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market, e.g. BTCUSD |
| side | Integer | Y | 0:All 1: Sell, 2: Buy |
| offset | Integer |  Y | Offset, means query from a certain record |
| limit | Integer |  Y | The number of records acquired at a time, the default is 20 and the maximum is 100. |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  "records": [
    {
      'order_id': 10,
      'position_id': 0,
      'market': 'BTCUSD',
      'type': 1,
      'side': 2,
      'target': 2,
      'effect_type': 1,
      'user_id': 10,
      'create_time': 102001.123,
      'update_time': 102003.123,
      'source': 'API',
      'price': '9100.1',
      'amount': '100',
      'taker_fee': '0.005',
      'maker_fee': '-0.002',
      'left': '80',         // Unexecuted Amount
      'deal_stock': '0.9',  // Executed Value
      'deal_fee': '0.01',   // Used Tx Fees
      'leverage': '10',     // Leverage
      'position_type': 1,    // Position Type 1: Isolated Margin 2: Cross Margin
      'stop_id': 0          // Stop Order ID
    },
    ...
  ],
  "total": 10,
  "offset": 10,
  "limit": 5
}
```

### Query finished order

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/finished
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | |
| side | Integer | Y | 0 for no limit, 1 for sell, 2 for buy |
| start_time | Integer | N | |
| end_time | Integer | N | |
| offset | Integer | Y | |
| limit | Integer | Y | |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  "records": [
    {
      'order_id': 10,
      'position_id': 0,
      'market': 'BTCUSD',
      'type': 1,
      'side': 2,
      'target': 2,
      'effect_type': 1,
      'user_id': 10,
      'create_time': 102001.123,
      'update_time': 102003.123,
      'source': 'API',
      'price': '9100.1',
      'amount': '100',
      'taker_fee': '0.005',
      'maker_fee': '-0.002',
      'left': '80',         // Unexecuted Amount
      'deal_stock': '0.9',  // Executed Value
      'deal_fee': '0.01',   // Used Tx Fees
      'leverage': '10',     // Leverage
      'position_type': 1,   // Position Type 1: Isolated Margin 2: Cross Margin
      'stop_id': 0         // Stop Order ID
    },
    ...
  ],
  "offset": 10,
  "limit": 5
}
```

### Query pending stop order

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/stop_pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market, e.g. BTCUSD |
| side | Integer | Y | 0:All 1: Sell, 2: Buy |
| offset | Integer |  Y | Offset, means query from a certain record |
| limit | Integer |  Y | The number of records acquired at a time, the default is 20 and the maximum is 100. |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  "records": [
    {
      'order_id': 10,
      'market': 'BTCUSD',
      'type': 1,
      'side': 2,
      'effect_type': 1, // Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. "GTC Order" is set by default.
      'stop_type': 1,   // Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at
      'user_id': 10,
      'create_time': 102001.123,
      'update_time': 102003.123,
      'source': 'web',
      'state': 1,
      'stop_price': '9200',
      'price': '9100.1',
      'amount': '100',
      'taker_fee': '0.005',
      'maker_fee': '-0.002',
    },
    ...
  ],
  "total": 10,
  "offset": 10,
  "limit": 5
}
```

### Query finished stop order

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/stop_finished
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market, e.g. BTCUSD|
| side | Integer | Y | 0:All 1: Sell, 2: Buy |
| start_time | Integer | N | |
| end_time | Integer | N | |
| offset | Integer | Y | |
| limit | Integer | Y | |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  "records": [
    {
    'order_id': 10,
    'market': 'BTCUSD',
    'type': 1,
    'side': 2,
    'effect_type': 1, // Effect Type, 1: GTC Order, 2: IOC Order, 3: FOK Order. "GTC Order" is set by default.
    'stop_type': 1,   // Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at
    'user_id': 10,
    'create_time': 102001.123,
    'update_time': 102003.123,
    'source': 'web',
    'client_id': 'abc',
    'state': 1,
    'stop_price': '9200',
    'price': '9100.1',
    'amount': '100',
    'taker_fee': '0.005',
    'maker_fee': '-0.002',
    'status': 1 // 1: actived, 2: failed, 3: cancel
    },
    ...
  ],
  "offset": 10,
  "limit": 5
}
```

### Query order status

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/status
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market|
| order_id | Integer | Y | Order ID |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'position_id': 0,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'target': 2,
  'effect_type': 1,
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'API',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'left': '80',         // Unexecuted Amount
  'deal_stock': '0.9',  // Executed Value
  'deal_fee': '0.01',   // Used Tx Fees
  'leverage': '10',     // Leverage
  'position_type': 1,   // Position Type 1: Isolated Margin 2: Cross Margin
  'stop_id': 0,         // Stop Order ID
  'status': "not_deal"  // not_deal: unexecuted; part_deal: partly executed; done: executed; cancel: cancelled;
}
```

### Query stop_order status

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/stop_status
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market|
| order_id | Integer | Y | Order ID |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'order_id': 10,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'effect_type': 1,
  'stop_type': 1,   // Stop Type 1: Trigger at the latest price 2: Trigger at the mark price 3: Trigger at
  'user_id': 10,
  'create_time': 102001.123,
  'update_time': 102003.123,
  'source': 'web',
  'client_id': 'abc',
  'state': 1,
  'stop_price': '9200',
  'price': '9100.1',
  'amount': '100',
  'taker_fee': '0.005',
  'maker_fee': '-0.002',
  'status': "not_deal" //not_deal: unexecuted, activated: active success, fail: active fail, cancel: cancelled;
}
```

# Position api

### Query pending position

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/position/pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | N | Perpetual Market |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|


* Data:

```
"data": [
  {
    'position_id': 1,
    'create_time': 111.11,
    'update_time': 222.11,
    'market': 'BTCUSD',
    'user_id': 2,
    'type': 1, //1: Isolated Margin 2: Cross Margin
    'side': 1, //1: Sell， 2:Buy
    'amount': '100',  // Position Amount
    'amount_max': '120',  // Max. Position Amount
    'close_left': 20,     // Positions left to close
    'open_price': '100',  // Avg. Opening Price
    'open_val': '0.1',    // Cumulative Opening Value
    'open_val_max': '0.2', // Max. Opening Value
    'open_margin': '0.01', // Margin Rate
    'mainten_margin': '0.005', // Maintenance Margin Rate
    'mainten_margin_amount': '0.015', // Maintenance Margin
    'margin_amount': '1.2',  // Margin Amount = Initial Margin + Increased Margin - Transferred Margin
    'profit_real': '0.1',    // Realized PNL
    'profit_clearing': "-1.1", // Unrealized PNL
    'liq_price': '11.22'。     // Forced Liquidation Price, when it is greater than 1000000000000, back to "Infinity"
    'bkr_price': '11',         // Bankruptcy Price, when it is greater than 1000000000000, back to "Infinity"
    'leverage': '10',       // Leverage
    'adl_sort': 100,        // Sort Auto-leveraging
    'total': 10             // Total Holders
  }
]
```

### Query User Funding History

* Request type: GET
* Signature required: Yes
* Request Url: https://api.coinex.com/perpetual/v1/position/funding
* Request:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | |
| start_time | Integer | N | |
| end_time | Integer | N | |
| offset | Integer | Y | |
| limit | Integer | Y | |

* Data:

```
"data": {
  "offset": 10,
  "limit": 100,
  "records": [
    {
      "user_id": 8888,
      "time": 1622548800.916702,
      "market": "BTCUSD",
      "asset": "BTC",
      "type": 1, //1: pay, 2: receive
      "position_id": 1111,
      "side": 1, //1: short position, 2: long position
      "amount": "3500",
      "price": "35000",
      "funding_rate": "0.00175", //funding rate
      "real_funding_rate": "0.00175", //real funding rate
      "funding": "-0.000175",
      "value": "0.1", //position value
    }
       ...
  ]
}
```

### Ajust position margin

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/position/adjust_margin
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | Perpetual Market|
| amount | String | Y | Adjust Amount |
| type | Integer | Y | Adjust Type: 1: Increase Margin, 2: Decrease Margin |
| timestamp | Integer | Y | Timestamp in milliseconds|
| windowtime | Integer | N | Window time in milliseconds|

* Data:

```
"data": {
  'position_id': 1,
  'create_time': 111.11,
  'update_time': 222.11,
  'market': 'BTCUSD',
  'user_id': 2,
  'type': 1, // 1: Isolated Margin, 2: Cross Margin
  'side': 1, //1: Sell, 2:Buy
  'amount': '100',  // Position Amount
  'amount_max': '120',  // Max. Position Amount
  'close_left': 20,     // Positions left to close
  'open_price': '100',  // Avg. Opening Price
  'open_val': '0.1',    // Cumulative Opening Value
  'open_val_max': '0.2', // Max. Opening Value
  'open_margin': '0.01', // Margin Rate
  'mainten_margin': '0.005', // Maintenance Margin Rate
  'mainten_margin_amount': '0.015', // Maintenance Margin
  'margin_amount': '1.2',  // Margin Amount = Initial Margin + Increased Margin - Transferred Margin
  'profit_real': '0.1',    // Realized PNL
  'profit_clearing': "-1.1", // Unrealized PNL
  'liq_price': '11.22'。     //Forced Liquidation Price, when it is greater than 1000000000000, back to "Infinity"
  'bkr_price': '11',         //Bankruptcy Price, when it is greater than 1000000000000, back to "Infinity"
  'leverage': '10',   // Leverage
  'adl_sort': 100,        // Sort Auto-leveraging
  'total': 10             // Total Holders
}
```
