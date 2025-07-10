
from django.db import models
from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services
from django_middleware_global_request import get_request


class SystemCategory(models.Model):
    UserName = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام کاربر',default=None)
    Title = models.CharField(max_length=500, verbose_name='نام دسته بندی')
    Parent = models.ForeignKey('SystemCategory', related_name='SystemCategoryParents', null=True, blank=True,
                               on_delete=models.CASCADE, verbose_name='نام دسته بندی پدر',default=None)
    Icon = models.ImageField(upload_to='media/', verbose_name='ایکون', null=True, blank=True)
    OrderNumber = models.IntegerField(verbose_name='ترتیب', null=True, blank=True)

    def __str__(self):
        return self.Title

    @property
    def Level(self):
        ParentId = self.Parent_id
        ParentExist = SystemCategory.objects.filter(id=ParentId).count()
        Level = 0
        while ParentExist > 0:
            Level = Level + 1
            QS = SystemCategory.objects.get(id=ParentId)
            ParentId = QS.Parent_id
            ParentExist = SystemCategory.objects.filter(id=ParentId).count()
        return Level

    def PermittedURLCount(self, UserName):
        pass

    # یوزرنیم میگیره میگه
    @property
    def HasURL(self):
        HasURL = True if SystemCategoryURL.objects.filter(SystemCategory=self.id).exists() else False
        return HasURL

    @property
    def RelatedURL(self):
        request = get_request()
        api_client = new_api_client(request)
        RelatedURL = SystemCategoryURL.objects.filter(SystemCategory=self.id).first()
        if RelatedURL:
            app_url_id = RelatedURL.AppURL

            _, _, app_url = services.get_app_url(app_url_id, api_client=api_client)
            app_code = app_url.get("AppCode")
            URL = app_url.get("URL")

            _, _, app = services.get_app_by_appcode(app_code, api_client=api_client)
            system_code = app.get("SystemCode")

            _, _, system = services.get_system(system_code, api_client=api_client)
            server_id = system.get("Server")

            _, _, server = services.get_server(server_id, api_client=api_client)
            port_number = server.get("PortNumber")
            base_url = server.get("IPAddress")

            full_url = base_url + ':' + str(port_number) + '/' + URL
            return full_url
        return ''


class SystemCategoryURL(models.Model):
    AppURL = models.BigIntegerField(null=True)
    SystemCategory = models.ForeignKey('SystemCategory', related_name='SystemCategoryURLSystemCategorys', null=True,
                                       blank=True, db_constraint=False, on_delete=models.CASCADE,
                                       verbose_name='دسته بندی برنامه',default=None)


