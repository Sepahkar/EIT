from django.db import models
import HR.models as HRMODEL
from django_middleware_global_request.middleware import get_request


class AbstractDateTime(models.Model):
    class Meta:
        abstract = True
    CreateDate = models.DateTimeField(
        auto_now_add=True, null=True,blank=True, verbose_name="تاریخ ایجاد")
    ModifyDate = models.DateTimeField(
        auto_now=True, null=True,blank=True, verbose_name="تاریخ ویرایش")
    CreatorUserName = models.ForeignKey(
        HRMODEL.Users, db_constraint=False, null=True,blank=True, verbose_name="ایجاد کننده",
        related_name="%(app_label)s_%(class)s_cr"
    ,on_delete=models.DO_NOTHING)
    ModifierUserName = models.ForeignKey(
        HRMODEL.Users, db_constraint=False, null=True,blank=True, verbose_name="ویرایش کننده", on_delete=models.DO_NOTHING
        ,related_name="%(app_label)s_%(class)s_md")

    def save(self,*args,**kwargs):
        request = get_request()
        username = None
        if request.user.is_authenticated:
            username = request.user.UserName.lower()

        if self._state.adding:
            # insert new data
            self.CreatorUserName_id = username
        else:
            # update data
            self.ModifierUserName_id = username

        super().save(*args,**kwargs)


class RoleCategory(models.Model):

    CategoryName = models.CharField(max_length=100, verbose_name='دسته بندی')
    Conditions = 'C'
    Duties = 'D'
    DescriptionTypeChoice = ((Conditions,'شرایط احراز'), (Duties,'شرح وظایف'))
    DescriptionType = models.CharField(max_length=1, choices=DescriptionTypeChoice, verbose_name='نوع')

    class Meta:
        verbose_name ='دسته بندی سمت'
        verbose_name_plural ='دسته بندی های سمت'

    def __str__(self):
        return self.CategoryName + '(' + dict(self.DescriptionTypeChoice)[self.DescriptionType] + ')'


class RoleDescription(AbstractDateTime):
    class Meta:
        verbose_name = 'توضیحات سمت'
        verbose_name_plural = 'توضیحات سمت ها'

    RoleId = models.ForeignKey(HRMODEL.Role, verbose_name='شناسه سمت', null=True,db_column='RoleId', on_delete=models.CASCADE)
    LevelId = models.ForeignKey(HRMODEL.RoleLevel, verbose_name='شناسه سطح', null=True,db_column='LevelId'
                               , on_delete=models.CASCADE)
    Superior = models.BooleanField(verbose_name='ارشد', default=False)
    Title = models.CharField(max_length=4000, verbose_name='شرح')
    Category = models.ForeignKey('RoleCategory', on_delete=models.CASCADE,verbose_name='نوع')
    IsConfirm = models.BooleanField(default=False, verbose_name='تایید')


class RolePermission(AbstractDateTime):
    class Meta:
        verbose_name = 'دسترسی سمت'
        verbose_name_plural = 'دسترسی سمت ها'
    Role = models.ForeignKey(HRMODEL.Role,on_delete=models.CASCADE,db_constraint=False,verbose_name='سمت')
    Permission = models.IntegerField(verbose_name='دسترسی')
    #Permission = models.ForeignKey(A.Permission, on_delete=models.CASCADE, db_constraint=False, verbose_name='دسترسی')

    def __str__(self):
        return self.Role.RoleName


class Request(models.Model):
    CurrentStep = ""
    Username = ""
    FromTeam = ""
    FromLevel = ""
    ToTeam = ""
    ToLevel = ""


class Step(models.Model):
    Order = ""
    Titlte = ""
    RolesStep = ""


class RequestStep(models.Model):
    Step = ""
    Opinioner = ""
    Comment = ""
    CommenType = ""


