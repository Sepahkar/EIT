from django import template
from django.contrib.auth import get_user_model

UserModel = get_user_model()

register = template.Library()

@register.filter(name='get_user_profile_img')
def get_user_profile_img(username):
    if username:
        return "/media/HR/PersonalPhoto/"+username.replace("@eit","") + ".jpg"
    return ''


@register.filter(name='check_is_superuser')
def check_is_superuser(username):
    ret = False
    user = UserModel.objects.filter(username=username.replace("@eit", ""), is_active=True).first()
    if user and user.is_superuser:
        ret = True
    return ret


@register.filter(name='get_all_users')
def get_all_users(request):
    active_uesrs = UserModel.objects.filter(is_active=True)
    return active_uesrs


@register.filter(name='remove_duplicate_team')
def remove_duplicate_team(teams):
    _tmp = []
    _return_teams = []
    for item in teams:
        if item.get('TeamCode') not in _tmp:
            _tmp.append(item.get('TeamCode'))
            _return_teams.append(item)

    return _return_teams
