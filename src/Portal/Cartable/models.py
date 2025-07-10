from django.db import models
import jdatetime
import datetime
from django_middleware_global_request.middleware import get_request
import pytz
from django.db.models import QuerySet, Q
from django.shortcuts import get_list_or_404
from django.db import transaction
from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services

ir_tz = pytz.timezone("Asia/Tehran")

class Document(models.Model):
    AppDocId = models.IntegerField(verbose_name='شناسه', blank=True)
    # شناسه همون فرم در سیستم خودش
    Priority =models.CharField(max_length=100,verbose_name='اولویت', blank=True)
    DocState =models.CharField(max_length=100,verbose_name='وضعیت', blank=True)
    DocumentTitle = models.CharField(max_length=500,null=True,verbose_name='نوع', blank=True)
    AppCode = models.CharField(max_length=200,null=True,blank=True,verbose_name='مسیر برنامه')
    DocumentOwner = models.CharField(max_length=100, null=True,blank=True,default=None)
    DocumentOwnerNationalCode = models.CharField(max_length=10, null=True,blank=True,default=None)



class DocumentFlow(models.Model):
    DocumentId= models.ForeignKey('Document',related_name='Documents',null=True,blank=True,on_delete=models.CASCADE,verbose_name='شناسه ')
    ReceiveDate = models.DateTimeField(null=True,blank=True,verbose_name='تاریخ دریافت',auto_now_add=True)
    IsRead=models.BooleanField(default=False,verbose_name='خوانده شده', blank=True)
    SendDate=models.DateTimeField(null=True,blank=True,verbose_name='تاریخ ارسال',default=None)
    InboxOwner = models.CharField(max_length=100,verbose_name='کاربر', blank=True)
    InboxOwnerNationalCode = models.CharField(max_length=10, null=True,blank=True,default=None)
    SenderUser= models.CharField(max_length=100,verbose_name='کاربر ارسال کننده', blank=True)
    SenderUserNationalCode = models.CharField(max_length=10, null=True,blank=True,default=None)
    DueDate=models.DateField(null=True,blank=True,verbose_name='مهلت پاسخ گویی')
    PersonalDueDate=models.DateField(null=True,blank=True,verbose_name='زمان انجام کار')
    PreviousFlow = models.ForeignKey('DocumentFlow',related_name='DocumenrFlows',null=True,blank=True,on_delete=models.CASCADE,verbose_name='قبلی ')
    IsVisible = models.BooleanField(default=True,verbose_name='قابل مشاهده')
    ReadDate = models.DateTimeField(null=True, blank=True, verbose_name='زمان خوانده شده')
    TeamCode = models.CharField(max_length=3, verbose_name='شناسه تیم', null=True)
    RoleId = models.PositiveIntegerField(verbose_name='شناسه سمت', null=True)
    WorkFlowStep = models.CharField(max_length=100,verbose_name='مرحله', null=True)

    @staticmethod
    def get_flow_details(doc_id:int) -> QuerySet["DocumentFlow"]:
        # bad practice
        request = get_request()
        api_client = new_api_client(request)

        flows = get_list_or_404(DocumentFlow, DocumentId=doc_id)
        _, _, user_info = services.get_all_user_team_roles(flows[0].SenderUser, api_client=api_client)
        init_node = DocumentFlow(
            InboxOwner=flows[0].SenderUser,
            SendDate=flows[0].ReceiveDate - datetime.timedelta(minutes=1),
            RoleId=user_info[0].get("RoleId") if user_info else None,
            TeamCode=user_info[0].get("TeamCode") if user_info else None,
            WorkFlowStep="شروع فرایند")
        init_node._next_step = flows[0].id
        flows.insert(0, init_node)
        
        return flows
    
    @property
    def OwnerFullName(self) -> str:
        # bad practice
        request = get_request()
        api_client = new_api_client(request)

        if not hasattr(self, "_owner_user"):
            _, _, self._owner_user = services.get_all_user_team_roles(self.InboxOwner, api_client=api_client)
        return self._owner_user[0].get("FullName") if self._owner_user else None
        
    
    def Comments(self, username):
        return Comment.objects.filter(Q(IsPublic=True) | Q(commenttargetuser__TargetUser=username), DocumentFlow=self)
    
    @property
    def RoleName(self):
        # bad practice
        request = get_request()
        api_client = new_api_client(request)
       
        # HACK FOR ROLE MANAGEMENT DEMO (MUST BE DELETED)
        if self.TeamCode == "SPM":
            self.RoleId = 132
        elif self.TeamCode == "SPC":
            self.RoleId = 82

        _, _, data = services.get_role(self.RoleId, api_client=api_client) 
        return data.get("RoleName") if self.RoleId else None
    
    
    @property
    def TeamName(self):
        # bad practice
        request = get_request()
        api_client = new_api_client(request)

        # HACK FOR ROLE MANAGEMENT DEMO (MUST BE DELETED)
        if self.TeamCode == "SPM":
            self.TeamCode = "MIS"
        elif self.TeamCode == "SPC":
            self.TeamCode = "MAN"
        
        _, _, data = services.get_team(self.TeamCode, api_client=api_client) 

        return data.get("TeamName") if self.TeamCode else None
    
    @property
    def Image(self):
        # bad practice
        request = get_request()
        api_client = new_api_client(request)
        _, _, data = services.get_user_more_detail(self.InboxOwner, api_client=api_client)
        return data.get("StaticPhotoURL") if data else None

    @staticmethod
    def _get_time_passed_text(to_date: datetime.datetime, from_date=datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))):
        time_passed = from_date - to_date
        
        days_passed =  time_passed.days
        hours = time_passed.seconds // 3600
        minutes = time_passed.seconds // 60

        message = ""
        
        if days_passed > 0:
            message = f"{days_passed} روز"
        elif hours > 0:
            message = f"{hours} ساعت"
        elif minutes > 0:
            message = f"{minutes} دقیقه"
        else:
            message = "1 دقیقه"

        return message

    @property
    def PersianSendDate(self):
        if self.SendDate:
            jdate = jdatetime.datetime.fromgregorian(date=self.SendDate)
            ir_localized_datetime = jdate.astimezone(ir_tz)
            return ir_localized_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return ''

    @property
    def PersianReciveDate(self):
        if self.ReceiveDate:
            jdate = jdatetime.datetime.fromgregorian(date=self.ReceiveDate)
            ir_localized_datetime = jdate.astimezone(ir_tz)
            return ir_localized_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return ''
    
    @property
    def PersianReadDate(self):
        if self.ReadDate:
            jdate = jdatetime.datetime.fromgregorian(date=self.ReadDate)
            ir_localized_datetime = jdate.astimezone(ir_tz)
            return ir_localized_datetime.strftime("%Y-%m-%d %H:%M:%S")
        return ''
    
    @property
    def ReadAfter(self):
        if not self.ReceiveDate:
            return None
        elif not self.ReadDate:
            return self._get_time_passed_text(
                self.ReceiveDate,
                jdatetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            )
        
        return self._get_time_passed_text(self.ReceiveDate, self.ReadDate)
    
    @property
    def SendAfter(self):
        if not self.ReadDate:
            return None
        elif not self.SendDate:
            return self._get_time_passed_text(
                self.ReadDate,
                jdatetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
            )
        
        return self._get_time_passed_text(self.ReadDate, self.SendDate)
    
    @property
    def NextStep(self):
        if self.id:
            return list(DocumentFlow.objects.filter(PreviousFlow=self).values_list("id", flat=True))
        return [self._next_step]

class Comment(models.Model):
    CreateDate = models.DateTimeField(
        auto_now_add=True, null=True,blank=True, verbose_name="تاریخ ایجاد")
    ModifyDate = models.DateTimeField(
        auto_now=True, null=True,blank=True, verbose_name="تاریخ ویرایش")
    # CreatorUserName = models.ForeignKey(
    #     HRMODEL.Users, db_constraint=False, null=True,blank=True, verbose_name="ایجاد کننده",
    #     related_name="%(app_label)s_%(class)s_cr"
    # ,on_delete=models.DO_NOTHING)
    CreatorUserName = models.CharField(max_length=100, null=True, blank=True, verbose_name="ایجاد کننده", default=None)
    # ModifierUserName = models.ForeignKey(
    #     HRMODEL.Users, db_constraint=False, null=True,blank=True, verbose_name="ویرایش کننده", on_delete=models.DO_NOTHING
    #     ,related_name="%(app_label)s_%(class)s_md")
    ModifierUserName = models.CharField(max_length=100, null=True, blank=True, verbose_name="ویرایش کننده", default=None)
    IsPublic= models.BooleanField(verbose_name='نظرعمومی است',default=True)
    Comment = models.CharField(max_length=4000,null=True,blank=True,verbose_name='توضیحات')
    #CommentDate = models.DateField(verbose_name='تاریخ اعلام نظر')
    # TargetUser = models.ManyToManyField(HRMODEL.Users, db_constraint=False)
    Document = models.ForeignKey(Document, on_delete=models.CASCADE,null=True,blank=True, related_name='DocumentComments',verbose_name='شناسه سند')
    DocumentFlow = models.ForeignKey(DocumentFlow, on_delete=models.CASCADE, null=True, blank=True, related_name='DocumentFlowComments', verbose_name='شناسه مرحله')

    def save(self,*args,**kwargs):
        username = None
        if "custom_username" in kwargs:
            username = kwargs.get('custom_username')
            kwargs.pop("custom_username")
        else:
            request = get_request()
            # username = request.user.username + "@eit"
            username = "e.rezaee@eit"

        if self._state.adding:
            # insert new data
            self.CreatorUserName = username
        else:
            # update data
            self.ModifierUserName = username

        super().save(*args,**kwargs)

    @transaction.atomic
    def create_comment(username:str, is_public:bool, comment:str, target_users: list[str]=None, doc_id: int=None, doc_flow_id: int=None):
        if not (doc_id or doc_flow_id):
            raise ValueError("Provide a doc id or doc flow id")

        cm = Comment.objects.create(
            CreateDate=datetime.datetime.now(tz=pytz.timezone("Asia/Tehran")),
            CreatorUserName=username,
            IsPublic=is_public,
            Comment=comment,
            Document_id=doc_id,
            DocumentFlow_id=doc_flow_id
        )
        if not is_public:
            CommentTargetUser.objects.bulk_create([CommentTargetUser(CommentId=cm, TargetUser=user) for user in target_users])

    @transaction.atomic
    def update_comment(self, comment:str, username:str):
        self.Comment = comment
        self.ModifierUserName = username
        self.ModifyDate = datetime.datetime.now(tz=pytz.timezone("Asia/Tehran"))
        self.save()

        CommentViewHistory.objects.filter(CommentId=self.id).delete()


class CommentTargetUser(models.Model):
    CommentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    TargetUser = models.CharField(max_length=300, verbose_name='مخاطب')


class CommentViewHistory(models.Model):
    CommentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
    Person = models.CharField(max_length=100)
    ViewDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["CommentId", "Person"], name="UniqueView")
        ]