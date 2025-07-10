from django.http import JsonResponse
from HR.models import (
    Team,
    Role,
    TeamAllowedRoles,
    SetTeamAllowedRoleRequest,
    UserTeamRole,
    ConstValue,
    SetTeamAllowedRoleRequest,
    NewRoleRequest,
    RoleInformation,
    ROLE_MANAGER_STATUS_CHOICES
)
from django.shortcuts import render, redirect
from django.db import transaction
import json
from Utility.APIManager.Portal.register_document import v2 as register_doc_nCode
from Utility.APIManager.Portal.send_document import ver2 as send_doc_nCode
from Utility.APIManager.Portal.update_document import v1 as update_doc_nCode
from Utility.APIManager.Portal.terminate import v1 as terminate_document_flow
from Utility.APIManager.Portal.success_finish import v1 as success_finish_document_flow
from Utility.APIManager.Portal.failed_finish import v1 as failed_finish_document_flow
from Utility.APIManager.Notfication.email import v1 as notify

import ast
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from shared_lib import core as slcore
import requests as r
from django.conf import settings
from urllib.parse import urlencode


UserModel = get_user_model()

def cartable_inbox_new_role(request, request_id):
    doc_flow = request.GET.get("doc_flow")
    team_code = request.GET.get("team_code")
    query_params = {}

    if team_code=="None":
        team_code=None

    url = reverse("RoleManager_NewRole:showNewRoleRequest",kwargs={"requestID": request_id})
    if team_code: 
        query_params = {"d":team_code}
    
    # filled ReadDate and IsRead for documentflow in Portal 
    if doc_flow:
        read_api_url = f"http://{settings.MAIN_SERVER}:{settings.PORTAL_PORT}/Cartable/api/v1/{request.GET.get('doc_flow')}/read/"

        # no matter, it gives 200 or error
        r.post(read_api_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
        
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)

def cartable_outbox_new_role(request, request_id):
    query_params = {}
    url = reverse("RoleManager_NewRole:showNewRoleRequest",kwargs={"requestID": request_id})
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)

def cartable_mybox_new_role(request, request_id):
    query_params = {}
    url = reverse("RoleManager_NewRole:showNewRoleRequest",kwargs={"requestID": request_id})
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)


def cartable_inbox_change_allowed_role(request, request_id):
    doc_flow = request.GET.get("doc_flow")
    team_code = request.GET.get("team_code")
    query_params = {}

    if team_code=="None":
        team_code=None

    url = reverse("RoleManager_ChangeAllowedRole:showSetTeamAllowedRoleRequest",kwargs={"requestID": request_id})
    if team_code: 
        query_params = {"d":team_code}
    
    # filled ReadDate and IsRead for documentflow in Portal 
    if doc_flow:
        read_api_url = f"http://{settings.MAIN_SERVER}:{settings.PORTAL_PORT}/Cartable/api/v1/{request.GET.get('doc_flow')}/read/"

        # no matter, it gives 200 or error
        r.post(read_api_url, headers={"Service-Authorization":slcore.generate_token("e.rezaee")})
        
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)

def cartable_outbox_change_allowed_role(request, request_id):
    query_params = {}
    url = reverse("RoleManager_ChangeAllowedRole:showSetTeamAllowedRoleRequest",kwargs={"requestID": request_id})
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)

def cartable_mybox_change_allowed_role(request, request_id):
    query_params = {}
    url = reverse("RoleManager_ChangeAllowedRole:showSetTeamAllowedRoleRequest",kwargs={"requestID": request_id})
    redirect_url = f"{url}?{urlencode(query_params)}"
    return redirect(redirect_url)



# ################### Views ###################
@csrf_exempt
def setTeamAllowedRoleRequest(request):
    # دریافت اطلاعات کاربر فعلی
    information = get_currentUser_CTO_manager_information(request)

    # hack
    information["currentUser_role"] = "DEF"

    TEAM = Team.objects.all()
    ROLE = Role.objects.order_by("RoleId")
    ALLOWEDTEAMROLE = list(
        TeamAllowedRoles.objects.values("TeamCode", "RoleId", "AllowedRoleCount")
    )
    TEAMNAMES = list(Team.objects.values("TeamName", "TeamCode"))
    ROLENAMES = list(Role.objects.values("RoleName", "RoleId"))
    CURRENTUSER_REQUEST = get_currentUser_request(
        information["currentUser_nationalCode"], targetedTable=SetTeamAllowedRoleRequest
    )
    # CURRENTUSER_REQUEST["Status"] = False

    # محاسبه افرادی که مشغول به کار هستند در آن تیم و سمت
    for item in ALLOWEDTEAMROLE:
        item["EntryCount"] = UserTeamRole.objects.filter(
            TeamCode_id=item["TeamCode"], RoleId_id=item["RoleId"]
        ).count()

    if request.method == "POST":
        document_title = "درخواست تغییر سمت های مجاز تیم"
        doc_state = "بررسی مدیر"
        if information["currentUser_role"] != "DEF":
            doc_state = "بررسی مدیر عامل"

        try:
            body_data = json.loads(request.body)
            newRecord = SetTeamAllowedRoleRequest.objects.create(
                TeamAllowedRoles=body_data,
                RequestorId=information["currentUser_nationalCode"],
                ManagerId=information["currentUser_managers"][0],
                CTOId=information["cto_nationalCode"],
                StatusCode="MANREV"
                if information["currentUser_role"] == "DEF"
                else "CTOREV",
            )

            register_document(information, newRecord, document_title, doc_state, "ORGRCM")
            RESPONSE = send_document(information, newRecord, newRecord.DocId, team_code="SPM", work_flow_step="اظهار نظر مدیر مستقیم")
            notify()
            return JsonResponse(RESPONSE)

        except Exception as error:
            return JsonResponse({"Error": True, "Message": "بروز خطا در ایجاد درخواست"})

    return render(
        request,
        "roleManager/SetTeamAllowedRoleRequest.html",
        context={
            "Teams": TEAM,
            "Roles": ROLE,
            "allowedTeam": json.dumps(ALLOWEDTEAMROLE),
            "roleNames": json.dumps(ROLENAMES),
            "teamNames": json.dumps(TEAMNAMES),
            "currentUser_request": CURRENTUSER_REQUEST,
        },
    )


@csrf_exempt
def newRoleRequest(request):
    information = get_currentUser_CTO_manager_information(request)
    
    # hack
    information["currentUser_role"] = "DEF"
    
    if request.method == "POST":
        doc_state = "بررسی مدیر"
        if information["currentUser_role"] != "DEF":
            doc_state = "بررسی مدیر عامل"
        try:
            body_data = json.loads(request.body)
            normalizedText = normalize_persian(body_data["RoleTitle"])
            if Role.objects.filter(RoleName__iexact=normalizedText).exists():
                raise ValueError("نام سمت تکراری میباشد")
            document_title = f"درخواست ایجاد سمت جدید '{body_data['RoleTitle']}'"
            newRecord = NewRoleRequest.objects.create(
                RoleTitle=body_data["RoleTitle"],
                HasLevel=body_data["HasLevel"],
                HasSuperior=body_data["HasSuperior"],
                AllowedTeams=body_data["AllowedTeams"],
                ConditionsText=body_data["Conditions"],
                DutiesText=body_data["Duties"],
                RequestorId=information["currentUser_nationalCode"],
                ManagerId=information["currentUser_managers"][0],
                CTOId=information["cto_nationalCode"],
                StatusCode="MANREV"
                if information["currentUser_role"] == "DEF"
                else "CTOREV",
                ManagerType=ConstValue.objects.get(id=int(body_data["ManagerType"])),
                RoleType=ConstValue.objects.get(id=int(body_data["RoleType"])),
                NewRoleTypeTitle=body_data["NewRoleTypeTitle"],
            )

            register_document(information, newRecord, document_title, doc_state, "ORGNRL")
            RESPONSE = send_document(information, newRecord, newRecord.DocId, team_code="SPM", work_flow_step="اظهار نظر مدیر مستقیم")
            notify()
            return JsonResponse(RESPONSE)
        except ValueError as error:
            return JsonResponse({"error": True, "message": str(error)})
        except Exception as error:
            return JsonResponse(
                {"error": True, "message": "بروز خطا در ایجاد درخواست سمت مجاز تیم"}
            )
    else:
        CURRENTUSER_REQUEST = get_currentUser_request(
            information["currentUser_nationalCode"], targetedTable=NewRoleRequest
        )
        TEAMS = Team.objects.all()
        MANAGERS_TYPE = ConstValue.objects.filter(
            Code__in=["ManagerType_General", "ManagerType_Test", "ManagerType_Support"]
        ).order_by("OrderNumber")
        ROLE_TYPE = ConstValue.objects.filter(
            Code__in=[
                "Role_Auditor",
                "Role_Programmer",
                "Role_Tester",
                "Role_Support",
                "Role_Manager",
                "Role_Other",
            ]
        ).order_by("OrderNumber")

    return render(
        request,
        "roleManager/newRoleRequest.html",
        context={
            "teams": TEAMS,
            "managerType": MANAGERS_TYPE,
            "currentUser_request": CURRENTUSER_REQUEST,
            "managerType": MANAGERS_TYPE,
            "roleType": ROLE_TYPE,
        },
    )


@csrf_exempt
def showSetTeamAllowedRoleRequest(request, requestID):
    DATA = {
        "error": False,
        "status": "",
        "message": "",
    }
    DENIED_ACCESS_STATUS = [
        "FINSUC",
        "FINREJ",
        "FAILED",
    ]

    information = get_currentUser_CTO_manager_information(request)
    REQUEST = SetTeamAllowedRoleRequest.objects.get(id=requestID)
    requestData = ast.literal_eval(REQUEST.TeamAllowedRoles)
    teams = Team.objects.all()
    roles = Role.objects.all()

    # Hack
    display_mode = request.GET.get("d")
    if display_mode and display_mode=="SPM":
        information["currentUser_role"] = "MAN"
    elif display_mode and display_mode=="SPC":
        information["currentUser_role"] = "CTO"
    else:
        information["currentUser_role"] = "DEF"

    if request.method == "POST":
        bodyData = json.loads(request.body)
        try:
            if bodyData["status"] == "ACCEPT":
                if information["currentUser_role"] == "CTO":
                    try:
                        REQUEST.TeamAllowedRoles = bodyData["teamAllowedRoles"]
                        for team in REQUEST.TeamAllowedRoles:
                            for role in team["Roles"]:
                                teamAllowedRoles_record = TeamAllowedRoles.objects.get(
                                    TeamCode=team["TeamCode"], RoleId=role["RoleId"]
                                )
                                teamAllowedRoles_record.AllowedRoleCount = role[
                                    "RoleCount"
                                ]
                                teamAllowedRoles_record.SetTeamAllowedRoleRequest = (
                                    REQUEST
                                )
                                teamAllowedRoles_record.save()
                        REQUEST.StatusCode = "FINSUC"
                        REQUEST.save()

                        success_finish_document_flow(REQUEST.DocId)
                        

                        DATA["message"] = "تغییرات با موفقیت ثبت شد"
                    except Exception as e:
                        raise ValueError("بروز خطا در قسمت ذخیره اطلاعات")

                elif information["currentUser_role"] == "MAN":
                    try:
                        response = send_document(information, REQUEST, REQUEST.DocId, team_code="SPC", work_flow_step="اظهار نظر مدیر عامل")
                        notify()
                        update_document_state(REQUEST)
                        if response["Error"]:
                            raise ValueError(response["Message"])
                        else:
                            REQUEST.TeamAllowedRoles = bodyData["teamAllowedRoles"]
                            REQUEST.StatusCode = "CTOREV"
                            REQUEST.ManagerOpinion = 1
                            REQUEST.save()
                            update_document_state(REQUEST)

                            DATA["message"] = "درخواست با موفقیت تایید شد"
                    except Exception:
                        raise ValueError("بروز خطا در قسمت ذخیره اطلاعات")

            elif bodyData["status"] == "REJECT":
                if information["currentUser_role"] == "CTO":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.CTOOpinion = 0
                    REQUEST.save()

                    failed_finish_document_flow(REQUEST.DocId)
                    

                    DATA["message"] = "درخواست با موفقیت از طرف مدیر عامل رد شد"
                elif information["currentUser_role"] == "MAN":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.ManagerOpinion = 0
                    REQUEST.save()

                    failed_finish_document_flow(REQUEST.DocId)
                    

                    DATA["message"] = "درخواست با موفقیت از طرف مدیر رد شد"

        except SetTeamAllowedRoleRequest.DoesNotExist:
            DATA["error"] = True
            DATA["message"] = "درخواست مورد نظر یافت نشد"
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()

            terminate_document_flow(REQUEST.DocId)

            return JsonResponse(DATA)
        except TeamAllowedRoles.DoesNotExist:
            DATA["error"] = True
            DATA["message"] = "اطلاعات نقش تیم مورد نظر یافت نشد"
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()

            terminate_document_flow(REQUEST.DocId)

            return JsonResponse(DATA)

        except ValueError as error:
            DATA["error"] = True
            DATA["message"] = str(error)
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()
            
            terminate_document_flow(REQUEST.DocId)

            return JsonResponse(DATA)
        except Exception as error:
            DATA["error"] = True
            DATA["message"] = "متاسفانه خطایی رخ داده است"
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()
            
            terminate_document_flow(REQUEST.DocId)
            
            return JsonResponse(DATA)

        return JsonResponse(DATA)
    else:
        if information["error"]:
            DATA["error"] = True
            DATA["message"] = information["message"]
        else:
            for team in requestData:
                team["TeamName"] = (
                    teams.filter(TeamCode=team["TeamCode"]).first().TeamName
                )
                for role in team["Roles"]:
                    role["RoleName"] = (
                        roles.filter(RoleId=role["RoleId"]).first().RoleName
                    )
                    # محاسبه افرادی که مشغول به کار هستند در آن تیم و سمت
                    role["EntryCount"] = UserTeamRole.objects.filter(
                        TeamCode_id=team["TeamCode"], RoleId_id=role["RoleId"]
                    ).count()
            REQUEST.TeamAllowedRoles = requestData

            match information["currentUser_role"]:
                case "CTO":
                    if REQUEST.StatusCode == "CTOREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "MAN":
                    if REQUEST.StatusCode == "MANREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "DEF":
                    if information["currentUser_nationalCode"] == REQUEST.RequestorId:
                        if REQUEST.StatusCode == "DRAFTR":
                            DATA["status"] = "EDIT"
                        else:
                            DATA["status"] = "READONLY"
                    else:
                        DATA["error"] = True
                        DATA["message"] = (
                            "متاسفانه شما میتوانید فقط درخواست های خود را مشاهده کنید"
                        )

    return render(
        request,
        "roleManager/showSetTeamAllowedRoleRequest.html",
        context={
            "request": REQUEST,
            "permisionDataJson": json.dumps(DATA),
            "permisionData": DATA,
            "deniedAccessStatus": DENIED_ACCESS_STATUS,
        },
    )


@csrf_exempt
def showNewRoleRequest(request, requestID):
    DATA = {
        "error": False,
        "status": "",
        "message": "",
    }

    information = get_currentUser_CTO_manager_information(request)
    REQUEST = NewRoleRequest.objects.get(id=requestID)
    request_data = ast.literal_eval(REQUEST.AllowedTeams)
    TEAMS = Team.objects.all()
    for team in request_data:
        team["TeamName"] = TEAMS.filter(TeamCode=team["TeamCode"]).first().TeamName
    REQUEST.AllowedTeams = request_data
    REQUEST.ConditionsText = ast.literal_eval(REQUEST.ConditionsText)
    REQUEST.DutiesText = ast.literal_eval(REQUEST.DutiesText)
    # اگر status درخواست یکی از اینا باشه دکمه های تایید یا رد درخواست نشون داده نمیشه
    DENIED_ACCESS_STATUS = [
        "FINSUC",
        "FINREJ",
        "FAILED",
    ]
    
    display_mode = request.GET.get("d")
    if display_mode and display_mode=="SPM":
        information["currentUser_role"] = "MAN"
    elif display_mode and display_mode=="SPC":
        information["currentUser_role"] = "CTO"
    else:
        information["currentUser_role"] = "DEF"


    if request.method == "POST":
        try:
            bodyData = json.loads(request.body)
            if bodyData["status"] == "ACCEPT":
                if information["currentUser_role"] == "CTO":
                    saveData_resoponse = saveData_in_newRoleRequest_record(
                        newRoleRequest=REQUEST,
                        bodyData=bodyData,
                        currentUserCtoManager_information=information,
                    )
                    if saveData_resoponse["error"]:
                        raise ValueError(saveData_resoponse["message"])

                    response = saveNewRoleRequest(newRoleRequest=REQUEST)
                    if response["error"]:
                        raise ValueError(response["message"])
                    else:
                        DATA["message"] = response["message"]

                elif information["currentUser_role"] == "MAN":
                    response = send_document(information, REQUEST, REQUEST.DocId, team_code="SPC",  work_flow_step="اظهار نظر مدیر عامل")
                    notify()
                    if response["Error"]:
                        raise ValueError(response["Message"])
                    else:
                        saveData_resoponse = saveData_in_newRoleRequest_record(
                            newRoleRequest=REQUEST,
                            bodyData=bodyData,
                            currentUserCtoManager_information=information,
                        )
                        if saveData_resoponse["error"]:
                            raise ValueError(saveData_resoponse["message"])
                        else:
                            DATA["message"] = saveData_resoponse["message"]

            # رد درخواست
            elif bodyData["status"] == "REJECT":
                if information["currentUser_role"] == "CTO":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.CTOOpinion = 0
                    REQUEST.save()

                    failed_finish_document_flow(REQUEST.DocId)

                    DATA["message"] = "درخواست از طرف مدیر عامل با موفقیت رد شد"
                elif information["currentUser_role"] == "MAN":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.ManagerOpinion = 0
                    REQUEST.save()
                    
                    failed_finish_document_flow(REQUEST.DocId)
                    

                    DATA["message"] = "درخواست از طرف مدیر با موفقیت رد شد"
        except ValueError as error:
            DATA["error"] = True
            DATA["message"] = str(error)
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()
            terminate_document_flow(REQUEST.DocId)

            return JsonResponse(DATA)
        except Exception as error:
            DATA["error"] = True
            DATA["message"] = "متاسفانه خطایی رخ داده است"
            REQUEST.StatusCode = "FAILED"
            REQUEST.save()
            terminate_document_flow(REQUEST.DocId)

            return JsonResponse(DATA)

        return JsonResponse(DATA)
    else:
        if information["error"]:
            DATA["error"] = True
            DATA["message"] = information["message"]
        else:
            match information["currentUser_role"]:
                case "CTO":
                    if REQUEST.StatusCode == "CTOREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "MAN":
                    if REQUEST.StatusCode == "MANREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "DEF":
                    if information["currentUser_nationalCode"] == REQUEST.RequestorId:
                        if REQUEST.StatusCode == "DRAFTR":
                            DATA["status"] = "EDIT"
                        else:
                            DATA["status"] = "READONLY"
                    else:
                        DATA["error"] = True
                        DATA["message"] = (
                            "متاسفانه شما میتوانید فقط درخواست های خود را مشاهده کنید"
                        )
            MANAGERS_TYPE = ConstValue.objects.filter(
                Code__in=[
                    "ManagerType_General",
                    "ManagerType_Test",
                    "ManagerType_Support",
                ]
            ).order_by("OrderNumber")
            ROLE_TYPE = ConstValue.objects.filter(
                Code__in=[
                    "Role_Auditor",
                    "Role_Programmer",
                    "Role_Tester",
                    "Role_Support",
                    "Role_Manager",
                    "Role_Other",
                ]
            ).order_by("OrderNumber")

    return render(
        request,
        "roleManager/showNewRoleRequest.html",
        context={
            "request": REQUEST,
            "permisionDataJson": json.dumps(DATA),
            "permisionData": DATA,
            "deniedAccessStatus": DENIED_ACCESS_STATUS,
            "managerType": MANAGERS_TYPE,
            "roleType": ROLE_TYPE,
            "teams": TEAMS,
        },
    )


# ################### Functions ###################

# با فراخوانی این تابع لیستی از مدیران کاربر فعلی را دریافت میکنیم.


def get_currentUser_managers_nationalCode(currentUser_nationalCode: str) -> list:
    # hack
    return ["1280419180"]
    try:
        if not currentUser_nationalCode:
            raise ValueError("کد پرسنلی کاربر فعلی معتبر نمیباشد.")

        managers_nationalCode = []
        UserTeamRole_currentUser_records = UserTeamRole.objects.filter(
            NationalCode=currentUser_nationalCode
        )

        if not UserTeamRole_currentUser_records.exists():
            raise ValueError("اطلاعات شما در پایگاه داده موجود نمیباشد")

        for currentUser in UserTeamRole_currentUser_records:
            currentUser_manager = currentUser.ManagerUserName
            manager_nationalCode = currentUser_manager.NationalCode
            if manager_nationalCode not in managers_nationalCode:
                managers_nationalCode.append(manager_nationalCode)

        return managers_nationalCode
    # هر جایی از روند که درست پیش نرفت خطای مناسب اون رو در خروجی قرار میدیم و status رو false میزاریم
    except ValueError as error:
        raise ValueError(str(error))
    except Exception as error:
        raise Exception(f" خطای نامشخص در دریافت مدیران کاربر: {error}")


# در این تابع داکیومن ساخته و ارسال میشود
# و درون آن رکورد جدول docID را وارد میکند


def register_document(
    information: dict, newRecord, document_title: str, doc_state: str, app_code:str
) -> dict:
    # پیامی که به کاربر نشان خواهیم داد
    RESPONSE = {
        "Error": False,
        "Message": "",
    }
    try:
        # ایجاد داکیومنت
        try:
            registerResult = register_doc_nCode(
                app_doc_id=newRecord.id,
                priority="عادی",
                doc_state=doc_state,
                # پیش نویس
                # بررسی مدیر
                # بررسی مدیر عامل
                # رد شده توسط مدیر
                # رد شده توسط مدیر عامل
                # خاتمه موفق
                document_title=document_title,
                app_code=app_code,
                owner_nationalcode=information["currentUser_nationalCode"],
            )
        except Exception as error:
            raise Exception("بروز خطای نامشخص در ایجاد داکیومنت")
        if "data" not in registerResult or "id" not in registerResult["data"]:
            raise ValueError("خطا در دریافت اطلاعات داکیومنت")

        # ذخیره شماره رکورد داکیومنت در اطلاعات درخواست
        newRecord.DocId = registerResult["data"]["id"]
        newRecord.save()

    # خطاهایی که امکان دارن اتفاق بیوفتن
    except ValueError as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE
    # خطاهایی که نامشخص هستند
    except Exception as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE

def update_document_state(REQUEST: NewRoleRequest | SetTeamAllowedRoleRequest) -> dict:
    # پیامی که به کاربر نشان خواهیم داد
    RESPONSE = {
        "Error": False,
        "Message": "",
    }
    doc_id = REQUEST.DocId
    doc_state = ROLE_MANAGER_STATUS_CHOICES.get(REQUEST.StatusCode)

    try:
    #    آپدیت کردن داکیومنت
        try:
            update_doc_nCode(doc_id, {"DocState":doc_state})

        except Exception as error:
            raise Exception("بروز خطای نامشخص در آپدیت وضعیت داکیومنت")

        RESPONSE["Message"] = "درخواست با موفقیت ثبت و ارسال شد."
        return RESPONSE

    # خطاهایی که امکان دارن اتفاق بیوفتن
    except ValueError as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE
    # خطاهایی که نامشخص هستند
    except Exception as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE

def send_document(information: dict, newRecord, doc_id: int, **kwargs) -> dict:
    # پیامی که به کاربر نشان خواهیم داد
    team_code=kwargs.get("team_code")
    role_id=kwargs.get("role_id")
    work_flow_step=kwargs.get("work_flow_step")
    
    RESPONSE = {
        "Error": False,
        "Message": "",
    }
    try:
        # ارسال داکیومنت
        try:
            inbox_owner_nationalcode = information["currentUser_managers"][0]
            send_doc_nCode(
                doc_id=doc_id,
                sender_national_code=information["currentUser_nationalCode"],
                inbox_owners_national_code=[{"national_code":inbox_owner_nationalcode, "team_code":team_code, "role_id":role_id}],
                work_flow_step=work_flow_step
            )
        except Exception as error:
            # raise Exception("بروز خطای نامشخص در ارسال داکیومنت")
            raise Exception(str(error))

        # تغییر وضعیت در صورت تطابق کد ملی مدیرعامل با مدیران کاربر
        if information["currentUser_role"] == "DEF":
            newRecord.StatusCode = "MANREV"
        elif information["currentUser_role"] == "MAN":
            newRecord.StatusCode = "CTOREV"
        elif information["currentUser_role"] == "CTO":
            newRecord.StatusCode = "CTOREV"

        # ثبت تغییرات درخواست
        newRecord.save()

        RESPONSE["Message"] = "درخواست با موفقیت ثبت و ارسال شد."
        return RESPONSE

    # خطاهایی که امکان دارن اتفاق بیوفتن
    except ValueError as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE
    # خطاهایی که نامشخص هستند
    except Exception as error:
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE


# این تابع اطلاعات کاربر فعلی ، مدیران کاربر فعلی، مدیر عامل را به ما میدهد


def get_currentUser_CTO_manager_information(request) -> dict:
    information = {
        "error": False,
        "message": "",
        "currentUser_nationalCode": None,
        "currentUser_username": None,
        "cto_nationalCode": None,
        "currentUser_role": "",
        "currentUser_managers": None,
    }

    try:
        currentUser_nationalCode = request.user.national_code
        currentUser_username = request.user.username

        # دریافت کد ملی مدیرعامل از جدول تنظیمات
        cto_nationalCode = ConstValue.objects.get(Code="AllowedRole_CTO").Caption

        # دریافت لیست کد ملی مدیران کاربر فعلی
        managers_nationalCode = get_currentUser_managers_nationalCode(
            currentUser_nationalCode
        )

        # تکمیل اطلاعات خروجی
        information.update(
            {
                "currentUser_nationalCode": currentUser_nationalCode,
                "currentUser_username": currentUser_username,
                "cto_nationalCode": cto_nationalCode,
                "currentUser_managers": managers_nationalCode,
            }
        )

        # تعیین نقش کاربر در سیستم
        if currentUser_nationalCode == cto_nationalCode:
            information["currentUser_role"] = "CTO"  # مدیرعامل
        elif cto_nationalCode in managers_nationalCode:
            information["currentUser_role"] = "MAN"  # مدیر
        else:
            information["currentUser_role"] = "DEF"  # کاربر عادی

        return information

    except ValueError as error:
        information["error"] = True
        information["message"] = str(error)
        return information
    except ConstValue.DoesNotExist:
        information["error"] = True
        information["message"] = "اطلاعات مدیرعامل در سیستم یافت نشد"
        return information
    except Exception as error:
        information["error"] = True
        information["message"] = f"خطای نامشخص در دریافت اطلاعات: {str(error)}"
        return information


# با فراخوانی این تابع ما میخوایم چک کنیم که آیا کاربر فعلی با کد ملی خودش درخواست جدیدی ثبت کرده است یا خیر
# "نام جدول" اسم جدولی است که میخواهیم در آن به دنبال درخواست کاربر بگردیم
def get_currentUser_request(currentUser_NationalCode: str, targetedTable) -> dict:
    RESPONSE = {
        "Status": True,
        "Error": False,
        "Message": "",
        "requestID": None,
    }

    try:
        if not currentUser_NationalCode:
            raise ValueError("کد ملی کاربر نامعتبر است")

        # تمام درخواست های کاربر فعلی رو میریزیم اینجا
        # بستگی داره که روی کدوم جدول بخوایم جستجو کنیم
        user_requests = targetedTable.objects.filter(
            RequestorId=currentUser_NationalCode
        )

        # اگر هیچ درخواستی وجود نداشت
        if not user_requests.exists():
            RESPONSE["Status"] = False
            RESPONSE["Message"] = "درخواستی برای کاربر فعلی یافت نشد"
            return RESPONSE

        # بررسی وضعیت تمام درخواست‌ها
        COMPLETED_STATUSES = ["FINSUC", "FINREJ", "FAILED"]
        for request in user_requests:
            if request.StatusCode not in COMPLETED_STATUSES:
                RESPONSE["requestID"] = request.id
                RESPONSE["Status"] = True
                RESPONSE["Message"] = "شما یک درخواست باز دارید"
                return RESPONSE

        # اگر همه درخواست‌ها تکمیل شده بودند
        RESPONSE["Status"] = False
        RESPONSE["Message"] = "تمام درخواست های کاربر با موفقیت ثبت شده اند"
        return RESPONSE

    except ValueError as error:
        RESPONSE["Status"] = False
        RESPONSE["Error"] = True
        RESPONSE["Message"] = str(error)
        return RESPONSE
    except Exception as error:
        RESPONSE["Status"] = False
        RESPONSE["Error"] = True
        RESPONSE["Message"] = f"خطای نامشخص در بررسی درخواست های کاربر فعلی"
        return RESPONSE


def normalize_persian(text):
    return text.replace("ي", "ی").replace("ك", "ک").replace("‌", " ").strip()


# با فراخوانی این تابع قصد داریم که یک سمت جدید اضافه کنیم، این تابع فقط توسط مدیر عامل فراخوانی میشود
# درون این تابع بعد از ثبت اطلاعات سمت جدید در جدول سمت ها، درون جداول دیگر هم رکورد ثبت میشود
# اطلاعات دریافتی :
# آن رکوردی که میخواهیم ثبت کنیم


def saveNewRoleRequest(newRoleRequest) -> dict:
    RESPONSE = {
        "message": str,
        "error": False,
    }

    @transaction.atomic
    def save_in_role_table():
        lastRole = Role.objects.select_for_update().order_by("-RoleId").first()
        nextRole_id = (lastRole.RoleId if lastRole else 0) + 1

        try:
            newRoleObject = Role(
                RoleId=nextRole_id,
                RoleName=newRoleRequest.RoleTitle,
                HasLevel=newRoleRequest.HasLevel,
                HasSuperior=newRoleRequest.HasSuperior,
                NewRoleRequest=newRoleRequest,
                ManagerType=newRoleRequest.ManagerType.id,
                RoleType=newRoleRequest.RoleType.id,
            )
            newRoleObject.save(force_insert=True)

            return newRoleObject
        except Exception:
            raise ValueError("خطایی در ایجاد رکورد در جدول سمت ها پیش آمده است")


    def save_in_teamAllowedRoles_table(newRoleObject):
        try:
            for team in newRoleRequest.AllowedTeams:
                TeamAllowedRoles.objects.create(
                    TeamCode=Team.objects.get(TeamCode=team["TeamCode"]),
                    RoleId=newRoleObject,
                    AllowedRoleCount=team["RoleCount"],
                )
        except Exception:
            raise ValueError(
                "خطایی در ایجاد رکورد در جدول Team Allowed Roles پیش آمده است"
            )

    def save_in_roleInformation_table(newRoleObject):
        try:
            for condition in newRoleRequest.ConditionsText:
                RoleInformation.objects.create(
                    Title=condition["text"],
                    RoleID=newRoleObject,
                    DescriptionType="C",
                )
            for duty in newRoleRequest.DutiesText:
                RoleInformation.objects.create(
                    Title=duty["text"],
                    RoleID=newRoleObject,
                    DescriptionType="D",
                )
        except Exception as error:
            raise ValueError(
                "خطایی در ایجاد رکورد در جدول Role Information پیش آمده است"
            )

    try:
        newRoleObject = save_in_role_table()
        save_in_teamAllowedRoles_table(newRoleObject)
        save_in_roleInformation_table(newRoleObject)
        newRoleRequest.StatusCode = "FINSUC"
        newRoleRequest.CTOOpinion = 1
        newRoleRequest.save()
        
        success_finish_document_flow(newRoleRequest.DocId)

        RESPONSE["message"] = "سمت جدید با موفقیت ثبت شد"

    except ValueError as error:
        RESPONSE["error"] = True
        RESPONSE["message"] = str(error)
        return RESPONSE
    except Exception as e:
        RESPONSE["error"] = True
        RESPONSE["message"] = "در روند ثبت سمت جدید مشکلی پیش آمده است"
        return RESPONSE

    return RESPONSE


# با فراخوانی این تابع ما قصد داریم تا اطلاعاتی را درون یکی از رکورد های جدول newRoleRequest بریزیم.
# اطلاعات دریافتی عبارت است از :
# آن رکوردی که میخوایم درونش اطلاعات رو بریزیم
# اطلاعاتی که از طرف صفحه میاد
# اطلاعات مدیر، مدیر عامل و کاربر فعلی


def saveData_in_newRoleRequest_record(
    newRoleRequest, bodyData, currentUserCtoManager_information: dict
) -> dict:
    RESPONSE = {"message": str, "error": False}
    try:
        newRoleRequest.RoleTitle = bodyData["RoleTitle"]
        newRoleRequest.HasLevel = bodyData["HasLevel"]
        newRoleRequest.HasSuperior = bodyData["HasSuperior"]
        newRoleRequest.AllowedTeams = bodyData["AllowedTeams"]
        newRoleRequest.ConditionsText = bodyData["Conditions"]
        newRoleRequest.DutiesText = bodyData["Duties"]
        newRoleRequest.RequestorId = currentUserCtoManager_information[
            "currentUser_nationalCode"
        ]
        newRoleRequest.ManagerId = currentUserCtoManager_information[
            "currentUser_managers"
        ][0]
        newRoleRequest.ManagerType = ConstValue.objects.get(
            id=int(bodyData["ManagerType"])
        )
        newRoleRequest.RoleType = ConstValue.objects.get(id=int(bodyData["RoleType"]))
        newRoleRequest.NewRoleTypeTitle = bodyData["NewRoleTypeTitle"]
        newRoleRequest.ManagerOpinion = 1
        newRoleRequest.CTOId = currentUserCtoManager_information["cto_nationalCode"]
        newRoleRequest.StatusCode = "CTOREV"
        newRoleRequest.save()
        update_document_state(newRoleRequest)
        RESPONSE["message"] = "درخواست با موفقیت ثبت و ارسال شد."
    except Exception:
        RESPONSE["message"] = "بروز خطا در تغییر رکورد سمت."
        RESPONSE["error"] = True
        return RESPONSE

    return RESPONSE
