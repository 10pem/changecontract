"""
hs300 和 IF 的价差统计
"""

import pandas as pd
import numpy as np
import tushare as ts
from matplotlib import pyplot as plt
from datetime import datetime


from mymodule import sa
from mymodule.general import nextmonthsymbol
from mymodule.plot import date_deco
# from mymodule.mongo import connect


class spreads(object):

    def __init__(self, spotsymbol, futuresymbol, start, end):

        self.ret = pd.DataFrame()
        self.spot = ts.get_k_data(spotsymbol, '2015-01-01')[['date', 'close']]
        self.start = futuresymbol + start
        self.end = futuresymbol + end

    def calc(self):
        while True:
            future = sa.get_future_data(self.start)[['date', 'close']]

            df = pd.merge(future, self.spot, on='date', suffixes=[self.start, 'hs300'])
            df['spread'] = df['close' + self.start] - df['close' + 'hs300']
            df['name'] = '{}-{}'.format(self.start, 'hs300')
            self.ret = self.ret.append(df)

            self.start = nextmonthsymbol(self.start)
            if int(self.start[-4:]) > int(self.end[-4:]):
                break

    def plots(self):
        """画在一张图上"""
        groups = np.unique(np.array(self.ret['name']))
        fig, axis = plt.subplots(1, 1, figsize=(12, 9))
        for group in groups:
            data = self.ret[self.ret['name'] == group]
            axis.plot(list(data['spread']), label=group)
        plt.grid()
        plt.legend()
        # plt.show()

    @date_deco('%Y/%m%d')
    def plotone(self, spreadname):
        """
        画出单个价差数据
        :param spreadname: ser; self.ret.name like, IH1705-hs300;
        :return:
        """
        x = [datetime.strptime(x, '%Y-%m-%d') for x in self.ret[self.ret['name'] == spreadname]['date']]
        y = self.ret[self.ret['name'] == spreadname]['spread']
        s = self.ret[self.ret['name'] == spreadname]['closehs300']

        plt.plot(x, y, 'r', label='spread')
        plt.twinx()
        plt.plot(x, s, label='hs300')
        plt.grid()
        plt.legend()


if __name__ == '__main__':
    test = spreads('hs300', 'IF', '1601', '1612')
    test.calc()
    test.plots()
    plt.title('Future-Stocks in 2016')
    # test.plotone('IF1603-hs300')
    plt.show()
