import traceback

def tokeninfo(request):
    data = {
        "user_Gender":request.user.gender,
        "username":request.user.username + "@eit",
        "user_FullName":request.user.fullname,
        "team_role_info": request.user.team_roles["current"] if request.user.team_roles else []
    }
    context_extras = {}
    for key,value in data.items():
                try:
                    new_key = "cnt_"+key
                    context_extras.update({
                        new_key:value
                    })
                except:
                    traceback.print_exc()
            

    return context_extras

