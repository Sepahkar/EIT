import socket
import traceback
from django.shortcuts import render,redirect,reverse
import Systems.models as SystemsModel
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import get_user_model

from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services

UserModel = get_user_model()

def RedirectToLoadSystem(request):
    url = reverse('Systems:Systems_view')
    response = HttpResponseRedirect(url)

    delegate_user_logout = request.GET.get("delegate_logout")
    if delegate_user_logout and int(delegate_user_logout)==1:
        response.delete_cookie("portal_delegated_user", path="/")
        logout(request)
    return response

def find_app_from_all_apps(_dict,id):
    ret = None
    if _dict:
        for item in _dict:
            if item.get('id') and int(item.get('id')) == int(id):
                ret = item
                break
    return ret

def find_in_qs(_list,id):
    ret = None
    if _list:
        for item in _list:
            if int(item.id) == int(id):
                ret = item
                break
    return ret

def find_in_recursive(_list,id):
    qs = None
    for item in _list:
        if id is not None and int(item.id) == int(id):
            qs = item

    return qs


def find_all_childs(category_urls,categories):
    system_list = []
    cat_ids = []
    tmp = []
    dict_levels = {}
    for item in category_urls:
        a = 0
        if item.SystemCategory_id in tmp:
            continue
        tmp.append(item.SystemCategory_id)
        qs = categories.filter(id=item.SystemCategory_id).first()
        while qs:
            a+=1
            system_list.append(qs)
            cat_ids.append(qs.id)
            qs = categories.filter(id=qs.Parent_id).first()


    return system_list,cat_ids


def find_levels(SystemCategory):
    _d = {}
    categories = SystemsModel.SystemCategory.objects.all()

    for item in SystemCategory:
        if item.Parent_id is None:
            _d.update({str(item.id):0})

    for item in SystemCategory:
        if item.Parent_id is not None:
            parent_id = item.Parent_id
            level = 0
            while parent_id is not None:
                level += 1
                parent_id = categories.filter(id=parent_id).first().Parent_id
            _d.update({str(item.id):level})
    return _d

def get_http_host_ip(request):
    try:
        # one or both the following will work depending on your scenario
        socket.gethostbyname(socket.gethostname())
        return socket.gethostbyname(socket.getfqdn())
    except:
        return request.get_host().split(":")[0]


def check_and_set_cookie(request, response):
    team = request.COOKIES.get('team')
    user_team_roles = request.user.team_roles["current"] if request.user.team_roles else []
    if team:
        if team not in [item.get('team_code') for item in user_team_roles]:
            response.set_cookie('team',user_team_roles[0].get('team_code'))
    else:
        response.set_cookie('team', user_team_roles[0].get('team_code'))
    return response


def LoadSystems(request):
    api_client = new_api_client(request)
    UserName = request.user.username + "@eit"
    user_team_roles = (
        request.user.team_roles["current"] if request.user.team_roles else []
    )
    TeamCode = user_team_roles[0].get("team_code")
    TeamName = user_team_roles[0].get("team_name")
    try:
        _, _, all_user_urls = services.get_user_all_urls(
            UserName, api_client=api_client
        )
        ids = all_user_urls.get("ids")
        category_urls = SystemsModel.SystemCategoryURL.objects.filter(AppURL__in=ids)

        categories = SystemsModel.SystemCategory.objects.all()

        SystemCategory, cat_ids = find_all_childs(category_urls, categories)
        dict_levels = find_levels(SystemCategory)
        system_category_ids = SystemsModel.SystemCategoryURL.objects.filter(
            SystemCategory_id__in=cat_ids
        ).values_list("SystemCategory_id", flat=True)
    except:
        traceback.print_exc()
        print("Access Control App is not running...")

    _, _, all_apps_urls = services.get_all_apps_url(api_client=api_client)
    _, _, all_apps = services.apps(api_client=api_client)
    _, _, all_systems = services.systems(api_client=api_client)
    _, _, all_servers = services.servers(api_client=api_client)
    SystemList = []
    url = ""

    for s in SystemCategory:
        if s.id in system_category_ids:
            app_url_id = category_urls.filter(SystemCategory_id=s.id).first().AppURL # s.get('AppURL')
            for item in all_apps_urls:
                if int(item.get('id')) == int(app_url_id):
                    app_code = item.get('AppCode')
                    url = item.get('URL')
                    break

            for item in all_apps:
                if item.get('Code') == app_code:
                    system_code = item.get('SystemCode')
                    break

            for item in all_systems:
                if item.get('Code') == system_code:
                    system = item
                    server_id = item.get('Server')
                    break

            for item in all_servers:
                if int(item.get('id')) == int(server_id):
                    server = item

            server_id = system.get('Server')
            port_number = system.get('PortNumber')
            schema = "https://" if request.is_secure() else "http://"
            base_url = schema + server.get('IPAddress')
            filter_url = url if url.startswith("/") else '/' + url
            FullURL= base_url + ':' + str(port_number) + filter_url
            FullURL = FullURL.replace("192.168.50.15",get_http_host_ip(request))
            System = {
                'FullURL': FullURL,
                'Title': s.Title,
                'Parent': s.Parent_id,
                'HasURL': True,
                'id': s.id,
                'Icon': s.Icon,
                'Level': dict_levels.get(str(s.id)),
            }
        else:
            System = {
                'FullURL': '',
                'Title': s.Title,
                'Parent': s.Parent_id,
                'HasURL': False,
                'id': s.id,
                'Icon': s.Icon,
                'Level': dict_levels.get(str(s.id)),
            }

        SystemList.append(System)

    tmp_check = []
    tmp_SystemList = []
    for item in SystemList:
        if int(item.get('id')) not in tmp_check:
            tmp_check.append(int(item.get('id')))
            tmp_SystemList.append(item)
    SystemList = tmp_SystemList

    content ={
        'SystemList':SystemList,
    }

    list_teams = [item.get('TeamCode') for item in user_team_roles]
    list_teams = list(set(list_teams))
    content.update({'TeamName':TeamName,'TeamCode':TeamCode,'team_cookie':request.COOKIES.get('team')})
    response = render(request, 'Portal/Systems.html', content)
    response = check_and_set_cookie(request, response)
    return response



@csrf_exempt
def change_my_team(request):
    user_team_roles = request.user.team_roles["current"] if request.user.team_roles else []
    url = request.POST.get('next_url')
    response = redirect(url)
    if request.method == "POST":
        selected_team = request.POST.get('selected_team')
        if selected_team in [item.get('team_code') for item in user_team_roles]:
            response.set_cookie('team',selected_team)

    return response

@csrf_exempt
def generate_link_fake_user(request):
    if request.method == "POST":
        if request.user.is_superuser:
            change_to_username = request.POST.get('change_to_username')
            user = UserModel.objects.get(username=change_to_username.replace("@eit",""))
            if user.team_roles and user.team_roles["current"]: 
                response = JsonResponse(data={'state':"ok", "url":reverse("Systems:Systems_view")}, status=200)
                response.set_cookie("portal_delegated_user", change_to_username.replace("@eit",""), httponly=True)
                return response
            else:
                # the response should be 404 but the lovely Jquery doesnt runs fallbacks when got failure response!
                return JsonResponse(data={'state': 'error', 'details':f'There is no team / role for {change_to_username}'}, status=200)
        return JsonResponse(data={'state': 'error', 'details':'delegation requestor is not superuser'}, status=403)
    return JsonResponse(data={'state':'error', 'details':'method is not allowed'},status=405)