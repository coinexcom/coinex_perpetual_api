#!/usr/bin/python3
# -*- coding: utf-8 -*-\

import websockets
import json
import hashlib
import time
import zlib
import ssl
import certifi
import asyncio
import logging

# https://websockets.readthedocs.io/en/stable/index.html

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

access_id = ""
secret_key = ""

class websocketTest(object):
    def __init__(self):
        super(websocketTest, self).__init__()
        self.url = "wss://perpetual.coinex.com"
        self.ws = ...
        self.order_bids = {}
        self.order_asks = {}

    def depth_merge(self, order_dict, message):
        if not order_dict:
            return
        for item in message:
            if item[1] == '0':
                del order_dict[item[0]]
            else:
                order_dict[item[0]] = item[1]

    def depth_checksum(self):
        asks = sorted(self.order_asks.items(), key=lambda s:s[0], reverse=False)
        bids = sorted(self.order_bids.items(), key=lambda s:s[0], reverse=True)

        check_sum_str = ""
        for item in bids:
            if len(check_sum_str) > 0:
                check_sum_str += ":"
            check_sum_str += item[0] + ":" + item[1]

        for item in asks:
            if len(check_sum_str) > 0:
                check_sum_str += ":"
            check_sum_str += item[0] + ":" + item[1]
        
        #print(check_sum_str)
        return zlib.crc32(bytes(check_sum_str, encoding="utf-8"))

    def depth_process(self, message):
        clean = message['params'][0]
        depth_data = message['params'][1]
        checksum = depth_data['checksum']
        if clean:
            self.order_bids.clear()
            for item in depth_data['bids']:
                self.order_bids[item[0]] = item[1]

            self.order_asks.clear()
            for item in depth_data['asks']:
                self.order_asks[item[0]] = item[1]
        else:
            if 'bids' in depth_data:
                self.depth_merge(self.order_bids, depth_data['bids'])
            
            if 'asks' in depth_data:
                self.depth_merge(self.order_asks, depth_data['asks'])

        print("bids")
        print(self.order_bids)
        print("asks")
        print(self.order_asks)

        if checksum == self.depth_checksum():
            print("checksum success")
        else:
            print("checksum failed !!!!!!!")

    def get_sign(self, time_int):
        str_params = "access_id={}&timestamp={}&secret_key={}".format(access_id, time_int, secret_key).encode()
        print("str_params", str_params)
        token = hashlib.sha256(str_params).hexdigest()
        print("str_params:", str_params, "token:", token)
        return token

    def sign(self):
        time_int = int(time.time() * 1000)
        token = self.get_sign(time_int)
        params = {"id":11, "method":"server.sign", "params":[access_id, token, time_int]}
        return params

    def ping(self):
        param = {"id": 1, "method": "server.ping", "params": []}
        return json.dumps(param)

    def depth_subscribe(self):
        params = {"id":11, "method":"depth.subscribe", "params":["BTCUSDT", 10, "0.01"]}
        return json.dumps(params)

    def bbo_subscribe(self):
        params = {"id":11, "method":"bbo.subscribe", "params":["BTCUSDT"]}
        return json.dumps(params)

    async def task(self):
        # start subscribe
        await self.ws.send(self.depth_subscribe()) # type: ignore

        # process message
        while True:
            message = await self.ws.recv() # type: ignore
            message_json = json.loads(message)
            if "method" in message_json:
                if message_json["method"] == "depth.update":
                    self.depth_process(message_json)
                else:
                    print("message: %s" % message)

    async def start(self, compress: str = "deflate"):
        # mote: must close websockets ping feature, set ping_interval to None
        self.ws = await websockets.connect(uri=self.url, compression=compress, ping_interval=None) # type: ignore

        # start subscribe and process message
        asyncio.create_task(self.task())

        # ping to coinex websocket server keep alive
        while True:
            await self.ws.send(self.ping())
            await asyncio.sleep(2)


if __name__ == '__main__':
    # 开启运行状态追踪。debug 的时候最好打开它，便于追踪定位问题。https://websockets.readthedocs.io/en/stable/topics/logging.html#log-levels
    logging.basicConfig(format="%(message)s",level=logging.DEBUG,)

    loop = asyncio.get_event_loop()
    asyncio.run(websocketTest().start())

