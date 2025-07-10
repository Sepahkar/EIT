from jdatetime import datetime as jdatetime

def to_shamsi(date):
    return jdatetime.fromgregorian(date=date).strftime(f'%Y/%m/%d')

