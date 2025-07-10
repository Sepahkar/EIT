import json

from django.http import JsonResponse
from django.shortcuts import render

from HR import models as HRMODEL
from datetime import datetime,timedelta
from django.db.models import F, ExpressionWrapper, fields
from .models import RoleDescription,RoleCategory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from collections import Counter
from django.shortcuts import redirect,reverse
from HR.backends import LdapBackend


@login_required(login_url=LdapBackend.REDIRECT_LOGIN)
def index(request):
    context = {}
    username = request.user.UserName
    qs_teams = get_current_user_teams(username)
    team = request.GET.get('team',qs_teams[0].TeamCode.TeamCode)
    users_of_manager,roles_list,users_study_degree, role_count_list = get_role_user(username,team)
    users_ids_in_manager = list(users_of_manager.values_list("UserName_id",flat=True))
    users_ids_in_manager = list(set(users_ids_in_manager))
    qs_descriptions = RoleDescription.objects.filter(CreatorUserName_id__in=users_ids_in_manager)
    #conditions_count = qs_descriptions.filter(Category__DescriptionType=RoleCategory.Conditions).count()
    #duties_count = qs_descriptions.filter(Category__DescriptionType=RoleCategory.Duties).count()
    abundance_role_list = Counter(role_count_list)
    qs_roles_list = HRMODEL.Role.objects.filter(RoleId__in=list(set(roles_list)))
    roles_conditions_duties = {item.RoleId: {'conditions': qs_descriptions.filter(Category__DescriptionType=RoleCategory.Conditions,RoleId=item.RoleId).count(),'duties': qs_descriptions.filter(Category__DescriptionType=RoleCategory.Duties, RoleId=item.RoleId).count()} for item in qs_roles_list}
    role_level_superior = {item.RoleId:{'HasSuperior':item.HasSuperior,'HasLevel':item.HasLevel,'name':item.RoleName} for item in qs_roles_list}
    categories = RoleCategory.objects.all()
    categories_c = [{'id':item.id,'name':item.CategoryName} for item in categories if item.DescriptionType == "C"]
    categories_d = [{'id':item.id,'name':item.CategoryName} for item in categories if item.DescriptionType == "D"]
    my_teams = [{'TeamCode':item.TeamCode.TeamCode,'TeamName':item.TeamCode.TeamName} for item in qs_teams]
    role_users =[ {
                'username':item.UserName.UserName,
                'age':item.get_birth,
                'contract':item.get_contract,
                'name':item.UserName.FirstName + " " + item.UserName.LastName,
                'FieldOfStudy':item.UserName.FieldOfStudy if hasattr(item.UserName,'FieldOfStudy') else '',
                'DegreeType':item.UserName.DegreeType,
                'RoleId':item.RoleId.RoleId,
                'LevelId': item.LevelId.id if item.LevelId is not None else "None",
                'LevelName': item.LevelId.LevelName if item.LevelId is not None else "None",
                'Superior': "1" if item.Superior else "0",
                'img':str(item.UserName.UserName).replace("@eit",".jpg")
                }
        for item in users_of_manager
    ]
    qs_descriptions = qs_descriptions.select_related("Category","RoleId","LevelId")
    descriptions_c = [{'id':item.id,'RoleId':item.RoleId.RoleId,'LevelId':item.LevelId,'Superior':item.Superior,'Title':item.Title,'Category':item.Category_id,'IsConfirm':item.IsConfirm} for item in qs_descriptions if item.Category.DescriptionType == "C"]
    descriptions_d = [{'id': item.id, 'RoleId': item.RoleId.RoleId, 'LevelId': item.LevelId, 'Superior': item.Superior, 'Title': item.Title,'Category': item.Category_id, 'IsConfirm': item.IsConfirm} for item in qs_descriptions if item.Category.DescriptionType == "D"]
    conditions_count = 0
    duties_count = 0
    for k,v in  roles_conditions_duties.items():
        conditions_count += int(v.get('conditions'))
        duties_count += int(v.get('duties'))
    context.update({
        'username':username,
        'conditions_count': conditions_count,
        'duties_count': duties_count,
        'roles_list': roles_list,
        'qs_roles_list': qs_roles_list,
        'team': qs_teams[0].TeamCode,
        'roles_conditions_duties':roles_conditions_duties,
        'role_level_superior':json.dumps(role_level_superior),
        'role_users':json.dumps(role_users),
        'abundance_role_list':abundance_role_list,
        'my_teams': my_teams,
        'firstteam': my_teams[0].get('TeamCode'),
        'users_study_degree':json.dumps(users_study_degree),
    })

    if ("view" in request.GET and request.GET.get("view") == "du") or "view" not in request.GET:
        context.update({
            'categories': categories_d,
            'descriptions': descriptions_d,
        })
    elif "view" in request.GET and request.GET.get("view") == "cd":
        context.update({
            'categories': categories_c,
            'descriptions': descriptions_c,
        })

    return render(request,'Duties/index.html',context=context)


@login_required(login_url=LdapBackend.REDIRECT_LOGIN)
def insert_description(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        level = None if int(request.POST.get('level')) == 0 else int(request.POST.get('level'))
        role = request.POST.get('role')
        superior = False if int(request.POST.get('superior')) == 0 else True
        isupdate = request.POST.get('isupdate')
        id = request.POST.get('id')
        if isupdate == "1":
            id = int(id)
            obj = RoleDescription.objects.filter(id=id).first()
            if obj:
                obj.Title = title
                obj.Category_id = category
                obj.save()
                return JsonResponse({"state": "ok", "id": obj.id}, status=200)
        elif isupdate == "0":
            obj = RoleDescription(
                Title=title,
                Category_id=category,
                LevelId_id=level,
                RoleId_id=role,
                Superior=superior,
            )
            obj.save()

        if obj:
            return JsonResponse({"state":"ok","id":obj.id},status=200)
    return JsonResponse({"state": "error"}, status=400)


@login_required(login_url=LdapBackend.REDIRECT_LOGIN)
def delete_description(request):
    if request.method == "POST":
        id = request.POST.get('id')
        obj = RoleDescription.objects.filter(id=id).first()
        if obj:
            obj.delete()
            return JsonResponse({"state":"ok"},status=200)
    return JsonResponse({"state": "error"}, status=400)



def get_user_teamrole(request,teamcode,roleid,levelid,superior):
    context = {}

    now = datetime.now().date()

    durationBirthDate = ExpressionWrapper(now - F('UserName__BirthDate'), output_field=fields.DurationField())

    durationContractDate = ExpressionWrapper(now - F('UserName__ContractDate'), output_field=fields.DurationField())

    data = HRMODEL.UserTeamRole.objects.filter(RoleId=roleid, TeamCode=teamcode, LevelId__id=levelid
                                   , Superior=superior).annotate(duration=durationBirthDate,duration_contract=durationContractDate)#.values('UserName__UserName','UserName__FirstName','UserName__LastName','UserName__FieldOfStudy','UserName__DegreeType')

    context.update({'data':data,'now':now})

    return render(request,"Duties/userinfo.html",context)


def get_current_user_teams(username):
    qs1 = HRMODEL.UserTeamRole.objects.filter(UserName=username).distinct()
    qs2 = HRMODEL.UserTeamRole.objects.filter(ManagerUserName_id=username).distinct()
    qs = qs1.union(qs2)
    tmp = []
    data = []
    for item in qs:
        if item.TeamCode_id not in tmp:
            tmp.append(item.TeamCode_id)
            data.append(item)
    return data


def get_role_user(username,team):
    queryset = HRMODEL.UserTeamRole.objects.filter(Q(ManagerUserName__UserName=username) | Q(UserName=username)).filter(TeamCode__TeamCode=team).select_related("RoleId","UserName")
    users = list(queryset.values_list("UserName_id",flat=True))
    role_list1 = HRMODEL.V_RoleTeam.objects.filter(ManagerUserName=username,TeamCode_id=team).values_list("RoleID",flat=True).distinct()
    role_list2 = HRMODEL.V_UserTeamRole.objects.filter(UserName=username,TeamCode_id=team).values_list("RoleId",flat=True).distinct()
    users_study_degree = HRMODEL.EducationHistory.objects.filter(Person_id__in=users).values("Person__Degree_Type__Caption","Person","EducationTendency__FieldOfStudy__Title","EducationTendency__Title")
    users_study_degree = {item.get('Person'):{"degree":item.get('Person__Degree_Type__Caption'),"study":item.get('EducationTendency__FieldOfStudy__Title'),"title":item.get('EducationTendency__Title')} for item in users_study_degree}
    role_count_list = list(HRMODEL.UserTeamRole.objects.filter(ManagerUserName=username,TeamCode_id=team).values_list("RoleId",flat=True)) + list(HRMODEL.UserTeamRole.objects.filter(UserName=username,TeamCode_id=team).values_list("RoleId",flat=True))
    return queryset, list(role_list1) + list(role_list2), users_study_degree, role_count_list


