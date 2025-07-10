
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from HR import models
from HR import serializers
from .farsi_message import not_found
from django.db.models.functions import Lower


class Province(APIView):
    def get(self, request, id):
        """return the Province record that match with the given id."""

        queryset = models.Province.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('استان'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.ProvinceSerializer(instance=queryset,
                                                    many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request):
        """ getting all the Province instances"""
        queryset = models.Province.objects.all()
        serialized = serializers.ProvinceSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class City(APIView):
    def get(self, request, id):
        """return the City record that match with the given id."""

        queryset = models.City.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('شهر'), status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.CitySerializer(instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.City.objects.all()
        serialized = serializers.CitySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class CityDistrict(APIView):
    def get(self, request, id):
        """return the CityDistrict record that match with the given id."""

        queryset = models.CityDistrict.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('محله'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.CityDistrictSerializer(instance=queryset,
                                                        many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.CityDistrict.objects.all()
        serialized = serializers.CityDistrictSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class Users(APIView):

    def get(self, request, usernames: str):
        """usernames seperated by , """
        # FIXME: is it bad practice to use dynamic variable here?
        users = usernames.replace(' ', '')
        users = usernames.split(',')
        queryset = models.Users.objects.filter(UserName__in=users)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('کاربر/کاربران'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.SimpleUserSerializer(instance=queryset,
                                                      many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_by_national_code(request):
        codes = request.query_params.getlist("NationalCode")
        qs = models.Users.objects.filter(NationalCode__in=codes)
        if qs.exists: 
            data = serializers.SimpleUserSerializer(instance=qs, many=True).data
            return Response(data, status=200)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    @api_view(['GET'])
    def get_all_users_minimal_info(request):
        """minimal information means 3 fields:
        username, fullname and photoUrl
        """
        qs = models.Users.objects.all()
        serialized = serializers.MinimalUserInfoSerializer(qs, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    @api_view(['GET'])
    def get_full_info(request, usernames: str):
        users = usernames.replace(' ', '')
        users = usernames.split(',')
        queryset = models.Users.objects.filter(UserName__in=users)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('کاربر/کاربران'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.FullInfoUserSerializer(instance=queryset,
                                                        many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def get_full_info_by_national_code(request):
        codes = request.query_params.getlist("NationalCode")
        qs = models.Users.objects.filter(NationalCode__in=codes)
        if qs.exists: 
            data = serializers.FullInfoUserSerializer(instance=qs, many=True).data
            return Response(data, status=200)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.Users.objects.all()
        serialized = serializers.SimpleUserSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PostalAddress(APIView):
    def get(self, request, id):
        """return the PostalAddress record that match with the given id."""

        queryset = models.PostalAddress.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('آدرس پستی'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.PostalAddressSerializer(instance=queryset,
                                                         many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.PostalAddress.objects.all()
        serialized = serializers.PostalAddressSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class EmailAddress(APIView):
    def get(self, request, id):
        """return the EmailAddress record that match with the given id."""

        queryset = models.EmailAddress.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('پست الکترونیک'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.EmailAddressSerializer(instance=queryset,
                                                        many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.EmailAddress.objects.all()
        serialized = serializers.EmailAddressSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PhoneNumber(APIView):
    def get(self, request, id):
        """return the City record that match with the given id."""

        queryset = models.PhoneNumber.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('شماره تلفن'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.PhoneNumberSerializer(instance=queryset,
                                                       many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.PhoneNumber.objects.all()
        serialized = serializers.PhoneNumberSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class ConstValue(APIView):
    def get(self, request, id):
        pass
        """return the ConstValue record that match with the given id."""

        queryset = models.ConstValue.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('مقدارثابت'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.ConstValueSerializer(instance=queryset,
                                                      many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.ConstValue.objects.all()
        serialized = serializers.ConstValueSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class University(APIView):
    def get(self, request, id):
        """return the City record that match with the given id."""

        queryset = models.University.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('دانشگاه'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.UniversitySerializer(instance=queryset,
                                                      many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.University.objects.all()
        serialized = serializers.UniversitySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class FieldOfStudy(APIView):
    def get(self, request, id):
        """return the Field Of Study record that match with the given id."""

        queryset = models.FieldOfStudy.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('رشته تحصیلی'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.FieldOfStudySerializer(instance=queryset,
                                                        many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.FieldOfStudy.objects.all()
        serialized = serializers.FieldOfStudySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class Tendency(APIView):
    def get(self, request, id):
        """return the City record that match with the given id."""

        queryset = models.Tendency.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('گرایش'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.TendencySerializer(instance=queryset,
                                                    many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.Tendency.objects.all()
        serialized = serializers.TendencySerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class EducationHistory(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.EducationHistory.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('سابقه تحصیلی'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.EducationHistorySerializer(instance=queryset,
                                                            many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass


class Team(APIView):
    def get(self, request, team_code):
        """return the EducationHistort record that match with the given id."""

        queryset = models.Team.objects.filter(TeamCode=team_code)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('تیم'), status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.TeamSerializer(instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request):
        """Get all teams by filters that takes as query param"""
        active_in_service = request.query_params.get('ActiveInService')
        active_in_evaluation = request.query_params.get('ActiveInEvaluation')

        if not active_in_service and not active_in_evaluation:
            qs = models.Team.objects.all()
        elif not active_in_service:
            qs = models.Team.objects.filter(
                ActiveInEvaluation=active_in_evaluation)
        elif not active_in_evaluation:
            qs = models.Team.objects.filter(ActiveInService=active_in_service)
        elif active_in_evaluation and active_in_service:
            qs = models.Team.objects.filter(ActiveInService=active_in_service,
                                            ActiveInEvaluation=active_in_evaluation)

        ser_data = serializers.TeamSerializer(instance=qs, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class Role(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.Role.objects.filter(RoleId=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('نقش'), status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.RoleSerializer(instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['get'])
    def get_all(request):
        qs = models.Role.objects.all()
        ser_data = serializers.RoleSerializer(instance=qs, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class UserTeamRole(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.UserTeamRole.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('نقش'), status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.SimpleUserTeamRoleSerializer(
            instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass


class RoleLevel(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.RoleLevel.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('سطح'), status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.RoleLevelSerializer(instance=queryset,
                                                     many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['get'])
    def get_all(request):
        qs = models.RoleLevel.objects.all()
        ser_data = serializers.RoleLevelSerializer(instance=qs, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ChangeRole(APIView):
    def get(self, request, id):
        """return the ChangeRole record that match with the given id."""

        queryset = models.ChangeRole.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('تغییر نقش'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.ChangeRoleSerializer(instance=queryset,
                                                      many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        queryset = models.ChangeRole.objects.all()
        serialized = serializers.ChangeRoleSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class RoleGroup(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.RoleGroup.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('گروه بندی نقش'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.RoleGroupSerializer(instance=queryset,
                                                     many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        pass


class RoleGroupTargetException(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.RoleGroupTargetException.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('گروه بندی نقشtarget exception'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.RoleGroupTargetExceptionSerializer(
            instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        pass


class AccessPersonnel(APIView):
    def get(self, request, id):
        """return the EducationHistort record that match with the given id."""

        queryset = models.AccessPersonnel.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('دسترسی پرسنل'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.AccessPersonnelSerializer(instance=queryset,
                                                           many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class OrganizationChartRole(APIView):
    def get(self, request, id):
        """return the OrganizationChartRole record that match with the given id."""

        queryset = models.OrganizationChartRole.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('چارت سازمانی نقش'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.OrganizationChartRoleSerializer(
            instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        pass


class OrganizationChartTeamRole(APIView):
    def get(self, request, id):
        """return the OrganizationChartTeamRole record that match with the given id."""

        queryset = models.OrganizationChartTeamRole.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('چارت سازمانی تیم نقش'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.OrganizationChartTeamRoleSerializer(
            instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, ):
        pass

    def put(self, request, ):
        pass

    def delete(self, request, ):
        pass

    @api_view(['GET'])
    def get_all(request, ):
        pass


class UserHistory(APIView):
    def get(self, request, id):
        """return the OrganizationChartTeamRole record that match with the given id."""

        queryset = models.UserHistory.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('تاریخچه کاربر'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.UserHistorySerializer(instance=queryset,
                                                       many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PreviousUserTeamRole(APIView):
    def get(self, request, id):
        """return the OrganizationChartTeamRole record that match with the given id."""

        queryset = models.PreviousUserTeamRole.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('تیم نقش کاربر previous ed.'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.PreviousUserTeamRoleSerializer(
            instance=queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PageInformation(APIView):
    def get(self, request, id):
        """return the OrganizationChartTeamRole record that match with the given id."""

        queryset = models.PageInformation.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('اطلاعات صفحه'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.PageInformationSerializer(instance=queryset,
                                                           many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class PagePermission(APIView):
    def get(self, request, id):
        """return the OrganizationChartTeamRole record that match with the given id."""

        queryset = models.PagePermission.objects.filter(id=id)
        if not queryset.exists():
            # return not found if there is no matching instance
            return Response(not_found('اطلاعات دسترسی به صفحه'),
                            status=status.HTTP_404_NOT_FOUND)
        serialized = serializers.PagePermissionSerializer(instance=queryset,
                                                          many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def locations(request):
    building_code_prefix = "Building_"

    qs = models.ConstValue.objects.filter(Code__startswith=building_code_prefix)

    if not qs:
        return Response(status=404)

    buildings = []
    for building in qs:
        floors_qs = models.ConstValue.objects.filter(Parent_id=building.id)
        buildings.append(
            dict(
                code=building.Code,
                title=building.Caption,
                floors=floors_qs
            )
        )
    return Response(serializers.BuildingSerializer(buildings, many=True).data, status=200)


class UserLocation(APIView):
    def get(self, r, username):
        user = models.Users.objects.filter(UserName=username).first()

        if not user:
            return Response(status=404)

        return Response(
            {
                "latestBuilding": user.LastBuilding.Code if user.LastBuilding else None,
                "latestFloor": user.LastFloor.Code if user.LastFloor else None
            },
            status=200
        )
    
    @api_view(['GET'])
    def get_by_national_code(r, national_code):
        
        user = models.Users.objects.filter(NationalCode=national_code).first()

        if not user:
            return Response(status=404)

        return Response(
            {
                "latestBuilding": user.LastBuilding.Code if user.LastBuilding else None,
                "latestFloor": user.LastFloor.Code if user.LastFloor else None
            },
            status=200
        )



    def patch(self, r, username):
        user_instance = models.Users.objects.filter(UserName=username).first()
        ser = serializers.UserLocationSerializer(user_instance, data=r.data, partial=True)

        if ser.is_valid():
            ser.save()
            return Response(status=200)
        return Response(ser.errors, status=400)
    

@api_view(["GET"])
def user_identity_convertor(request):
    national_code = request.query_params.get("national_code")
    username = request.query_params.get("username")
    if all([national_code, username]) or not any([national_code, username]):
        return Response(status=404)
        
    if national_code:
        username = models.Users.objects.get(NationalCode=national_code).UserName
        return Response({"UserName":username}, status=200)
    
    if username:
        if  "@eit" not in username:
            username = f"{username}@eit"
        national_code = models.Users.objects.annotate(username_lower=Lower("UserName")).get(username_lower=username).NationalCode
        return Response({"NationalCode":national_code}, status=200)
    

