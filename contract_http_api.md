# 一. api鉴权：
*1.http报文的输入的参数字符串如下：
market=BTCBCH&type=buy&price=680&amount=1.0&time=1550743431

*2.在上面最后拼接secret_key得到如下：
market=BTCBCH&type=buy&price=680&amount=1.0&time=1550743431&secret_key=B51068CF10B34E7789C374AB932696A05E0A629BE7BFC62F 
备注：发送http报文体不需要带上secret_key参数，该步骤只是为了计算sha256签名。

*3.对上面字符串进行sha256即签名，转换为16进制小写，长度为64位，再把这个签名加入到http的头中如下：  
Authorization:3e9e58c40d18358bb129c98139eec99af781275708895e522f572a87dc8d9137

*4.在http的头中增加Access_id,服务端根据Access_id寻找对应的用户信息
Access_id=4DA36FFC61334695A66F8D29020EB589

*4.服务端收到http报文后，根据Access_id找到用户的secret_key，进行上面同样的操作，判断收到的签名与自己计算的签名是否相等，如果相等则鉴权成功，否则失败。 

# 二. 时间戳验证：
*服务器收到请求时会判断请求中的时间戳timestamp，如果是5000毫秒之前发出的，则请求会被认为无效。这个时间窗口值可以通过发送可选参数recvWindow来自定义。

* timestamp  | Integer | 必选字段 | 客户端时间戳，单位：毫秒|
* windowtime | Integer | 可选字段 | 时间窗口，单位：毫秒|


# 三. 响应报文体：
* {"code": 0, "data": null, "message": "ok"}
* code为0表示成功，其他表示失败；
* data表示需要返回的数据；
* message为"ok"表示成功，其他表示错误原因；


# 四. api接口：
* 请求参数说明：required为Yes:表示必选参数，为No表示可选参数

## 1. ping

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/ping
* Example

```
# Request
GET https://api.coinex.com/contract/v1/ping

# Response
{
  "code": 0,
  “data”: "pong",
  "message": "ok"
}

```

## 2. 获取服务器时间戳

* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/time
* Example

```
# Request
GET https://api.coinex.com/contract/v1/time

# Response
{
  "code": 0,
  “data”: 1550735154, #服务端系统时间戳
  "message": "ok"
}

```

## 3. 获取合约市场列表
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/list
* Return value description:

| name | type | description |
| ------ | ------ | ------ |
| name | String | 市场名 |
| stock | String| 基础货币 |
| money | String| 计价货币 |
| fee_prec | String| 费率精度 |
| stock_prec | String| 基础货币精度 |
| money_prec | String| 计价货币精度 |
| multiplier | String| 合约乘数，一般为1|


* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/list

# Response
{
	"code": 0,
	"data": [{
		"name": "BTCUSD",
		"stock": "BTC",
		"money": "USD",
		"fee_prec": 4,
		"stock_prec": 8,
		"money_prec": 6,
		"multiplier": "1"
	}, {
		"name": "BCHUSD",
		"stock": "BCH",
		"money": "USD",
		"fee_prec": 4,
		"stock_prec": 8,
		"money_prec": 6,
		"multiplier": "1"
	}, {
		"name": "ETHUSD",
		"stock": "ETH",
		"money": "USD",
		"fee_prec": 4,
		"stock_prec": 8,
		"money_prec": 6,
		"multiplier": "1"
	}],
	"message": "ok"
}

```

## 4. 获取合约状态数据
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/state
* Request parameter: 

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场，例如：BTCUSD合约市场 |
| period | Integer | No | 查看周期，单位秒，默认为86400，最大不超过86400 * 3 |

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| market | String | 合约市场，原样返回 |
| period | Integer | 查看周期，原样返回 |
| sign_price | String | 最新标记价 |
| index_price | String | 最新指数价 |
| last | String | 最新成交价 |
| open | String | 开盘价 |
| close | String | 收盘价 |
| high | String | 最近24小时最高价 |
| low | String | 最近24小时最低价 |
| vol | String | 最近24小时成交量 |
| deal | String | 最近24小时成交量额|
| funding_rate | String | 最近一次资金费率 |
| rest_time | Integer | 资金费率倒计时，单位：分钟 |
| insurance | String | 保险基金余额 |

* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/state?market=BTCUSD
# Response
{
  "code": 0,
  “data”:
  {
    "market": "BTCUSD",
    "period": 86400,
    "insurance": "0",
    "deal": "87497920.57",
    "last": "3985",
    "rest_time": 455,
    "index_price": "3964.01",
    "funding_rate": "-0.00070866",
    "high": "3985",
    "vol": "22383",
    "low": "3909.09",
    "sign_price": "3961.34",
    "close": "3985",
    "open": "3909.09"	
  },
  "message": "ok"
}
```

## 5. 获取合约深度
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/depth
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场，例如：“BTCUSD”合约市场 |
| merge | String | Yes | 精度合并，取值为：["0", "0.1", "0.01"]中的其中一个 |
| limit | Integer | Yes | 获取的条数，取值为：[5, 10, 20, 50]中的其中一个 |

* Return value description:

| name | type | description |
| ------ | ------ | ------ |
| last | String | 最新价格 |
| asks | Array | 卖出深度 |
| asks[0][0] | String | 合约价格 |
| asks[0][1] | String | 合约数量 |
| bids | Array | 买入深度 |
| bids[0][0] | String | 合约价格 |
| bids[0][1] | String | 合约数量 |

* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/depth?market=BTCUSD&merge=0&limit=20

# Response
{
	"code": 0,
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
		"last": "3740"
	},
	"message": "ok"
}

```

## 6. 获取合约最近交易
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/deals
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约名称 |
| last_id | Integer |  yes | 获取交易id大于last_id的数据 |

* Return value description:

| name | type | description |
| ------ | ------ | ------ |
| id | Integer | 交易id |
| time | Long | 交易时间，单位：秒 |
| price | String | 交易价格 |
| amount | String | 交易数量 |
| type | Integer | 1: 卖，2: 买 |

* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/deals?market=BTCUSD&last_id=1111

# Response   //每次最多获取100条最近交易信息
{
  "code": 0,
  "data":
  [
      {
	       "price": "3740",
	       "id": 579,
	       "amount": "1",
	       "time": 1550738642.9848311,
	       "type": 2
      }, 
      {
	       "price": "3700",
	       "id": 573,
	       "amount": "1",
	       "time": 1550738021.0449791,
	       "type": 1
       }
  ],
  "message": "ok"
}
```

## 7. 获取合约k线信息
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/kline
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| limit | Integer | No | 获取K线数量，不能超过1000，默认为1000|
| type | String | Yes | K线信息类别，支持如下参数，1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week|

* Return value description:

| name | type | description |
| ------ | ------ | ------ |
| data[0][0] | String | K线时间 |
| data[0][1] | String | 开盘价 |
| data[0][2] | String | 收盘价 |
| data[0][3] | String | 最高价 |
| data[0][4] | String | 最低价 |
| data[0][5] | String | 交易量 |
| data[0][6] | String | 交易额 |
| data[0][7] | String | 市场名 |

* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/kline?market=BTCUSD&type=1min&limit=500 //表示获取500条k线数据，
每条数据为1min类型k线数据

# Response
{
  "code": 0,
  "message": "Ok",
  "data":
  [
    [
      1440308700,    # 时间
      233.37,        # 开盘价
      233.48,        # 收盘价
      243.37,        # 最高价
      223.48,        # 最低价
      52，           # 交易量
      22.2810015     # 交易额
      "BTCUSD"		 # 市场名
    ],
    [
      1440308701,   # 时间
      233.31,       # 开盘价
      233.41,       # 收盘价
      243.31,       # 最高价
      223.41,       # 最低价
      51，          # 交易量
      21.2810015    # 交易额
      "BTCUSD"		# 市场名
    ]
  ]
}
```

## 8. 获取风险限额配置  
* Request type: GET
* Signature required: No
* Request Url: https://api.coinex.com/contract/v1/market/risk_config
* Request parameter: No request params
* Return value description: 列表参数为：风险限额， 起始保证金率，维持保证金率
* Example

```
# Request
GET https://api.coinex.com/contract/v1/market/risk_config

# Response
{
  "code": 0,
	"data": 
	{
		"BTCUSD": [
			["200", "0.01", "0.005"], //分别为风险限额，起始保证金率，维持保证金率
			["500", "0.02", "0.01"],
			["1000", "0.03", "0.015"],
			["2000", "0.04", "0.02"]
		],
		"BCHUSD": [
			["200", "0.01", "0.005"],
			["500", "0.02", "0.01"],
			["1000", "0.03", "0.015"],
			["2000", "0.04", "0.02"]
		],
		"ETHUSD": [
			["1000", "0.01", "0.005"],
			["2500", "0.02", "0.01"],
			["5000", "0.03", "0.015"],
			["10000", "0.04", "0.02"]
		]
	},
	"message": "ok"
}

```

## 9. 获取合约账户资金列表
* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/account/asset
* Return value description: 返回所有资产

| name | type | description |
| ------ | ------ |------ |
| available | String | 账户可用余额 |
| balance_all | String | 账号资产 =  available+ frozen + margin_all |
| margin_all | String | 保证金余额 |
| margin_position | String| 仓位保证金|
| frozen | String | 冻结额度 |
| profit_unreal | String | 未实现盈亏 |
| profit_real | String | 已实现盈亏 |

* Example

```
# Request
GET https://api.coinex.com/contract/account/asset

# Response
{
  "code": 0,
  "message": "ok",
  "data":
  {
      "BTC": 
	   {
			"available": "0",
			"frozen": "0",
			"balance_all": "0",
			"margin_all": "0",
			"margin_position": "0",
			"profit_unreal": "0",
			"profit_real": "0"
		}
		"ETH": 
		{
			"available": "0",
			"frozen": "0",
			"balance_all": "0",
			"margin_all": "0",
			"margin_position": "0",
			"profit_unreal": "0",
			"profit_real": "0"
		}
	},
	"message": "ok"
}

```


## 10. 限价委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/put_limit
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| side | Integer | Yes | 委托类型 1表示卖空，2表示买多|
| amount | String | Yes | 委托数量 |
| price | String | Yes | 委托价格 |
| effect_type | Integer | No | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| market | String | 合约市场 |
| user_id | Integer | 用户id|
| order_id | Integer | 委托订单id |
| position_id | Integer | 合约市场当前仓位ID，如果当前无仓位该字段为0 |
| type | Integer | 委托方式，1:限价委托，2:市价委托|
| side | Integer | 委托方向，1:卖空，2:买多 |
| target | Integer | 0为普通委托 |
| position_type | Integer | 仓位类型，1:逐仓，2:全仓 |
| effect_type | Integer | 委托生效类型 |
| create_time | Integer | 委托时间 |
| update_time | Integer | 委托最近一次更新时间 |
| amount | String | 委托数量 |
| price | String | 委托价格 |
| source | String | 委托来源 |
| taker_fee | String | taker费率 |
| maker_fee | String | maker费率 |
| left | String | 未成交合约数 |
| deal_stock | String | 已成交合约消费的币数量 |
| deal_amount | String | 已成交合约数量 |
| deal_margin | String | 已成交合约的保证金数量 |
| deal_fee | String | 已成交合约产生的手续费 |
| leverage | String | 杠杆倍数 |
| mainten_margin | String | 维持保证金率 |
| risk_limit | String | 风险限额 |
| use_risklimit | String | 已使用风险限额 |
| deal_price_avg | String | 平均交易价格 |

* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/put_limit
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",    # 合约市场
  "price": "99.50",      # 委托价格
  "amount": "134.55",    # 委托数量
  "side": 1,             # 委托类型
  "effect_type": 1,      # 委托生效类型
  "time": 1550743431     # 客户端请求时间戳
}

# Response
{
  "code": 0,
  "data":
   {
        "left": "10",
        "amount": "10",
        "leverage": "5",
        "order_id": 1197,
        "market": "BCHUSD",
        "price": "150",
        "deal_margin": "0",
        "position_type": 1,
        "position_id": 0,
        "side": 1,
        "update_time": 1550742670.491004,
        "effect_type": 1,
        "type": 1,
        "user_id": 551,
        "target": 0,
        "maker_fee": "-0.0002",
        "taker_fee": "0.0005",
        "create_time": 1550742670.491004,
        "source": "web",
        "maiten_margin": "0.005",
        "deal_stock": "0",
        "deal_amount": "0",
        "use_risklimit": "0.01432153",
        "deal_fee": "0",
        "risk_limit": "200",
        "deal_price_avg": "0"
    },
    "message": "ok"
}

```

## 11. 市价委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/put_market
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| side | Integer | Yes | 委托类型 1表示卖空，2表示买多|
| amount | String | Yes | 委托数量 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:
  返回值类型请参考接口contract/v1/order/put_limit的返回值

* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/put_market
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",  
  "amount": "5",       
  "side": 2,   
  "time": 1550743431          
}

# Response
{
  "code": 0,
  "data":
  {
      "left": "10",
      "amount": "10",
      "leverage": "5",
      "order_id": 1197,
      "market": "BCHUSD",
      "price": "150",
      "deal_margin": "0",
      "position_type": 1,
      "position_id": 0,
      "side": 1,
      "update_time": 1550742670.491004,
      "effect_type": 1,
      "type": 1,
      "user_id": 551,
      "target": 0,
      "maker_fee": "-0.0002",
      "taker_fee": "0.0005",
      "create_time": 1550742670.491004,
      "source": "web",
      "maiten_margin": "0.005",
      "deal_stock": "0",
      "deal_amount": "0",
      "use_risklimit": "0.01432153",
      "deal_fee": "0",
      "risk_limit": "200",
      "deal_price_avg": "0"
    },
    "message": "ok"
}

```

## 12. 限价计划委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/put_stop_limit
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| side | Integer | Yes | 委托类型 1表示卖空，2表示买多|
| stop_type | Integer | Yes | 触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发|
| amount | String | Yes | 委托数量 |
| stop_price | String | Yes | 触发价格 |
| price | String | Yes | 委托价格 |
| effect_type | Integer | No | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| status | String | 计划委托下单成功返回：success|

* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/put_stop_limit
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",    # 合约市场
  “side”: 1              # 卖
  "stop_type": 1         #触发类型为最新成交价格
  "amount": "134.55",    # 委托数量
  "stop_price": "99.50", # 触发价格
  "price": "99.50",      # 委托价格
  "effect_type": 1,      # 委托生效类型
  "time": 1550743431     # 客户端请求时间戳
}

# Response
{
  "code": 0,
  "data":
   {
       "status": "success"
   },
   "message": "ok"
}

```

## 13. 市价计划委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/put_stop_market
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| side | Integer | Yes | 委托类型 1表示卖空，2表示买多|
| stop_type | Integer | Yes | 触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发|
| amount | String | Yes | 委托数量 |
| stop_price | String | Yes | 触发价格 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| status | String | 计划委托下单成功返回：success|

* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/put_stop_market
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",    # 合约市场
  “side”: 1              # 卖
  "stop_type": 1         #触发类型为最新成交价格
  "amount": "134.55",    # 委托数量
  "stop_price": "99.50", # 触发价格
  "time": 1550743431     # 客户端请求时间戳
}

# Response
{
  "code": 0,
  "data":
   {
       "status": "success"
   },
   "message": "ok"
}

```

## 13. 取消未完成订单委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/cancel
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| order_id | Integer | Yes | 未完成订单ID |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值参考接口contract/v1/order/put_limit
* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/cancel
# Request.Body
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",   # 合约市场
  "order_id": 1121,     # 订单ID
  "tonce": 1550743431   # 客户端请求时间戳
}

# Response
{
  "code": 0,
  "data":
  {
      "left": "10",
      "amount": "10",
      "leverage": "5",
      "order_id": 1197,
      "market": "BCHUSD",
      "price": "150",
      "deal_margin": "0",
      "position_type": 1,
      "position_id": 0,
      "side": 1,
      "update_time": 1550742670.491004,
      "effect_type": 1,
      "type": 1,
      "user_id": 551,
      "target": 0,
      "maker_fee": "-0.0002",
      "taker_fee": "0.0005",
      "create_time": 1550742670.491004,
      "source": "web",
      "maiten_margin": "0.005",
      "deal_stock": "0",
      "deal_amount": "0",
      "use_risklimit": "0.01432153",
      "deal_fee": "0",
      "risk_limit": "200",
      "deal_price_avg": "0"
  },
  "message": "ok"
}

```

## 14. 获取未完成委托订单
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/pending
* Request parameter: 返回数据为列表

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场，例如BTCUSD, ALL：表示所有市场 |
| side | Integer | Yes | 委托类型 0:全部(买与卖) 1:卖, 2: 买 |
| offset | Integer |  Yes | 偏移量，即从哪条开始获取 |
| limit | Integer |  Yes | 一次获取记录数，默认为20条，最大为100条 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值参考接口contract/v1/order/put_limit
* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/pending
{
	'access_id': 'D867F8EF576C4221809D7D1926212EC8',
	'market': 'BTCUSD',
	'side': 2,
	'offset': 0,
	'limit': 100,
	'time': 1550748047
}

# Response
{
  "code": 0,
  "data": 
  {
    "total": 1,   #返回数据的总条数
    "offset": 0,  #与请求字段的offset相同
    "limit": 100, #与请求字段的limit相同
    "records": 
    [
        {
            "left": "10",
            "amount": "10",
	        "leverage": "5",
	        "order_id": 1197,
      	    "market": "BCHUSD",
      		"price": "150",
      	    "deal_margin": "0",
            "position_type": 1,
            "position_id": 0,
            "side": 1,
            "update_time": 1550742670.491004,
            "effect_type": 1,
            "type": 1,
            "user_id": 551,
            "target": 0,
            "maker_fee": "-0.0002",
            "taker_fee": "0.0005",
            "create_time": 1550742670.491004,
            "source": "web",
            "maiten_margin": "0.005",
            "deal_stock": "0",
            "deal_amount": "0",
            "use_risklimit": "0.01432153",
            "deal_fee": "0",
            "risk_limit": "200",
            "deal_price_avg": "0"
        }
    ]
  }
  "message": "ok"
}

```

## 15. 获取指定委托单的信息
* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/order/order_detail
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场， 可为空，为空获取所有市场的未完成委托订单|
| order_id | Integer | Yes | 订单id |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值参考接口contract/v1/order/put_limit
* Example

```
# Request
POST https://api.coinex.com/contract/v1/order/order_detail
{
	'access_id': 'D867F8EF576C4221809D7D1926212EC8',
	'market': 'BTCUSD',
	'order_id': 2,
	'time': 1550748047
}

# Response
{
  "code": 0,
  "data": 
  {
      "left": "10",
      "amount": "10",
	  "leverage": "5",
	  "order_id": 1197,
      "market": "BCHUSD",
      "price": "150",
      "deal_margin": "0",
      "position_type": 1,
      "position_id": 0,
      "side": 1,
      "update_time": 1550742670.491004,
      "effect_type": 1,
      "type": 1,
      "user_id": 551,
      "target": 0,
      "maker_fee": "-0.0002",
      "taker_fee": "0.0005",
      "create_time": 1550742670.491004,
      "source": "web",
      "maiten_margin": "0.005",
      "deal_stock": "0",
      "deal_amount": "0",
      "use_risklimit": "0.01432153",
      "deal_fee": "0",
      "risk_limit": "200",
      "deal_price_avg": "0"
  }
  "message": "ok"
}

```

## 16. 限价平仓委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/position/close_limit
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场，例如BTCUSD, ALL：表示所有市场 |
| position_id | Integer | Yes | 仓位ID |
| amount | String | Yes | 平仓数量 |  |
| price | String | Yes | 价格 |
| effect_type | Integer | No | 委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值参考接口contract/v1/order/put_limit
* Example

```
# Request
POST https://api.coinex.com/contract/v1/position/close_limit
{
    "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
    "market": "btcusdt",
    "position_id": 12,     
    "amount": 100,         
    "price": "11.21",
    "time": 1550748047
}

# Response
{
  "code": 0,
  "data": 
  {
      "left": "10",
      "amount": "10",
	  "leverage": "5",
	  "order_id": 1197,
      "market": "BCHUSD",
      "price": "150",
      "deal_margin": "0",
      "position_type": 1,
      "position_id": 0,
      "side": 1,
      "update_time": 1550742670.491004,
      "effect_type": 1,
      "type": 1,
      "user_id": 551,
      "target": 0,
      "maker_fee": "-0.0002",
      "taker_fee": "0.0005",
      "create_time": 1550742670.491004,
      "source": "web",
      "maiten_margin": "0.005",
      "deal_stock": "0",
      "deal_amount": "0",
      "use_risklimit": "0.01432153",
      "deal_fee": "0",
      "risk_limit": "200",
      "deal_price_avg": "0"
  },
  "message": "ok"

```

## 17. 市价平仓委托
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/position/close_market
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场 |
| position_id | Integer | Yes | 仓位ID |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值参考接口contract/v1/order/put_limit
* Example

```
# Request
POST https://api.coinex.com/contract/v1/position/close_market
{
    "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
    "market": "btcusdt",
    "position_id": 1121, 
    "time": 1550748047
}

# Response
{
  "code": 0,
  "data": 
  {
      "left": "10",
      "amount": "10",
	  "leverage": "5",
	  "order_id": 1197,
      "market": "BCHUSD",
      "price": "150",
      "deal_margin": "0",
      "position_type": 1,
      "position_id": 0,
      "side": 1,
      "update_time": 1550742670.491004,
      "effect_type": 1,
      "type": 1,
      "user_id": 551,
      "target": 0,
      "maker_fee": "-0.0002",
      "taker_fee": "0.0005",
      "create_time": 1550742670.491004,
      "source": "web",
      "maiten_margin": "0.005",
      "deal_stock": "0",
      "deal_amount": "0",
      "use_risklimit": "0.01432153",
      "deal_fee": "0",
      "risk_limit": "200",
      "deal_price_avg": "0"
  },
  "message": "ok"
}

```

## 18. 获取用户未平仓仓位列表
* Request type: GET
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/position/pending
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场, 例如：BTCUSD， ALL:表示所有市场 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| position_id | Integer | 仓位id |
| market | String | 合约市场 |
| amount | String | 仓位数量|
| open_price | String | 开仓价格 |
| close_price | String | 平仓价格 |
| open_time | String | 开仓时间 |
| close_time | String | 平仓时间 |
| adl_sort_percent | String | 减仓风险 |
| type | Integer | 1 逐仓 2 全仓|
| side | Integer | 1 空仓 2 多仓|
| adl_sort | Integer | 自动减仓排序|
| liq_price | String | 强平价格 |
| bkr_price | String | 破产价格 |
| leverage |  String | Yes | 杠杆 |
| mainten\_margin\_amount | String | 维持保证金 |
| margin\_amount| String | 全部保证金 |
| margin\_rate | String | 保证金率 |
| profit_real | String | 已实现盈亏 |
| profit_unreal | String | 未实现盈亏 |
| liq_risk | String | 爆仓风险 |
| risk_limit | String | 风险限额 |
| frozen_fee | String | 冻结手续费|
| finish_type | Integer | 平仓类型 0 未平仓 1 自主平仓 2 强制平仓 3 被减仓 |
| mainten_margin | String | 维持保证金率 |
| init_margin    | String | 启始保证金率 |
| liq_price_extra  | String | 全仓时，去掉可用余额去计算的强平价 |
| bkr_price_extra  | String | 全仓时，去掉可用余额去计算的破产价 |
| open_margin_extra  | String | 全仓时，去掉可用余额去计算的保证金率 |
| profit_rate    | String | 回报率 |
| open_val       | String | 开仓价值 |
| position_val   | String | 仓位价值 |
| fair_price     | String | 标记价格 |
| use_risklimit  | String | 已使用风险限额 |

* Example

```
# Request
GET https://api.coinex.com/contract/v1/position/pending?access_id=D867F8EF576C4221809D7DXXXXXXXXC8&market=&time=1550748047

# Response
{
  "code": 0,
  "data":
  [
  	   {
            "side": 2,
            "bkr_price": "0.149997",
            "position_id": 106,
            "liq_price": "0.149997",
            "market": "BTCUSD",
            "user_id": 278,
            "type": 2,
            "mainten_margin": "0.01",
            "adl_sort": 4,
            "finish_type": 1,
            "open_time": 1548845636.7650371,
            "update_time": 1550635200.480464,
            "close_time": 0.0,
            "adl_sort_percent": 0.25,
            "amount": "9",
            "init_margin": "0.02",
            "liq_price_extra": "2791.73119",
            "margin_amount": "0.00009103",
            "open_price": "3705.529019",
            "close_price": "0",
            "profit_real": "-0.0004022",
            "risk_limit": "500",
            "leverage": "50",
            "open_val": "0.0024288",
            "fair_price": "3891.710199",
            "mainten_margin_amount": "0.00000269",
            "frozen_fee": "0.00000121",
            "liq_risk": "4e-8",
            "bkr_price_extra": "2770.855671",
            "open_margin_extra": "0.337323",
            "profit_unreal": "0.0001162",
            "margin_rate": "0.03747941",
            "profit_rate": "21.55844155844155844155844155844155",
            "position_val": "0.0023126",
            "use_risklimit": "0.04337757"
        }
  	],
  	 "message": "ok"
}

```

# 19. 调整仓位保证金
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/position/adjust_margin
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | :------ |
| market | String | Yes | 合约市场, 例如：BTCUSD |
| amount | String | Yes | 调整额度 |
| type | Integer | Yes | 调整类型：1表示增加保证金，2表示减少保证金 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description: 返回值字段参考接口position/pending
* Example

```
# Request
POST https://api.coinex.com/api/contract/v1/position/adjust_margin
{
  "access_id" : "BFFA64957AA240F6BBEA26F4E07EC0D9",
  "market": "BTCUSD",    
  "amount": "10.12",    
  "type": 1,
  "time": 1550748047
}

# Response
{
  "code": 0,
  "data": 
  {
        "side": 2,
        "bkr_price": "0.149997",
        "position_id": 106,
        "liq_price": "0.149997",
        "market": "BTCUSD",
        "user_id": 278,
        "type": 2,
        "mainten_margin": "0.01",
        "adl_sort": 4,
        "finish_type": 1,
        "open_time": 1548845636.7650371,
        "update_time": 1550635200.480464,
        "close_time": 0.0,
        "adl_sort_percent": 0.25,
        "amount": "9",
        "init_margin": "0.02",
        "liq_price_extra": "2791.73119",
        "margin_amount": "0.00009103",
        "open_price": "3705.529019",
        "close_price": "0",
        "profit_real": "-0.0004022",
        "risk_limit": "500",
        "leverage": "50",
        "open_val": "0.0024288",
        "fair_price": "3891.710199",
        "mainten_margin_amount": "0.00000269",
        "frozen_fee": "0.00000121",
        "liq_risk": "4e-8",
        "bkr_price_extra": "2770.855671",
        "open_margin_extra": "0.337323",
        "profit_unreal": "0.0001162",
        "margin_rate": "0.03747941",
        "profit_rate": "21.55844155844155844155844155844155",
        "position_val": "0.0023126",
        "use_risklimit": "0.04337757"
   },
   "message": "ok"
}
```

## 20. 调整风险限额
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/position/adjust_risk_limit
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场, 例如：BTCUSD |
| risk_limit | String | Yes | 风险限额 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| init_margin | String | 起始保证金率 |
| mainten_margin | String | 维持保证金率|
| risk_limit | String | 风险限额 |
| leverage | String | 当前仓位采用的杠杆 |

* Example

```
# Request
POST https://api.coinex.com/contract/v1/market/adjust_risk
{
  "access_id":"D867F8EF576C4221809D7D1926212EC8",
  "market":"BCHUSD",
  "risk_limit":"500",
  "time": 1550748047
}

# Response
{
  "code": 0,
  "data":
   {
      "init_margin": "0.02",
      "mainten_margin": "0.01",
      "risk_limit": "500",
      "leverage": "10"
   },
   "message": "ok"
}

```

## 21. 调整杠杆
* Request type: POST
* Signature required: Yes
* Request Header: Authorization: "xxxx"，"Access_id": "xxx"
* Request Url: https://api.coinex.com/contract/v1/market/adjust_leverage
* Request parameter:

| name | type | required | description |
| ------ | ------ | ------ | ------ |
| market | String | Yes | 合约市场, 例如：BTCUSD |
| leverage | String | Yes | 调整杠杆大小，在不同风险限额下，只能取某些值，具体参考合约规则文档 |
| timestamp | Integer | Yes | 客户端时间戳，单位：毫秒|
| windowtime | Integer | No | 时间窗口，单位：毫秒|

* Return value description:

| name | type | description |
| ------ | ------ |------ |
| init_margin | String | 起始保证金率 |
| mainten_margin | String | 维持保证金率|
| risk_limit | String | 风险限额 |
| leverage | String | 调整后的杠杆 |

* Example

```
# Request
POST https://api.coinex.com/contract/v1/market/adjust_leverage
{
  "access_id":"D867F8EF576C4221809D7D1926212EC8",
  "market":"BCHUSD",
  "leverage": 10,
  "time": 1550748047
}

# Response
{
  "code": 0,
  "data":
   {
      "init_margin": "0.02",
      "mainten_margin": "0.01",
      "risk_limit": "500",
      "leverage": "10"
   },
   "message": "ok"
}

```
