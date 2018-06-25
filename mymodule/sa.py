"""
新浪期货api接口
"""


import pandas as pd
from datetime import datetime
import json
import requests


def get_future_data(code, t=''):
    """
    获取期货数据接口
    --------------------
    
    Parameters
    ----------
    code : str
        代码
    t: str
        数据周期
    
    Returns
    -------
    df: pandas.DataFrame
        
    """
    if not t:
        t = 'DailyKLine'
    else:
        t = 'MiniKLine{}m'.format(t)
    
    if code[:2] in ["IC", 'IH', 'IF']:
        line = 'http://stock2.finance.sina.com.cn/futures/api/json.php/CffexFuturesService.getCffexFutures{t}?symbol={code}'.format(code=code, t=t)
    else:
        line = 'http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFutures{t}?symbol={code}'.format(code=code, t=t)
    
    
    df = pd.read_json(line)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'amount']
    try:
        df.index = list(map(lambda x:datetime.strptime(x, '%Y-%m-%d'), df.date))
    except:
        df.index = list(map(lambda x:datetime.strptime(x, '%Y-%m-%d %H:%M:%S'), df.date))

    return df


def get_realtime_quotes(code):
    """
    返回实时数据
    需要提供接受多个合约代码的功能
    """
    data = requests.get('http://hq.sinajs.cn/list=' + code).content.decode('gbk')
    l = data.split(',')
    d = {}
    d['symbol'] = l[0][l[0].index('str_')+4:l[0].index('=')]
    #d['']
    return d

