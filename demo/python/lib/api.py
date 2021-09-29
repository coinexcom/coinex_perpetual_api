#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from .request_client import RequestClient


class CoinexPerpetualApi(object):
    ORDER_DIRECTION_SELL = 1
    ORDER_DIRECTION_BUY = 2

    MARGIN_ADJUST_TYPE_INCRESE = 1
    MARGIN_ADJUST_TYPE_DECREASE = 2

    POSITION_TYPE_ISOLATED = 1
    POSITION_TYPE_CROSS_MARGIN = 2

    def __init__(self, access_id, secret_key, logger=None):
        self.request_client = RequestClient(access_id, secret_key, logger)

    # System API
    def ping(self):
        """
        # Request
        GET https://api.coinex.com/perpetual/v1/ping

        # Response
        {
        "code": 0,
        “data”: "pong",
        "message": "ok"
        }
        """
        path = '/v1/ping'
        return self.request_client.get(path, sign=False)

    # Market API
    def get_market_info(self):
        """
        # params:
            name	String	市场名
            stock	String	基础货币
            money	String	计价货币
            fee_prec	String	费率精度
            stock_prec	String	基础货币精度
            money_prec	String	计价货币精度
            multiplier	String	合约乘数，一般为1

        # Request
        GET https://api.coinex.com/perpetual/v1/market/list

        # Response
        {
            "message": "OK",
            "code": 0,
            "data": [
                {
                    "stock_prec": 8,
                    "amount_prec": 0,
                    "stock": "BTC",
                    "leverages": [
                        "3", "5", "8", "10", "15", "20", "50", "100"
                    ],
                    "name": "BTCUSD",
                    "fee_prec": 5,
                    "multiplier": "1",
                    "money": "USD",
                    "money_prec": 0
                },
                {
                    "stock_prec": 8,
                    "amount_prec": 0,
                    "stock": "BCH",
                    "leverages": [
                        "3", "5", "6", "10", "15", "20", "30", "50", "100"
                    ],
                    "name": "BCHUSD",
                    "fee_prec": 5,
                    "multiplier": "1",
                    "money": "USD",
                    "money_prec": 4
                },
            ]
        }
        """
        path = '/v1/market/list'
        return self.request_client.get(path, sign=False)

    def get_market_state(self, market):
        """
        # Request
        GET https://api.coinex.com/perpetual/v1/market/ticker?market=BTCUSD
        # Response
        {
            "message": "OK",
            "code": 0,
            "data": {
                "date": 1568097425927,
                "ticker": {
                    "vol": "260102",
                    "low": "6000.0000",
                    "open": "10000.0000",
                    "high": "14999.99999999999999992500",
                    "buy": "6000.0000",
                    "buy_amount": "9998",
                    "sell_amount": "0",
                    "last": "6000.0000",
                    "period": 86400,
                    "position_amount": "10000.0000",
                    "funding_time": 9,
                    "funding_rate_last": "-0.00144",
                    "sell_total": "1321512",
                    "sign_price": "6000",
                    "funding_rate_next": "-0.00375",
                    "insurance": "2.43679741441092111045",
                    "buy_total": "498108",
                    "sell": "0"
                }
            }
        }
        """
        path = '/v1/market/ticker'
        params = {
            'market': market
        }
        return self.request_client.get(path, params, sign=False)

    def get_market_deals(self, market, last_id=0):
        """
        # params:
            id	Integer	交易id
            time	Long	交易时间，单位：秒
            price	String	交易价格
            amount	String	交易数量
            type	Integer	1: 卖，2: 买

        # Request
        GET https://api.coinex.com/perpetual/v1/market/deals?market=BTCUSD&last_id=1111

        # Response   //每次最多获取100条最近交易信息
        {
        "code": 0,
        "data":
        [
            {
                "id": 291,
                "type": "sell",
                "price": "10000.0000",
                "amount": "10000",
                "date": 1567839458,
                "date_ms": 1567839458117
            },
            ...
        ],
        "message": "ok"
        }
        """
        path = '/v1/market/deals'
        params = {
            'market': market,
            'last_id': last_id
        }
        return self.request_client.get(path, params, sign=False)

    def tickers(self):
        """
        # Request
        GET https://api.coinex.com/perpetual/v1/market/ticker/all

        # Response
        {
            "code": 0,
            "data": {
                "date": 1513865441609,
                "ticker": {
                    "BCHXUSD": {
                        "buy": "0",
                        "vol": "0",
                        "funding_rate_last": "-0.00375",
                        "low": "0",
                        "open": "0",
                        "funding_rate_next": "-0.00328",
                        "last": "295.1688",
                        "high": "0",
                        "funding_time": 215,
                        "period": 86400,
                        "position_amount": "0",
                        "insurance": "0",
                        "sell": "301.1233",
                        "sign_price": "298.8372",
                        "sell_total": "10",
                        "buy_total": "11",
                        "buy_amount": "0",
                        "sell_amount": "100"
                    },
                    ...
                }
            },
            "message": "Ok"
        }
        """
        path = '/v1/market/ticker/all'
        return self.request_client.get(path, sign=False)

    def depth(self, market, merge=0, limit=50):
        """
        # params merge: '0', '0.1', '0.01'
        # params limit: 5/10/20/50
        # Request
        GET https://api.coinex.com/perpetual/v1/market/depth?market=BTCUSD&merge=0&limit=20

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
                    ["3700", "35"], # 合约价格，合约数量
                    ["3650", "80"],
                    ["3600", "305"],
                    ["3599", "20"],
                    ["3598", "10"],
                    ["3597", "20"]
                ],
                "last": "3740"      # 最新价格
            },
            "message": "ok"
        }
        """
        path = '/v1/market/depth'
        params = {
            'market': market,
            'merge': merge,
            'limit': limit
        }
        return self.request_client.get(path, params, sign=False)

    def kline(self, market, kline_type, limit):
        """
        # params market
        # params limit: 获取K线数量，不能超过1000，默认为1000
        # params type: K线信息类别，支持如下参数，1min,3min,5min,15min,30min,1hour,2hour,4hour,6hour,12hour,1day,3day,1week
        # Request
        GET https://api.coinex.com/perpetual/v1/market/kline?market=BTCUSD&type=1min&limit=500 //表示获取500条k线数据，每条数据为1min类型k线数据

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
        """
        path = '/v1/market/kline'
        params = {
            'market': market,
            'type': kline_type,
            'limit': limit
        }
        return self.request_client.get(path, params, sign=False)

    def risk_config(self):
        """
        # Request
        GET https://api.coinex.com/perpetual/v1/market/limit_config

        # Response
        {
        "code": 0,
            "data": 
            {
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
                    ],
                ...
            },
            "message": "ok"
        }
        """
        path = '/v1/market/limit_config'
        return self.request_client.get(path, sign=False)

    # Account API
    def query_account(self):
        """
        # params:
            available	String	账户可用余额
            balance_all	String	账号资产 = available+ frozen + margin_all
            margin_all	String	保证金余额
            margin_position	String	仓位保证金
            frozen	String	冻结额度
            profit_unreal	String	未实现盈亏
            profit_real	String	已实现盈亏

        # Request
        GET https://api.coinex.com/perpetual/v1/asset/query

        # Response
        {
            "code": 0,
            "message": "ok",
            "data":
            {
                "BTC": {
                    "balance_total": "1000.00000000000000000000",
                    "transfer": "1000.00000000000000000000",
                    "available": "1000.00000000000000000000",
                    "margin": "0",
                    "frozen": "0"
                },
                "ETH": {
                    "balance_total": "500.00000000000000000000",
                    "transfer": "500.00000000000000000000",
                    "available": "500.00000000000000000000",
                    "margin": "0",
                    "frozen": "0"
                },
            },
            "message": "ok"
        }
        """
        path = '/v1/asset/query'
        return self.request_client.get(path)

    # Trading API
    def put_limit_order(self, market, side, amount, price, effect_type=1):
        """
        # params:
            market	String	Yes	合约市场
            side	Integer	Yes	委托类型 1表示卖空，2表示买多
            amount	String	Yes	委托数量
            price	String	Yes	委托价格
            effect_type	Integer	No	委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1
        
        # Request
        POST https://api.coinex.com/perpetual/v1/order/put_limit
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
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
            "data": {
                "source": "API",
                "order_id": 281,
                "side": 1,
                "user_id": 12,
                "position_id": 0,
                "left": "10",
                "update_time": 1568187004.051227,
                "market": "BTCUSD",
                "effect_type": 1,
                "maker_fee": "0.00000",
                "position_type": 2,
                "deal_stock": "0",
                "create_time": 1568187004.051227,
                "target": 0,
                "type": 1,
                "price": "10090.0000",
                "taker_fee": "0.00075",
                "deal_profit": "0",
                "amount": "10",
                "deal_fee": "0",
                "leverage": "3"
            },
            "message": "ok"
        }
        """
        path = '/v1/order/put_limit'
        data = {
            'market': market,
            'effect_type': effect_type,
            'side': side,
            'amount': str(amount),
            'price': str(price)
        }
        return self.request_client.post(path, data)

    def put_market_order(self, market, side, amount):
        """
        # params:
            market	String	Yes	合约市场
            side	Integer	Yes	委托类型 1表示卖空，2表示买多
            amount	String	Yes	委托数量

        # Request
        POST https://api.coinex.com/perpetual/v1/order/put_market
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "BTCUSD",
            "amount": "5",
            "side": 2,
            "time": 1550743431
        }

        # Response
        {
            "code": 0,
            "data": {
                "source": "API",
                "order_id": 424,
                "side": 1,
                "user_id": 12,
                "position_id": 0,
                "left": "0",
                "update_time": 1568192886.694576,
                "market": "BTCUSD",
                "effect_type": 0,
                "maker_fee": "0",
                "position_type": 2,
                "deal_stock": "0.00010000000000000000",
                "create_time": 1568192886.694551,
                "target": 0,
                "type": 2,
                "price": "0",
                "taker_fee": "0.00075",
                "deal_profit": "0",
                "amount": "1",
                "deal_fee": "0.00000007500000000000",
                "leverage": "3"
            },
            "message": "ok"
        }
        """
        path = '/v1/order/put_market'
        data = {
            'market': market,
            'amount': str(amount),
            'side': side
        }
        return self.request_client.post(path, data)

    def put_stop_limit_order(self, market, side, amount, price, stop_price, stop_type=3, effect_type=1):
        """
        # params:
            market	    String	Yes	合约市场
            side	    Integer	Yes	委托类型 1表示卖空，2表示买多
            amount	    String	Yes	委托数量
            stop_type	Integer	Y	触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发
            stop_price	String	Y	触发价格
            price	    String	Yes	委托价格
            effect_type	Integer	No	委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1

        # Request
        POST https://api.coinex.com/perpetual/v1/order/put_stop_limit

        # Response
        {
            "code": 0,
            "data": {
                "status": "success"
            },
            "message": "ok"
        }
        """
        path = '/v1/order/put_stop_limit'
        data = {
            'market': market,
            'effect_type': effect_type,
            'side': side,
            'amount': str(amount),
            'price': str(price),
            'stop_price': str(stop_price),
            'stop_type': stop_type
        }
        return self.request_client.post(path, data)

    def put_stop_market_order(self, market, side, amount, stop_price, stop_type=3):
        """
        # params:
            market	    String	Yes	合约市场
            side	    Integer	Yes	委托类型 1表示卖空，2表示买多
            amount	    String	Yes	委托数量
            stop_type	Integer	Y	触发类型 1: 最新成交价格触发，2:标记价格触发，3: 指数价格触发
            stop_price	String	Y	触发价格
        
        # Request
        POST https://api.coinex.com/perpetual/v1/order/put_stop_market

        # Response
        {
            "code": 0,
            "data": {
                "status": "success"
            },
            "message": "ok"
        }
        """
        path = '/v1/order/put_stop_market'
        data = {
            'market': market,
            'side': side,
            'amount': str(amount),
            'stop_price': str(stop_price),
            'stop_type': stop_type
        }
        return self.request_client.post(path, data)

    def close_limit(self, market, position_id, amount, price, effect_type=None):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            position_id	Integer	Yes	仓位ID
            amount	String	Yes	平仓数量
            price	String	Yes	价格
            effect_type	Integer	No	委托生效类型，1: 一直有效直至取消, 2: 立刻成交或取消, 3: 完全成交或取消。默认为1
        
        # Request
        POST https://api.coinex.com/perpetual/v1/position/close_limit
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "btcusdt",
            "position_id": 12,
            "amount": 100,
            "price": "11.21",
            "time": 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
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
        """
        path = '/v1/order/close_limit'
        data = {
            'market': market,
            'position_id': position_id,
            'amount': str(amount),
            'price': str(price)
        }
        if effect_type:
            data['effect_type'] = effect_type

        return self.request_client.post(path, data)

    def close_market(self, market, position_id):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            position_id	Integer	Yes	仓位ID
        # Request
        POST https://api.coinex.com/perpetual/v1/position/close_market
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "btcusdt",
            "position_id": 1121, 
            "time": 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
                "source": "API",
                "deal_profit": "0",
                "update_time": 1568201078.584071,
                "order_id": 682,
                "target": 0,
                "maker_fee": "0.00000",
                "position_id": 0,
                "position_type": 2,
                "leverage": "3",
                "price": "9700.0000",
                "market": "BTCUSD",
                "create_time": 1568201078.584071,
                "side": 2,
                "type": 1,
                "effect_type": 1,
                "taker_fee": "0.00075",
                "deal_stock": "0",
                "user_id": 12,
                "amount": "1",
                "left": "1",
                "deal_fee": "0"
            },
            "message": "OK"
        }
        """
        path = '/v1/order/close_market'
        data = {
            'market': market,
            'position_id': position_id
        }
        return self.request_client.post(path, data)

    def cancel_order(self, market, order_id):
        """
        # Request
        POST https://api.coinex.com/perpetual/v1/order/cancel
        # Request.Body
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "BTCUSD",   # 合约市场
            "order_id": 1121,     # 订单ID
            "tonce": 1550743431   # 客户端请求时间戳
        }

        # Response
        {
            "code": 0,
            "data": {
                "source": "web",
                "order_id": 518,
                "side": 2,
                "user_id": 12,
                "position_id": 0,
                "left": "10",
                "update_time": 1568194210.967061,
                "market": "BTCUSD",
                "effect_type": 1,
                "maker_fee": "0.00000",
                "position_type": 2,
                "deal_stock": "0",
                "create_time": 1568194210.967061,
                "target": 0,
                "type": 1,
                "price": "8888.0000",
                "taker_fee": "0.00075",
                "deal_profit": "0",
                "amount": "10",
                "deal_fee": "0",
                "leverage": "3"
            },
            "message": "OK"
        }
        """
        path = '/v1/order/cancel'
        params = {
            'market': market,
            'order_id': order_id
        }
        return self.request_client.post(path, params)

    def cancel_all_order(self, market):
        """
        # Request
        POST https://api.coinex.com/perpetual/v1/order/cancel_all
        # Request.Body
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "BTCUSD",   # 合约市场
            "tonce": 1550743431   # 客户端请求时间戳
        }

        # Response
        {
            "data": {
                "status": "success"
            },
            "code": 0,
            "message": "OK"
        }
        """
        path = '/v1/order/cancel_all'
        params = {
            'market': market
        }
        return self.request_client.post(path, params)

    def query_order_pending(self, market, side, offset, limit=100):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            side	Integer	Yes	委托类型 0:全部(买与卖) 1:卖, 2: 买
            offset	Integer	Yes	偏移量，即从哪条开始获取
            limit	Integer	Yes	一次获取记录数，默认为20条，最大为100条

        # Request
        POST https://api.coinex.com/perpetual/v1/order/pending
        {
            'access_id': 'BFFA64957AA240F6BBEA26FXXXX',
            'market': 'BTCUSD',
            'side': 2,
            'offset': 0,
            'limit': 100,
            'time': 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
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
        """
        path = '/v1/order/pending'
        params = {
            'market': market,
            'side': side,
            'offset': offset,
            'limit': limit
        }
        return self.request_client.get(path, params)

    def query_stop_pending(self, market, side, offset, limit=100):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            side	Integer	Yes	委托类型 0:全部(买与卖) 1:卖, 2: 买
            offset	Integer	Yes	偏移量，即从哪条开始获取
            limit	Integer	Yes	一次获取记录数，默认为20条，最大为100条

        # Request
        POST https://api.coinex.com/perpetual/v1/order/stop_pending
        {
            'access_id': 'BFFA64957AA240F6BBEA26FXXXX',
            'market': 'BTCUSD',
            'side': 2,
            'offset': 0,
            'limit': 100,
            'time': 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
                "total": 1,   #返回数据的总条数
                "offset": 0,  #与请求字段的offset相同
                "limit": 100, #与请求字段的limit相同
                "records":
                [
                    {
                        "market": "btcusd",
                        "create_time": 1568205393.025454,
                        "stop_type": 3,
                        "order_id": 694,
                        "effect_type": 1,
                        "amount": "10",
                        "stop_price": "3.0000",
                        "state": 1,
                        "source": "API",
                        "user_id": 12,
                        "type": 1,
                        "side": 2,
                        "maker_fee": "0.00000",
                        "update_time": 1568205393.025454,
                        "price": "8000.0000",
                        "taker_fee": "0.00075",
                        "direction": "buy"
                    }
                ]
            }
            "message": "ok"
        }
        """
        path = '/v1/order/stop_pending'
        params = {
            'market': market,
            'side': side,
            'offset': offset,
            'limit': limit
        }
        return self.request_client.get(path, params)

    def query_position_pending(self, market=''):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场

        # Request
        GET https://api.coinex.com/perpetual/v1/position/pending?access_id=D867F8EF576C4221809D7DXXXXXXXXC8&market=&time=1550748047

        # Response
        {
            "code": 0,
            "data": [
                {
                    "mainten_margin_amount": "0.17268961860639441659",
                    "liq_order_time": 0.0,
                    "side": 1,                          # 1: 空仓， 2:多仓  
                    "position_id": 40036,               #
                    "create_time": 1568797686.771109,
                    "update_time": 1569352866.381876,
                    "mainten_margin": "0.01",
                    "open_margin": "0.38453533430782908185",
                    "type": 1,                                  # 1: 逐仓， 2:全仓
                    "open_val": "17.26896186063944165950",
                    "open_val_max": "29.30629489150890631978",
                    "liq_price": "16239.69656662650735328702",  # 强平价格, 有可能是 "Infinity"
                    "sys": 0,
                    "open_price": "10157.35638398734428484298", # 平均开仓价格
                    "market": "BTCUSD",     #
                    "finish_type": 1,
                    "user_id": 12,
                    "leverage": "3",                            # 杠杆
                    "liq_order_price": "0.00000000000000000000",
                    "close_left": "175407",
                    "amount": "175407",                         # 仓位数量
                    "amount_max": "298945",
                    "liq_price_imply": "15008.57056756566782818489",
                    "liq_amount": "0",
                    "total": 6,
                    "open_margin_imply": "0.33322959483310553171",
                    "liq_profit": "0.00000000000000000000",
                    "bkr_price": "16503.55731236668455564542",
                    "margin_amount": "6.64052602223013782625",
                    "profit_real": "6.93023339422833871190",    # 已实现盈亏
                    "profit_clearing": "0.00066833232495527191",
                    "adl_sort_val": "26414.62429524",
                    "liq_time": 0.0,
                    "bkr_price_imply": "15233.66409978098835205736",
                    "adl_sort": 1
                }
            ],
            "message": "OK"
        }
        """
        path = '/v1/position/pending'
        params = {}
        if market:
            params['market'] = market

        return self.request_client.get(path, params)

    def query_order_finished(self, market, side, offset, limit=100):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            side	Integer	Yes	委托类型 0:全部(买与卖) 1:卖, 2: 买
            offset	Integer	Yes	偏移量，即从哪条开始获取
            limit	Integer	Yes	一次获取记录数，默认为20条，最大为100条

        # Request
        POST https://api.coinex.com/perpetual/v1/order/finished
        {
            'access_id': 'BFFA64957AA240F6BBEA26FXXXX',
            'market': 'BTCUSD',
            'side': 2,
            'offset': 0,
            'limit': 100,
            'time': 1550748047
        }

        # Response
        {
            "data": {
                "records": [
                    {
                        "user_id": 12,
                        "source": "API",
                        "update_time": 1569248726.511807,
                        "order_id": 8337543,
                        "price": "9723",
                        "deal_stock": "0.01647058823529411764",
                        "deal_profit": "0.0007184580597463307",
                        "leverage": "3",
                        "position_id": 0,
                        "deal_fee": "0.00001235294117647058",
                        "market": "BTCUSD",
                        "position_type": 2,
                        "create_time": 1569248726.511796,
                        "amount": "160",
                        "taker_fee": "0.00075",
                        "type": 1,
                        "target": 0,
                        "side": 2,
                        "effect_type": 1,
                        "left": "0",
                        "maker_fee": "-0.00025"
                    }
                ],
                "offset": 1,
                "limit": 1
            },
            "code": 0,
            "message": "OK"
        }
        """
        path = '/v1/order/finished'
        params = {
            'market': market,
            'side': side,
            'offset': offset,
            'limit': limit
        }
        return self.request_client.get(path, params)

    def query_order_status(self, market, order_id):
        """
        # Request
        POST https://api.coinex.com/perpetual/v1/order/status
        {
            'access_id': 'BFFA64957AA240F6BBEA26FXXXX',
            'market': 'BTCUSD',
            'order_id': 2,
            'time': 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
                "user_id": 12,
                "deal_stock": "0",
                "order_id": 8397331,
                "target": 0,
                "position_id": 0,
                "update_time": 1569295003.825343,
                "create_time": 1569295003.825343,
                "price": "9988",
                "side": 2,
                "amount": "10",
                "market": "BTCUSD",
                "position_type": 2,
                "type": 1,
                "taker_fee": "0.00075",
                "effect_type": 1,
                "deal_profit": "0",
                "leverage": "3",
                "source": "API",
                "left": "10",
                "maker_fee": "-0.00025",
                "deal_fee": "0",
                "status": "not_deal"
            },
            "message": "OK"
        }
        """
        path = '/v1/order/status'
        params = {
            'market': market,
            'order_id': order_id
        }
        return self.request_client.get(path, params)

    def query_user_deals(self, market, offset, limit=100, side=0):
        """
        # params:
            market	String	Yes	合约市场，例如BTCUSD, ALL：表示所有市场
            side	Integer	Yes	委托类型 0:全部(买与卖) 1:卖, 2: 买
            offset	Integer	Yes	偏移量，即从哪条开始获取
            limit	Integer	Yes	一次获取记录数，默认为20条，最大为100条
            start_time	Integer	Y	
            end_time	Integer	Y	
        # Request
        POST https://api.coinex.com/perpetual/v1/market/user_deals
        {
            'access_id': 'BFFA64957AA240F6BBEA26FXXXX',
            'market': 'BTCUSD',
            'side': 2,
            'offset': 0,
            'limit': 100,
            'time': 1550748047
        }

        # Response
        {
            "data": {
                "offset": 0,
                "records": [
                    {
                        "price": "10202.78",
                        "margin_amount": "0.23849878448422181142",  //成交后的仓位保证金
                        "position_amount": "7312",
                        "deal_type": 3,     1, //1 open position, 2 add position, 3 sub position, 4 close position, 5 sys close, 6 position liq, 7 position adl
                        "id": 161047,
                        "market": "BTCUSD",
                        "time": 1568791743.216231,
                        "fee_rate": "0",
                        "position_id": 123,
                        "amount": "5",
                        "open_price": "10219.47905950375373185054",
                        "leverage": "3",
                        "order_id": 6144365,
                        "deal_insurance": "0",  // 消耗或增加的保险基金
                        "user_id": 12,
                        "deal_user_id": 12,
                        "role": 1,  //1: maker, 2: taker
                        "deal_margin": "0.0001630872432195171", //交易的保证金
                        "deal_order_id": 6144366,
                        "side": 1,  //1: sell, 2: buy
                        "position_type": 2,
                        "deal_profit": "-0.0000008007827998907",
                        "deal_fee": "0",
                        "deal_stock": "0.00049006251237407843"  
                    }
                ],
                "limit": 1
            },
            "code": 0,
            "message": "OK"
        }
        """
        path = '/v1/market/user_deals'
        params = {
            'market': market,
            'side': side,
            'offset': offset,
            'limit': limit,
        }
        return self.request_client.get(path, params)

    def adjust_margin(self, market, amount, adjust_type):
        """
        # params:
            market	String	Yes	合约市场, 例如：BTCUSD
            amount	String	Yes	调整额度
            type	Integer	Yes	调整类型：1表示增加保证金，2表示减少保证金

        # Request
        POST https://api.coinex.com/api/perpetual/v1/position/adjust_margin
        {
            "access_id" : "BFFA64957AA240F6BBEA26FXXXX",
            "market": "BTCUSD",
            "amount": "10.12",
            "type": 1,
            "time": 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
                "profit_real": "-0.00013473733333333333",
                "liq_order_price": "0",
                "position_id": 67,
                "margin_amount": "50.00006666666666666667",
                "user_id": 12,
                "finish_type": 1,
                "sys": 0,
                "total": 4,
                "market": "BTCUSD",
                "mainten_margin": "0.005",
                "profit_clearing": "0",
                "open_val": "0.00020000000000000000",
                "update_time": 1568204207.577103,
                "create_time": 1568195992.528048,
                "liq_price": "Infinity",
                "amount": "2",
                "open_val_max": "0.00100000000000000000",
                "close_left": "2",
                "type": 1,
                "open_margin_imply": "150000.33333333333333335000",
                "liq_time": 0.0,
                "mainten_margin_amount": "0.00000100000000000000",
                "side": 1,
                "bkr_price": "Infinity",
                "adl_sort": 4,
                "leverage": "5",
                "open_margin": "250000.33333333333333335000",
                "amount_max": "10",
                "open_price": "10000.00000000000000000000",
                "liq_profit": "0",
                "liq_order_time": 0.0,
                "adl_sort_val": "0.03999994",
                "liq_amount": "0",
                "liq_price_imply": "Infinity",
                "bkr_price_imply": "Infinity"
            },
            "message": "OK"
        }
        """
        path = '/v1/position/adjust_margin'
        data = {
            'market': market,
            'amount': amount,
            'type': adjust_type
        }
        return self.request_client.post(path, data)

    def adjust_leverage(self, market, position_type, leverage):
        """
        # params:
            market	String	Yes	合约市场, 例如：BTCUSD
            leverage	String	Yes	调整杠杆大小，在不同风险限额下，只能取某些值，具体参考合约规则文档
            position_type	Integer	Y	1 逐仓 2 全仓

        # Request
        POST https://api.coinex.com/perpetual/v1/market/adjust_leverage
        {
            "access_id":"BFFA64957AA240F6BBEA26FXXXX",
            "market":"BCHUSD",
            "leverage": 10,
            "time": 1550748047
        }

        # Response
        {
            "code": 0,
            "data": {
                "position_type": 2,
                "leverage": "3"
            },
            "message": "OK"
        }

        """
        path = '/v1/market/adjust_leverage'
        data = {
            'market': market,
            'position_type': position_type,
            'leverage': leverage
        }
        return self.request_client.post(path, data)


if __name__ == "__main__":
    access_id = ''
    secret_key = ''
    api = CoinexContractApi(access_id, secret_key)
    print(api.ping())
