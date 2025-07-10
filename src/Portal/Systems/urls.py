from django.urls import path
import Systems.views as v

app_name = "Systems"

urlpatterns = [
    path('Systems/', v.LoadSystems, name="Systems_view"),
    # path('RefreshLogout/',v.refresh_logout,name='refresh_logout'),
    # path('TranslateUser/',v.translate_user,name='translate_user'),
    path('ChangeMyTeam/',v.change_my_team,name='change_my_team'),
    path('GenerateLinkFakeUser/',v.generate_link_fake_user,name='generate_link_fake_user'),
    #path('GetPermittedSystemlist/<str:username>/',v.GetPermittedSystemlist),
]