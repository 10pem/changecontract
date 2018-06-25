"""
Tushare Api 的包装装饰器
"""

import tushare as ts

# 定义装饰器直接进行数据筛选
def get_choosen(func):
    def wrapper(*args, **kw):
        """对func返回的数据进行删选"""
        df = func(*args, **kw)
        # 下面返回函数里面写了args[1]来获取 newdata这个数据
        return df.loc[list(map(lambda x:x in args[0], df.code))]
    return wrapper


@get_choosen
def profit_data(stocklist):
    return ts.profit_data()