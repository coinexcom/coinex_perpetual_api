# 鉴权：
1.http报文的输入的参数字符串如下：
market=BTCUSD&type=buy&price=680&amount=1.0&time=1550743431000

2.在上面最后拼接secret_key得到如下：
market=BTCUSD&type=buy&price=680&amount=1.0&time=1550743431000&secret_key=B51068CF10B34E7789C374AB932696A05E0A629BE7BFC62F 
备注：发送http报文体不需要带上secret_key参数，该步骤只是为了计算sha256签名。

3.对上面字符串进行sha256即签名，转换为16进制小写，长度为64位，再把这个签名加入到http的头中如下：  
Authorization: 3e9e58c40d18358bb129c98139eec99af781275708895e522f572a87dc8d9137

4.在http的头中增加AccessId,服务端根据AccessId寻找对应的用户信息
AccessId: 4DA36FFC61334695A66F8D29020EB589

5.服务端收到http报文后，根据AccessId找到用户的secret key，进行上面同样的操作，判断收到的签名与自己计算的签名是否相等，如果相等则鉴权成功，否则失败。 

# 时间戳验证：
*服务器收到请求时会判断请求中的时间戳timestamp，如果是5000毫秒之前发出的，则请求会被认为无效。这个时间窗口值可以通过发送可选参数recvWindow来自定义。

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒 |
| windowtime | Integer | N | 时间窗口，单位：毫秒 | 

# 请求报文：
**GET类请求**

```
http://api.coinex.com/perpetual/v1/market/depth?market=BTCUSD&merge=1
```

**POST类请求**

```
http://api.coinex.com/perpetual/v1/order/put_limit

请求参数以application/x-www-form-urlencoded的方式放入http body中
```

# 响应报文体：

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

**Ping**

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/ping
* Params: none
* Data:

```
"data": "pong"
```

**System Time**

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/time
* Params: none
* Data:

```
"data": 11111123455 // millisecond
```
# Market Api
 
**Market List**

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/list
* Params: none
* Data:

```
'data': [
  {
    'name': 'BTCUSD',
    'type': 1, // 1: 正向合约, 2: 反向合约
    'stock': 'BTC',
    'money': 'USD',
    'fee_prec': 4,
    'stock_prec': 8,
    'money_prec': 8,
    'multiplier': 1,
    'amount_prec': 0,
    'amount_min': '10',
    'tick_size': '0.5', //价格最小增量
    'leverages': ["3", "5", "8", "10", "15", "20", "30", "50", "100"]
  }
]
```

**Market Limit config**
 
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

**Market Ticker**

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

**Market Ticker All**

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

**Market Depth**

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/depth
* Params: 

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场，例如：“BTCUSD”合约市场 |
| merge | String | Y | 精度合并，取值为：["10", "1", "0", "0.1", "0.01"]中的其中一个 |
| limit | Integer | Y | 获取的条数，取值为：[5, 10, 20, 50, 100]中的其中一个 |

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

**Market deals**

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

**Market Funding History**

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

**User deals**

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
      'margin_amount': '220', //成交后的仓位保证金
      'leverage': '10',
      'deal_stock': '0.222',
      'deal_fee': '0.001',
      'deal_margin': '20', //交易的保证金
      'fee_rate': '0.02',
      'deal_profit': '100',      
      'deal_insurance': '0.004' // 消耗或增加的保险基金
    }
      ...
  ]
}
```

**Market Kline**

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/perpetual/v1/market/kline
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| limit | Integer | N | 获取K线数量，不能超过1000，默认为1000|
| type | String | Y | K线信息类别，支持如下参数，1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week|

* Data:

```
"data": [
  [
    1440308700,    # 时间
    233.37,        # 开盘价
    233.48,        # 收盘价
    243.37,        # 最高价
    223.48,        # 最低价
    52，           # 交易量
    22.2810015     # 交易额
    "BTCUSD"     # 市场名
  ],
  [
    1440308701,   # 时间
    233.31,       # 开盘价
    233.41,       # 收盘价
    243.31,       # 最高价
    223.41,       # 最低价
    51，          # 交易量
    21.2810015    # 交易额
    "BTCUSD"    # 市场名
  ]
]
```

**Ajust leverage**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/market/adjust_leverage
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场|
| leverage | String | Y | 可取的值: |
| position_type | Integer | Y | 1 逐仓 2 全仓|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": {
  "position_type": 1, //仓位类型
  "leverage": "10"    //杠杆
}
```

**Get position amount**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/market/position_expect
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场|
| price | String | Y | 价格 |
| side | Integer | Y | 1 卖 2 买|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": {
  "position_expect": "10"    //预计可开仓位数
}
```


## Asset Api

**asset query**

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/asset/query
* Params: None
* Data:

```
"data": {
  "BTC": {
    "available": "250", // 可用余额
    "frozen": "10",    // 冻结
    "tranfer": "10",   // 可转
    "balance_total": "11", // 账户余额
    "margin", "10", // 保证金
    "profit_unreal": "100" //未实现盈亏
  },
  "ETH": {
    "available": "250", // 可用余额
    "frozen": "10",    // 冻结
    "tranfer": "10",   // 可转
    "balance_total": "11", // 账户余额
    "margin", "10",// 保证金
    "profit_unreal": "100" //未实现盈亏
  }
}
```


## Order Api

**Put limit order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y |  |
| side | Integer | Y | 1 sell, 2 buy |
| amount | String | Y | 委托数量 |
| price | String | Y | 委托价格 |
| effect_type | Integer | N | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| option | Integer | N | 选项, 1:只下maker单。默认为0 |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| client_id | String | N | 自定义id,限长64个字节,有效字符为大小写英文字母，数字, _ -|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
}
```

**Put market order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_market
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| side | Integer | Y | 委托类型 1表示卖空，2表示买多|
| amount | String | Y | 委托数量 |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| client_id | String | N | 自定义id,限长64个字节,有效字符为大小写英文字母，数字, _ -|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
}
```

**Put stop limit order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_stop_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| side | Integer | Y | 委托类型 1表示卖空，2表示买多|
| stop_type | Integer | Y | 触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发|
| amount | String | Y | 委托数量 |
| stop_price | String | Y | 触发价格 |
| price | String | Y | 委托价格 |
| effect_type | Integer | N | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| option | Integer | N | 选项, 1:只下maker单。默认为0 |
| client_id | String | N | 自定义id,限长64个字节,有效字符为大小写英文字母，数字, _ -|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": "success"
```

**Put stop market order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/put_stop_market
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| side | Integer | Y | 委托类型 1表示卖空，2表示买多|
| stop_type | Integer | Y | 触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发|
| amount | String | Y | 委托数量 |
| stop_price | String | Y | 触发价格 |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| client_id | String | N | 自定义id,限长64个字节,有效字符为大小写英文字母，数字, _ -|
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Data:

```
"data": "success"
```

**Cancel pending order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| order_id | Integer | Y | 未完成订单ID |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
}
```

**Cancel all pending order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_all
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": "success"
```

**Cancel pending stop order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_stop
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| order_id | Integer | Y | 未完成订单ID |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": {
  'order_id': 10,
  'market': 'BTCUSD',
  'type': 1,
  'side': 2,
  'effect_type': 1, // 有效时间 1: 长效单, 2: 立即成交或取消, 3:全部成交或取消
  'stop_type': 1,   // 触发方式 1: 最新成交价, 2: 指数价, 3: 标记价格
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

**Cancel all pending stop order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/cancel_stop_all
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场 |
| side | Integer | N | 订单类型 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": "success"
```

**Query pending order**

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场，例如BTCUSD |
| side | Integer | Y | 0:全部 1:卖, 2: 买 |
| offset | Integer |  Y | 偏移量，即从哪条开始获取 |
| limit | Integer |  Y | 一次获取记录数，默认为20条，最大为100条 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
      'left': '80',         //未成交数量
      'deal_stock': '0.9',  //已成交的价值
      'deal_fee': '0.01',   //已使用手续费
      'leverage': '10',     //杠杆
      'position_type': 1   //仓位类型 1:逐仓 2:全仓
    },
    ...
  ],
  "total": 10,
  "offset": 10,
  "limit": 5
}
```

**Query finished order**

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
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
      'left': '80',         //未成交数量
      'deal_stock': '0.9',  //已成交的价值
      'deal_fee': '0.01',   //已使用手续费
      'leverage': '10',     //杠杆
      'position_type': 1   //仓位类型 1:逐仓 2:全仓
    },
    ...
  ],
  "offset": 10,
  "limit": 5
}
```

**Query pending stop order**

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/stop_pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场，例如BTCUSD |
| side | Integer | Y | 0:全部 1:卖, 2: 买 |
| offset | Integer |  Y | 偏移量，即从哪条开始获取 |
| limit | Integer |  Y | 一次获取记录数，默认为20条，最大为100条 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": {
  "records": [
    {
      'order_id': 10,
      'market': 'BTCUSD',
      'type': 1,
      'side': 2,
      'effect_type': 1, // 有效时间 1: 长效单, 2: 立即成交或取消, 3:全部成交或取消
      'stop_type': 1,   // 触发方式 1: 最新成交价, 2: 指数价, 3: 标记价格
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

**Query order status**

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/status
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场|
| order_id | Integer | Y | 订单id |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
  'status': "not_deal" //not_deal: unexecuted; part_deal: partly executed; done: executed; cancel: cancelled;
}
```

**Put limit close order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/close_limit
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| position_id | Integer | Yes | 仓位ID |
| amount | String | Yes | 平仓数量 |  |
| price | String | Yes | 价格 |
| effect_type | Integer | No | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| option | Integer | N | 选项, 1:只下maker单。默认为0 |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
}
```

**Put market close order**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/order/close_market
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| position_id | Integer | Yes | 仓位ID |
| use_cet | Integer | N | 是否使用cet抵扣手续费 1: 使用, 0: 不使用。默认为0|
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

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
  'left': '80',         //未成交数量
  'deal_stock': '0.9',  //已成交的价值
  'deal_fee': '0.01',   //已使用手续费
  'leverage': '10',     //杠杆
  'position_type': 1   //仓位类型 1:逐仓 2:全仓
}
```

## Position api

**Query pending position**

* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/position/pending
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | N | 合约市场 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": [
  {
    'position_id': 1,
    'create_time': 111.11,
    'update_time': 222.11,
    'market': 'BTCUSD',
    'user_id': 2,
    'type': 1, //1: 逐仓， 2:全仓
    'side': 1, //1: 空仓， 2:多仓
    'amount': '100',  //仓位数量
    'amount_max': '120',  //历史最大仓位数量
    'close_left': 20,     //剩余可平
    'open_price': '100',  //平均开仓价格
    'open_val': '0.1',    //累计开仓价值
    'open_val_max': '0.2', //最大开仓价值
    'open_margin': '0.01', //保证金率
    'mainten_margin': '0.005', //维持保证金率
    'mainten_margin_amount': '0.015', //维持保证金
    'margin_amount': '1.2',  //保证金 起始保证金 + 追加保证金 - 转出保证金
    'profit_real': '0.1',    //已实现盈亏
    'profit_clearing': "-1.1", //待结算盈亏
    'liq_price': '11.22'。     //强平价格 当强平价格大于1000000000000时，返回"Infinity"
    'bkr_price': '11',         //破产价格 当破产价格大于1000000000000时，返回"Infinity"
    'leverage': '10',       //杠杆
    'adl_sort': 100,        //自动减仓排序
    'total': 10             //持仓人数
  }
]
```

**Ajust position margin**

* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"AccessId": "xxx"
* Request Url: https://api.coinex.com/perpetual/v1/position/adjust_margin
* Params:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Y | 合约市场|
| amount | String | Y | 调整额度 |
| type | Integer | Y | 调整类型：1表示增加保证金，2表示减少保证金 |
| timestamp | Integer | Y | 客户端时间戳，单位：毫秒|
| windowtime | Integer | N | 时间窗口，单位：毫秒|

* Data:

```
"data": {
  'position_id': 1,
  'create_time': 111.11,
  'update_time': 222.11,
  'market': 'BTCUSD',
  'user_id': 2,
  'type': 1, //1: 逐仓， 2:全仓
  'side': 1, //1: 空仓， 2:多仓
  'amount': '100',  //仓位数量
  'amount_max': '120',  //历史最大仓位数量
  'close_left': 20,     //剩余可平
  'open_price': '100',  //平均开仓价格
  'open_val': '0.1',    //累计开仓价值
  'open_val_max': '0.2', //最大开仓价值
  'open_margin': '0.01', //保证金率
  'mainten_margin': '0.005', //维持保证金率
  'mainten_margin_amount': '0.015', //维持保证金
  'margin_amount': '1.2',  //保证金 起始保证金 + 追加保证金 - 转出保证金
  'profit_real': '0.1',    //已实现盈亏
  'profit_clearing': "-1.1", //待结算盈亏
  'liq_price': '11.22'。     //强平价格， 当强平价格大于1000000000000时，返回"Infinity"
  'bkr_price': '11',         //破产价格, 当破产价格大于1000000000000时，返回"Infinity"
  'leverage': '10',   //杠杆
  'adl_sort': 100,        //自动减仓排序
  'total': 10             //持仓人数
}
```
