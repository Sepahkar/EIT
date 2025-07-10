from django.urls import path

from .api import (
    GetAppTeams,
    GetAllAppsInfo,
    CheckUserPermission,
    GetPermittedUrl,
    CheckUserPermissionList,
    GetAppURL,
    GetSystem,
    GetAppBySystemCode,
    GetAppByAppCode,
    GetApps,
    GetServer,
    GetAppByLabelSystem,
    GetAllAppsURL,
    GetPermittedAllUrl,
    GetAllSystems,
    GetAllServers,
    CheckUrlIsPublic,
)
from .views import list_app_urls, list_app_users, grant_user_access

app_name = "AccessControl"
urlpatterns = [
    # grant user access (minimal form )
    path('ListAppPermissions/', list_app_urls, name='permission_list'),
    path('PermissionUsers/', list_app_users, name='permission_users'),
    path('GrantUserAccess', grant_user_access, name='grant_access'),

    path('CheckUserPermission/<str:permission_code>/<str:username>/',CheckUserPermission.as_view(),name="check_user_permission"),
    path('GetAppTeams/<str:app_label>/',GetAppTeams.as_view()),
    path('GetUserURLs/<str:app_label>/<str:username>/', GetPermittedUrl.as_view(),name="get_permitted_url"),
    path('GetUserPermissions/<str:app_label>/<str:username>/', CheckUserPermissionList.as_view(), name="check_user_permission_list"),
    # api urls
    path('api/check-user-permission/<str:permission_code>/<str:username>/',CheckUserPermission.as_view(),name="check_user_permission"),
    path('api/get-app-teams/<str:app_label>/', GetAppTeams.as_view()),
    path('api/get-user-urls/<str:app_label>/<str:username>/', GetPermittedUrl.as_view(),name="get_permitted_url"),
    path('api/get-user-all-urls/<str:username>/', GetPermittedAllUrl.as_view(),name="get_permitted_all_url"),
    path('api/get-user-permissions/<str:app_label>/<str:username>/', CheckUserPermissionList.as_view(), name="check_user_permission_list"),

    path('api/get-all-apps-info/', GetAllAppsInfo.as_view(),name="all_app_info"),
    path('api/get-app-url/<str:app_url_id>/', GetAppURL.as_view(),name="get_app_url"),
    path('api/get-all-apps-url/', GetAllAppsURL.as_view(),name="get_all_apps_url"),
    path('api/get-system/<str:system_code>/', GetSystem.as_view(),name="get_system"),
    path('api/get-all-systems/', GetAllSystems.as_view(),name="get_all_systems"),
    path('api/get-server/<str:server_id>/', GetServer.as_view(),name="get_server"),
    path('api/get-all-servers/', GetAllServers.as_view(),name="get-all_servers"),
    path('api/get-app-by-systemcode/<str:system_code>/', GetAppBySystemCode.as_view(),name="get_app_by_systemcode"),
    path('api/get-app-by-appcode/<str:app_code>/', GetAppByAppCode.as_view(),name="get_app_by_appcode"),
    path('api/get-apps/', GetApps.as_view(),name="get_apps"),
    path('api/get-app-by-label-system/<str:app_label>/<str:system_code>/', GetAppByLabelSystem.as_view(), name='get_app_by_label_system'),
    path('api/check-url-is-public/', CheckUrlIsPublic.as_view(), name="check_url_is_public"),
    
]

