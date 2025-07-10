from django.urls import path
from . import views

app_name="RoleManager_ChangeAllowedRole"
urlpatterns = [
    path("", views.setTeamAllowedRoleRequest, name="setTeamAllowedRoleRequest"),
    path("<int:requestID>", views.showSetTeamAllowedRoleRequest, name="showSetTeamAllowedRoleRequest"),

    # Cartable Standard Gateway
    path('Inbox/<int:request_id>/', views.cartable_inbox_change_allowed_role, name="cartable_inbox"),
    path('Outbox/<int:request_id>/',views.cartable_outbox_change_allowed_role , name="cartable_outbox"),
    path('Mybox/<int:request_id>/', views.cartable_mybox_change_allowed_role, name="cartable_mybox"),
]