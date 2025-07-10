import json
import os
import socket
import traceback


from django.shortcuts import render,reverse, redirect
from .models import DocumentFlow,Document
import Systems.models as SystemsModel
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.http.response import JsonResponse
from django.http import StreamingHttpResponse
from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services



def get_current_server_ip():
    socket.gethostbyname(socket.gethostname())
    ip = socket.gethostbyname(socket.getfqdn())
    return ip


def check_and_set_cookie(request, response):
    team = request.COOKIES.get('team')
    user_team_roles = request.user.team_roles["current"] if request.user.team_roles else []
    if team:
        if team not in [item.get('team_code') for item in user_team_roles]:
            response.set_cookie('team',user_team_roles[0].get('team_code'))
    else:
        response.set_cookie('team', user_team_roles[0].get('team_code'))
    return response


def my_cartable(request):
    api_client = new_api_client(request)
    username = request.user.username + "@eit"
    user_team_roles = request.user.team_roles["current"] if request.user.team_roles else []
    context = {}
    
    _, _, all_apps_urls = services.get_all_apps_url(api_client=api_client)
    _, _, all_users = services.get_all_users(api_client=api_client)  
    all_users = {str(item.get('UserName')).lower():item for item in all_users}
    inbox = DocumentFlow.objects.filter(InboxOwner=username, IsVisible=True).order_by('-ReceiveDate')
    outbox = DocumentFlow.objects.filter(SenderUser=username).order_by('-id')
    my_document = Document.objects.filter(DocumentOwner=username).values_list('id')
    mybox = DocumentFlow.objects.filter(DocumentId__in=my_document).order_by('-ReceiveDate')
    _, _, all_apps = services.get_all_apps_info(params={"return-dict":"1"}, api_client=api_client)
    prefix_url_get_timed_email = all_apps.get('ProcessManagement').get('FullUrl')
    user_teams_rows = [{'TeamCode':item.get('TeamCode'),'TeamName':item.get('TeamName')} for item in user_team_roles] if user_team_roles else []
    context.update({'server_ip':get_current_server_ip(),'all_apps_urls':all_apps_urls,'user_teams_rows':user_teams_rows})
    context.update({'rows':inbox,'sender_rows':outbox,'my_cartable_rows':mybox ,'prefix_url_get_timed_email':prefix_url_get_timed_email,'all_users':all_users,'all_users_json':json.dumps(all_users)})
    response = render(request,'Cartable/my_cartable.html',context=context)
    response = check_and_set_cookie(request, response)
    return response


@csrf_exempt
def my_cartable_ajax(request):
    api_client = new_api_client(request)
    activeid = request.GET.get('activeid')
    username = request.user.username + "@eit"
    _, _, all_apps_urls = services.get_all_apps_url(api_client=api_client)
    context = {'activeid':activeid,'server_ip':get_current_server_ip(),'all_apps_urls':all_apps_urls}
    inbox = DocumentFlow.objects.filter(InboxOwner=username,IsVisible=True).order_by('-ReceiveDate')
    outbox = DocumentFlow.objects.filter(SenderUser=username).order_by('-id')
    my_document = Document.objects.filter(DocumentOwner=username).values_list('id')
    mybox = DocumentFlow.objects.filter(DocumentId__in=my_document).order_by('-ReceiveDate')
    context.update({'rows':inbox,'sender_rows':outbox,'my_cartable_rows':mybox})
    return render(request,'Cartable/my_cartable_ajax.html',context=context)



def doc_flow_sse(request):
    username = request.user.username + "@eit"
    def event_stream():
        rows = list(DocumentFlow.objects.filter(InboxOwner=username, SendDate__isnull=True,IsVisible=True).order_by('-id'))
        sender_rows = list(DocumentFlow.objects.filter(InboxOwner=username, SendDate__isnull=False,IsVisible=True).order_by('-id'))
        my_cartable_rows = list(DocumentFlow.objects.filter(SenderUser=username, PreviousFlow_id__isnull=True,IsVisible=True).order_by('-id'))
        return "data: {'rows':"+str(rows)+",'sender_rows':"+str(sender_rows)+",'my_cartable_rows':"+str(my_cartable_rows)+"} \n\n"

    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')





def find_app_from_all_apps(_dict,id):
    ret = None
    for item in _dict:
        if int(item.get('id')) == int(id):
            ret = item
            break
    return ret


def GetPermittedSystemlist(request,username):
    api_client = new_api_client(request)
    SystemCategory = SystemsModel.SystemCategory.objects.all()
    systemlist = []
    _, _, all_apps_url = services.get_all_apps_url(api_client=api_client)
    for s in SystemCategory:
        if s.HasURL:
            try:
                RelatedURL = SystemsModel.SystemCategoryURL.objects.filter(SystemCategory_id=s.id).first()
                app_url_id = RelatedURL.AppURL
                app_url = find_app_from_all_apps(all_apps_url,app_url_id)
                if app_url is None:
                    continue
                app_code = app_url.get('AppCode')
                _, _, app = services.get_app_by_appcode(app_code, api_client=api_client)
                AppLabel = app.get('AppLabel')
                data = services.get_user_urls(AppLabel, username, api_client=api_client)
                haspermission=data.get('HasPermission')
                if haspermission:
                    systemlist.append(s)
                    ParentId = s.Parent_id
                    ParentExist = SystemsModel.SystemCategory.objects.filter(id=ParentId).count()
                    while ParentExist > 0:
                        QS = SystemsModel.SystemCategory.objects.get(id=ParentId)
                        ParentId = QS.Parent_id
                        ParentExist = SystemsModel.SystemCategory.objects.filter(id=ParentId).count()
                        systemlist.append(QS)
            except:
                pass
                traceback.print_exc()
    return systemlist


def LoadSystems(request):
    UserName = request.user.username + "@eit"
    user_team_roles = request.user.team_roles["current"] if request.user.team_roles else []
    TeamCode = user_team_roles[0].get('TeamCode')
    try:
        SystemCategory=GetPermittedSystemlist(request,UserName)
    except:
        traceback.print_exc()
        print("Access Control App is not running...")
    SystemList = []
    for s in SystemCategory:
        FullURL=''
        if s.HasURL:
            FullURL=s.RelatedURL
            FullURL = FullURL.replace("192.168.50.15","192.168.20.81")
            FullURL = FullURL.replace('@TeamCode','')
            FullURL = FullURL.replace('@UserName', '')
            FullURL = FullURL.replace('@username', '')
            tmp = FullURL.split("/")
            tmp = [item for item in tmp if item]
            FullURL = "/".join(tmp)
            FullURL += '/?team='+TeamCode
        System = {
                'FullURL':FullURL,'Title':s.Title,'Parent':s.Parent_id
                ,'HasURL':s.HasURL,'id':s.id,'Icon':s.Icon,'Level':s.Level
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

    response = render(request, 'Portal/Systems.html', content)
    return response


def refresh_logout(request):
    logout(request)
    response = redirect(reverse('AuthUser:auth_detect'))
    response.delete_cookie(key='access')
    response.delete_cookie(key=os.getcwd().split("\\")[-1] + '_sessionid')
    return response


@csrf_exempt
def exit_from_cartable(request, id):
    UserName = request.user.username + "@eit"
    doc_flow = DocumentFlow.objects.filter(id=id,InboxOwner=UserName).first()
    if doc_flow:
        if doc_flow.IsVisible is True:
            doc_flow.IsVisible = False
            doc_flow.save()
            return JsonResponse({'state':'ok','updated_before':0},status=200)
        elif doc_flow.IsVisible is False:
            return JsonResponse({'state': 'ok', 'updated_before': 0,'not_change_this':1}, status=200)

    return JsonResponse({'state':'error'},status=400)


def workflow_visual(request, doc_id):
    return render(request, "Cartable/WorkFlow.html",context={"doc_id": doc_id})

