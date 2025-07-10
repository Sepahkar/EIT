from rest_framework.views import APIView
from .models import (
    AppTeam,
    System,
    Permission,
    GroupUser,
    UserRoleGroupPermission,
    App,
    RelatedPermissionAPPURL,
    AppURL,
    PermissionGroup,
    Server,
)
from InternalAccess.models import AppInfo
from .serializers import (
    AppTeamSerializer,
    AllAppsInfoSerializer,
    AppUrlSerializer,
    SystemSerializer,
    AppBySystemCodeSerializer,
    AppByAppCodeSerializer,
    ServerSerializer,
    AppSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services



class GetAppTeams(APIView):
    def get(self, *args, **kwargs):
        app_label = kwargs.get('app_label')
        qs = AppTeam.objects.filter(AppCode__AppLabel=app_label)
        if qs:
            app_team_serializer = AppTeamSerializer(qs, many=True)
            return Response({'data': app_team_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': 'error'}, status=status.HTTP_400_BAD_REQUEST)



class GetAllAppsInfo(APIView):
    def get(self, request, *args, **kwargs):
        qs = AppInfo.objects.all()
        if request.data.get('return-dict') == '1' or request.GET.get('return-dict') == '1' or request.POST.get(
                'return-dict') == '1' or kwargs.get('return-dict') == '1':
            tmp = {}
            for item in qs:
                _item = item.__dict__
                _item.pop('_state')
                _item.update({
                    'FullUrl': item.FullUrl
                })
                obj = {
                    str(item.AppName): _item
                }
                tmp.update(obj)
            return Response({'data': tmp}, status=status.HTTP_200_OK)
        else:
            if qs:
                all_apps_info_serializer = AllAppsInfoSerializer(qs, many=True)
                return Response({'data': all_apps_info_serializer.data}, status=status.HTTP_200_OK)



class CheckUserPermission(APIView):
    def get(self, request, *args, **kwargs):
        api_client = new_api_client(request)

        permission_code = kwargs.get('permission_code')
        username = kwargs.get('username')
        state = "ok"
        HasPermission = False
        StatusCode = 403
        Message = ""
        if not Permission.objects.filter(Code=permission_code).exists():
            StatusCode = 400
            Message = "مجوز نامعتبر است"
        else:
            _ , status_code, _ = services.get_user(username, api_client=api_client)
            if status_code != 200:
                StatusCode = 400
                Message = "کاربر نامعتبر است"
            else:
                # پیدا کردن گروه های کاربر
                UserGroups = GroupUser.objects.filter(User=username)

                if UserGroups:
                    for Group in UserGroups:
                        if UserRoleGroupPermission.objects.filter(PermissionCode__Code=permission_code,
                                                                  OwnerPermissionGroup__id=Group.Group.id).exists():
                            HasPermission = True
                            StatusCode = 200
                if StatusCode != 200:
                    UserRoles = []
                    is_successfull, _,data = services.get_user_roles(request.user.username, api_client=api_client)
                    if is_successfull: 
                        UserRoles = data
                    if UserRoles:
                        for Role in UserRoles:
                            if UserRoleGroupPermission.objects.filter(PermissionCode__Code=permission_code,
                                                                      OwnerPermissionRole=Role).exists():
                                HasPermission = True
                                StatusCode = 200
                if StatusCode != 200:
                    if UserRoleGroupPermission.objects.filter(PermissionCode__Code=permission_code,
                                                              OwnerPermissionUser=username).exists():
                        HasPermission = True
                        StatusCode = 200
                if StatusCode != 200:
                    Message = "دسترسی این کاربر مجاز نمی باشد"

        return Response({'data': HasPermission, "Message": Message, "state": state}, status=StatusCode)



class GetPermittedAllUrl(APIView):
    def get(self, request, *args, **kwargs):
        api_client = new_api_client(request)
        username = kwargs.get('username')

        UserGroup = list(GroupUser.objects.filter(User=username).values_list('Group_id', flat=True))
        UserPermissionGroup = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionGroup__in=UserGroup).values_list('PermissionCode',
                                                                                                   flat=True))
        _, status_code, data = services.get_user_roles(username, api_client=api_client)
        UserRole = []
        if status_code == 200:
            UserRole = data
        UserPermissionRole = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionRole__in=UserRole).values_list('PermissionCode',
                                                                                                 flat=True))

        UserPermission = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionUser=username).values_list('PermissionCode',
                                                                                             flat=True))

        Permissions = UserPermissionGroup + UserPermissionRole + UserPermission

        AppPermission = list(
            Permission.objects.filter(PermissionType=Permission.PermissionType_Desktop,
                                      Code__in=Permissions).values_list('Code', flat=True))

        URlPermission = list(
            RelatedPermissionAPPURL.objects.filter(Permission__Code__in=AppPermission).values_list('AppURL__URL',
                                                                                                   flat=True))
        qs1 = AppURL.objects.filter(URL__in=URlPermission)
        qs2 = AppURL.objects.filter(IsPublic=True)
        qs = qs1.union(qs2)
        StatusCode = 200
        return Response({'data': {'rows': qs.values(), 'ids': qs.values_list('id', flat=True)}},
                        status=StatusCode)



class GetPermittedUrl(APIView):
    def get(self, request, *args, **kwargs):
        api_client = new_api_client(request)
        app_label = kwargs.get('app_label')
        username = kwargs.get('username')
        
        
        StatusCode = 403
        Message = ""
        HasPermission = False
        list_app_codes = App.objects.filter(AppLabel=app_label)
        app_code = list_app_codes.first().Code
        v = Validation(request)
        v.check_username(username)
        v.check_app_code(app_code)

        UserGroup = list(GroupUser.objects.filter(User=username).values_list('Group_id', flat=True))
        UserPermissionGroup = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionGroup__in=UserGroup).values_list('PermissionCode',
                                                                                                   flat=True))
        _, status_code, data = services.get_user_roles(username, api_client=api_client)
        UserRole = []
        if status_code == 200:
            UserRole = data
        UserPermissionRole = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionRole__in=UserRole).values_list('PermissionCode',
                                                                                                 flat=True))

        UserPermission = list(
            UserRoleGroupPermission.objects.filter(OwnerPermissionUser=username).values_list('PermissionCode',
                                                                                             flat=True))

        Permissions = UserPermissionGroup + UserPermissionRole + UserPermission

        AppPermission = list(
            Permission.objects.filter(PermissionType=Permission.PermissionType_Desktop,
                                      AppCode__Code__in=list(list_app_codes.values_list("Code", flat=True)),
                                      Code__in=Permissions).values_list('Code', flat=True))

        URlPermission = list(
            RelatedPermissionAPPURL.objects.filter(Permission__Code__in=AppPermission).values_list('AppURL__URL',
                                                                                                   flat=True))

        AppURLPermission = list(
            AppURL.objects.filter(AppCode__Code__in=list(list_app_codes.values_list("Code", flat=True)),
                                  URL__in=URlPermission).values_list('URL', flat=True))
        publiuc_url_permission = list(AppURL.objects.filter(IsPublic=True).values_list('URL', flat=True))

        AppURLPermission += publiuc_url_permission
        StatusCode = 200
        return Response({'data': {'URL': AppURLPermission, "Message": Message,"HasPermission": True if len(AppURLPermission) > 0 else False}},status=StatusCode)



class CheckUserPermissionList(APIView):
    def get(self, request, *args, **kwargs):
        api_client = new_api_client(request)

        app_label = kwargs.get('app_label')
        username = kwargs.get('username')
        
        
        state = "ok"
        PermissionList = []
        StatusCode = 403
        Message = ""
        app_code = App.objects.filter(AppLabel=app_label).first().Code

        v = Validation(request)
        v.check_username(username)
        v.check_app_code(app_code)

        UserGroups = list(GroupUser.objects.filter(User=username).values_list('Group_id', flat=True))
        
        if UserGroups:
            StatusCode = 200
            PermissionList = list(
                UserRoleGroupPermission.objects.filter(OwnerPermissionGroup__in=UserGroups).values_list(
                    'PermissionCode__Code', flat=True))

            _, status_code, data = services.get_user_roles(username, api_client=api_client)
            UserRoles = []
            if status_code == 200:
                UserRoles = data

            if UserRoles:
                PermissionList = PermissionList + list(
                    UserRoleGroupPermission.objects.filter(OwnerPermissionRole__in=UserRoles).values_list(
                        'PermissionCode__Code', flat=True))
            PermissionList = PermissionList + list(
                UserRoleGroupPermission.objects.filter(OwnerPermissionUser=username).values_list('PermissionCode__Code',
                                                                                                 flat=True))

        return Response({'data': PermissionList, }, status=StatusCode)


class Validation():
    StatusCode = 406
    Message = ""

    def __init__(self, request):
        self.request = request

    def check_username(self, username):
        api_client = new_api_client(self.request)
        uname = username
        
        _, status_code, data = services.get_user_roles(uname, api_client=api_client)
        if status_code != 200:
            StatusCode = 406
            Message = "نام کاربری معتبر نمی باشد"
            return Response({"Message": Message}, status=StatusCode)

    def check_app_code(self, app_code):
        if not (App.objects.filter(Code=app_code)).exists():
            StatusCode = 406
            Message = "کد برنامه معتبر نیست"
            return Response({"Message": Message}, status=StatusCode)

    def check_group(self, group_id):
        if not (PermissionGroup.objects.filter(PermissionGroup__id=group_id)).exists():
            StatusCode = 406
            Message = "گروه دسترسی معتبر نیست"
            return Response({"Message": Message}, status=StatusCode)

    def check_permission(self, permission_code):
        if not (Permission.objects.filter(Permission__Code=permission_code)).exists():
            StatusCode = 406
            Message = "دسترسی معتبر نیست"
            return Response({"Message": Message}, status=StatusCode)



class GetAppURL(APIView):
    def get(self, *args, **kwargs):
        app_url_id = int(kwargs.get('app_url_id'))
        qs = AppURL.objects.filter(id=app_url_id).first()
        if qs:
            app_code_url_serializer = AppUrlSerializer(qs)
            return Response({'data': app_code_url_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAllAppsURL(APIView):
    def get(self, *args, **kwargs):
        qs = AppURL.objects.all().select_related("AppCode__SystemCode")
        if qs:
            app_url_serializer = AppUrlSerializer(qs, many=True)
            return Response({'data': app_url_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetSystem(APIView):
    def get(self, *args, **kwargs):
        system_code = kwargs.get('system_code')
        qs = System.objects.filter(Code=system_code).first()
        if qs:
            system_serializer = SystemSerializer(qs)
            return Response({'data': system_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAllSystems(APIView):
    def get(self, *args, **kwargs):
        qs = System.objects.all()
        if qs:
            server_serializer = SystemSerializer(qs, many=True)
            return Response({'data': server_serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetServer(APIView):
    def get(self, *args, **kwargs):
        server_id = int(kwargs.get('server_id'))
        qs = Server.objects.filter(id=server_id).first()
        if qs:
            server_serializer = ServerSerializer(qs)
            return Response({'data': server_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAllServers(APIView):
    def get(self, *args, **kwargs):
        qs = Server.objects.all()
        if qs:
            server_serializer = ServerSerializer(qs, many=True)
            return Response({'data': server_serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAppBySystemCode(APIView):
    def get(self, *args, **kwargs):
        system_code = kwargs.get('system_code')
        qs = App.objects.filter(SystemCode_id=system_code).first()
        if qs:
            app_serializer = AppBySystemCodeSerializer(qs)
            return Response({'data': app_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAppByAppCode(APIView):
    def get(self, *args, **kwargs):
        app_code = kwargs.get('app_code')
        qs = App.objects.filter(Code=app_code).first()
        if qs:
            app_serializer = AppByAppCodeSerializer(qs)
            return Response({'data': app_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetApps(APIView):
    def get(self, *args, **kwargs):
        qs = App.objects.all()
        if qs:
            app_serializer = AppByAppCodeSerializer(qs, many=True)
            return Response({'data': app_serializer.data}, status=status.HTTP_200_OK)

        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class GetAppByLabelSystem(APIView):
    def get(self, request, *args, **kwargs):
        app_label = kwargs.get('app_label')
        system_code = kwargs.get('system_code')
        qs = App.objects.filter(AppLabel=app_label, SystemCode_id=system_code).first()
        if qs:
            current_serializer = AppSerializer(qs)
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': {'state': 'error'}}, status=status.HTTP_400_BAD_REQUEST)



class CheckUrlIsPublic(APIView):
    def post(self, request, *args, **kwargs):
        return Response(status=501)


def get_obj_with_key(_key, _val, _list):
    ret = {}
    for item in _list:
        if _key in item:
            val = item.get(_key).lower()
            if val == _val.lower():
                ret = item
                break
    return ret
