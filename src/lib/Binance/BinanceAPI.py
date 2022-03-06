import hashlib
import hmac
import json
import requests
from time import time

class BinanceAPI:
    def __init__(self):
        self.config = json.loads(open("./BinanceConfig.json", "r").read())
        self.url = "https://api.binance.com/api/v3"
        self.accounts = self.getAccounts()["balances"]

    def getCandles(self, symbol, period = "1m", start = ""):
        url = self.url + "/klines?symbol={}&interval={}".format(symbol, period)
        if start != "":
            url = url + "&startTime={}".format(start)
        return requests.get(url).json()


    def getAccounts(self):
        url = self.url + "/account"
        sign = "timestamp=" + str(round(time() * 1000))
        h = hmac.new(bytes(self.config["secret"], "utf-8"), bytes(sign, "utf-8"), hashlib.sha256).hexdigest()
        url = url + "?" + sign + "&signature=" + h
        return requests.get(url, headers={"X-MBX-APIKEY": self.config["key"]}).json()

    def getAccount(self, symbol):
        self.accounts = self.getAccounts()["balances"]
        for account in self.accounts:
            if account["asset"] == symbol:
                return account
        return 0

    def createOrder(self, side, size):
        url = self.url + "/order?"
        sign = "timestamp=" + str(round(time() * 1000)) + "&symbol=ADAUSDT&type=market&side=" + side
        if (side == "buy"):
            sign = sign + "&quoteOrderQty="+ str(round(size - 1))
        else:
            sign = sign + "&quantity=" + str(round(size - 1))
        h = hmac.new(bytes(self.config["secret"], "utf-8"), bytes(sign, "utf-8"), hashlib.sha256).hexdigest()
        url = url+sign+"&signature="+h
        return requests.post(url, headers={"X-MBX-APIKEY": self.config["key"]}).json()

    def ticker(self, symbol = "ADAUSDT"):
        return requests.get(self.url + "/ticker/price?symbol="+symbol).json()