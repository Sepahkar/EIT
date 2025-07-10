from django.db import connection, IntegrityError
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect

import AccessControl.models as ACM



def list_app_urls(request):
    """This is the very first page when you click on 'control e dastersi >
    Afzoodan e control dastresi e moredi e afrad' in your working desktop.
    it will return a list of all permission that exists for desktop apps"""

    # this list only contains the Desktop permission
    permissions_url: QuerySet = ACM.RelatedPermissionAPPURL.objects.filter(
        Permission__PermissionType=ACM.Permission.PermissionType_Desktop
    ).order_by("Permission")

    permissions_associated_urls = [
        # Tables heading
        (x.Permission.Code,  # used for hidden input
         x.AppURL.URL,
         x.Permission.Title,
         x.Permission.AppCode.Title) for x in permissions_url]

    return render(request, "grant-access-homepage.html", context={
        "title_associated_urls": permissions_associated_urls
    })


def list_app_users(request):
    """This page is used to display all related user to this permission,
    and also you can add new user."""

    # title is the persian caption of permission
    title, permission = request.GET.get("title"), request.GET.get("permission")

    if title and permission:
        # if request comes from the list_app_urls view must have these 2
        # title and permission
        request.session["title"] = title
        request.session["permission"] = permission

    elif request.session.get("title") and request.session.get("permission"):
        # if request comes from the grant_user_access... when new user
        # inserted into database after that for confirmation of the
        # insertion this view is shown
        title = request.session.get("title")
        permission = request.session.get("permission")
    else:
        # sometime folks try to execute this view directly. without the data
        # of title and permission!It cannot work properly without these
        # items, so they've going 1 step back to the main permission list (
        # list_app_urls view) and trying again
        return redirect("AccessControl:permission_list")

    users_with_this_permission = ACM.UserRoleGroupPermission.objects.filter(
        PermissionCode=permission,
        OwnerPermissionUser__isnull=False
    ).values_list("OwnerPermissionUser", flat=True)
    context = {
        "title"     : title,
        "permission": permission,
        "users"     : users_with_this_permission,
        "error"     : None,
        "success"   : None,

    }
    # error and success will fill by grant_user_access feedback data
    error = request.session.get("error")
    success = request.session.get("success")
    if error:
        context["error"] = error

        # just want to display the error for 1 time not more !
        del request.session["error"]
    if success:
        # new user-permission insertion means success operation. UI msg
        # handled in template
        context["success"] = success
        del request.session["success"]

    return render(request, "grant-access-appuser.html", context)


def grant_user_access(request):
    permission = request.session.get("permission")
    username = request.POST.get("username").strip()

    if not username:
        request.session["error"] = "نام کاربری تمی تونه خالی باشه"
        return redirect("AccessControl:permission_users")

    elif "@eit" not in username:
        request.session["error"] = "@eit رو فراموش کردی بگذاری"
        return redirect("AccessControl:permission_users")

    # database directly connection (HRMODEL aka HR PACKAGE problem forced me
    # to do this, abusing database integrity)
    with connection.cursor() as cursor:
        with open("AccessControl/raw_queries/UserRoleGroupPermission.sql",
                  "r") as CheckDuplicationsQuery:
            q = CheckDuplicationsQuery.read()
            cursor.execute(q, [username, permission])
            row = cursor.fetchone()

        if row:
            # means duplicate permission for the user
            request.session["error"] = "دسترسی از قبل وجود دارد"
            return redirect("AccessControl:permission_users")

        with open("AccessControl/raw_queries/InsertAccess.sql",
                  "r") as InsertNewAccess:
            q = InsertNewAccess.read()
            try:
                # im inserting username directly into the table cuz I cannot
                # use DEPRECATED HR MODEL that is incompatible with current
                # HR database
                cursor.execute(q, [username, permission])
                request.session["success"] = True
                return redirect("AccessControl:permission_users")

            except IntegrityError:
                request.session[
                    "error"] = "هنگام درج در جدول خطایی از سمت دیتابیس پیش " \
                               "آمده است در حال نقض کردن Integrity دیتابیس " \
                               "هستید به صفحه اصلی رفته و دوباره تلاش کنید"
                return redirect("AccessControl:permission_users")
