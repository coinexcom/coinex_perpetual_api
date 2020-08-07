# 说明
* **websocket地址是 wss://perpetual.coinex.com/**

* **在一个连接中如果对同一个数据重复订阅，前一个订阅会被取消**

* 请求参数: 
 	1. method: method, String.
	2. params: parameter, Array.
  3. id: Request id, Integer

```
{
    "id": 4,
    "method": "state.subscribe",
    "params": []
}
```

* 返回结果

	1. result: Json object, null for failure.
	2. error: Json objesct, null for success, non-null for failure.
	3. id: Request id, Integer.

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

* **推送**
	
	1. method: method, String
   2. params: parameter, Array
   3. id: Null

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
* params: 见示例
* example:

```
//Request
{
  "method":"server.sign",
  "params": [
    "4DA36FFC61334695A66F8D29020EB589", //access_id
    "3e9e58c40d18358bb129c98139eec99af781275708895e522f572a87dc8d9137", //sign data, 对字符串access_id={access_id}&timestamp={timestamp}&secret_key={secret_key} 做sha256计算，转换为16进制小写，长度为64位
    1513746038205  //timestamp for milliseconds spent from Unix epoch to current time and error between tonce and server time can not exceed plus or minus 1min
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
    "BTCUSD",           // 市场
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
     "funding_time": 10, //距离下次资金费用时间，分钟
     "position_amount": "100", //当前持仓量
     "funding_rate_last": "0.001", //上次资金费用
     "funding_rate_next": "0.001", //预测资金费用
     "insurance": "1000", //当前保险基金
     "sign_price": "100", //标记价格
     "index_price": "200", //指数价格
     "sell_total": "", //过去1000笔成交中卖的数量
     "buy_total": "" //过去1000笔成交中买的数量
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
           "funding_time": 10, //距离下次资金费用时间，分钟
           "position_amount": "100", //当前持仓量
           "funding_rate_last": "0.001", //上次资金费用
           "funding_rate_next": "0.001", //预测资金费用
           "insurance": "1000", //当前保险基金
           "sign_price": "100", //标记价格
           "index_price": "200", //指数价格
           "sell_total": "", //过去1000笔成交中卖的数量
           "buy_total": "" //过去1000笔成交中买的数量
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
    20,                 //limit int, [5, 10, 20, 50, 100]中的其中一个
    "0"                 //interval String ["10", "1", "0", "0.1", "0.01"]的其中一个 
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
    60                     //second for each cycle now supports: 1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week.
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
        'left': '80',         //未成交数量
        'deal_stock': '0.9',  //已成交的价值
        'deal_fee': '0.01',   //已成交手续费
        'leverage': '10',     //杠杆
        'position_type': 1   //仓位类型 1:逐仓 2:全仓
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
        'last_deal_amount': '100', //最新成交数量
        'last_deal_price': '1000', //最新成交价格
        'left': '80',         //未成交数量
        'deal_stock': '0.9',  //已成交的价值
        'deal_fee': '0.01',   //已成交手续费
        'leverage': '10',     //杠杆
        'position_type': 1   //仓位类型 1:逐仓 2:全仓
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
          "available": "250", // 可用余额
          "frozen": "10",    // 冻结
          "tranfer": "10",   // 可转
          "balance_total": "11", // 账户余额
          "margin", "10" // 保证金
    },
    "BTC":{
          "available": "250", // 可用余额
          "frozen": "10",    // 冻结
          "tranfer": "10",   // 可转
          "balance_total": "11", // 账户余额
          "margin", "10" // 保证金
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
          "available": "250", // 可用余额
          "frozen": "10",    // 冻结
          "tranfer": "10",   // 可转
          "balance_total": "11", // 账户余额
          "margin", "10" // 保证金
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
      'type': 1, //1:逐仓, 2:全仓
      'finish_type': 2,
      'side': 1, //1:空仓, 2:多仓
      'sys': 0,
      'amount': '100', 仓位数量
      'amount_max': '120', // 历史最大仓位数
      'close_left': 20, //剩余可平
      'open_price': '100', //开仓均价
      'open_val': '0.1', // 累计开仓价值即仓位价值
      'open_val_max': '0.2', // 历史最大开仓价值
      'open_margin': '0.01', // 开仓保证金率
      'open_margin_imply': '0',
      'mainten_margin': '0.005', // 维持保证金率
      'mainten_margin_amount': '0.015', //维持保证金数
      'margin_amount': '1.2',  //保证金
      'profit_real': '0.1', // 已实现盈亏
      'profit_clearing': "-1.1", // 待结算盈亏
      'adl_sort_val': '1.1', // 自动减仓排序指标
      'liq_time': 111.11,
      'liq_order_time': 222.22,
      'liq_amount': '10', //强平仓位数
      'liq_profit': '0.1', // 强平产生的盈亏
      'liq_order_price': '11.11', 
      'liq_price': '11.22' // 强平价格
      'liq_price_imply': '0',
      'bkr_price': '11', // 破产价格
      'bkr_price_imply': '0',
      'leverage': '10', //当前杠杆
      'adl_sort': 100, // 自动减仓排序
      'total': 10 // 仓位总数
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
