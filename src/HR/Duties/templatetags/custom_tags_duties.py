from django import template
register = template.Library()
import os
from django.conf import settings


@register.filter(name="custom_stringformat")
def custom_stringformat(string1,string2):
    return str(string1).format(string2)


@register.filter(name="check_img_ex")
def check_img_ex(teamcode):
    prefix = "EIT/images/TeamIcon"
    src = str("/static_eit/"+prefix+"/{teamcode}.png").format(teamcode=teamcode)
    if not os.path.exists(os.path.join(settings.STATIC_ROOT_EIT,prefix+"/{teamcode}.png".format(teamcode=teamcode))):
        src = "/static_eit/EIT/images/DefaultDutiesTeam.png"
    return src


@register.filter(name="check_img")
def check_img(src,defualt):
    if not os.path.exists(defualt):
        return src
    return defualt


@register.filter(name="get_dict_key_c")
def get_dict_key_c(_key,_dict):
    if _key in _dict:
        if "conditions" in _dict[_key]:
            return _dict[_key]["conditions"]
    return ''


@register.filter(name="get_dict_key_d")
def get_dict_key_d(_key,_dict):
    if _key in _dict:
        if "duties" in _dict[_key]:
            return _dict[_key]["duties"]
    return ''


@register.filter(name="get_dict")
def get_dict(_key,_dict):
    if _key in _dict:
        return _dict[_key]
    return ''


@register.filter(name="timedelta_to_years")
def timedelta_to_years(timedelta):
    if timedelta:
        return int(timedelta.days / 365)
    return ''