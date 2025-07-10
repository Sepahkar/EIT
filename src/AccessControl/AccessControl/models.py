from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.utils.text import slugify


class Server(models.Model):
    class Meta:
        verbose_name = "سرور"
        verbose_name_plural = "سرورها"

    IPAddress = models.GenericIPAddressField(verbose_name="ادرس")
    DNSName = models.CharField(
        max_length=200, null=True, blank=True, verbose_name="نام سرور"
    )
    ServerName = models.CharField(max_length=200, verbose_name="نام ")


class System(models.Model):
    class Meta:
        verbose_name = "سیستم"
        verbose_name_plural = "سیستم ها"

    Code = models.CharField(
        max_length=3, db_column="Code", primary_key=True, verbose_name="کد"
    )
    Title = models.CharField(max_length=100, verbose_name="عنوان")
    PortNumber = models.IntegerField(verbose_name="پورت")
    Logo = models.ImageField(
        upload_to="media/", verbose_name="تصویر", null=True, blank=True
    )
    Server = models.ForeignKey(
        "Server", null=True, on_delete=models.CASCADE, verbose_name="نام سرور"
    )

    def __str__(self):
        return self.Title


class PermissionVariable(models.Model):
    class Meta:
        verbose_name = "متغیر"
        verbose_name_plural = "متغیر ها"

    Code = models.CharField(max_length=5, verbose_name="کد")
    Title = models.CharField(max_length=100, verbose_name="عنوان")
    VariableDescription = models.CharField(max_length=200, verbose_name="شرح")

    def __str__(self):
        return self.Title


class PermissionVariableValue(models.Model):
    class Meta:
        verbose_name = "مقدار متغیر"
        verbose_name_plural = "مقادیر متغیرها"

    PermissionVariable = models.ForeignKey(
        "PermissionVariable", on_delete=models.CASCADE, verbose_name="نام تغیر"
    )

    # @متغیر #مقدار
    App = models.ForeignKey("App", on_delete=models.CASCADE, verbose_name="نام برنامه")
    OwnerVariableRole = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="سمت",
    )
    OwnerVariableGroup = models.ForeignKey(
        "PermissionGroup",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="گروه",
    )
    OwnerVariableUser = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="کاربر",
    )

    def __str__(self):
        return self.App.Title + "-" + self.PermissionVariable.Title


class VariableValueRelated(models.Model):
    class Meta:
        verbose_name = "مقدار "
        verbose_name_plural = "مقادیر "

    ValueTitle = models.CharField(max_length=200, verbose_name="مقدار متغیر")
    VariableValue = models.ForeignKey(
        "PermissionVariableValue",
        on_delete=models.CASCADE,
        null=True,
        verbose_name=" متغیر",
    )


class App(models.Model):
    class Meta:
        verbose_name = "برنامه"
        verbose_name_plural = "برنامه ها"

    Code = models.CharField(
        max_length=6, db_column="Code", primary_key=True, verbose_name="کد"
    )
    Title = models.CharField(max_length=200, verbose_name="عنوان")
    SystemCode = models.ForeignKey(
        "System", verbose_name="کدسیستم", on_delete=models.CASCADE
    )
    AppLabel = models.SlugField(
        max_length=100, null=True, blank=True, verbose_name="نام لاتین برنامه"
    )

    def save(self, *args, **kwargs):
        self.AppLabel = slugify(str(self.AppLabel).lower())
        super(App, self).save(*args, **kwargs)

    def __str__(self):
        if self.AppLabel is None:
            return ""
        return self.AppLabel


class AppURL(models.Model):
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس ها"

    AppCode = models.ForeignKey(
        "App", on_delete=models.CASCADE, db_column="AppCode", verbose_name="کد اپلیکیشن"
    )
    URL = models.CharField(max_length=500, verbose_name="مسیر دسترسی")
    IsPublic = models.BooleanField(default=False)

    def __str__(self):
        extra = "(admin)" if "admin" in self.URL else ""
        return str(self.AppCode) + extra


class AppPermissionType(models.Model):
    class Meta:
        verbose_name = "نوع دسترسی"
        verbose_name_plural = "نوع های دسترسی "

    AppCode = models.ForeignKey(
        "App", db_column="AppCode", on_delete=models.CASCADE, verbose_name="کد برنامه"
    )
    PermissionType = models.CharField(max_length=100)

    def __str__(self):
        return str(self.AppCode)


class PermissionGroup(models.Model):
    class Meta:
        verbose_name = "گروه دسترسی"
        verbose_name_plural = "گروه های دسترسی "

    Title = models.CharField(max_length=100, verbose_name="شرح")

    def __str__(self):
        return self.Title


class UserRoleGroupPermission(models.Model):
    class Meta:
        verbose_name = "دسته بندی دسترسی "
        verbose_name_plural = "دسته بندی دسترسی ها "

    PermissionCode = models.ForeignKey(
        "Permission",
        on_delete=models.CASCADE,
        db_column="PermissionCode",
        verbose_name="کددسترسی",
    )
    OwnerPermissionRole = models.IntegerField(null=True, blank=True)
    OwnerPermissionGroup = models.ForeignKey(
        "PermissionGroup",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="OwnerPermissionGroup",
        verbose_name="گروه",
    )
    OwnerPermissionUser = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.PermissionCode)

    def clean(self):
        if (
            self.OwnerPermissionRole is None
            and self.OwnerPermissionGroup is None
            and self.OwnerPermissionUser is None
        ):
            raise ValidationError(
                "حتما یکی از گزنه های نقش وگروه و یا کاربر باید انتخاب شود"
            )
        if (
            (
                self.OwnerPermissionRole is not None
                and (
                    self.OwnerPermissionGroup is not None
                    or self.OwnerPermissionUser is not None
                )
            )
            or (
                self.OwnerPermissionGroup is not None
                and (
                    self.OwnerPermissionRole is not None
                    or self.OwnerPermissionUser is not None
                )
            )
            or (
                self.OwnerPermissionUser is not None
                and (
                    self.OwnerPermissionGroup is not None
                    or self.OwnerPermissionRole is not None
                )
            )
        ):
            raise ValidationError(
                "فقط یکی از کزینه های نقش و گروه و کاربر را میتوانید انخاب کنید"
            )


class Permission(models.Model):
    class Meta:
        verbose_name = "  دسترسی "
        verbose_name_plural = "دسترسی ها "

    Code = models.CharField(
        max_length=10, db_column="Code", primary_key=True, verbose_name="کد"
    )
    Title = models.CharField(max_length=100, verbose_name="عنوان")
    AppCode = models.ForeignKey(
        "App", verbose_name="کد برنامه", on_delete=models.CASCADE
    )
    PermissionType_View = "V"
    PermissionType_Edit = "E"
    PermissionType_Admin = "A"
    PermissionType_URL = "U"
    PermissionType_Desktop = "D"
    PermissionType_Choices = (
        (PermissionType_View, "مجوز مشاهده"),
        (PermissionType_Edit, "مجوز ویرایش"),
        (PermissionType_Admin, "دسترسی کامل"),
        (PermissionType_URL, "دسترسی ادرس"),
        (PermissionType_Desktop, "دسترسی پورتال"),
    )
    PermissionType = models.CharField(
        choices=PermissionType_Choices, max_length=1, verbose_name="نوع مجوز"
    )

    def __str__(self):
        return self.Title


class GroupUser(models.Model):
    class Meta:
        verbose_name = "گروه کاربری "
        verbose_name_plural = "گروه های کاربری "

    User = models.CharField(max_length=50)
    Group = models.ForeignKey(
        "PermissionGroup", on_delete=models.CASCADE, verbose_name="گروه"
    )

    def __str__(self):
        return self.Group.Title


class RelatedPermissionAPPURL(models.Model):
    class Meta:
        verbose_name = "ارتباط آدرس با دسترسی "
        verbose_name_plural = "آدرس ها و دسترسی های مرتبط "

    Permission = models.ForeignKey(
        "Permission", on_delete=models.CASCADE, verbose_name="نام دسترسی"
    )
    AppURL = models.ForeignKey("AppURL", on_delete=models.CASCADE, verbose_name="آدرس")

    def __str__(self):
        return self.Permission.Title


class AppTeam(models.Model):
    class Meta:
        verbose_name = "تیم برنامه "
        verbose_name_plural = "تیم های برنامه ها "

    AppCode = models.ForeignKey(
        "App", verbose_name="نام برنامه", on_delete=models.CASCADE
    )
    TeamCode = models.CharField(max_length=3)

    def __str__(self):
        return self.AppCode.Title
