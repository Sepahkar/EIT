from django.test import TestCase

    if request.method == "POST":
        information["currentUser_role"] = "MAN"
        try:
            # اطلاعاتی که از طرف صفحه میاد
            body_data = json.loads(request.body)
            # تایید درخواست
            if body_data["status"] == "ACCEPT":
                if information["currentUser_role"] == "CTO":
                    response = saveNewRoleRequest(newRoleRequest=REQUEST)
                    if response["error"]:
                        raise ValueError(response["message"])
                    else:
                        DATA["message"] = response["message"]

                elif information["currentUser_role"] == "MAN": #این قسمت خطا نمیده باید از اول بررسی بشه، از وقتی که چک میکنه که درخواست پست یا نه!
                    
                    try:
                        response = register_send_document(
                            information=information,
                            newRecord=REQUEST,
                            document_title="تایید درخواست ایجاد سمت جدید",
                            doc_state="بررسی مدیر عامل",
                        )
                        if response["Error"]:
                            raise ValueError(response["message"])
                        else:
                            REQUEST.RoleTitle = body_data["RoleTitle"]
                            REQUEST.HasLevel = body_data["HasLevel"]
                            REQUEST.HasSuperior = body_data["HasSuperior"   ]
                            REQUEST.AllowedTeams = body_data["AllowedTeams"]
                            REQUEST.ConditionsText = body_data["Conditions"]
                            REQUEST.DutiesText = body_data["Duties"]
                            REQUEST.RequestorId = information["currentUser_nationalCode"]
                            REQUEST.ManagerId = information["currentUser_managers"][0]
                            REQUEST.ManagerOpinion = 1
                            REQUEST.CTOId = information["cto_nationalCode"]
                            REQUEST.StatusCode = "CTOREV"
                            REQUEST.RelevantManager = body_data["RelevantManager"]
                            REQUEST.save()
                    DATA["message"] = response["message"]
                    except Exception as error:
                        print(error, str(error), type(error))
                        raise ValueError(str(error))
            # رد درخواست
            elif body_data["status"] == "REJECT":
                if information["currentUser_role"] == "CTO":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.CTOOpinion = 0
                    REQUEST.save()
                    DATA["message"] = "درخواست از طرف مدیر عامل با موفقیت رد شد"
                elif information["currentUser_role"] == "MAN":
                    REQUEST.StatusCode = "FINREJ"
                    REQUEST.ManagerOpinion = 0
                    REQUEST.save()
                    DATA["message"] = "درخواست از طرف مدیر با موفقیت رد شد"
        except ValueError as error:
            DATA["error"] = True
            DATA["message"] = str(error)
            return JsonResponse(DATA)
        except Exception as error:
            DATA["error"] = True
            DATA["message"] = "متاسفانه خطایی رخ داده است"
            print(error)
            return JsonResponse(DATA)

        return JsonResponse(DATA)
    else:
        if information["error"]:
            DATA["error"] = True
            DATA["message"] = information["message"]
        else:
            match information["currentUser_role"]:
                case "CTO":
                    if REQUEST.StatusCode == "CTOREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "MAN":
                    if REQUEST.StatusCode == "MANREV":
                        DATA["status"] = "EDIT"
                    else:
                        DATA["status"] = "READONLY"
                case "DEF":
                    if information["currentUser_nationalCode"] == REQUEST.RequestorId:
                        if REQUEST.StatusCode == "DRAFTR":
                            DATA["status"] = "EDIT"
                        else:
                            DATA["status"] = "READONLY"
                    else:
                        DATA["error"] = True
                        DATA["message"] = "متاسفانه شما میتوانید فقط درخواست های خود را مشاهده کنید"
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    except Exception as error:
        print("Hello")
