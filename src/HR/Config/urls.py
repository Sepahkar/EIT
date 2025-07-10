from django.urls import path, include


urlpatterns = [
    path("HR/", include("HR.urls")),
    # path("RoleManager/AllowRoleTeamRequest/", include("roleManager.urls_change_allowed_role")),
    # path("RoleManager/NewRoleRequest/", include("roleManager.urls_new_role")),
]
