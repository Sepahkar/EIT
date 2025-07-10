import traceback

from django.db import connections
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from HR.models import (
    PreviousUserTeamRole,
    Role,
    Team,
    Users,
    UserTeamRole,
    V_HR_RoleTarget,
    V_RoleTeam,
)
from HR.serializers import (
    TeamSerializer,
    UsersSerializer,
    UserTeamRoleSerializer,
    UserTeamRoleWithNationalCodeSerializer,
)


class AllUsers(APIView):

    def get(self, request, *args, **kwargs):
        qs = Users.objects.select_related("DegreeType").only('DegreeType__Caption','DegreeType','BirthDate','FirstName','LastName','Gender','ContractDate', 'NationalCode').all()
        if qs:
            if "return_dict" in request.GET:
                user_serializer = UsersSerializer(qs, many=True)
                qs = user_serializer.data
                data = {str(item.get('UserName')).lower().strip():item for item in qs}
            else:
                user_serializer = UsersSerializer(qs, many=True)
                data = user_serializer.data
            return Response({'data':data},status=status.HTTP_200_OK)

        return Response(data={'state':'error'},status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self,request, *args, **kwargs):
        qs = Users.objects.filter(UserName=kwargs.get('username')).first()
        if qs:
            user_serializer = UsersSerializer(qs)
            return Response({'data':user_serializer.data},status=status.HTTP_200_OK)

        return Response(data={'state':'error'},status=status.HTTP_400_BAD_REQUEST)

class GetUserByNationalCode(APIView):
    def get(self, request, national_code):
        try:
            user = Users.objects.get(NationalCode=national_code)
            serializer = UsersSerializer(user)
            return Response({'data':serializer.data},status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(
                {"error": "User with this national code does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )



class GetUserTeamRole(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        qs = UserTeamRole.objects.filter(UserName__UserName=username)
        if qs:
            if "return_dict" in request.GET:
                qs = qs.values()
                data = {item.get('TeamCode_id'):item for item in qs}
            else:
                user_team_role_serializer = UserTeamRoleSerializer(qs,many=True)
                data = user_team_role_serializer.data
            return Response({'data':data},status=status.HTTP_200_OK)

        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserTeamRoleByNationalCode(APIView):
    def get(self, request, national_code):
        qs = UserTeamRole.objects.filter(NationalCode=national_code)
        if qs:
            if "return_dict" in request.GET:
                qs = qs.values()
                data = {item.get('TeamCode_id'):item for item in qs}
            else:
                user_team_role_serializer = UserTeamRoleWithNationalCodeSerializer(qs,many=True)
                data = user_team_role_serializer.data
            return Response({'data':data},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)
    

class GetUserAllTeamRole(APIView):

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        current_teamroles = UserTeamRole.objects.filter(UserName__UserName=username)
        previous_teamroles = PreviousUserTeamRole.objects.filter(UserName__UserName=username)
        
        
        if current_teamroles or previous_teamroles:
            current_teamroles_serialized = UserTeamRoleSerializer(current_teamroles, many=True).data
            previous_teamroles_serialized = UserTeamRoleSerializer(previous_teamroles, many=True).data
        
            return Response(
                {
                    'data':current_teamroles_serialized+previous_teamroles_serialized},
                    status=status.HTTP_200_OK
                )

        return Response({'state':'error', "desc":"record not found!"}, status=status.HTTP_404_NOT_FOUND)

class GetUserAllTeamRoleByNationalCode(APIView):
    def get(self, request, national_code):
        current_teamroles = UserTeamRole.objects.filter(NationalCode=national_code)
        previous_teamroles = PreviousUserTeamRole.objects.filter(NationalCode=national_code)
        
        
        if current_teamroles or previous_teamroles:
            current_teamroles_serialized = UserTeamRoleWithNationalCodeSerializer(current_teamroles, many=True).data
            previous_teamroles_serialized = UserTeamRoleWithNationalCodeSerializer(previous_teamroles, many=True).data
        
            return Response(
                {
                    'data':current_teamroles_serialized+previous_teamroles_serialized},
                    status=status.HTTP_200_OK
                )

        return Response({'state':'error', "desc":"record not found!"}, status=status.HTTP_404_NOT_FOUND)

class GetUserTeamRoles(APIView):

    def get(self, request, *args, **kwargs):
        foreign_key_fields = [field.name for field in UserTeamRole._meta.fields if 'ForeignKey' in field.get_internal_type()]
        wich_users = request.data.get('wich_users', 'active')
        if wich_users == 'active':
            qs = UserTeamRole.objects.select_related(*foreign_key_fields).filter(EndDate__isnull=True)
        elif wich_users == 'all':
            qs = UserTeamRole.objects.select_related(*foreign_key_fields).all()

        user_team_role_serializer = UserTeamRoleSerializer(qs, many=True)
        data = user_team_role_serializer.data
        return Response({'data':data},status=status.HTTP_200_OK)

        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserRoles(APIView):

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        qs = UserTeamRole.objects.filter(UserName_id=username)
        if qs:
            return Response({'data':list(qs.values_list("RoleId_id",flat=True))},status=status.HTTP_200_OK)

        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserRolesByNationalCode(APIView):
    def get(self, request, national_code):
        qs = UserTeamRole.objects.filter(NationalCode=national_code)
        if qs:
            return Response({'data':list(qs.values_list("RoleId_id",flat=True))},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetAllRoles(APIView):
    def get(self, request, *args, **kwargs):
        qs = Role.objects.values()
        if qs:
            if "return_dict" in request.GET:
                data = {item.get('RoleId'): item for item in qs}
            else:
                data = list(qs)
            return Response({'data':data},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetAllTeams(APIView):
    def get(self, request, *args, **kwargs):
        qs = Team.objects.values()
        if qs:
            if "return_dict" in request.GET:
                data = {item.get('TeamCode'): item for item in qs}
            else:
                data = list(qs)
            return Response({'data':data},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetViewRoleTarget(APIView):
    def get(self, request, *args, **kwargs):
        _filters = request.data.get('filters')
        filters = {}
        fields = request.data.get('fields')
        for k,v in _filters.items():
            if v not in ['', ' ']:
                filters.update({k:v})
        qs = V_HR_RoleTarget.objects.filter(**filters).values(*fields)
        if qs:
            return Response({'data':list(qs)},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetViewRoleTeam(APIView):
    def get(self, request, *args, **kwargs):
        try:
            filters = request.data.get('filters')
            qs = V_RoleTeam.objects.filter(RoleID__in=filters.get('role_ids'),TeamCode=filters.get('team_code')).values_list("RoleID",flat=True)
            if qs:
                return Response({'data':list(qs)},status=status.HTTP_200_OK)
            return Response({'data': []}, status=status.HTTP_200_OK)
        except:
            return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class GetAllViewRoleTeam(APIView):
    def get(self, request, *args, **kwargs):
        try:
            if request.data:
                qs = V_RoleTeam.objects.filter(**request.data)
            else:
                qs = V_RoleTeam.objects.all()
            data = qs.values()
            return Response({'data':list(data)},status=status.HTTP_200_OK)
        except:
            return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)


class ExistsUsers(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        ex = False
        if Users.objects.filter(pk=pk).exists():
            ex = True

        return Response({'data': ex}, status=200)


class ExistsRole(APIView):
    def get(self,request,*args,**kwargs):
        pk = kwargs.get('pk')
        ex = False
        if Role.objects.filter(pk=pk).exists():
            ex = True

        return Response({'data':ex},status=200)


class AllTeamService(APIView):
    def get(self, request, *args, **kwargs):
        qs = Team.objects.filter(ActiveInService=True)
        team_serializer = TeamSerializer(qs,many=True)
        if team_serializer:
            return Response({'data':team_serializer.data},status=status.HTTP_200_OK)

        return Response(data={'state':'error'},status=status.HTTP_400_BAD_REQUEST)


class AllTeamEvaluation(APIView):
    def get(self, request, *args, **kwargs):
        qs = Team.objects.filter(ActiveInEvaluation=True)
        team_serializer = TeamSerializer(qs,many=True)
        if team_serializer:
            return Response({'data':team_serializer.data},status=status.HTTP_200_OK)

        return Response(data={'state':'error'},status=status.HTTP_400_BAD_REQUEST)


class FindTeam(APIView):
    def get(self, request, *args, **kwargs):
        qs = Team.objects.filter(**request.data).first()
        team_serializer = TeamSerializer(qs)
        if team_serializer:
            return Response({'data':team_serializer.data},status=status.HTTP_200_OK)

        return Response(data={'state':'error'},status=status.HTTP_400_BAD_REQUEST)


class CallSpAssessorsEducator(APIView):
    # call_sp_assessors_educator
    def get(self, request, *args, **kwargs):
        TeamCode = 0 if request.data.get('TeamCode') is None else request.data.get('TeamCode')
        RoleIdTarget = 0 if request.data.get('RoleIdTarget') is None else request.data.get('RoleIdTarget')
        LevelIdTarget = 0 if request.data.get('LevelIdTarget') is None else request.data.get('LevelIdTarget')
        SuperiorTarget = 0 if request.data.get('SuperiorTarget') is None else request.data.get('SuperiorTarget')
        Temporary = 0 if request.data.get('Temporary') is None else request.data.get('Temporary')
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            InfoID = UserTeamRole.objects.filter(UserName__UserName=request.data.get('InfoID'), TeamCode_id=request.data.get('current_team')).first()
            InfoID = InfoID.id if InfoID else 0
            cursor.execute("EXEC [dbo].[HR_GetAssessorsAndEducators] @TeamCode ='%s' ,@InfoID = %s,@RoleIdTarget = %s,@LevelIdTarget = %s,@SuperiorTarget = %s,@Temporary = %s,@Type = %s" % (TeamCode,InfoID,RoleIdTarget,LevelIdTarget,SuperiorTarget,Temporary,request.data.get('Type')))
            result_set = cursor.fetchall()
            data = list(result_set[0])
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = []
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class CallSpGetTeamsOfRole(APIView):
    # call_sp_get_teams_of_role
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            cursor.execute("EXEC [dbo].[HR_GetTeamManager] @RoleId='%s',@TeamCode='%s' " % (request.data.get('RoleId'),request.data.get('TeamCode')))
            data = cursor.fetchall()
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = []
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class CallSpGetManagerOfTeam(APIView):
    # call_sp_get_manager_of_team
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            cursor.execute("EXEC [dbo].[HR_GetTeamManager] @RoleId=%s,@TeamCode='%s' " % (request.data.get('RoleId'), request.data.get('TeamCode')))
            data = cursor.fetchall()
            data = data[0][0]
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = []
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class CallSpGetTargetRole(APIView):
    # call_sp_get_target_role
    def get(self, request, *args , **kwargs):
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            InfoID = UserTeamRole.objects.filter(UserName__UserName=request.data.get('InfoID'),
                                                 TeamCode_id=request.data.get('TeamCode')).first()
            InfoID = InfoID.id if InfoID else 0
            cursor.execute("EXEC [dbo].[HR_GetTargetRole] @ID = %s,@Type = %s" % (InfoID, request.data.get('Type')))
            data = cursor.fetchall()
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = []
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class CallSpGetTargetRoleByNationalCode(APIView):
    # call_sp_get_target_role_by_national_code  
    def get(self, request, *args , **kwargs):
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            InfoID = UserTeamRole.objects.filter(
                NationalCode=request.data.get('InfoID'),
                TeamCode_id=request.data.get('TeamCode')).first()
            InfoID = InfoID.id if InfoID else 0
            cursor.execute("EXEC [dbo].[HR_GetTargetRole] @ID = %s,@Type = %s" % (InfoID, request.data.get('Type')))
            data = cursor.fetchall()
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = []
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class CallFuncEducatorGetTeamManager(APIView):
    # call_func_educator_get_team_manager
    def get(self, request, *args, **kwargs):
        cursor = connections['default'].cursor()
        _status = status.HTTP_200_OK
        _state = 'ok'
        try:
            cursor.execute("SELECT [dbo].[HR_Name_GetTeamManager] ('%s','%s','%s')" % (request.data.get('role_id'), request.data.get('team_code'), 'U'))
            result_set = cursor.fetchall()
            data = {'manager':result_set[0][0]}
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
            _state = 'error'
            traceback.print_exc()
            data = {'manager':''}
        finally:
            cursor.close()
            return Response(data={'state':_state,'data':data},status=_status)


class GetPreviousUserTeamRoles(APIView):
    def get(self, request, *args, **kwargs):
        foreign_key_fields = [field.name for field in PreviousUserTeamRole._meta.fields if 'ForeignKey' in field.get_internal_type()]
        qs = PreviousUserTeamRole.objects.select_related(*foreign_key_fields).all()
        if qs:
            data = []
            for item in qs:
                obj = {
                    'UserName':item.UserName.UserName,
                    'NationalCode':item.NationalCode,
                    'FullName':item.UserName.FullName,
                    'Gender':item.UserName.Gender,
                    'TeamCode':item.TeamCode.TeamCode,
                    'TeamName':item.TeamCode_id,
                    'RoleId':item.RoleId_id,
                    'RoleName':item.RoleId.RoleName,
                    'LevelId':item.LevelId_id,
                    'LevelName':item.LevelId.LevelName if item.LevelId_id else None,
                    'Superior':item.Superior,
                    'ManagerUserName':item.ManagerUserName.UserName,
                    'ManagerNationalCode':item.ManagerNationalCode,
                    'StartDate':item.StartDate,
                    'EndDate':item.EndDate,
                    'Birth':item.get_birth,
                    'Contract':item.get_contract,
                }
                data.append(obj)
            return Response({'data':data},status=status.HTTP_200_OK)
        return Response({'state':'error'}, status=status.HTTP_400_BAD_REQUEST)

