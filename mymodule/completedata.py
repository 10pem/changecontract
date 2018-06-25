"""
股票日线数据库的维护,包括区间维护, 日常维护, 单独个股数据维护;
完成内容主要是:
    1. 缺失值数据处理(停牌期过长比如超过8个月可能出现错误的情况)
        停牌期间个股所有价格设定为最近的收盘价, 成交量设定为0;
    2. 数据对齐
--------------------------------------
可能存在的问题, 超长期的停牌个股可能会出现无法补录数据的情况
"""

from datetime import datetime
import tushare as ts
import datetime as dt
from mymodule.mongo import connect


CREATE = True

def completestockdata(start, end):
    """
    构建股票数据库的函数, 完成数据对齐的操作
    :param start:str，2017-01-02
    :param end:str, 2017-12-21
    :return:
    """
    db = connect('TuShareDaily')
    failedList = []

    codes = list(ts.get_today_all().code)
    print('\n获取股票code列表完成')
    datalen = len(ts.get_k_data('hs300', start=start, end=end))

    date2 = datetime.strptime(start ,'%Y-%m-%d') - dt.timedelta(250)    # 三个月前的数据
    start = date2.strftime('%Y-%m-%d')
    # 利用指数数据时间进行数据时间对齐的操作
    # 同时对于是否停牌进行标识
    data = ts.get_k_data('hs300', start=start, end=end).set_index('date')[[]]

    for code in codes:
        coll = db[code]
        if CREATE:
            coll.create_index("datetime", unique=True)
        try:
            df = ts.get_k_data(code, start, end).set_index('date')[['open', 'high', 'low', 'close', 'volume']]
            df = data.join(df)
            df['close'] = df.close.fillna(method='ffill')
            df = df.apply(naHandle, axis=1)
            df['date'] = [x[:4] + x[5:7] + x[8:10] for x in df.index]
            df['datetime'] = [datetime.strptime(x, '%Y-%m-%d') for x in df.index]
            df = df.tail(datalen)
            df.dropna(inplace=True) # 针对新股, 去掉新股数据前期的空值数据
            coll.insert_many(df.to_dict(orient='records'))

        except:
            failedList.append(code)

    print('-' * 30)
    for code in failedList:
        completeSingle(code, start, end)

    print('End building')

def naHandle(r):
    """按行处理空值数据"""
    if not r.volume >= 1:
        r.volume = 0
        r.open = r.close
        r.high = r.close
        r.low = r.close
    return r

def dailyUpdate(n=1):
    """
    利用TuShare的get_today_all进行数据更新, 不可跨日;
    -----------------

    Param: n 上一个交易日距离今天的日期
        在早上开盘补充数据是需要传入这个参数, 默认为1, 代表上昨天就是上一个交易日;
    """

    # 获得的data没有其他数据, 只有一个收盘价格
    db = connect('TuShareDaily')
    data = ts.get_today_all()[['code', 'open', 'high', 'low', 'trade', 'volume']]
    data.columns = ['code','open', 'high', 'low', 'close', 'volume']
    today = datetime.now()
    lastday = today - dt.timedelta(n)
    data = data.apply(naHandle, axis=1) # 这里获得的数据已经是可存储数据

    if today.time() > dt.time(15, 0):   # 在下午收盘之后进行数据的补充
        data['date'] = today.date().strftime('%Y%m%d')
        data['datetime'] = dt.datetime(today.year, today.month, today.day)
    else:       # 在早上进行前一个交易日数据的补充
        data['date'] = lastday.date().strftime('%Y%m%d')
        data['datetime'] = dt.datetime(lastday.year, lastday.month, lastday.day)

    for i in range(len(data)):
        temp = data.iloc[i].to_dict()
        stock = temp.pop('code')
        db[stock].update({'date':temp['date']}, temp, upsert=True)


def completeSingle(code, start, end):
    """补充单个股票的数据"""

    db = connect('TuShareDaily')
    datalen = len(ts.get_k_data('hs300', start=start, end=end))

    date2 = datetime.strptime(start, '%Y-%m-%d') - dt.timedelta(400)
    start = date2.strftime('%Y-%m-%d')
    data = ts.get_k_data('hs300', start=start, end=end).set_index('date')[[]]

    coll = db[code]
    if CREATE:
        coll.create_index("datetime", unique=True)
    try:
        df = ts.get_k_data(code, start, end).set_index('date')[['open', 'high', 'low', 'close', 'volume']]
        df = data.join(df)
        df['close'] = df.close.fillna(method='ffill')
        df = df.apply(naHandle, axis=1)
        df['date'] = [x[:4] + x[5:7] + x[8:10] for x in df.index]
        df['datetime'] = [datetime.strptime(x, '%Y-%m-%d') for x in df.index]
        df = df.tail(datalen)
        df.dropna(inplace=True) # 针对新股, 去掉空值数据
        coll.insert_many(df.to_dict(orient='records'))

    except:
        print('Failed to complete {}'.format(code))


if __name__ == '__main__':
    start = '2018-06-11'
    end =  '2018-06-18'
    print('make sure your have time')
    completestockdata(start, end)
