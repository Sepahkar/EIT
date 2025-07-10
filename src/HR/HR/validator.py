import re
from datetime import datetime
from django.core.exceptions import ValidationError



class Validator:
    def GPA_Validator(value):
        if value is not None:
            if value > 20 or value < 0:
                raise ValidationError("معدل صحیح نیست")
        return value

    def NationalCode_Validator(value):
        if not re.search(r'^\d{10}$', value):
            raise ValidationError("کد ملی صحیح نیست")
        check = int(value[9])
        s = sum(int(value[x]) * (10 - x) for x in range(9)) % 11

        if (s < 2 and check == s) or (check + s == 11):
            return True
        else:
            raise ValidationError("کد ملی صحیح نیست")

    def BirthDate_Validator(value):
        Age = datetime.today().year - value.year
        if Age < 18:
            raise ValidationError("حداقل سن برای ثبت نام در سایت برابر با 18 سال می باشد")
        return value

    def YearNumber(value):
        now = datetime.now()
        y = now.year - 620
        if value < 1350 or value >= y:
            raise ValidationError("سال معتبر نیست")
        return True

    def PhoneNumber(obj):
        # اگر شماره موبایل باشد باید حتماً با 9 شروع شود و 10 رقمی باشد
        if obj.TelType.Code == 'TelType_Mobile':
            if not 9001111111 < obj.TelNumber < 9999111111:
                raise ValidationError('شماره تلفن همراه را به درستی وارد کنید')
            # اگر شماره موبایل وارد شده باشد، نباید کد شهرستان انتخاب شده باشد
            obj.City = None
        else:
            # شماره تماس یا باید 4 رقمی باشد یا 8 رقمی
            if not 1000 < obj.TelNumber < 9999 and not 20000000 < obj.TelNumber < 90000000:
                raise ValidationError('شماره تلفن ثابت را به درستی وارد کنید')
            # برای شماره ثابت حتماً باید کد شهرستان انتخاب شده باشد
            if obj.City is None:
                raise ValidationError('در صورت انتخاب شماره ثابت، حتماً بایستی کد شهرستان انتخاب شود')

    def PersonCompanyValidator(obj, fieldname):
        if obj.Company is None and obj.Person is None:
            raise ValidationError('حتما یکی از موارد شخص یا شرکت باید برای ' + fieldname + ' انتخاب شود')
        if obj.Company is not None and obj.Person is not None:
            raise ValidationError('تنها یکی از موارد شخص یا شرکت باید برای ' + fieldname + ' انتخاب شود')

    def PostalCode(value):
        if not 10000 < value < 99999 and not 1000000000 < value < 9999999999:
            raise ValidationError('کدپستی معتبر نمی باشد')

    def OrganizationChart(obj):
        if obj.ParentRole is not None:
            if obj.ParentRole.Company != obj.Company:
                raise ValidationError("سمت پدر بایستی مربوط به همین شرکت باشد")


class DefaultValue:
    Country = 1  # ایران
    Province = 8  # تهران
    City = 103  # تهران


