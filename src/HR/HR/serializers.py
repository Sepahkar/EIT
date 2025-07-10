from rest_framework import serializers
from HR import models


class UsersSerializer(serializers.ModelSerializer):
    UserName = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    FullName = serializers.SerializerMethodField()
    degree = serializers.SerializerMethodField()
    contract = serializers.SerializerMethodField()
    user_image_name = serializers.SerializerMethodField()
    Gender = serializers.SerializerMethodField()
    GenderTitle = serializers.SerializerMethodField()
    GenderTitlePrefix = serializers.SerializerMethodField()
    GenderTitlePrefixFullName = serializers.SerializerMethodField()
    Email = serializers.SerializerMethodField()
    Study = serializers.SerializerMethodField()
    NationalCode = serializers.SerializerMethodField()

    class Meta:
        model = models.Users
        fields = (
            "UserName",
            "age",
            "FullName",
            "degree",
            "contract",
            "user_image_name",
            "Gender",
            "GenderTitle",
            "GenderTitlePrefix",
            "GenderTitlePrefixFullName",
            "Email",
            "Study",
            "NationalCode",
        )

    def get_UserName(self, obj):
        return str(obj.UserName).lower()

    def get_age(self, obj):
        return obj.get_birth

    def get_FullName(self, obj):
        return obj.FullName

    def get_degree(self, obj):
        return obj.get_degree

    def get_contract(self, obj):
        return obj.get_contract

    def get_user_image_name(self, obj):
        return obj.user_image_name

    def get_Gender(self, obj):
        return obj.Gender

    def get_GenderTitle(self, obj):
        return obj.GenderTitle

    def get_GenderTitlePrefix(self, obj):
        return obj.GenderTitlePrefix

    def get_GenderTitlePrefixFullName(self, obj):
        return obj.GenderTitlePrefixFullName

    def get_Email(self, obj):
        return (obj.UserName.replace("@eit", "")) + "@iraneit.com"

    def get_Study(self, obj):
        return obj.get_study

    def get_NationalCode(self, obj):
        return obj.NationalCode


class UserTeamRoleSerializer(serializers.ModelSerializer):
    FullName = serializers.CharField(source="UserName.FullName")
    Gender = serializers.BooleanField(source="UserName.Gender")
    TeamName = serializers.CharField(source="TeamCode.TeamName")
    RoleName = serializers.CharField(source="RoleId.RoleName")
    LevelName = serializers.CharField(source="LevelId.LevelName", allow_null=True)
    ActiveInService = serializers.BooleanField(source="TeamCode.ActiveInService")
    ActiveInEvaluation = serializers.BooleanField(source="TeamCode.ActiveInEvaluation")
    UserName = serializers.SerializerMethodField()
    ManagerUserName = serializers.SerializerMethodField()

    class Meta:
        model = models.UserTeamRole
        fields = [item.name for item in models.UserTeamRole._meta.fields]
        fields.append("FullName")
        fields.append("Gender")
        fields.append("TeamName")
        fields.append("RoleName")
        fields.append("LevelName")
        fields.append("ActiveInService")
        fields.append("ActiveInEvaluation")

    def get_UserName(self, obj):
        return str(obj.UserName.UserName).lower()

    def get_ManagerUserName(self, obj):
        return str(obj.ManagerUserName.UserName).lower() if obj.ManagerUserName else ""


class UserTeamRoleWithNationalCodeSerializer(UserTeamRoleSerializer):
    NationalCode = serializers.SerializerMethodField()

    class Meta(UserTeamRoleSerializer.Meta):
        fields = UserTeamRoleSerializer.Meta.fields + ["NationalCode"]

    def get_NationalCode(self, obj):
        return obj.NationalCode


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = "__all__"


class FloorSerializer(serializers.Serializer):
    code = serializers.CharField(source="Code")
    title = serializers.CharField(source="Caption")


class BuildingSerializer(serializers.Serializer):
    code = serializers.CharField()
    title = serializers.CharField()
    floors = FloorSerializer(many=True)


class UserLocationSerializer(serializers.Serializer):
    latestBuilding = serializers.CharField()
    latestFloor = serializers.CharField()

    def update(self, instance, validated_data):
        new_building_code = validated_data.get("latestBuilding")
        new_floor_code = validated_data.get("latestFloor")

        new_building_instance = models.ConstValue.objects.get(Code=new_building_code)
        new_floor_instance = models.ConstValue.objects.get(Code=new_floor_code)

        instance.LastBuilding, instance.LastFloor = (
            new_building_instance,
            new_floor_instance,
        )

        instance.save()
        return instance


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ['id',
                  'CityTitle',
                  'IsCapital',
                  'CityCode',
                  'Province_id',

                  # FK Title
                  'ProvinceTitle',
                  ]
        extra_kwargs = {
            'ProvinceTitle': {'read_only': True},
        }


class CityDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CityDistrict
        fields = ['id',
                  'DistrictTitle',
                  'City_id',

                  # FK Title
                  'CityTitle',
                  ]
        extra_kwargs = {
            'CityTitle': {'read_only': True}
        }


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostalAddress
        fields = ['id',
                  'Title',
                  'AddressText',
                  'No',
                  'UnitNo',
                  'PostalCode',
                  'IsDefault',

                  'City_id',
                  'CityDistrict_id',
                  'Person_id',

                  # FK Title
                  'CityTitle',
                  'CityDistrictTitle',
                  ]
        extra_kwargs = {
            'CityTitle'        : {'read_only': True},
            'CityDistrictTitle': {'read_only': True},
        }


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EmailAddress
        fields = [
            'id',
            'Email',
            'Title',
            'IsDefault',
            'Person_id',

            # FK Title
            'PersonFullname',
            # FIXME be able to get this when we have Person_id?
        ]
        extra_kwargs = {
            'PersonFullname': {'read_only': True},
            # FIXME be able to get this when we have Person_id?

        }


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumber
        fields = [
            'id',
            'TelNumber',
            'Title',
            'IsDefault',

            'Person_id',
            'Province_id',
            'TelType_id',

            # FK Title
            'ProvinceTitle',
            'TelTypeTitle',
        ]
        extra_kwargs = {
            'ProvinceTitle': {'read_only': True},
            'TelTypeTitle' : {'read_only': True},
        }


class MinimalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = [
            'UserName',
            'NationalCode',
            'FullName',
            'StaticPhotoURL', ]

        extra_kwargs = {
            'StaticPhotoURL': {'read_only': True},

        }

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = [
            'UserName',
            'FirstName',
            'LastName',
            'FullName',
            'FirstNameEnglish',
            'LastNameEnglish',
            'BirthDate',
            'ContractDate',
            'ContractEndDate',
            'About',
            'Gender',
            # 'DegreeType', # FIXME choice field
            # 'MarriageStatus', # FIXME choice field
            'NumberOfChildren',
            'NationalCode',
            'FatherName',
            'IdentityNumber',
            'IdentityRegisterDate',
            # 'IdentitySerialNumber',
            'InsuranceNumber',
            # 'Address',
            # 'AuthLoginDate',
            # 'AuthLoginKey',
            'CVFile',

            # FK
            'BirthCity_id',
            'Religion_id',
            'DegreeType_id',
            'LivingAddress_id',
            'MarriageStatus_id',
            'MilitaryStatus_id',
            # 'MilitaryStatus_id',  # FIXME choice field
            'ContractType_id',
            'UserStatus_id',

            # FK Titles
            'LivingAddressText',
            'Degree_TypeTitle',
            'Marriage_StatusTitle',
            'Military_StatusTitle',
            'UserStatusTitle',
            'ContractTypeTitle',
            'BirthCityTitle',
            'IdentityCityTitle',
            'ReligionTitle',
            'PhotoURL',
            'StaticPhotoURL', ]

        extra_kwargs = {
            'LivingAddressText'   : {'read_only': True},
            'Degree_TypeTitle'    : {'read_only': True},
            'Marriage_StatusTitle': {'read_only': True},
            'Military_StatusTitle': {'read_only': True},
            'BirthCityTitle'      : {'read_only': True},
            'ReligionTitle'       : {'read_only': True},
            'PhotoURL'            : {'read_only': True},
            'StaticPhotoURL'      : {'read_only': True},
            'FullName'            : {'read_only': True},

            # FIXME where should i put path const ???
        }


class FullInfoUserSerializer(serializers.ModelSerializer):
    all_phone_number = serializers.SerializerMethodField()
    all_team_role = serializers.SerializerMethodField()
    corresponding_degree_info = serializers.SerializerMethodField()
    found_in_educational_history = serializers.SerializerMethodField()

    class Meta:
        model = models.Users
        fields = [
            'UserName',
            'FirstName',
            'LastName',
            'FullName',
            'FirstNameEnglish',
            'LastNameEnglish',
            'BirthDate',
            'ContractDate',
            'ContractEndDate',
            'About',
            'Gender',
            # 'DegreeType', # FIXME choice field
            # 'MarriageStatus', # FIXME choice field
            'NumberOfChildren',
            'NationalCode',
            'FatherName',
            'IdentityNumber',
            'IdentityRegisterDate',
            # 'IdentitySerialNumber',
            'InsuranceNumber',
            # 'Address',
            # 'AuthLoginDate',
            # 'AuthLoginKey',
            'CVFile',

            # FK
            'BirthCity_id',
            'Religion_id',
            'DegreeType_id',
            'LivingAddress_id',
            'MarriageStatus_id',
            'MilitaryStatus_id',
            'UserStatus_id',
            'ContractType_id',


            # FK Titles
            'LivingAddressText',
            'Degree_TypeTitle',
            'found_in_educational_history',
            'Marriage_StatusTitle',
            'Military_StatusTitle',
            'UserStatusTitle',
            'ContractTypeTitle',
            'BirthCityTitle',
            'IdentityCityTitle',
            'ReligionTitle',
            'PhotoURL',  # FK ???? DFQ
            'StaticPhotoURL',

            # Child relations
            'all_phone_number',
            'all_team_role',
            'corresponding_degree_info',

        ]
        extra_kwargs = {
            'LivingAddressText'   : {'read_only': True},
            'Degree_TypeTitle'    : {'read_only': True},
            'Marriage_StatusTitle': {'read_only': True},
            'Military_StatusTitle': {'read_only': True},
            'BirthCityTitle'      : {'read_only': True},
            'ReligionTitle'       : {'read_only': True},
            'IdentityCityTitle'   : {'read_only': True},
            'PhotoURL'            : {'read_only': True},
            'StaticPhotoURL'      : {'read_only': True},
            'FullName'            : {'read_only': True},

            # FIXME where should i put path const ???
        }

    def get_all_phone_number(self, obj):
        all_phone_numbers = obj.phone_number.all()
        return PhoneNumberSerializer(instance=all_phone_numbers, many=True).data

    def get_all_team_role(self, obj):
        all_team_role = obj.UserTeamRoleUserNames.all()
        return UserTeamRoleSerializer(instance=all_team_role, many=True).data

    def get_found_in_educational_history(self, obj):
        if not obj.DegreeType_id:
            return False
        last_degree_info = obj.education_history.filter(
            Degree_Type_id=obj.DegreeType_id)

        if last_degree_info:
            return True
        return False



    def get_corresponding_degree_info(self, obj):
        degree_in_users_table = obj.DegreeType_id

        last_degree_info = obj.education_history.filter(
            Degree_Type_id=degree_in_users_table)
        if last_degree_info:
            return EducationHistorySerializer(instance=last_degree_info,
                                          many=True).data
        return {}


class ConstValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConstValue
        fields = ['id',
                  'Caption',
                  'Code',
                  'IsActive',
                  'OrderNumber',
                  'ConstValue',
                  'Parent_id',

                  # FK Title
                  'ParentTitle',
                  ]
        extra_kwargs = {
            'ParentTitle': {'read_only': True}
        }


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.University
        fields = [
            'id',
            'Title',
            # 'UniversityType',  # FIXME: ??? CHOICE TYPE???!   ???
            'UniversityCity_id',
            'University_Type_id',

            # FK Title
            'UniversityCityTitle',
            'UniversityTypeTitle',
        ]
        extra_kwargs = {
            'UniversityCityTitle': {'read_only': True},
            'UniversityTypeTitle': {'read_only': True}
        }


class FieldOfStudySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FieldOfStudy
        fields = '__all__'


class TendencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tendency
        fields = [
            'id',
            'Title',
            'FieldOfStudy_id',

            # FK Title
            'FieldOfStudyTitle',
        ]
        extra_kwargs = {
            'FieldOfStudyTitle': {'read_only': True}
        }


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EducationHistory
        fields = ["id",
                  # "DegreeType", # FIXME choice field
                  "StartDate",
                  "EndDate",
                  "StartYear",
                  "EndYear",
                  "IsStudent",
                  "GPA",
                  "Degree_Type_id",
                  "EducationTendency_id",
                  "Person_id",
                  "University_id",

                  # FK Title
                  'DegreeTitle',
                  'TendencyTitle',
                  'PersonFullName',
                  # FIXME be able to get this when we have Person_id?
                  'UniversityTitle',

                  ]
        extra_kwargs = {
            'DegreeTitle'    : {'read_only': True},
            'TendencyTitle'  : {'read_only': True},
            'PersonFullName' : {'read_only': True},
            # FIXME be able to get this when we have Person_id?
            'UniversityTitle': {'read_only': True}

        }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'


class SimpleUserTeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTeamRole
        fields = ['id',
                  'Superior',
                  'StartDate',
                  'EndDate',
                  'LevelId_id',
                  'ManagerUserName_id',
                  'RoleId',
                  'TeamCode',
                  'UserName',
                  'NationalCode',
                  'ManagerNationalCode',

                  # FK Title
                  'LevelTitle',
                  'RoleTitle',
                  'TeamName',
                  ]
        extra_kwargs = {
            'LevelTitle': {'read_only': True},
            'RoleTitle' : {'read_only': True},
            'TeamName'  : {'read_only': True},
        }


# class UserTeamRoleSerializer(serializers.ModelSerializer):
#     all_employee = serializers.SerializerMethodField()

#     class Meta:
#         model = models.UserTeamRole
#         fields = ['id',
#                   'Superior',
#                   'StartDate',
#                   'EndDate',
#                   'LevelId_id',
#                   'ManagerUserName_id',
#                   'RoleId',
#                   'TeamCode',
#                   'UserName',

#                   # FK Title
#                   'LevelTitle',
#                   'RoleTitle',
#                   'TeamName',

#                   # Child
#                   'all_employee',
#                   ]
#         extra_kwargs = {
#             'LevelTitle': {'read_only': True},
#             'RoleTitle' : {'read_only': True},
#             'TeamName'  : {'read_only': True},
#         }

#     def get_all_employee(self, obj):
#         employees_list = models.UserTeamRole.objects.filter(ManagerUserName=obj.UserName).filter(
#             TeamCode=obj.TeamCode).values_list('UserName',
#                                                flat=True)

#         employees_full_info_qs = models.Users.objects.filter(UserName__in=employees_list)
#         return FullInfoUserSerializer(instance=employees_full_info_qs, many=True).data


class RoleLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoleLevel
        fields = '__all__'


class ChangeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChangeRole
        fields = [
            'id',
            'Superior',
            'SuperiorTarget',
            'Education',
            'Educator',
            'Evaluation',
            'Assessor',
            'RequestGap',
            'Assessor2',
            'ReEvaluation',
            'PmChange',
            'ITChange',

            'LevelId_id',
            'LevelIdTarget_id',
            'RoleID_id',
            'RoleIdTarget_id',  # FIXME: ROLE ID TARGET ID !? what is this name ?

            # FK Title
            'CurrentLevelTitle',
            'LevelTargetTitle',
            'CurrentRoleTitle',
            'RoleTargetTitle',
        ]
        extra_kwargs = {
            'CurrentLevelTitle': {'read_only': True},
            'LevelTargetTitle' : {'read_only': True},
            'CurrentRoleTitle' : {'read_only': True},
            'RoleTargetTitle'  : {'read_only': True}
        }


class RoleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoleGroup
        fields = ['id',
                  'RoleGroup',
                  'RoleGroupName',
                  'RoleID_id',

                  # FK Title
                  'RoleTitle',
                  ]
        extra_kwargs = {
            'RoleTitle': {'read_only': True}
        }


class RoleGroupTargetExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoleGroupTargetException
        fields = '__all__'


class AccessPersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccessPersonnel
        fields = '__all__'


class OrganizationChartRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationChartRole
        fields = [
            'id',
            'LevelId_id',
            'RoleId_id',

            # FK Title
            'LevelTitle',
            'RoleTitle',
        ]
        extra_kwargs = {
            'LevelTitle': {'read_only': True},
            'RoleTitle' : {'read_only': True}
        }


class OrganizationChartTeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationChartTeamRole
        fields = ['id',
                  'RoleCount',
                  'ManagerUserName_id',
                  'OrganizationChartRole_id',
                  'TeamCode_id',

                  # FK Title
                  'LevelTitle',
                  'RoleTitle',
                  'TeamTitle',
                  ]
        extra_kwargs = {
            'LevelTitle': {'read_only': True},
            'RoleTitle' : {'read_only': True},
            'TeamTitle' : {'read_only': True},
        }


class UserHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserHistory
        fields = '__all__'


class PreviousUserTeamRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PreviousUserTeamRole
        fields = [
            'id',
            'Superior',
            'StartDate',
            'EndDate',
            'LevelId_id',
            'ManagerUserName_id',
            'RoleId_id',
            'TeamCode',
            'UserName',
            'NationalCode',
            'ManagerNationalCode',
            

            # FK Title
            'LevelTitle',
            'RoleTitle',
            'TeamTitle',

        ]
        extra_kwargs = {
            'LevelTitle': {'read_only': True},
            'RoleTitle' : {'read_only': True},
            'TeamTitle' : {'read_only': True},
        }


class PageInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PageInformation
        fields = '__all__'


class PagePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PagePermission
        fields = [
            'id',
            'GroupId',
            'Editable',
            'Page_id',

            # FK Title
            'PageTitle',
        ]
        extra_kwargs = {
            'PageTitle': {'read_only': True}
        }
