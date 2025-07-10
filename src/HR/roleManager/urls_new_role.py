from django.urls import path
from . import views

app_name="RoleManager_NewRole"
urlpatterns = [
    path("", views.newRoleRequest, name="newRoleRequest"),
    path("<int:requestID>", views.showNewRoleRequest, name="showNewRoleRequest"),


    # Cartable Standard Gateway
    path('Inbox/<int:request_id>/', views.cartable_inbox_new_role, name="cartable_inbox"),
    path('Outbox/<int:request_id>/',views.cartable_outbox_new_role , name="cartable_outbox"),
    path('Mybox/<int:request_id>/', views.cartable_mybox_new_role, name="cartable_mybox"),

]
