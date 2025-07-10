from django.urls import path
from .views import index,get_user_teamrole,get_role_user,insert_description,delete_description


app_name = "Duties"
urlpatterns = [
    path('', index, name='index'),
    path('InsertDescription/', insert_description, name='insert_description'),
    path('DeleteDescription/', delete_description, name='delete_description'),
    path('getuserteamrole/<str:teamcode>/<int:roleid>/<int:levelid>/<int:superior>/',get_user_teamrole,name='get_user_teamrole'),
    path('getuserrole/',get_role_user,name='get_role_user'),
    path('getuserteamrole/<str:teamcode>/<int:roleid>/<int:levelid>/<int:superior>/',get_user_teamrole,name='get_user_teamrole'),
]


