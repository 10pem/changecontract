"""
自动根据当昨天是否是停牌状态进行各个股票的需要持仓数量进行计算;
TODO: 手动更改各股票下单数量;
"""

import tushare as ts
from mymodule.mongo import connect
import numpy as np
import pandas as pd
import datetime as dt
import csv


db = connect('TuShareDaily')
last = ts.get_k_data("hs300").iloc[-1, 0]
LASTTRADEDAY = last[:4] + last[5:7] + last[8:10]


def calc():
    """计算各个股票的应有持仓股数"""
    weight = ts.get_hs300s()
    hs = ts.get_k_data('hs300')
    date = str(weight.date[0])[:10]
    spot = float(hs[hs.date == date].close)
    portfolioValue = spot * 300

    weight['value'] = weight['weight'] * portfolioValue
    weight['close'] = weight.apply(getPrice, axis=1)
    weight['theoNum'] = weight['value'] / weight['close']
    weight['flag'] = weight.apply(getFlag, axis=1)

    allocateValue = weight.value.sum() - (weight.value * weight.flag).sum()
    perAllocateValue = allocateValue / weight.flag.sum()
    weight['adjustValue'] = weight.apply(adjustValue(perAllocateValue), axis=1)
    return weight


def getPrice(x):
    """从数据库获取价格数据"""
    code = x.code
    date = x.date.strftime('%Y%m%d')
    close = db[code].find_one({"date": date})['close']
    return close


def getFlag(x):
    """对当日是否可以交易进行标识"""
    code = x.code
    volume = db[code].find_one({"date": LASTTRADEDAY})['volume']
    if not volume > 100:
        flag = False
    else:
        flag = True
    # TODO: 通过交易所网站更新flag标识
    return flag


def adjustValue(perAllocateValue):
    """
    对每个股票分配的市值进行调整
    :param
        data: DataFrame,the weight data
    :return
        df: DataFrame,
    """
    def adjust(x):
        if x['flag']:
            return x['value'] + perAllocateValue
        else:
            return 0
    return adjust         # TODO: 市值的调整方法待定


def  adjustNum(x):
    """对thenNum进行调整, 确定当日可以发单的数量"""
    return x['adjustValue'] / x['close']


def saveBook():
    """保存当天的发单表"""
    pass


def generateTradeDay():
    """生成交易日序列"""

    today = dt.date.today()
    oneday = dt.timedelta(1)

    with open('TradeDay.csv', 'w') as f:
        f_csv = csv.DictWriter(f)
        for i in range(365):
            curr = today + i * oneday
            if curr.isoweekday() == 6 or curr.isoweekday() == 7:
                description = 'weekend'
            else:
                description = ''
            record = (str(curr), description)
            f_csv.writerow(record)


def getIsChange():
    """查询交易所网站, 核对停复盘状态"""
    pass



