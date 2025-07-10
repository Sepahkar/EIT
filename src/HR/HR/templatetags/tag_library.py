from django import template
import re

register = template.Library()

persian_digits = {
    '0': '۰',
    '1': '۱',
    '2': '۲',
    '3': '۳',
    '4': '۴',
    '5': '۵',
    '6': '۶',
    '7': '۷',
    '8': '۸',
    '9': '۹',
}

@register.filter(name='to_persian')
def to_persian(value):
    """Convert numbers in a string or non-string to Persian format."""
    if value is None or value == "": 
        return 
    value_str = str(value)
    return re.sub(r'[0-9]', lambda x: persian_digits[x.group()], value_str)

@register.filter()
def zarb(num1,num2):
    return int(num1)*int(num2)

@register.filter(name='get_dic_key')
def get_dic_key(d, key):
    return d.get(key, '')



@register.filter()
def to_money(value):
    return '{:,}'.format(value).split(".")[0]


@register.filter(name="get_dict")
def get_dict(_d,key):
    if _d:
        if key in _d.keys():
            return _d.get(key)
    return ''


@register.filter(name="get_team_corp_value")
def get_team_corp_value(_l,keys):
    ret = ''
    try:
        if _l and len(keys.split(',')) == 2:

            arr = keys.split(',')
            team_name = arr[0]
            corp_name = arr[1]

            for item in _l:
                if item.get('corp') == corp_name and item.get('team') == team_name:
                    ret = item.get('weight')
                    ret = float(ret * 100)
                    ret = "{:.2f}".format(ret)
                    break
    except:
        ret = 0
    return ret

@register.filter(name="concat_str")
def concat_str(val1,val2):
    return val1 + ',' + val2



@register.filter(name="active_bookmark")
def active_bookmark(value, arg):
    if str(value) == arg:
        return 'active'
    return ''
