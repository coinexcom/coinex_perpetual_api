# API Invocation Instruction
* **websocket url wss://perpetual.coinex.com/**

* **If you repeat a subscription to the same data in a connection, the previous subscription will be cancelled**

* Request Parameters: 
 	1. method: method, String.
	2. params: parameter, Array.
  3. id: Request id, Integer

> Request Demo: 

```
{
    "id": 4,
    "method": "state.subscribe",
    "params": []
}
```

* Response

	1. result: Json object, null for failure.
	2. error: Json objesct, null for success, non-null for failure.
	3. id: Request id, Integer.

> Response Demo:

```
//success
{
    "error": null,
    "id": 4,
    "result": "success"
}

//success with result
{
    "error": null
    "id": 4,
    "result": {

    }
}

//error
{
    "error": {
        "code": 1,
        "message": ""
    },
    "id": 4,
    "result": null
}

```

* **Push**
	
	1. method: method, String
  2. params: parameter, Array
  3. id: Null

> Push Demo:

```
{
    "id": null,
    "method": "state.update",
    "params": [

    ]
}
```

# Server Api

## Server Sign

* method: "server.sign"
* params: 
  1. access_id
  2. sign data, use sha256 algorithm to encrypt the signature string access_id={access_id}&timestamp={timestamp}&secret_key={secret_key} and convert encrypted string to 64 lowercase characters.
  3. timestamp, the timestamp is in milliseconds and the difference between the timestamp and the server timestamp should not be greater than 1 minute.
* example:

> Authorization Demo:

```
//Request
{
  "method":"server.sign",
  "params": [
    "4DA36FFC61334695A66F8D29020EB589", //access_id
    "3e9e58c40d18358bb129c98139eec99af781275708895e522f572a87dc8d9137", //sign data
    1513746038205  //timestamp
  ],
  "id": 15,
 }

//Response
{
  "error": null,
  "result": {
    "status": "success"
  },
  "id": 15
}
```

## Server Ping

* method: "server.ping"
* params: empty
* example:

```
//Request
{
  "method":"server.ping",
  "params":[],
  "id": 11
}

//Response
{
  "error": null,
  "result": "pong",
  "id": 11
}
```

## Server Time

* method: "server.time"
* params: empty
* example:

```
//Request
{
  "method":"server.time",
  "params":[],
  "id": 11
}

//Response
{
  "error": null,
  "result": 1493285895, // timestamp seconds
  "id": 11
}
```

# Market API

## Market status API

* Acquire market status

```
//Request
{
  "method":"state.query",
  "params":[
    "BTCUSD",           // Market
     86400,             // cycle period，Integer, e.g. 86400 for last 24 hours
  ],
  "id":15
}

//Response
{
  "error": null, 
  "result": {
     "close":"430.33", //close price
     "deal":"1574489.5181782117",  //value
     "high":"445.68", //highest price
     "last":"430.33", //latest price
     "low":"420.32",  //lowest price
     "open":"434.11", //open price
     "period":86400,  //cycle period
     "volume":"3624.85992531" //volume
     "funding_time": 10, //xx mins before next funding time
     "position_amount": "100", //current positions
     "funding_rate_last": "0.001", //last funding rate
     "funding_rate_next": "0.001", //estimated funding rate
     "insurance": "1000", //current insurance fund
     "sign_price": "100", //signed price
     "index_price": "200", //index price
     "sell_total": "", //total selling in 1000 executed deals
     "buy_total": "" // total buying in 1000 executed deals
  },
  "id": 15
 }
```

* Subscribe market 24H status

```
//Request
{
  "method":"state.subscribe",
  "params":[
      "BTCUSD".   #1.empty for subscribe all
  ],
  "id":15
}

//notify
{
  "method": "state.update", 
  "params": [
       {
        "BTCUSD": {
          "close":"430.33", //close price
          "deal":"1574489.5181782117",  //value
          "high":"445.68", //highest price
          "last":"430.33", //latest price
          "low":"420.32",  //lowest price
          "open":"434.11", //open price
          "period":86400,  //cycle period
          "volume":"3624.85992531" //volume
          "funding_time": 10, //xx mins before next funding time
          "position_amount": "100", //current positions
          "funding_rate_last": "0.001", //last funding rate
          "funding_rate_next": "0.001", //estimated funding rate
          "insurance": "1000", //current insurance fund
          "sign_price": "100", //signed price
          "index_price": "200", //index price
          "sell_total": "", //total selling in 1000 executed deals
          "buy_total": "" // total buying in 1000 executed deals
        },
    }
  ], 
  "id": 15
}
```
 
## Market depth API

* Acquire market depth

```
//Request
{
  "method":"depth.query",
  "params":[
    "BTCUSD",           //market
    20,                 //limit, Int, one of the following: [5, 10, 20, 50, 100]
    "0"                 //interval, String one of the following: ["10", "1", "0", "0.1", "0.01"]
  ],
  "id":15
}

//Response
{
  "error": null, 
  "result": {
    "bids": [          //Depth of Buy
      [
        "12.25",       //Buy in price
        "0.0588"       //Buy in count
      ]
    ],
    "asks": [          //Depth of Sell
      [
        "12.94",       //Sell out price
        "0.1524"       //Sell out count
      ]
    ]，
    "last": "3740",
    "time": 111111,
    "sign_price": "3750",
    "index_price": "3750"
  },
  "id": 15
 }
```

* Subscribe market depth

```
//Request
{
  "method":"depth.subscribe",
  "params":[
    "BTCBCH",               #1.market: See<API invocation description·market> 
    5,                      #2.limit: Count limit
    "0"                     #3.interval: Merge，String
  ],
  "id":15
}

//notify
{
  "method": "depth.update", 
  "params": [
    false,                 //Boolean, true: for complete result，false: for update based on latest retrun result
    {                       //Update info
        "bids": [          //Depth of Buy
          [
            "12.25",       //Buy in price
            "0.0588"       //Buy in count
          ]
        ],
        "asks": [          //Depth of Sell
          [
            "12.94",       //Sell out price
            "0.1524"       //Sell out count
          ]
        ]，
        "last": "3740",
        "time": 111111,
        "sign_price": "3750",
        "index_price": "3750"
    }
  ], 
  "id": null
}
```

## Latest executed deal API

* Acquire latest executed deal list

```
//Request
{
  "method":"deals.query",
  "params":[
    "BTCUSD",                       //market 
    "10",                           //limit
    "0"                             //last_id:largest ID of last returned result
  ],
  "id":16
}

//Response
{
  "error": null, 
  "result": [
    {
      "type": "sell",            //deal type
      "time": 1496458040.059284, //deal time
      "price": "17868.41",       //deal price
      "id": 29433,               //deal no.
      "amount": "10"             //deal count
    }
  ],
  “id": 16
}
```

* Subscribe latest executed deal list

```
// Request
{
  "method":"deals.subscribe",
  "params":[
    "BTCBCH"                        //market
  ],
  "id":16
}

// Notify
{
  "method": "deals.update", 
  "params": [
    "BTCUSD",                        //market 
    [
      {
        "type": "sell",             //deal type
        "time": 1496458040.059284,  //deal time  
        "price": "17868.41",        //deal price
        "id": 29433,                //deal no.
        "amount": "0.0281"          //deal count
      }
    ]
  ], 
  "id": null
}
```

## KLine

* Acquire K line data

```
// Request
{
  "method":"kline.query",
  "params":[
    "BTCUSD",              // market
    60                     //second for each cycle now supports: 1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week.
    1629375022,            // start timestamp
    1629720622             // end timestamp
  ],
  "id": 5
}

// Response
{
  "error": null, 
  "result": [
    [
      1496458500,  // time 
      "16.65",     // opening
      "11.57",     // closing
      "17.65",     // highest
      "10.57",     // lowest
      "1862"       // volume
    ]
  ],
  "id": 5
}
```

* Subscribe Kline data

```
// Request
{
  "method":"kline.subscribe",
  "params":[
    "BTCUSD",              // market
    60                     // second for each cycle now supports: 1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week.
  ],
  "id": 5
}

// Notify
{
  "method": "kline.update", 
  "params":[
    [
      1496458500,  // time
      "16.65",     // opening
      "11.57",     // closing
      "17.65",     // highest
      "10.57",     // lowest
      "1862"       // volume
    ]
  ],
  "id": null
}
```


## Order API

**need auth, see server.sign**

* Query Order

```
// Request
{
  "method":"order.query",
  "params":[
    "BTCUSD",  // market
    0,         // side, 0 no limit, 1 sell, 2 buy
    0,         // ofsset
    10         // limit
  ],
  "id":15
}

// Response
{
  "error": null, 
  "result": {
    "limit": 10,
    "offset": 0,
    "total": 1,
    "records": [
      {
        'order_id': 10,
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
        'left': '80',         // unexecuted amount
        'deal_stock': '0.9',  // executed value
        'deal_fee': '0.01',   // executed tx fees
        'leverage': '10',     // leverage
        'position_type': 1    // position type 1: isolated margin 2: cross margin
      }
    ]
  },
  "id": 15
 }
```

* Subscribe Order

```
// Request
{
  "method":"order.subscribe",
  "params":["BTCUSD"], // market list
  "id":15
}

// Notify
{
  "method": "order.update", 
  "params": [
      3,      // event: event type，Integer, 1: PUT, 2: UPDATE, 3: FINISH
      {
        'order_id': 10,
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
        'last_deal_amount': '100', // latest deal volumn
        'last_deal_price': '1000', // latest deal price
        'left': '80',         // unexecuted amount
        'deal_stock': '0.9',  // executed value
        'deal_fee': '0.01',   // executed tx fees
        'leverage': '10',     // leverage
        'position_type': 1,   // position type 1: isolated margin 2: cross margin
        'last_deal_id': 1,    // latest deal id
        'last_deal_time': 1220003, // latest deal time
        'last_deal_type': 1,
        'last_deal_role': 1   // 1 maker, 2 taker
     }
  ], 
  "id": null
}
```

# Asset API

**need auth, see server.sign**

* Acquire Asset

```
// Request
{
  "method":"asset.query",
  "params":["BTC","ETH"], # asset list, empty for inquire all
  "id":15
}

// Response
{
  "error": null, 
  "result": {
    "BCH": {
          "available": "250", // available balance
          "frozen": "10",     // frozen
          "tranfer": "10",    // transferable
          "balance_total": "11", // account balance
          "margin", "10" // margin
    },
    "BTC":{
          "available": "250", // available balance
          "frozen": "10",     // frozen
          "tranfer": "10",    // transferable
          "balance_total": "11", // account balance
          "margin", "10" // margin
    }
  },
  "id": 15
}
```

* Subscribe Asset

```
//Request

{
  "method":"asset.subscribe",
  "params":["BTC"], # asset list
  "id":15
}

//notify
{
  "method": "asset.update", 
  "params": [
    {
      "BCH": {
          "available": "250", // available balance
          "frozen": "10",     // frozen
          "tranfer": "10",    // transferable
          "balance_total": "11", // account balance
          "margin", "10" // margin
      }
    }
  ], 
  "id": null
}
```

# Position API

**need auth, see server.sign**

* position query

```
//Request
{
  "method":"position.query",
  "params":["BTCUSD"]  //market list, empty for inquire all
  "id":15
}

//Response
{
  "error": null, 
  "result": {
    {
      //position detail
      'position_id': 1,
      'create_time': 111.11,
      'update_time': 222.11,
      'market': 'BTCUSD',
      'user_id': 2,
      'type': 1, //1: Isolated Margin, 2: Cross Margin
      'finish_type': 2,
      'side': 1, //1:Sell, 2:Buy
      'sys': 0,
      'amount': '100', // position amount
      'amount_max': '120', // Max. Position Amount
      'close_left': 20, // Positions left to close
      'open_price': '100', // Avg. Opening Price
      'open_val': '0.1', // Cumulative Opening Value
      'open_val_max': '0.2', // Max. Opening Value
      'open_margin': '0.01', // Margin Rate
      'open_margin_imply': '0',
      'mainten_margin': '0.005', // Maintenance Margin Rate
      'mainten_margin_amount': '0.015', // Maintenance Margin Amount
      'margin_amount': '1.2',  // Margin Amount
      'profit_real': '0.1', // Realized PNL
      'profit_clearing': "-1.1", // Unrealized PNL
      'adl_sort_val': '1.1', // Sort Auto-leveraging 
      'liq_time': 111.11,
      'liq_order_time': 222.22,
      'liq_amount': '10',  // Forced Liquidation Amount
      'liq_profit': '0.1', // Forced Liquidation PNL
      'liq_order_price': '11.11', 
      'liq_price': '11.22' // Forced Liquidation Price
      'liq_price_imply': '0',
      'bkr_price': '11', // Bankruptcy Price
      'bkr_price_imply': '0',
      'leverage': '10', // Current Leverage
      'total': 10 // Total Positions': '100', Position Amount
    },
    {
      //position detail
    }
  },
  "id": 15
}
```

* Subscribe position

```
//Request
{
  "method":"position.subscribe",
  "params":["BTCUSD"], # market list
  "id":15
}

//Notify
{
  "method": "position.update", 
  "params": [
    {
        //position detail
    }
  ], 
  "id": null
}
```
