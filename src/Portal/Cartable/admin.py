from django.contrib import admin
from .models import Document,DocumentFlow


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['AppDocId',
'Priority',
'DocState',
'DocumentTitle',
'AppCode']
    class Meta:
        model = Document



#admin.site.register(DocumentFlow)
@admin.register(DocumentFlow)
class DocumentFlowAdmin(admin.ModelAdmin):
    list_display = [
        'DocumentId',
        'InboxOwner',
        'SenderUser',
        'IsVisible',
    ]


    class Meta:
        model = DocumentFlow
