# ruff: noqa: E501
from django.urls import path
from HR import views
from HR import api_new
from HR import api

app_name = "HR"
urlpatterns = [
    path('api/all-users/', api.AllUsers.as_view(), name="all_users" ),
    path('api/all-team-service/', api.AllTeamService.as_view(), name="all-team-service" ),
    path('api/all-team-evaluation/', api.AllTeamEvaluation.as_view(), name="all-team-evaluation"),
    path('api/find-team/', api.FindTeam.as_view(), name="find-team"),
    path('api/get-user/<str:username>/', api.GetUser.as_view(), name="get_user" ),
    path('api/get-user-team-role/<str:username>/', api.GetUserTeamRole.as_view(), name="get_user_team_role" ),
    path('api/get-user-all-team-role/<str:username>/', api.GetUserAllTeamRole.as_view(), name="get_user_all_team_role" ),
    path('api/get-user-team-roles/', api.GetUserTeamRoles.as_view(), name="get_user_team_roles" ),
    path('api/get-user-roles/<str:username>/', api.GetUserRoles.as_view(), name="get_user_roles" ),
    path('api/get-all-roles/', api.GetAllRoles.as_view(), name="get_all_roles" ),
    path('api/get-all-teams/', api.GetAllTeams.as_view(), name="get_all_teams" ),
    path('api/get-v-role-target/', api.GetViewRoleTarget.as_view(), name="get_v_role_target"),
    path('api/get-v-role-team/', api.GetViewRoleTeam.as_view(), name="get_v_role_team"),
    path('api/get-previous-user-team-roles/', api.GetPreviousUserTeamRoles.as_view(), name="get_previous_user_team_roles"),
    path('api/get-all-v-role-team/', api.GetAllViewRoleTeam.as_view(), name="get_all_v_role_team"),

    # primary key is NationalCode
    path('api/get-user/<str:national_code>/v2/', api.GetUserByNationalCode.as_view(), name="get_user_by_national_code"),
    path('api/get-user-team-role/<str:national_code>/v2/', api.GetUserTeamRoleByNationalCode.as_view(), name="get_user_team_role_by_national_code" ),
    path('api/get-user-all-team-role/<str:national_code>/v2/', api.GetUserAllTeamRoleByNationalCode.as_view(), name="get_user_all_team_role_by_national_code" ),
    path('api/get-user-roles/<str:national_code>/v2/', api.GetUserRolesByNationalCode.as_view(), name="get_user_roles_by_national_code" ),


    # this urls for sp sql
    path('api/call-sp-assessors-educator/', api.CallSpAssessorsEducator.as_view(), name="call_sp_assessors_educator"),
    path('api/call-sp-get-teams-of-role/', api.CallSpGetTeamsOfRole.as_view(), name="call_sp_get_teams_of_role"),
    path('api/call-sp-get-manager-of-team/', api.CallSpGetManagerOfTeam.as_view(), name="call_sp_get_manager_of_team"),
    path('api/call-sp-get-target-role/', api.CallSpGetTargetRole.as_view(), name="call_sp_get_target_role"),
    path('api/call-func-educator-get-team-manager/', api.CallFuncEducatorGetTeamManager.as_view(), name="call_func_educator_get_team_manager"),

    # primary key is NationalCode
    path('api/call-sp-get-target-role/v2/', api.CallSpGetTargetRoleByNationalCode.as_view(), name="call_sp_get_target_role_by_national_code"),


    path('api/v1/provinces/<int:id>', api_new.Province.as_view(), name='province_by_id'),
    path('api/v1/provinces/', api_new.Province.get_all, name='all_provinces'),
    path('api/v1/cities/<int:id>', api_new.City.as_view(), name='city_by_id'),
    path('api/v1/cities/', api_new.City.get_all, name='all_cities'),
    path('api/v1/city-districts/<int:id>', api_new.CityDistrict.as_view(), name='city_district_by_id'),
    path('api/v1/city-districts/', api_new.CityDistrict.get_all, name='all_city_districts'),
    path('api/v1/users/<str:usernames>', api_new.Users.as_view(), name='multiple_users_by_username'),
    path('api/v1/users-minimal-info/', api_new.Users.get_all_users_minimal_info, name='all_users_minimal_info'),
    path('api/v1/users/full-info/<str:usernames>', api_new.Users.get_full_info, name='multiple_users_full_information_by_username'),
    path('api/v1/users/', api_new.Users.get_all, name='all_users'),
    path('api/v1/postal-addresses/<int:id>', api_new.PostalAddress.as_view(), name='postal_address_by_id'),
    path('api/v1/postal-addresses/', api_new.PostalAddress.get_all, name='all_postal_addresses'),
    path('api/v1/email-addresses/<int:id>', api_new.EmailAddress.as_view(), name='email_address_by_id'),
    path('api/v1/phone-numbers/<int:id>', api_new.PhoneNumber.as_view(), name='phone_number_by_id'),
    path('api/v1/const-values/<int:id>', api_new.ConstValue.as_view(), name='const_value_by_id'),
    path('api/v1/universities/<int:id>', api_new.University.as_view(), name='university_by_id'),
    path('api/v1/field-of-studies/<int:id>', api_new.FieldOfStudy.as_view(), name='field_of_study_by_id'),
    path('api/v1/tendencies/<int:id>', api_new.Tendency.as_view(), name='tendency_by_id'),
    path('api/v1/education-histories/<int:id>', api_new.EducationHistory.as_view(), name='education_history_by_id'),
    path('api/v1/teams/<str:team_code>', api_new.Team.as_view(), name='team_by_team_code'),
    path('api/v1/teams/', api_new.Team.get_all, name='all_team_by_filter'),
    path('api/v1/roles/<int:id>', api_new.Role.as_view(), name='role_by_id'),
    path('api/v1/roles/', api_new.Role.get_all, name='all_roles'),
    path('api/v1/user-team-roles/<int:id>', api_new.UserTeamRole.as_view(), name='user_team_role_by_id'),
    path('api/v1/role-levels/<int:id>', api_new.RoleLevel.as_view(), name='role_level_by_id'),
    path('api/v1/change-roles/<int:id>', api_new.ChangeRole.as_view(), name='change_role_by_id'),
    path('api/v1/role-groups/<int:id>', api_new.RoleGroup.as_view(), name='role_group_by_id'),
    path('api/v1/role-group-target-exceptions/<int:id>', api_new.RoleGroupTargetException.as_view(), name='role_group_exp_by_id'),
    path('api/v1/access-personnels/<int:id>', api_new.AccessPersonnel.as_view(), name='access_personnel_by_id'),
    path('api/v1/organization-chart-roles/<int:id>', api_new.OrganizationChartRole.as_view(), name='organization_chart_role_by_id'),
    path('api/v1/organization-chart-team-roles/<int:id>', api_new.OrganizationChartTeamRole.as_view(), name='organization_chart_team_role_by_id'),
    path('api/v1/user-histories/<int:id>', api_new.UserHistory.as_view(), name='user_history_by_id'),
    path('api/v1/previous-user-team-roles/<int:id>', api_new.PreviousUserTeamRole.as_view(), name='previous_user_team_role_by_id'),
    path('api/v1/page-informations/<int:id>', api_new.PageInformation.as_view(), name='page_information_by_id'),
    path('api/v1/page-permissions/<int:id>', api_new.PagePermission.as_view(), name='page_permission_by_id'),
    path('api/v1/locations/', api_new.locations, name='locations'),
    path('api/v1/user-location/<str:username>', api_new.UserLocation.as_view(), name='user_location'),

    # primary key is NationalCode
    path('api/users/v2/', api_new.Users.get_by_national_code, name='multiple_users_by_national_code'),
    path('api/users/full-info/v2/', api_new.Users.get_full_info_by_national_code, name='multiple_users_full_information_by_national_code'),
    path('api/user-location/<str:national_code>/v2/', api_new.UserLocation.get_by_national_code, name='user_location_by_national_code'),

    path('', views.PersonInfoPage, name="hr_personeli"),
    path('List/', views.UserPageList, name="hr_list"),
    path('<str:national_code>/', views.FirstPage, name="hr_firstpage"),
    path('contact/<str:national_code>/', views.ContactInfoPage, name="hr_contact"),
    path('person/<str:national_code>/', views.PersonInfoPage, name="hr_personeli"),
    path('job/<str:national_code>/', views.JobInfoPage, name="hr_job"),
    path('payment/<str:national_code>/', views.PaymentInfoPage, name="hr_payment"),
    path('worktime/<str:national_code>/', views.WorkTimeInfoPage, name="hr_worktime"),
    path('education/<str:national_code>/', views.EducationHistory, name="hr_personeli"),
    path('facilities/<str:national_code>/', views.FacilitiesInfoPage, name="hr_personeli"),
    path('save/', views.UserSave),
    path('save/<str:action_type>', views.UserSave),
    path('detail/delete', views.UserDetailDelete),
    path('detail/save', views.UserDetailSave),
    path('saveimageuser/', views.SaveImageUser ,name='save_image_user'),
    
    path('profile/user/<str:username>/', views.UserProfile, name='user_profile'),
    path('profile/team/<str:teamcode>/',  views.TeamProfile, name='team_profile'),
    path('profile/picture/save/',  views.SaveUserProfileImage, name='save_user_profile'),
    path('user-profile/search/', views.UserProfileSearch, name='user_profile_search'),

    # check exists api
    path('api/exists-users/<str:pk>/', api.ExistsUsers.as_view(), name="exists_users" ),
    path('api/exists-role/<str:pk>/', api.ExistsRole.as_view(), name="exists_role" ),

    path('api/user-identity-convertor/', api_new.user_identity_convertor),

]