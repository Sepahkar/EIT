from rest_framework import serializers
from Cartable.models import Document, DocumentFlow, Comment, CommentTargetUser


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentFlowSerializer(serializers.ModelSerializer):
    # TODO: WorkFlowStep must be required! 
    class Meta:
        model = DocumentFlow
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    PrivateUsers = serializers.SerializerMethodField()

    def get_PrivateUsers(self, obj):
        if not obj.IsPublic:
           return list(CommentTargetUser.objects.filter(CommentId=obj.id).values_list("TargetUser", flat=True))

    class Meta:
        model = Comment
        fields = ["id", "CreatorUserName", "Comment", "IsPublic", "CreateDate", "PrivateUsers"]
        read_only_fields = ["CreateDate"]


class DocumentFlowDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    OwnerFullName = serializers.CharField()
    RoleName = serializers.CharField()
    TeamName = serializers.CharField()
    Image = serializers.CharField()
    WorkFlowStep = serializers.CharField()
    ReceiveDate = serializers.DateTimeField(source="PersianReciveDate")
    ReadDate = serializers.DateTimeField(source="PersianReadDate")
    SendDate = serializers.DateTimeField(source="PersianSendDate")
    ReadAfter = serializers.CharField()
    SendAfter = serializers.CharField()
    Note = serializers.SerializerMethodField()
    ParentStep = serializers.IntegerField(source="PreviousFlow.id", required=False, default=None)
    NextStep = serializers.ListField()

    def get_Note(self, obj):
        return []
        # must be fixed when front decide to implement notes 
        # data = obj.Comments(self.context["username"])
        # return CommentSerializer(data, many=True).data


class CreateCommentSerializer(serializers.Serializer):
    IsPublic = serializers.BooleanField()
    PrivateUsers = serializers.ListField(required=False)
    Comment = serializers.CharField(max_length=4000)
    DocId = serializers.IntegerField(required=False)
    DocFlowId = serializers.IntegerField(required=False)

    def validate_DocId(self, doc_id):
        doc = Document.objects.filter(id=doc_id).first()
        if not doc:
            raise serializers.ValidationError({"error": "invalid DocId"})
        
        return doc.id
    
    def validate_DocFlowId(self, doc_flow_id):
        doc = DocumentFlow.objects.filter(id=doc_flow_id).first()
        if not doc:
            raise serializers.ValidationError({"error": "invalid DocFlowId"})
        
        return doc.id

    def validate(self, attrs):
        data = super().validate(attrs)
        if not data["IsPublic"] and not data.get("PrivateUsers"):
            raise serializers.ValidationError({"error":"Provide users when you want to create private comment"})
        
        if not (data.get("DocId") or data.get("DocFlowId")):
            raise serializers.ValidationError({"error": "Select a DocId or DocFlowId"})
        return data
    

class UpdateCommentSerializer(serializers.Serializer):
    Comment = serializers.CharField(max_length=4000)
    CommentId = serializers.IntegerField()