#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import hashlib
import json
import logging
import requests
import time
import traceback


class RequestClient(object):
    __headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
    }

    def __init__(self, access_id, secret_key, logger=None, debug=False):
        self.access_id = access_id
        self.secret_key = secret_key
        self.headers = self.__headers
        self.host = 'https://api.coinex.com/perpetual'
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter())
        session.mount('https://', requests.adapters.HTTPAdapter())
        self.http_client = session
        self.logger = logger or logging

    @staticmethod
    def get_sign(params, secret_key):
        data = ['='.join([str(k), str(v)]) for k, v in params.items()]

        str_params = "{0}&secret_key={1}".format(
            '&'.join(data), secret_key).encode()

        token = hashlib.sha256(str_params).hexdigest()
        return token

    def set_authorization(self, params, headers):
        headers['AccessId'] = self.access_id
        headers['Authorization'] = self.get_sign(params, self.secret_key)

    def get(self, path, params=None, sign=True):
        url = self.host + path
        params = params or {}
        params['timestamp'] = int(time.time()*1000)
        headers = copy.copy(self.headers)
        if sign:
            self.set_authorization(params, headers)
        try:
            response = self.http_client.get(
                url, params=params, headers=headers, timeout=5)
            # self.logger.info(response.request.url)
            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                self.logger.error(
                    'URL: {0}\nSTATUS_CODE: {1}\nResponse: {2}'.format(
                        response.request.url,
                        response.status_code,
                        response.text
                    )
                )
                return None
        except Exception as ex:
            trace_info = traceback.format_exc()
            self.logger.error('GET {url} failed: \n{trace_info}'.format(
                url=url, trace_info=trace_info))
            return None

    def post(self, path, data=None):
        url = self.host + path
        data = data or {}
        data['timestamp'] = int(time.time()*1000)
        headers = copy.copy(self.headers)
        self.set_authorization(data, headers)
        try:
            response = self.http_client.post(
                url, data=data, headers=headers, timeout=10)
            # self.logger.info(response.request.url)
            if response.status_code == requests.codes.ok:
                return response.json()
            else:
                self.logger.error(
                    'URL: {0}\nSTATUS_CODE: {1}\nResponse: {2}'.format(
                        response.request.url,
                        response.status_code,
                        response.text
                    )
                )
                return None
        except Exception as ex:
            trace_info = traceback.format_exc()
            self.logger.error('POST {url} failed: \n{trace_info}'.format(
                url=url, trace_info=trace_info))
            return None
