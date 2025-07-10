# ruff: noqa: E501
import datetime
import json

import jdatetime
from django.core.cache import cache
from django.db import models

from HR.validator import DefaultValue as d
from HR.validator import Validator as v
from django.conf import settings



def ConstValueChoice(ConstType):
    ParentId = ConstValue.objects.filter(Code=ConstType)
    choice = {"IsActive": True}  # , "Parent_Id": ParentId[0].id}
    return choice


class Province(models.Model):
    """استان های ایران"""
    class Meta:
        verbose_name = "استان"
        verbose_name_plural = "استان ها"

    ProvinceTitle = models.CharField(max_length=50, verbose_name="نام استان", unique=True)
    AbbreviationCode = models.CharField(max_length=2, verbose_name="کد استان", null=True, blank=True)
    PhoneCode = models.IntegerField(verbose_name="پیش شماره استان", null=True, blank=True)

    def __str__(self):
        return self.ProvinceTitle


class City(models.Model):
    """شهر های استان"""
    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"

    Province = models.ForeignKey("Province", verbose_name="استان مربوطه", on_delete=models.SET_DEFAULT, default=8)
    CityTitle = models.CharField(max_length=100, verbose_name="نام شهر")

    IsCapital = models.BooleanField(verbose_name="مرکز استان است؟", default=False)
    CityCode = models.CharField(max_length=4, verbose_name="کد شهر", null=True, blank=True)

    def __str__(self):
        return self.Province.ProvinceTitle + ' ' + self.CityTitle


class CityDistrict(models.Model):
    """مناطق شهری، برای مثال تهران دارای مناطق 22 گانه است"""
    class Meta:
        verbose_name = "ناحیه شهری"
        verbose_name_plural = "نواحی شهری"

    City = models.ForeignKey("City", verbose_name="شهر مربوطه", default=d.City, on_delete=models.CASCADE)
    DistrictTitle = models.CharField(max_length=50, verbose_name="نام منطقه")

    def __str__(self):
        if self.DistrictTitle is not None:
            return self.City.CityTitle + ' - منطقه ' + self.DistrictTitle

    @property
    def CityTitle(self):
        return self.City.CityTitle


class Users(models.Model):
    """جدول اطلاعات پرسنل که شامل تمامی پرسنل حال و گذشته است"""
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        db_table = 'Users'

    UserName = models.CharField(primary_key=True, max_length=100, verbose_name='نام کاربری')
    FirstName = models.CharField(max_length=200, verbose_name='نام')
    LastName = models.CharField(max_length=200, verbose_name='نام خانوادگی')
    FirstNameEnglish = models.CharField(max_length=80, verbose_name="نام لاتین", null=True, blank=True)
    LastNameEnglish = models.CharField(max_length=100, verbose_name="نام خانوادگی لاتین", null=True, blank=True)
    FatherName = models.CharField(max_length=200, null=True, blank=True, verbose_name='نام پدر')
    ContractDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ شروع همکاری')
    ContractDateMiladi = models.DateField(null=True, blank=True, verbose_name='تاریخ شروع همکاری میلادی')
    ContractEndDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ پایان همکاری')
    ContractEndDateMiladi = models.DateField(null=True, blank=True, verbose_name='تاریخ پایان همکاری میلادی')
    ContractType = models.ForeignKey(to='ConstValue', on_delete=models.SET_NULL, null=True, related_name='ContractType', verbose_name='نوع قرارداد')
    About = models.CharField(max_length=1000, verbose_name="درباره من", null=True, blank=True)
    Gender = models.BooleanField(default=False, verbose_name='جنسیت')
    LivingAddress = models.ForeignKey("PostalAddress", verbose_name="آدرس محل سکونت", on_delete=models.SET_NULL, null=True, blank=True)
    DegreeType = models.ForeignKey('ConstValue', on_delete=models.PROTECT, null=True, blank=True, verbose_name='آخرین مقطع تحصیلی')
    CVFile = models.FileField(verbose_name="فایل رزومه", null=True, blank=True)
    MarriageStatus = models.ForeignKey("ConstValue", verbose_name="وضعیت تاهل", on_delete=models.PROTECT, related_name='UsersMarriageStatus', null=True, blank=True)
    NumberOfChildren = models.PositiveSmallIntegerField(verbose_name="تعداد فرزند", default=0, null=True, blank=True)
    MilitaryStatus = models.ForeignKey("ConstValue", verbose_name='وضعیت خدمت', on_delete=models.PROTECT, related_name='UsersMilitaryStatus', null=True, blank=True)
    NationalCode = models.CharField(max_length=10, null=True, unique=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    BirthDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ تولد')
    BirthDateMiladi = models.DateField(null=True, blank=True, verbose_name='تاریخ تولد میلادی')
    BirthCity = models.ForeignKey("City", verbose_name="شهر محل تولد", default=d.City, on_delete=models.SET_DEFAULT)
    IdentityNumber = models.CharField(max_length=10,null=True, blank=True, verbose_name='شماره شناسنامه')
    IdentityCity = models.ForeignKey("City", verbose_name="شهر محل صدور شناسنامه", default=d.City, on_delete=models.SET_DEFAULT, related_name='IdentityCity',null=True)
    IdentityRegisterDate = models.DateField(verbose_name='تاریخ صدور شناسنامه', null=True)
    IdentitySerialNumber = models.CharField(max_length=20,null=True, blank=True, verbose_name='سریال شناسنامه')
    InsuranceNumber = models.CharField(max_length=20 ,null=True, blank=True, verbose_name='شماره بیمه')
    Religion = models.ForeignKey("ConstValue", verbose_name="دین", on_delete=models.PROTECT, related_name='UsersReligion', null=True, blank=True)
    UserStatus = models.ForeignKey("ConstValue", verbose_name='وضعیت کاربر', null=True, on_delete=models.CASCADE, related_name="UserStatus")
    IsActive = models.BooleanField(default=True, verbose_name='کاربر فعال است؟')
    LastBuilding = models.ForeignKey(to="ConstValue", related_name="UsersBuilding", on_delete=models.SET_NULL, null=True, blank=True)
    LastFloor = models.ForeignKey(to="ConstValue", related_name="UsersFloor", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.FirstName + ' ' + self.LastName

    @property
    def username(self):
        return str(self.UserName).lower()

    @property
    def FullName(self):
        return self.FirstName + " " + self.LastName

    @property
    def get_birth(self):
        if self.BirthDateMiladi:
            now = datetime.datetime.now().date()
            diff = now - self.BirthDateMiladi
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            return str(years) + " سال "
        return "25" + " سال "

    @property
    def jalali_birth_date(self):
        if self.BirthDateMiladi:
            jalali_date = jdatetime.date.fromgregorian(date=self.BirthDateMiladi)
            return jalali_date.strftime('%Y/%m/%d')  
        return None  

    @property
    def get_contract(self):
        ret = ''
        if self.ContractDateMiladi:
            now = datetime.datetime.now().date()
            diff = now - self.ContractDateMiladi
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            if years != 0:
                ret = str(years) + " سال " + "#"
            if months != 0:
                ret += str(months) + " ماه " + "#"
            if days != 0:
                ret += str(days) + " روز "
            if ret and ret[-1] == "#":
                ret = ret[0:-1]
            ret = ret.replace("#", " و ")

        return ret

    @property
    def user_image_name(self):
        return self.UserName.replace("@eit", ".jpg")

    @property
    def user_image_name_national_code(self):
        return self.NationalCode + ".jpg"

    @property
    def get_degree(self):
        if self.DegreeType:
            return self.DegreeType.Caption
        return ''

    @property
    def get_study(self):
        # for prevent run query every username , fetch all user for first time and set into cache
        try:
            key = 'EducationHistory_rows'
            if key in cache:
                data = json.loads(cache.get(key))
                ret = data.get(str(self.UserName).lower(), '')
            else:
                _data = EducationHistory.objects.select_related("EducationTendency").all()
                data = {str(item.Person_id).lower():item.EducationTendency.Title for item in _data}
                cache.set(key,json.dumps(data))
                ret = data.get(str(self.UserName).lower(),'')
        except:
            ret = ''
        return ret

    @property
    def GenderTitle(self):
        return 'آقا' if self.Gender else 'خانم'

    @property
    def GenderTitlePrefix(self):
        return 'جناب آقای' if self.Gender else 'سرکار خانم'

    @property
    def GenderTitlePrefixFullName(self):
        return f' جناب آقای {self.FullName}' if self.Gender else f' سرکار خانم {self.FullName}'

    @property
    def IdentityCityTitle(self):
        return self.IdentityCity.CityTitle

    @property
    def UserStatusTitle(self):
        return self.UserStatus.Caption

    @property
    def ContractTypeTitle(self):
        return self.ContractType.Caption

    @property
    def LivingAddressText(self):
        return self.LivingAddress.AddressText

    @property
    def Degree_TypeTitle(self):
        return self.DegreeType.Caption

    @property
    def Marriage_StatusTitle(self):
        return self.MarriageStatus.Caption

    @property
    def Military_StatusTitle(self):
        return self.MilitaryStatus.Caption

    @property
    def BirthCityTitle(self):
        return self.BirthCity.CityTitle

    @property
    def ReligionTitle(self):
        return self.Religion.Caption

    @property
    def PhotoURL(self):
        return "static/HR/images/personnel/" + self.user_image_name

    @property
    def StaticPhotoURL(self):
        return settings.HR + "media/HR/PersonalPhoto/" + self.user_image_name


class V_AllUserList(models.Model):
    class Meta:
        db_table = 'V_AllUserList'
        managed = False
    UserName = models.CharField(primary_key=True, max_length=100, verbose_name='نام کاربری')
    FirstName = models.CharField(max_length=200, verbose_name='نام')
    LastName = models.CharField(max_length=200, verbose_name='نام خانوادگی')
    ContractDate = models.DateField(null=True, blank=True, verbose_name='تاریخ شروع همکاری')
    NationalCode = models.CharField(max_length=10, null=True, unique=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    TeamName = models.CharField(max_length=100, verbose_name='نام تیم')
    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    RoleName = models.CharField(max_length=100, verbose_name='عنوان سمت')
    UserActive = models.BooleanField(default=True, verbose_name='کاربر فعال است؟')
    RoleActive = models.BooleanField(default=True, verbose_name='سمت کاربر فعال است؟')


class PostalAddress(models.Model):
    """آدرس پرسنل"""
    class Meta:
        verbose_name = "آدرس پستی"
        verbose_name_plural = "آدرس های پستی"

    Title = models.CharField(max_length=100, verbose_name="عنوان", null=True, blank=True)
    City = models.ForeignKey("City", verbose_name="شهر محل زندگی", default=d.City, on_delete=models.SET_DEFAULT)
    CityDistrict = models.ForeignKey("CityDistrict", verbose_name="منطقه", blank=True, null=True, on_delete=models.SET_NULL)
    AddressText = models.CharField(max_length=500, verbose_name="آدرس", null=True, blank=True)
    No = models.CharField(max_length=20, verbose_name="پلاک", null=True, blank=True)
    UnitNo = models.PositiveSmallIntegerField(verbose_name="شماره واحد", null=True, blank=True)
    PostalCode = models.BigIntegerField(verbose_name="کد پستی", null=True, blank=True, validators=[v.PostalCode])
    Person = models.ForeignKey("Users", verbose_name="فرد", blank=True, null=True, on_delete=models.CASCADE)
    PersonNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    IsDefault = models.BooleanField(default=False, verbose_name='آدرس پیش فرض است؟')

    def __str__(self):
        r = ""
        if self.Title is not None:
            r = self.Title + " : "
        if self.City.CityTitle is not None:
            r += self.City.CityTitle
        if self.AddressText is not None:
            r += ", " + self.AddressText
        if self.No is not None:
            r += ", " + self.No
        if self.UnitNo is not None:
            r += ", " + str(self.UnitNo)
        if self.PostalCode is not None:
            r += ", " + str(self.PostalCode)

        return r

    def clean(self):
        v.PersonCompanyValidator(self, 'آدرس')

    @property
    def CityTitle(self):
        return self.City.CityTitle

    @property
    def CityDistrictTitle(self):
        return self.CityDistrict.DistrictTitle


class EmailAddress(models.Model):
    """ایمیل پرسنل"""
    class Meta:
        verbose_name = "آدرس پست الکترونیکی"
        verbose_name_plural = "آدرس های پست الکترونیکی"

    Email = models.EmailField(verbose_name="ادرس ایمیل")
    Title = models.CharField(max_length=100, verbose_name="عنوان", null=True, blank=True)
    Person = models.ForeignKey("Users", verbose_name="فرد", null=True, blank=True, on_delete=models.CASCADE)
    PersonNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    IsDefault = models.BooleanField(default=False, verbose_name='آدرس ایمیل پیشفرض است؟')

    def __str__(self):
        val = self.Email
        if self.Title is not None:
            val = self.Title + " : " + val
        return val

    @property
    def PersonFullname(self):
        return self.Person.__str__()


class PhoneNumber(models.Model):
    """شماره تماس پرسنل که می تواند شماره تماس همراه، محل سکونت و شماره تماس مواقع ضروری باشد"""
    class Meta:
        verbose_name = "شماره تماس"
        verbose_name_plural = "شماره های تماس"

    Province = models.ForeignKey("Province", verbose_name="استان", default=d.City, null=True, blank=True, on_delete=models.SET_NULL, help_text="این فیلد زمانی پر می شود که تلفن خط ثابت باشد")
    TelNumber = models.BigIntegerField(verbose_name="شماره تماس", help_text=" شماره ثابت بدون داخلی وارد شود. (مثلا : 87654321) شماره موبایل بدون صفر وارد شود مثلاً 9121234567")
    TelType = models.ForeignKey("ConstValue", verbose_name="نوع", on_delete=models.PROTECT, help_text="منظور از نوع این است که می تواند، محل زندگی، همراه، ضروری و... باشد")
    Title = models.CharField(max_length=50, verbose_name="توضیحات", blank=True, null=True)
    Person = models.ForeignKey("Users", verbose_name="فرد", blank=True, null=True, on_delete=models.CASCADE, related_name= 'phone_number')
    PersonNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    IsDefault = models.BooleanField(default=False, verbose_name='پیش فرض')

    def clean(self):
        v.PersonCompanyValidator(self, 'تلفن')
        v.PhoneNumber(self)

    def __str__(self):
        return  str(self.TelNumber)

    def TelTypeTitle(self):
        if self.TelType is not None:
            return self.TelType.Caption
        return "Not Found"

    @property
    def ProvinceTitle(self):
        return self.Province.ProvinceTitle

    @property
    def TelTypeTitle(self):
        return self.TelType.Caption


class ConstValue(models.Model):
    """جدول مقادیر ثابت حاوی مقادیر کمکی است برای جداول دیگر برای مثال اطلاعات انواع آدرس ویا انواع قرارداد در این جدول قرار می گیرد و صرفا آیدی آنها به عنولن کلید خارجی استفاده می شود."""
    class Meta:
        verbose_name = "مقدار ثابت"
        verbose_name_plural = "مقادیر ثابت"
        ordering = ["Parent_id", "OrderNumber"]

    Caption = models.CharField(max_length=50, verbose_name="عنوان")
    Code = models.CharField(max_length=100, verbose_name="کد")
    Parent = models.ForeignKey("ConstValue", verbose_name="شناسه پدر", on_delete=models.CASCADE, null=True, blank=True)
    IsActive = models.BooleanField(verbose_name="فعال است؟", default=True)
    OrderNumber = models.PositiveSmallIntegerField(verbose_name="شماره ترتیب", null=True, blank=True, default=1)
    ConstValue = models.IntegerField(verbose_name="مقدار مربوطه", null=True, blank=True)

    def __str__(self):
        return self.Caption

    @property
    def ParentTitle(self):
        return self.Parent.Caption


class University(models.Model):
    """دانشگاه محل تحصیل"""
    class Meta:
        verbose_name = "دانشگاه"
        verbose_name_plural = "دانشگاه ها"

    Title = models.CharField(max_length=150, verbose_name="نام دانشگاه")
    University_Type = models.ForeignKey("ConstValue", verbose_name="نوع دانشگاه", on_delete=models.PROTECT, limit_choices_to=ConstValueChoice("UniversityType"), null=True, blank=True)
    UniversityCity = models.ForeignKey("City", verbose_name="شهر محل دانشگاه", default=d.City, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.UniversityCity.CityTitle + " - " + self.Title

    @property
    def DisplayUniversityType(self):
        return self.get_UniversityType_display()

    @property
    def UniversityCityTitle(self):
        return self.UniversityCity.CityTitle

    @property
    def UniversityTypeTitle(self):
        return self.University_Type.Caption


class FieldOfStudy(models.Model):
    """رشته های تحصیلی"""
    class Meta:
        verbose_name = "رشته تحصیلی"
        verbose_name_plural = "رشته های تحصیلی"
        ordering = ("Title",)

    Title = models.CharField(max_length=150, verbose_name="رشته")

    def __str__(self):
        return self.Title


class Tendency(models.Model):
    """گرایش های رشته های تحصیلی"""
    class Meta:
        verbose_name = "گرایش تحصیلی"
        verbose_name_plural = "گرایش های تحصیلی"

    Title = models.CharField(max_length=150, verbose_name="گرایش")
    FieldOfStudy = models.ForeignKey("FieldOfStudy", verbose_name="گرایش تحصیلی", on_delete=models.CASCADE)

    def __str__(self):
        return self.FieldOfStudy.Title + " - " + self.Title

    @property
    def FieldOfStudyTitle(self):
        return self.FieldOfStudy.Title


class EducationHistory(models.Model):
    """سوابق تحصیلی پرسنل"""
    class Meta:
        verbose_name = "سابقه تحصیلی"
        verbose_name_plural = "سوابق تحصیلی"

    Person = models.ForeignKey("Users", verbose_name="پرسنل", on_delete=models.CASCADE, related_name="education_history")
    PersonNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    Degree_Type = models.ForeignKey('ConstValue', on_delete=models.PROTECT, verbose_name=' مقطع تحصیلی')
    University = models.ForeignKey("University", verbose_name="دانشگاه محل تحصیل", null=True, blank=True, on_delete=models.SET_NULL)
    StartDate = models.DateField(verbose_name="تاریخ شروع", blank=True, null=True)
    EndDate = models.DateField(verbose_name="تاریخ خاتمه", blank=True, null=True)
    StartYear = models.PositiveSmallIntegerField(verbose_name="سال ورود", blank=True, null=True, validators=[v.YearNumber], help_text="تاریخ شمسی")
    EndYear = models.PositiveSmallIntegerField(verbose_name="سال فراغت از تحصیل", blank=True, null=True, validators=[v.YearNumber], help_text="تاریخ شمسی")
    IsStudent = models.BooleanField(verbose_name="دانشجو است؟", default=False)
    EducationTendency = models.ForeignKey("Tendency", verbose_name="گرایش تحصیلی", on_delete=models.PROTECT)
    GPA = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="معدل", null=True, blank=True)

    def __str__(self):
        r = ""
        if self.Person is not None:
            r = self.Person.LastName + " : "
        if self.University is not None:
            r += self.University.Title
        if self.EducationTendency is not None:
            r += " - " + self.EducationTendency.Title
        return r

    def DegreeTitle(self):
        if self.Degree_Type is not None:
            return self.Degree_Type.Caption

        return "Not Found"


    @property
    def TendencyTitle(self):
        return self.EducationTendency.Title

    @property
    def PersonFullName(self):
        return self.Person.FullName

    @property
    def UniversityTitle(self):
        return self.University.Title

ROLE_MANAGER_STATUS_CHOICES = {
        "DRAFTR": "پیش نویس",
        "MANREV": "بررسی مدیر",
        "CTOREV": "بررسی مدیر عامل",
        "FINSUC": "خاتمه - تایید",
        "FINREJ": "خاتمه - رد",
        "FAILED": "خطا",
    }

class NewRoleRequest(models.Model):
    """ این جدول شامل اطلاعات مربوط به درخواست های اضافه کردن سمت های جدید است """
    class Meta:
        verbose_name = 'درخواست افزودن سمت جدید'
        verbose_name_plural = 'درخواست افزودن سمت های جدید'

    

    
    RoleTitle = models.CharField(max_length=100, verbose_name='عنوان سمت')
    HasLevel = models.BooleanField(verbose_name='آیا این سمت دارای سطح است؟', default=False)
    HasSuperior = models.BooleanField(verbose_name='آیا این سمت دارای ارشد دارد؟', default=False)
    # [{TeamCode,RoleCount},{TeamCode,RoleCount}]
    AllowedTeams = models.CharField(max_length=1000, verbose_name='این سمت در چه تیم های فعال است؟')
    # ["ConditionText", "ConditionText", "ConditionText", "ConditionText", ...]
    ConditionsText = models.CharField(max_length=1000, verbose_name='این سمت چه شرایط احرازی دارد ؟', null=True)
    # ["DutiesText", "DutiesText", "DutiesText", "DutiesText", ...]
    DutiesText = models.CharField(max_length=1000, verbose_name='این سمت چه شرایح شغلی دارد ؟', null=True)
    RequestorId = models.CharField(max_length=10,
                                   validators=[v.NationalCode_Validator],
                                   verbose_name="کد ملی درخواست دهنده")
    RequestDate = models.DateField(verbose_name='تاریخ ارائه درخواست', auto_now_add=True)
    ManagerId = models.CharField(max_length=10,
                                 validators=[v.NationalCode_Validator],
                                 verbose_name="کد ملی مدیر درخواست دهنده")
    ManagerOpinion = models.BooleanField(verbose_name='نظر مدیر درخواست دهنده',
                                         help_text='در صورت موافقت مقدار یک و در غیر این صورت صفر می باشد', default=0)
    ManagerDate = models.DateField(verbose_name='تاریخ اظهار نظر مدیر درخواست دهنده', null=True)
    CTOId = models.CharField(max_length=10, null=True,
                             validators=[v.NationalCode_Validator],
                             verbose_name="کد ملی مدیر عامل")
    CTOOpinion = models.BooleanField(verbose_name='نظر مدیر عامل',
                                     help_text='در صورت موافقت مقدار یک و در غیر این صورت صفر می باشد', default=0,
                                     null=True)
    CTODate = models.DateField(verbose_name='تاریخ اظهار نظر مدیرعامل', null=True)
    StatusCode = models.CharField(choices=ROLE_MANAGER_STATUS_CHOICES, max_length=6, null=True, default="DRAFTR")
    DocId = models.IntegerField(verbose_name="شناسه سند", null=True, blank=True)
    ManagerType = models.ForeignKey(to="ConstValue",on_delete=models.SET_NULL, verbose_name="مدیر مربوطه", null=True, related_name='as_manager_type')
    RoleType = models.ForeignKey(to="ConstValue",on_delete=models.SET_NULL, verbose_name="کد نوع سمت", null=True, related_name='as_role_type')
    NewRoleTypeTitle = models.CharField(max_length=100, verbose_name="عنوان نوع سمت جدید", null=True)
    
    
class Team(models.Model):
    class Meta:
        db_table = 'Team'
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم ها'

    TeamCode = models.CharField(primary_key=True, max_length=3, verbose_name='کدتیم')
    TeamName = models.CharField(max_length=100, verbose_name='نام تیم')
    ActiveInService = models.BooleanField(default=True, verbose_name=' کتاب')
    ActiveInEvaluation = models.BooleanField(default=True, verbose_name='ارزیابی')
    GeneralManager = models.ForeignKey(to='Users', related_name='TeamGeneralManager', on_delete=models.SET_NULL, null=True, verbose_name='مدیر عمومی', help_text='مدیر عمومی می تواند، مدیر پروژه یا مدیر اداری، یا  مدیر اداری یا کلا هر مدیری باشد')
    SupportManager = models.ForeignKey(to='Users', related_name='TeamSupportManager', on_delete=models.SET_NULL, null=True, verbose_name='مدیر پشتیبانی', help_text='برای تیم های عملیانی مشخص می شود و برای غیر عملیاتی ها نال است')
    TestManager = models.ForeignKey(to='Users', related_name='TeamTestManager', on_delete=models.SET_NULL, null=True, verbose_name='مدیر تست', help_text='برای تیم های عملیانی مشخص می شود و برای غیر عملیاتی ها نال است')
    GeneralManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر عمومی")
    SupportManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر پشتیبانی")
    TestManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر تست")
    IsActive = models.BooleanField(default=True, verbose_name='آیا تیم فعال است؟')
    TeamDescription = models.TextField(db_column='TeamDescription',  blank=True, null=True) 
    ShortDescription = models.CharField(db_column='ShortDescription', max_length=1000, blank=True, null=True) 

    def __str__(self):
        return self.TeamName

    def get_pk(self):
        return self.pk

    def get_cls_name(self):
        return self.__class__.__name__

class RoleType(models.Model):
    TypeCode = models.CharField(max_length=1, primary_key=True)
    TypeTitle = models.CharField(max_length=200)

    class Meta:
        db_table = 'HR_RoleType'
        verbose_name = 'نوع سمت'
        verbose_name_plural = 'نوع سمت ها'

class Role(models.Model):
    class Meta:
        db_table = 'Role'
        verbose_name = 'سمت'
        verbose_name_plural = 'سمت ها'

    RoleId = models.IntegerField(primary_key=True, verbose_name='کد سمت')
    RoleName = models.CharField(max_length=100, verbose_name='نام سمت')
    HasLevel = models.BooleanField(default=False, verbose_name='دارای سطح')
    HasSuperior = models.BooleanField(default=False, verbose_name='ارشد دارد')
    Comment = models.CharField(max_length=200, verbose_name='توضیحات', null=True)
    NewRoleRequest = models.ForeignKey(to="NewRoleRequest", verbose_name='شناسه درخواست اضافه کردن سمت', null=True, on_delete=models.SET_NULL)
    RoleTypeCode = models.ForeignKey(to="RoleType", db_column="RoleTypeCode", on_delete=models.CASCADE)
    ManagerType = models.ForeignKey(to="ConstValue", on_delete=models.CASCADE, null=True)

    
    def __str__(self):
        return self.RoleName

# ruff: noqa: E501
class UserTeamRole(models.Model):
    class Meta:
        db_table = 'UserTeamRole'
        verbose_name = 'اطلاعات پرسنل'
        verbose_name_plural = 'اطلاعات همه ی پرسنل'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', related_name='UserTeamRoleUserNames', db_column='UserName', on_delete=models.CASCADE)
    NationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    LevelId = models.ForeignKey('RoleLevel', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح')
    Superior = models.BooleanField(verbose_name='ارشد', default=False)
    ManagerUserName = models.ForeignKey("Users", null=True, blank=True, verbose_name='نام مدیر', related_name='UserTeamRoleManagerUserNames', on_delete=models.CASCADE)
    ManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر")
    StartDate = models.CharField(max_length=10, verbose_name='تاریخ شروع')
    EndDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ پایان')

    def __str__(self):
        return '(' + self.RoleId.RoleName + ')' + '(' + self.TeamCode.TeamName + ')'

    @property
    def get_birth(self):
        if self.UserName.BirthDateMiladi:
            now = datetime.datetime.now().date()
            diff = now - self.UserName.BirthDateMiladi
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            return str(years) + " سال "
        return '25' + ' سال '

    @property
    def get_contract(self):
        ret = ''
        if self.UserName.ContractDate:
            now = datetime.datetime.now().date()
            diff = now - self.UserName.ContractDate
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            if years != 0:
                ret = str(years) + " سال " + "#"
            if months != 0:
                ret += str(months) + " ماه " + "#"
            if days != 0:
                ret += str(days) + " روز "
            if ret[-1] == "#":
                ret = ret[0:-1]
            ret = ret.replace("#", " و ")

        return ret

    @property
    def LevelTitle(self):
        return self.LevelId.LevelName

    @property
    def RoleTitle(self):
        return self.RoleId.RoleName

    @property
    def TeamName(self):
        return self.TeamCode.TeamName


class RoleLevel(models.Model):
    LevelName = models.CharField(verbose_name='نام سطح', max_length=20)

    class Meta:
        db_table = 'RoleLevel'
        verbose_name = 'سطح'
        verbose_name_plural = 'سطوح'

    def __str__(self):
        return self.LevelName


class V_UserTeamRole(models.Model):
    class Meta:
        db_table = 'V_UserTeamRole'
        managed = False
        verbose_name = 'اطلاعات پرسنل'
        verbose_name_plural = 'اطلاعات همه ی پرسنل'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', db_column='UserName', on_delete=models.CASCADE)
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    LevelId = models.ForeignKey('RoleLevel', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح')
    Superior = models.BooleanField(verbose_name='ارشد', default=False)
    StartDate = models.CharField(max_length=10, verbose_name='تاریخ شروع')
    EndDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ پایان')


class ChangeRole(models.Model):
    class Meta:
        verbose_name = 'اطلاعات تغییر سمت'
        verbose_name_plural = 'اطلاعات تغییر سمت ها'

    RoleID = models.ForeignKey('Role', related_name='ChangeRoleRoleIDs', on_delete=models.CASCADE, verbose_name='سمت فعلی')
    LevelId = models.ForeignKey('RoleLevel', related_name='ChangeRoleRoleLevels', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح فعلی')
    Superior = models.BooleanField(verbose_name='وضعیت فعلی ارشد', default=False)
    RoleIdTarget = models.ForeignKey('Role', related_name='ChangeRoleRoleIdTargets', on_delete=models.CASCADE, verbose_name='سمت جدید')
    LevelIdTarget = models.ForeignKey('RoleLevel', related_name='ChangeRoleLevelIdTargets', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح جدید')
    SuperiorTarget = models.BooleanField(verbose_name='وضعیت جدید ارشد', default=False)
    Education = models.BooleanField(default=True, verbose_name='آموزش نیاز دارد؟')
    Educator = models.CharField(max_length=100, null=True, blank=True, verbose_name='آموزش دهنده')
    Evaluation = models.BooleanField(default=True, verbose_name='ارزیابی نیاز دارد؟')
    Assessor = models.CharField(max_length=100, null=True, blank=True, verbose_name='ارزیابی کننده')
    RequestGap = models.IntegerField(null=True, blank=True, verbose_name='مدت زمان')
    Assessor2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='ارزیابی کننده دوم')
    ReEvaluation = models.BooleanField(default=True, verbose_name='ارزیابی  دوم نیاز دارد؟')
    PmChange = models.BooleanField(default=True, verbose_name='تغیرات PM؟')
    ITChange = models.BooleanField(default=True, verbose_name='تغیرات IT؟')

    def __str__(self):
        return self.RoleID.RoleName + ' به ' + self.RoleIdTarget.RoleName

    @property
    def CurrentLevelTitle(self):
        return self.LevelId.LevelName

    @property
    def LevelTargetTitle(self):
        return self.LevelIdTarget.LevelName

    @property
    def CurrentRoleTitle(self):
        return self.RoleID.RoleName

    @property
    def RoleTargetTitle(self):
        return self.RoleIdTarget.RoleName


class RoleGroup(models.Model):
    class Meta:
        verbose_name = 'گروه سمت'
        verbose_name_plural = 'گروه های سمت ها'

    RoleID = models.ForeignKey('Role', related_name='RoleGroupRoleIDs', on_delete=models.CASCADE, verbose_name='سمت فعلی')
    RoleGroup = models.CharField(max_length=50, verbose_name='گروه')
    RoleGroupName = models.CharField(max_length=100, null=True, blank=True, verbose_name=' نام گروه')

    def __str__(self):
        return self.RoleGroup

    @property
    def RoleTitle(self):
        return self.RoleID.RoleName


class RoleGroupTargetException(models.Model):
    class Meta:
        verbose_name = 'گروه سمت'
        verbose_name_plural = 'گروه های سمت ها'

    RoleGroup = models.CharField(max_length=100, verbose_name='گروه مبدا')
    RoleGroupTarget = models.CharField(max_length=100, verbose_name='گروه مقصد')

    def __str__(self):
        return self.RoleGroup + ' به ' + self.RoleGroupTarget


class AccessPersonnel(models.Model):
    class Meta:
        verbose_name = 'دسترسی انتخاب  سمت'
        verbose_name_plural = 'دسترسی های انتخاب همه سمت ها'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', related_name='AccessPersonnelUserNames', on_delete=models.CASCADE)
    NationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")


    def __str__(self):
        return self.UserName.LastName


class OrganizationChartRole(models.Model):
    class Meta:
        verbose_name = 'سمت و سطح'
        verbose_name_plural = 'سمت ها و سطح ها'

    RoleId = models.ForeignKey('Role', related_name='OrganizationChartRoleRoleIDs', on_delete=models.CASCADE, verbose_name='سمت')
    LevelId = models.ForeignKey('RoleLevel', related_name='OrganizationChartRoleRoleLevels', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح ')

    def __str__(self):
        return self.RoleId.RoleName

    @property
    def RoleTitle(self):
        return self.RoleId.RoleName

    @property
    def LevelTitle(self):
        return self.LevelId.LevelName


class OrganizationChartTeamRole(models.Model):
    class Meta:
        verbose_name = 'سمت  تیم'
        verbose_name_plural = 'سمت های تیم های عملیاتی'

    TeamCode = models.ForeignKey('Team', related_name='OrganizationChartTeamRoleTeamCodes', on_delete=models.CASCADE, verbose_name='نام تیم')
    RoleCount = models.IntegerField(verbose_name='ظرفیت سمت', null=True, blank=True)
    ManagerUserName = models.ForeignKey("Users", null=True, blank=True, verbose_name='نام مدیر', related_name='OrganizationChartTeamRoleManagerUserNames', on_delete=models.CASCADE)
    ManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر")
    OrganizationChartRole = models.ForeignKey('OrganizationChartRole', on_delete=models.CASCADE, verbose_name='مدیر تیم و سمت')

    def __str__(self):
        return self.TeamCode

    @property
    def RoleTitle(self):
        return self.OrganizationChartRole.RoleTitle

    @property
    def LevelTitle(self):
        return self.OrganizationChartRole.LevelTitle

    @property
    def TeamTitle(self):
        return self.TeamCode.TeamName


class UserHistory(models.Model):
    UserName = models.CharField(max_length=300)
    AppName = models.CharField(max_length=100, default=None, null=True)
    AuthLoginKey = models.CharField(max_length=300, null=True)
    RequestDate = models.DateTimeField(default=None)
    EnterDate = models.DateTimeField(default=None, null=True)
    RequestUrl = models.CharField(max_length=300, null=True)
    EnterUrl = models.CharField(max_length=300, null=True)
    IP = models.GenericIPAddressField(null=True)
    UserAgent = models.CharField(max_length=300, null=True)
    ChangedUserInfo = models.BooleanField(default=None, null=True)

    @property
    def GetEnterDate(self):
        if self.EnterDate is not None:
            return self.EnterDate.split(".")[0]
        return self.EnterDate

    @property
    def GetRequestDate(self):
        if self.RequestDate is not None:
            return self.RequestDate.split(".")[0]
        return self.RequestDate


class V_HR_RoleTarget(models.Model):
    class Meta:
        db_table = 'V_HR_RoleTarget'
        managed = False
        verbose_name = "تغییر جایگاه"
        verbose_name_plural = "تغییرات جایگاه"

    RoleID = models.ForeignKey('Role', db_column="RoleID", related_name='RoleTargetRoleIDs', on_delete=models.CASCADE, verbose_name='سمت')
    RoleTargetID = models.ForeignKey('Role', db_column="RoleTargetID", related_name='RoleTargetRoleTargetIDs', on_delete=models.CASCADE, verbose_name='سمت')
    RoleTargetName = models.CharField(max_length=100, verbose_name='نام سمت مقصد')
    LevelID = models.ForeignKey('RoleLevel', db_column="LevelID", related_name='RoleTargetLevelIDs', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح ')
    LevelIdTargetID = models.ForeignKey('RoleLevel', db_column="LevelIdTargetID", related_name='RoleTargetLevelIdTargetID', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح ')
    Superior = models.BooleanField(verbose_name='وضعیت فعلی ارشد', default=False)
    SuperiorTarget = models.BooleanField(verbose_name='وضعیت فعلی ارشد', default=False)
    Education = models.BooleanField(default=True, verbose_name='آموزش نیاز دارد؟')
    Educator = models.CharField(max_length=100, null=True, blank=True, verbose_name='آموزش دهنده')
    Evaluation = models.BooleanField(default=True, verbose_name='ارزیابی نیاز دارد؟')
    Assessor = models.CharField(max_length=100, null=True, blank=True, verbose_name='ارزیابی کننده')
    PmChange = models.BooleanField(default=True, verbose_name='تغیرات PM؟')
    ReEvaluation = models.BooleanField(default=True, verbose_name='ارزیابی مجدد')
    ITChange = models.BooleanField(default=True, verbose_name='تغیرات IT؟')
    RequestType = models.IntegerField(verbose_name='نوع درخواست')


class V_RoleTeam(models.Model):
    class Meta:
        db_table = 'V_RoleTeam'
        managed = False
        verbose_name = "سمت موجودر تیم"
        verbose_name_plural = "سمت های موجوددر تیم"

    Id = models.IntegerField(primary_key=True)
    RoleID = models.ForeignKey('Role', db_column="RoleID", related_name='RoleTeamRoleIDs', on_delete=models.CASCADE, verbose_name='سمت')
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', related_name='RoleTeamTeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    ManagerUserName = models.ForeignKey("Users", related_name='RoleTeamManagerUserName', verbose_name='نام مدیر', db_column='ManagerUserName', on_delete=models.CASCADE)
    ManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر")


class PreviousUserTeamRole(models.Model):
    class Meta:
        db_table = 'PreviousUserTeamRole'
        verbose_name = 'اطلاعات پرسنل'
        verbose_name_plural = 'اطلاعات همه ی پرسنل'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', related_name='UserNames', db_column='UserName', on_delete=models.CASCADE)
    NationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی")
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    LevelId = models.ForeignKey('RoleLevel', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح')
    Superior = models.BooleanField(verbose_name='ارشد', default=False)
    ManagerUserName = models.ForeignKey("Users", null=True, blank=True, verbose_name='نام مدیر', related_name='ManagerUserNames', on_delete=models.CASCADE)
    ManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر")
    StartDate = models.CharField(max_length=10, verbose_name='تاریخ شروع')
    EndDate = models.CharField(max_length=10, null=True, blank=True, verbose_name='تاریخ پایان')

    def __str__(self):
        return '(' + self.RoleId.RoleName + ')' + '(' + self.TeamCode.TeamName + ')'

    @property
    def get_birth(self):
        if self.UserName.BirthDateMiladi:
            now = datetime.datetime.now().date()
            diff = now - self.UserName.BirthDateMiladi
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            return str(years) + " سال "
        return '25' + ' سال '

    @property
    def get_contract(self):
        ret = ''
        if self.UserName.ContractDate:
            now = datetime.datetime.now().date()
            diff = now - self.UserName.ContractDate
            number_of_days = diff.days
            years = number_of_days // 365
            months = (number_of_days - years * 365) // 30
            days = (number_of_days - years * 365 - months * 30)
            if years != 0:
                ret = str(years) + " سال " + "#"
            if months != 0:
                ret += str(months) + " ماه " + "#"
            if days != 0:
                ret += str(days) + " روز "
            if ret[-1] == "#":
                ret = ret[0:-1]
            ret = ret.replace("#", " و ")

        return ret

    @property
    def LevelTitle(self):
        return self.LevelId.LevelName

    @property
    def RoleTitle(self):
        return self.RoleId.RoleName

    @property
    def TeamTitle(self):
        return self.TeamCode.TeamName


class SlipField(models.Model):
    class Meta:
        abstract = True
    YearNumber = models.IntegerField(verbose_name='سال')
    MonthNumber = models.IntegerField(verbose_name='ماه')
    ItemValue = models.BigIntegerField(verbose_name='مقدار مربوطه')
    Code = models.CharField(max_length=200, verbose_name="کد مورد مربوطه")



class UserSlipAverage(SlipField):
    class Meta:
        db_table = 'V_UserSlip_Average'
        managed = False
    pass

class UserSlip(SlipField):
    class Meta:
        db_table='HR_UserSlip'

    PersonnelCode = models.CharField(max_length=10, verbose_name='کدملی')
    Username = models.ForeignKey(to="Users", verbose_name='نام کاربری', on_delete=models.CASCADE, db_column='Username', null=True)

class PaymentField(models.Model):
    class Meta:
        abstract = True
    YearNumber = models.IntegerField(verbose_name='سال')
    Payment = models.BigIntegerField(null=True, blank=True, verbose_name='خالص دریافتی', help_text='این مبلغ خالص دریافتی کاربر است')
    TotalPayment = models.BigIntegerField(null=True, blank=True, verbose_name='حقوق ناخالص', help_text='کل پرداختی ها شامل حقوق پایه، اضافه کار، پاداش و ...')
    OtherPayment = models.BigIntegerField(null=True, blank=True, verbose_name='سایر هزینه های کارفرما', help_text="مثلا سوبسید ناهار تایم یا بیمه تکمیلی که شرکت برای این فرد پرداخت می کند")
    PaymentCost = models.BigIntegerField(null=True, blank=True, verbose_name='بهای تمام شده این فرد', help_text='بهای تمام شده فرد شامل کل حقوق دریافتی + بیمه کارفرما + سایر هزینه های پرداختی کارفرما است')
    BasePayment = models.BigIntegerField(null=True, blank=True, verbose_name='پایه حقوق', help_text='حقوق پایه یعنی مبلغ ناخالص قرارداد فرد')
    OverTimePayment = models.BigIntegerField(null=True, blank=True, verbose_name='هزینه اضافه کاری', help_text='مبلغی که فرد بابت اضافه کار در ماه دریافت کرده است')
    OverTime = models.IntegerField(null=True, blank=True, verbose_name='ساعت اضافه کاری', help_text='میزان اضافه کاری فرد بر حسب دقیقه')
    Reward = models.BigIntegerField(null=True, blank=True, verbose_name='مبلغ پاداش ماهانه', help_text='مبلغی که فرد به عنوان پاداش در آن ماه دریافت کرده است')


class Payment(PaymentField):
    class Meta:
        verbose_name = "حقوق"
        verbose_name_plural = "حقوق های پرسنل"
        db_table = 'HR_Payment'

    PersonnelCode = models.CharField(max_length=10, verbose_name='کدملی')
    Username = models.ForeignKey(to="Users", verbose_name='نام کاربری', on_delete=models.CASCADE, db_column='Username', null=True)
    MonthNumber = models.IntegerField(verbose_name='ماه')
    InsuranceAmount = models.BigIntegerField(db_column='InsuranceAmount', blank=True, null=True)  # Field name made lowercase.
    DataType = models.SmallIntegerField(db_column='DataType')  # Field name made lowercase.


    def __str__(self):
        return self.Username + '-' + str(self.YearNumber) + '-' + str(self.MonthNumber)


class PaymentAverage(PaymentField):
    class Meta:
        verbose_name = "میانگین حقوق سالانه"
        verbose_name_plural = "میانگین حقوق سالانه"
        managed = False
        db_table = 'V_Payment_Average'
    MonthNumber = models.IntegerField(verbose_name='ماه')
    def __str__(self):
        return str(self.YearNumber)


class PaymentRoleAverage(PaymentField):
    class Meta:
        verbose_name = "میانگین حقوق سالانه به تفکیک سمت"
        verbose_name_plural = "میانگین حقوق سالانه به تفکیک سمت"
        managed = False
        db_table = 'V_Payment_Role_Average'

    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    LevelId = models.ForeignKey('RoleLevel', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح')
    MonthNumber = models.IntegerField(verbose_name='ماه')

    def __str__(self):
        return str(self.YearNumber) + '-' + self.RoleId.RoleName + '-' + self.LevelId.LevelName


class PaymentYearly(PaymentField):
    class Meta:
        verbose_name = "حقوق"
        verbose_name_plural = "حقوق های پرسنل"
        managed = False
        db_table = 'V_Payment_Yearly'

    PersonnelCode = models.CharField(max_length=10, verbose_name='کدملی')
    Username = models.ForeignKey(to="Users", verbose_name='نام کاربری', on_delete=models.CASCADE, db_column='Username', null=True)

    def __str__(self):
        return self.Username + '-' + str(self.YearNumber) + '-' + str(self.MonthNumber)


class PaymentAverageYearly(PaymentField):
    class Meta:
        verbose_name = "میانگین حقوق سالانه"
        verbose_name_plural = "میانگین حقوق سالانه"
        managed = False
        db_table = 'V_Payment_Average_Yearly'

    def __str__(self):
        return str(self.YearNumber)


class PaymentRoleAverageYearly(PaymentField):
    class Meta:
        verbose_name = "میانگین حقوق سالانه به تفکیک سمت"
        verbose_name_plural = "میانگین حقوق سالانه به تفکیک سمت"
        managed = False
        db_table = 'V_Payment_Role_Average_Yearly'

    RoleId = models.ForeignKey("Role", db_column='RoleId', on_delete=models.CASCADE, verbose_name='کد سمت')
    LevelId = models.ForeignKey('RoleLevel', null=True, blank=True, on_delete=models.CASCADE, verbose_name='سطح')

    def __str__(self):
        return str(self.YearNumber) + '-' + self.RoleId.RoleName + '-' + self.LevelId.LevelName


class WorkTime(models.Model):
    class Meta:
        verbose_name = "اطلاعات چارگون"
        verbose_name_plural = "اطلاعات چارگون"
        db_table = 'WorkTime'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', related_name='WorkTimeUserNames', db_column='UserName', on_delete=models.CASCADE)
    YearNo = models.IntegerField(verbose_name='سال')
    MonthNo = models.IntegerField(verbose_name='ماه')
    PersonnelCode = models.CharField(max_length=10, verbose_name='کدملی')
    WorkHours = models.CharField(max_length=10, verbose_name='ساعت حضوری')
    RemoteHours = models.CharField(max_length=10, verbose_name='ساعت دورکاری')
    RemoteDays = models.IntegerField(verbose_name='روز دورکاری')
    OverTime = models.CharField(max_length=10, verbose_name='اضافه کار')
    DeductionTime = models.CharField(max_length=10, verbose_name='کسر کار')
    OffTimeHourly = models.CharField(max_length=10, verbose_name='ساعت مرخصی')
    OffTimeDaily = models.IntegerField(verbose_name='روز مرخصی')
    Id = models.IntegerField(primary_key=True)


class V_WorkTime(models.Model):
    class Meta:
        verbose_name = "اطلاعات چارگون"
        verbose_name_plural = "اطلاعات چارگون"
        managed = False
        db_table = 'V_WorkTime'

    UserName = models.ForeignKey("Users", verbose_name='نام کاربری', related_name='V_WorkTimeUserNames', db_column='UserName', on_delete=models.CASCADE)
    YearNo = models.IntegerField(verbose_name='سال')
    WorkHours = models.CharField(max_length=10, verbose_name='ساعت حضوری')
    RemoteHours = models.CharField(max_length=10, verbose_name='ساعت دورکاری')
    RemoteDays = models.IntegerField(verbose_name='روز دورکاری')
    OverTime = models.CharField(max_length=10, verbose_name='اضافه کار')
    DeductionTime = models.CharField(max_length=10, verbose_name='کسر کار')
    OffTimeHourly = models.CharField(max_length=10, verbose_name='ساعت مرخصی')
    OffTimeDaily = models.IntegerField(verbose_name='روز مرخصی')
    Id = models.IntegerField(primary_key=True)


class PageInformation(models.Model):
    class Meta:
        verbose_name = "اطلاعات صفحه"
        verbose_name_plural = "اطلاعات صفحات"

    PageName = models.CharField(max_length=30, verbose_name='نام صفحه')
    EnglishName = models.CharField(max_length=30, verbose_name='نام لاتین صفحه', )
    ColorSet = models.CharField(max_length=30, verbose_name='رنگ آیکون صفحه', )
    IconName = models.CharField(max_length=30, verbose_name='آیکون صفحه', )
    ShowDetail = models.BooleanField(default=False, verbose_name="جزییات نمایش داده شود؟")
    OrderNumber = models.PositiveSmallIntegerField(default=10, verbose_name='ترتیب نمایش')

    def __str__(self):
        return self.EnglishName


class PagePermission(models.Model):
    class Meta:
        verbose_name = "دسترسی صفحه"
        verbose_name_plural = "دسترسی های صفحات"

    Page = models.ForeignKey(verbose_name="نام صفحه", on_delete=models.CASCADE, to="PageInformation", null=True)
    GroupId = models.PositiveIntegerField(verbose_name='شناسه گروه')
    Editable = models.BooleanField(default=False, verbose_name='قابل ویرایش')

    @property
    def PageTitle(self):
        return self.Page.PageName


class V_PagePermission(models.Model):
    class Meta:
        verbose_name = "دسترسی صفحه"
        verbose_name_plural = "دسترسی های صفحات"
        managed = False
        db_table = "V_PagePermission"

    UserName = models.ForeignKey('Users', on_delete=models.CASCADE, verbose_name='نام کاربری')
    NationalCode = models.CharField(max_length=10)
    Page = models.ForeignKey(verbose_name="نام صفحه", on_delete=models.CASCADE, to="PageInformation", null=True)
    GroupId = models.PositiveIntegerField(verbose_name='شناسه گروه')
    Editable = models.BooleanField(default=False, verbose_name='قابل ویرایش')
    OrderNumber = models.PositiveSmallIntegerField(default=10, verbose_name='ترتیب نمایش')


class V_TeamInformation(models.Model):
    class Meta:
        verbose_name = "اطلاعات تیم"
        verbose_name_plural = "اطلاعات تیم ها"
        db_table = "TeamInformation"
        managed = False
        

    TeamCode = models.CharField(max_length=3, verbose_name='کد تیم')
    TeamName = models.CharField(max_length=100, verbose_name='نام تیم')
    TeamDesc =  models.CharField(max_length=4000, verbose_name='توضیحات تیم')
    ShortDesc= models.CharField(max_length=1000, verbose_name='توضیحات مختصر تیم')
    TeamCount = models.PositiveSmallIntegerField(verbose_name='تعداد نفرات تیم')
    IsTeamActive = models.BooleanField()
    def __str__(self):
        return self.TeamName


class V_KeyMembers(models.Model):
    class Meta:
        verbose_name = "فرد کلیدی"
        verbose_name_plural = "افراد کلیدی"
        db_table = "KeyMembers"
        managed = False

    UserName = models.CharField(max_length=250, verbose_name='نام')
    UserAlone = models.CharField(max_length=250, verbose_name='نام')
    FirstName = models.CharField(max_length=250, verbose_name='نام')
    LastName = models.CharField(max_length=250, verbose_name='نام خانوادگی')
    TeamCode = models.CharField(max_length=3, verbose_name='کد تیم')
    RoleName = models.CharField(max_length=100, verbose_name='سمت')
    Superior = models.BooleanField(verbose_name='ارشد')

class TeamAllowedRoles(models.Model):
    """  این کلاس برای مشخص کردن این است که چه سمت هایی در چه تیم هایی و به چه تعدادی مجاز هستند"""
    class Meta:
        verbose_name = 'سمت های مجاز تیم'
        verbose_name_plural = 'سمت های مجاز تیم ها'
        unique_together = ['TeamCode','RoleId']

    TeamCode = models.ForeignKey(to='Team', verbose_name='کد تیم مربوطه', db_column = 'TeamCode', on_delete = models.CASCADE)    
    RoleId = models.ForeignKey(to='Role', verbose_name='شناسه مربوطه', db_column = 'RoleId', on_delete = models.CASCADE)
    AllowedRoleCount = models.PositiveSmallIntegerField(verbose_name='تعداد مجاز', default='100', null=True)
    Comment = models.CharField(max_length=500, verbose_name='توضیحات')
    SetTeamAllowedRoleRequest = models.ForeignKey(to="SetTeamAllowedRoleRequest", verbose_name='شناسه درخواست مربوطه', null=True, on_delete=models.SET_NULL)

class SetTeamAllowedRoleRequest(models.Model):
    """ این جدول برای ذخیره درخواست های تعیین سمت های مجاز در تیم ها ایجاد شده است
    روال کلی به این صورت است که درخواست دهنده یک نمونه از فرم را تکمیل می کند، قرم برای مدیر وی و مدیر عامل ارسال می شود
    پس از تاییدات نهایی، رکورد متناظر در جدول مربوط به روز می گردد """

    class Meta:
        verbose_name = 'درخواست تغییرات سمت های مجاز تیم'
        verbose_name_plural = 'درخواست های تغییرات سمت های مجاز تیم ها'

    # اگر مقدار فیلد RoleCount برابر با -1 باشد یعنی آن سمت برای آن تیم دیگر مجاز نمی باشد
    # [{ TeamCode:CAR, Roles:[{ RoleId:53,RoleCount:7, PrevRoleCount : 0 },  {RoleID: 54, RoleCount:10}},{ TeamCode:LIF, Roles:[{ RoleId:32,RoleCount:1 }]
    TeamAllowedRoles = models.CharField(max_length=2000, verbose_name='اطلاعات تیم و سمت های مجاز')

    RequestorId = models.CharField(max_length=10, validators=[v.NationalCode_Validator], verbose_name="کد ملی درخواست دهنده")
    RequestDate = models.DateField(verbose_name='تاریخ ارائه درخواست', auto_now_add=True)
    ManagerId = models.CharField(max_length=10, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر درخواست دهنده")
    ManagerOpinion = models.BooleanField(verbose_name='نظر مدیر درخواست دهنده', help_text='در صورت موافقت مقدار یک و در غیر این صورت صفر می باشد', null=True)
    ManagerDate = models.DateField(verbose_name='تاریخ اظهار نظر مدیر درخواست دهنده', null=True)
    CTOId = models.CharField(max_length=10, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر عامل")
    CTOOpinion = models.BooleanField(verbose_name='نظر مدیر عامل', help_text='در صورت موافقت مقدار یک و در غیر این صورت صفر می باشد', null=True)
    CTODate = models.DateField(null=True,verbose_name='تاریخ اظهار نظر مدیرعامل')
    DocId = models.IntegerField(verbose_name="شناسه سند", null=True, blank=True)
    StatusCode = models.CharField(choices=ROLE_MANAGER_STATUS_CHOICES, max_length=6, null=True, default="DRAFTR") #MANREV, if both are true CTOREV , finish, failed

class RoleInformation(models.Model):
    class Meta:
        verbose_name ='دسته بندی سمت'
        verbose_name_plural ='دسته بندی های سمت'
        
    Conditions = 'C'
    Duties = 'D'
    DESCRIPTION_TYPE_CHOICE = ((Conditions,'شرایط احراز'), (Duties,'شرح وظایف'))
    
    RoleID = models.ForeignKey(to="Role", db_column="RoleID", on_delete=models.CASCADE, verbose_name='شناسه سمت')
    Title = models.CharField(max_length=50, db_column="Title", verbose_name="عنوان", null=True)
    DescriptionType = models.CharField(max_length=1, choices=DESCRIPTION_TYPE_CHOICE, verbose_name='نوع')


class V_HR_RoleManager(models.Model):
    class Meta:
        db_table = 'HR_RoleManager'
        managed = False

    Id = models.IntegerField(primary_key=True)
    RoleID = models.ForeignKey('Role', db_column="RoleId",  on_delete=models.CASCADE, verbose_name='سمت')
    TeamCode = models.ForeignKey("Team", db_column='TeamCode', on_delete=models.CASCADE, verbose_name='کدتیم')
    ManagerId = models.ForeignKey("Users", verbose_name='نام مدیر', db_column='ManagerId', on_delete=models.CASCADE)
    ManagerNationalCode = models.CharField(max_length=10, null=True, blank=True, validators=[v.NationalCode_Validator], verbose_name="کد ملی مدیر")


