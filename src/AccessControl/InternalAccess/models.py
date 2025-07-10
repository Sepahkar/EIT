from django.db import models


class AppInfo(models.Model):
    AppName = models.CharField(max_length=200,verbose_name="نام لاتین برنامه")
    AppTitle = models.CharField(max_length=200, verbose_name="عنوان برنامه")
    ENGINE = models.CharField(max_length=200,null=True,blank=True)
    NAME = models.CharField(max_length=200,null=True,blank=True)
    USER = models.CharField(max_length=200,null=True,blank=True)
    PASSWORD = models.CharField(max_length=200,null=True,blank=True)
    HOST = models.CharField(max_length=200,null=True,blank=True)
    PORT = models.CharField(max_length=200,null=True,blank=True)
    OPTIONS = models.JSONField(null=True,blank=True)
    APPIP = models.GenericIPAddressField(verbose_name="آیپی سرور برنامه",null=True,blank=True)
    APPPORT = models.IntegerField(verbose_name="پورت سرور برنامه",null=True,blank=True)
    APPSCHEMA = models.CharField(max_length=10,default="http://",blank=True,verbose_name="اس اس ال برنامه")

    class Meta:
        verbose_name = "اطلاعات برنامه"
        verbose_name_plural = "اطلاعات برنامه ها"

    @property
    def FullUrl(self):
        ret = ''
        if self.APPSCHEMA and self.APPIP and self.APPPORT and self.AppName:
            ret = self.APPSCHEMA + self.APPIP + ":" + str(self.APPPORT) + "/" + self.AppName + "/"
        return ret

    def __str__(self):
        return self.AppName + '-' + self.AppTitle


class PermissionUser(models.Model):
    class Meta:
        verbose_name = "مجوز کاربر"
        verbose_name_plural = "دسترسی کاربران"


class PermissionGroup(models.Model):
    class Meta:
        verbose_name = "مجوز گروه"
        verbose_name_plural = "دسترسی گروه ها"


class UserGroup(models.Model):

    class Meta:
        verbose_name = "گروه کاربر"
        verbose_name_plural = "اعضای گروه ها"


class UpdateAppInfo(models.Model):
    class Meta:
        verbose_name = "بروزرسانی"
        verbose_name_plural = "بروزرسانی اطلاعات برنامه ها"

    def __str__(self):
        return 'برنامه ها'


class VirtualUsers(models.Model):
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        managed = False





