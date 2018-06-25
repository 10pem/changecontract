from datetime import datetime
from matplotlib import dates as mdates
from matplotlib import pyplot as plt

# 画图时使用日期数据进行x轴画图的装饰器

def date_plot(func, intype, otype, xt, y, *args, **kw):
    """
    对数据进行画图时自动画出日期序列
    -------------
    Parameters
    -------------
        func : function
            真正用来画图的函数
        intype : str
            xt的日期结构类型
        xt : iter
            可迭代的日期序列
        y : iter
            可迭代的y序列
    """
    xt = [datetime.strptime(x, intype) for x in xt]
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(otype))
    plt.gcf().autofmt_xdate()
    
    func(xt, y, *args, **kw)

# -------------------------------------------
def date_deco(otype):
    """
    对数据进行画图时自动画出日期序列的装饰器
    需要对时间数据手动改成datetime格式
    -------------
    """
    def plot_d(func):
        def wrapper(*args, **kw):
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(otype))
            plt.gcf().autofmt_xdate()
            func(*args, **kw)
        return wrapper
    return plot_d