"""
统计当月和下月合约的价差
"""
import tushare as ts
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import math

from mymodule import sa
from mymodule import general as ge
from mymodule.plot import date_plot


class spreadCalc(object):

    def __init__(self, symbol, start, end):
        """
        Paramters:
            symbol : str
                IH like
            start, end : str
                合约时间， 1801 like
        """
        self.left = symbol + start
        self.right = symbol + start
        self.end = symbol + end
        self.df = sa.get_future_data(self.left)

        self.spreadDataList = [] # [{name:spreadname, t:[timeseries], spread:[spreadlist], spot:[dataframe]}, spread2, ...]

    # --------------------------------------
    def calc(self):
        """
        计算spread数据
        :return:
        """
        d = {}

        df1 = self.df
        df2 = sa.get_future_data(self.right)
        suffixes = [self.left, self.right]
        data = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=suffixes)
        spread = data['close'+ self.left] - data['close' + self.right]

        d['name'] = self.left + '-' + self.right
        d['spread'] = list(spread)
        d['timeser'] = list(data['date' + self.left])
        d['spot'] = list(data['close' + self.left])
        self.spreadDataList.append(d)

        self.df = df2

    def start(self):
        while self.right != self.end:
            self.right = ge.nextmonthsymbol(self.right)
            self.calc()
            self.left = self.right

    def plot(self, x):
        """
        :param x:
        :return:
        """
        fig = plt.figure(figsize=(12, 9))
        ax = plt.subplot(111)

        d = self.spreadDataList[x]
        #get_date_plot(plt.plot, )
        plt.plot(d['timeser', d['spread']])

    def boxplot(self, x):
        fig = plt.figure(figsize=(12, 9))
        ax = plt.subplot(111)
        data = self.spreadDataList[x]['spread']
        plt.boxplot(data)

    def getplos(self):
        fignum = math.ceil(len(self.spreadDataList) / 4)

        n = 0
        for i in range(fignum):
            fig, axes = plt.subplots(3, 4, sharey='row', figsize=(12, 9))
            subplots_adjust(wspace=0, hspace=0)

            for subi in range(4):
                try:
                    ind = i * 4 + subi
                    data = self.spreadDataList[ind]['spread']
                    name = self.spreadDataList[ind]['name']
                    spot = self.spreadDataList[ind]['spot']
                    timeser = self.spreadDataList[ind]['timeser']

                except:
                    data = []
                    spot = []
                    timeser = []
                    name = ''
                    print('data get end')


                ax = axes[0, subi]
                ax.boxplot(data)
                ax.set_title(name)

                ax2 = axes[1, subi]
                date_plot(ax2.plot, '%Y-%m-%d', '%Y/%m/%d', timeser, data, 'g-',label='spread')

                ax3 = axes[2, subi]
                date_plot(ax3.plot, '%Y-%m-%d', '%Y/%m/%d', timeser, spot, 'r-',label='close')
                #ax2.set_title(name)

            # plt.grid()
            filename = 'C:\\users\\Bin.Xu\\Desktop\\spreadFig\\sn_{}.png'.format(name)
            plt.savefig(filename, dpi=500)
            #plt.show()
            n += 1

    def outputdata(self):
        """输出数据"""
        for spreadData in self.spreadDataList:
            name = spreadData.pop('name')
            df = pd.DataFrame(spreadData)
            filename = 'C:\\users\\Bin.Xu\\Desktop\\spreadData\\sn_{}.csv'.format(name)
            df.to_csv(filename)



if __name__ == '__main__':
    import math
    from matplotlib.pylab import subplots_adjust

    ana = spreadCalc('IH', '1505', '1805')
    ana.start()
    ana.getplos()
    ana.outputdata()
