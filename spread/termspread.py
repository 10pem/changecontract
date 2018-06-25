"""
统计各个合约的价差
"""

import numpy as np
import pandas as pd
import tushare as ts
import json
import os
from matplotlib import pyplot as plt

from mymodule import sa

DATA_PATH = 'C:\\Users\\Bin.Xu\\Desktop\\data'
SETTING_FILE_NAME = 'termSpread.json'

def readJson(file):
    dir = os.path.split(__file__)[0]
    path = os.path.join(dir, SETTING_FILE_NAME)

    with open(path, 'r') as f:
        data = json.load(f)

    return data


def calcSpread(left, right, minute='5'):
    """计算价差"""
    leftDf = sa.get_future_data(left, minute)
    rightDf = sa.get_future_data(right, minute)

    data = leftDf.join(rightDf, lsuffix=left, rsuffix=right)
    spreadName = 'sp' + left[-2:] + right[-2:]
    data[spreadName] = data['close' + left] - data['close' + right]

    return data[['close' + left, 'close' + right, spreadName]].sort_index()



class Spread(object):
    """价差通用类"""

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.data = None
        self.spreadName = ''
        self.calcSpread()
        self.show()


    def calcSpread(self, minute='5'):
        """计算价差"""
        leftDf = sa.get_future_data(self.left, minute)
        rightDf = sa.get_future_data(self.right, minute)

        data = leftDf.join(rightDf, lsuffix=self.left, rsuffix=self.right)
        self.spreadName = 'sp' + self.left[-2:] + self.right[-2:]
        data[self.spreadName] = data['close' + self.left] - data['close' + self.right]

        self.data = data[['close' + self.left, 'close' + self.right, self.spreadName]].sort_index()


    def show(self):
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111)
        plt.plot(self.data.iloc[:, -1].values, 'g', label=self.data.iloc[:, -1].name)
        plt.twinx()
        plt.plot(self.data.iloc[:, 0].values, 'r', label=self.data.iloc[:, 0].name)
        plt.title(self.spreadName)
        plt.grid(True)
