"""
    nextmonthsymbol : 获取期货下月合约
"""

def nextmonthsymbol(symbol, datelen=4):
    """
    获取期期货合约的下月合约
    Parameter:
        ----------
        symbol : str
            'IH1805'
        datelen : int
            symbol's datelen IH1804 -> 4, MA809 -> 3

    Returns:
        newright : str
            symbol like, IH1804
    """

    month = (symbol[-2:])

    if int(month) <= 11:
        newmonth = str(int(month) + 1).zfill(2)
        newright = symbol[:-2] + newmonth
    else:
        newmonth = '01'
        newyear = str(int(symbol[-datelen:-2]) + 1)
        newright = symbol[:-datelen] + newyear + newmonth

    return newright


if __name__ == '__main__':
    print(nextmonthsymbol('MA805'))