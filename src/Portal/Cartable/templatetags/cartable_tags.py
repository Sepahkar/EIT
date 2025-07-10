from django import template
register = template.Library()


@register.filter(name="get_app_url")
def get_app_url(_list,app_code):
    ret = ''

    if _list:
        for item in _list:
            if item.get('AppCode') == app_code:
                ret = item.get('URL')
                break
    return ret

@register.filter(name="get_system_port")
def get_system_port(_list,app_code):
    ret = ''

    if _list:
        for item in _list:
            if item.get('AppCode') == app_code:
                ret = item.get('APPPORT')
                break
    return ret


@register.filter(name="get_full_name_of_user")
def get_full_name_of_user(_dict,username):
    ret = ''
    if _dict and username:
        username = str(username).lower()
        if username in _dict:
            ret = _dict.get(username).get('FullName')
    return ret

