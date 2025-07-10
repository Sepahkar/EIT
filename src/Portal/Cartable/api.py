from datetime import datetime

from django.db.models import Min
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Q

from Cartable.models import (
    DocumentFlow, Document, Comment, CommentViewHistory
)
from Cartable.serializers import (
    DocumentSerializer,
    DocumentFlowSerializer,
    DocumentFlowDetailsSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer
)

import pytz
from django.db import transaction
from shared_lib.utils import new_api_client
from shared_lib.services import v1 as services


class GetDocument(APIView):
    def get(self, request, *args, **kwargs):
        by = kwargs.get('by')
        id = kwargs.get('id')
        if by == 'appdocid':
            qs = Document.objects.filter(AppDocId=id).first()
        elif by == 'docid':
            qs = Document.objects.filter(id=id).first()
        if qs:
            current_serializer = DocumentSerializer(qs)
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentExtra(APIView):
    def get(self, request, *args, **kwargs):
        app_code = kwargs.get('app_code')
        id = kwargs.get('id')
        qs = Document.objects.filter(AppDocId=id,AppCode=app_code).first()
        if qs:
            current_serializer = DocumentSerializer(qs)
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class CreateDocument(APIView):
    def post(self, request, *args, **kwargs):
        current_serializer = DocumentSerializer(data= request.data)
        if current_serializer.is_valid():
            current_serializer.save()
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateDocument(APIView):
    def put(self, request, *args, **kwargs):
        id = kwargs.get('id')
        instance = Document.objects.filter(id=id).first()
        if instance:
            for k,v in request.data.items():
                setattr(instance,k,v)
            instance.save()
            current_serializer = DocumentSerializer(instance)
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateDocumentCustom(APIView):
    def put(self, request, *args, **kwargs):
        search_data = request.data.get('search_data')
        update_data = request.data.get('update_data')
        instance = Document.objects.filter(**search_data).first()
        if instance:
            for k,v in update_data.items():
                setattr(instance,k,v)
            instance.save()
            current_serializer = DocumentSerializer(instance)
            return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentFlow(APIView):
    def post(self, request, *args, **kwargs):
        is_read = bool(request.data.get('is_read',False))
        send_date_is_null = bool(request.data.get('send_date_is_null', False))
        qs = DocumentFlow.objects.filter(DocumentId_id=int(request.data.get('doc_id')),InboxOwner=request.data.get('sender_user'),SendDate__isnull=send_date_is_null)
        qs1 = qs
        if qs.count() > 1:
            try:
                id = qs.values('DocumentId_id').annotate(Min('id')).first().get('id__min')
                qs = DocumentFlow.objects.get(id=id)
            except:
                qs = qs1.first()
        else:
            qs = qs.first()

        if qs:
            doc_flow_serializer = DocumentFlowSerializer(qs)
            return Response({'data':doc_flow_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentFlowEx(APIView):
    def post(self, request, *args, **kwargs):
        qs = DocumentFlow.objects.filter(DocumentId_id=int(request.data.get('doc_id'))).last()
        if qs:
            doc_flow_serializer = DocumentFlowSerializer(qs)
            return Response({'data':doc_flow_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentFlowUnread(APIView):
    def post(self, request, *args, **kwargs):
        is_read = request.data.get('IsRead',False)
        qs = DocumentFlow.objects.filter(DocumentId_id=int(request.data.get('doc_id')), InboxOwner=request.data.get('inbox_owner'), IsRead=is_read).first()
        if qs:
            doc_flow_serializer = DocumentFlowSerializer(qs)
            return Response({'data':doc_flow_serializer.data}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentFlowByDocId(APIView):
    def get(self,request, *args, **kwargs):
        doc_id = request.GET.get('doc_id')
        qs = Document.objects.filter(AppDocId=doc_id).first()
        if qs:
            current_serializer = DocumentSerializer(qs)
            return Response({'data':current_serializer.data},status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class CreateDocumentFlow(APIView):
    def post(self, request, *args, **kwargs):
        # Get PreviousFlow from either PreviousFlow or PreviousFlowId
        previous_flow = request.data.get('PreviousFlow')
        if not previous_flow:
            previous_flow_id = request.data.get('PreviousFlowId')
            if previous_flow_id:
                previous_flow = DocumentFlow.objects.get(id=previous_flow_id)

        doc_flow = DocumentFlow.objects.create(
            DocumentId_id=int(request.data.get('DocumentId_id')),
            ReceiveDate=datetime.fromisoformat(request.data.get('ReceiveDate')),
            InboxOwner=request.data.get('InboxOwner'),
            SenderUser=request.data.get('SenderUser'),
            DueDate=request.data.get('DueDate'),
            PersonalDueDate=request.data.get('PersonalDueDate'),
            PreviousFlow=previous_flow,
            IsVisible=request.data.get('IsVisible'),
            TeamCode=request.data.get('TeamCode'),
            RoleId=request.data.get('RoleId'),
            WorkFlowStep=request.data.get('WorkFlowStep')
        )

        current_serializer = DocumentFlowSerializer(doc_flow)
        return Response({'data': current_serializer.data}, status=status.HTTP_200_OK)


class CreateDocumentFlowBulk(APIView):
    def post(self, request, *args, **kwargs):
        all_data = request.data
        users = all_data.get('users')
        receive_data = all_data.get('data')
        duplicate_users = all_data.get('d')
        if duplicate_users is False or duplicate_users is None:
            for item in users:
                if item:
                    doc_flow = DocumentFlow(
                        DocumentId_id=int(receive_data.get('DocumentId_id')),
                        ReceiveDate=receive_data.get('ReceiveDate'),
                        InboxOwner=item,
                        SenderUser=receive_data.get('SenderUser'),
                        DueDate=receive_data.get('DueDate'),
                        PersonalDueDate=receive_data.get('PersonalDueDate'),
                        PreviousFlow_id=receive_data.get('PreviousFlow'),
                        TeamCode=receive_data.get('TeamCode'),
                        RoleId=receive_data.get('RoleId'),
                        WorkFlowStep=receive_data.get('WorkFlowStep')
                    )
                    doc_flow.save()
        return Response({'data': 'ok', 'state': 'ok'}, status=status.HTTP_200_OK)
        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetDocumentFlowByOwner(APIView):
    def get(self,request, *args, **kwargs):
        owner = request.GET.get('owner')
        qs = DocumentFlow.objects.filter(InboxOwner=owner).first()
        if qs:
            current_serializer = DocumentSerializer(qs)
            return Response({'data':current_serializer.data},status=status.HTTP_200_OK)

        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class UpdateDocumentFlow(APIView):
    def put(self, request, *args, **kwargs):
        receive_data = request.data
        instance = DocumentFlow.objects.filter(id=kwargs.get('doc_flow_id')).first()
        if instance:
            for k,v in receive_data.items():
                setattr(instance, k, v)
            instance.save()
            doc_flow_serializer = DocumentFlowSerializer(instance)
            return Response({'data':doc_flow_serializer.data},status=status.HTTP_200_OK)

        return Response({'state': "error"}, status=status.HTTP_400_BAD_REQUEST)


class GetAllVisibeCartable(APIView):

    def get(self,request,*args,**kwargs):
        #qs = DocumentFlow.objects.filter(IsVisible=True).distinct().values_list("DocumentId__AppDocId",flat=True)
        qs = DocumentFlow.objects.all().distinct().values_list("DocumentId__AppDocId",flat=True)
        return Response({'data':qs})


class GetOfficeReceiveDate(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self,request,*args,**kwargs):
        ids = request.data.get('ids')
        app_doc_ids = list(Document.objects.filter(AppDocId__in=ids).values_list('id',flat=True))
        qs = DocumentFlow.objects.filter(InboxOwner='k.hosseinpour@eit',DocumentId__in=app_doc_ids)
        data_dict = {}
        for item in qs:
           data_dict.update({str(item.DocumentId.AppDocId):item.ReceiveDate})
        return Response({'data':data_dict})


class GetDocumentLAstUserInCartable(APIView):
    def post(self,request,*args,**kwargs):
        api_client = new_api_client(request)
        try:
            _, _, all_users = services.get_all_users(params={"return-dict":1}, api_client=api_client)
            app_doc_ids = request.data.get('app_doc_ids')
            doc_ids = Document.objects.filter(AppDocId__in=app_doc_ids).values_list("id",flat=True)
            doc_flow_ids = DocumentFlow.objects.filter(DocumentId__in=doc_ids,IsVisible=True).values("DocumentId_id").annotate(min_id=Min('id')).values_list("min_id",flat=True)
            list_doc_flow = DocumentFlow.objects.filter(id__in=doc_flow_ids).values("InboxOwner","DocumentId__AppDocId")
            data = {str(item.get('DocumentId__AppDocId')): all_users.get(str(item.get('InboxOwner')).lower()).get('FullName') for item in list_doc_flow if item.get('InboxOwner')} if list_doc_flow else []

            return Response({'data': data,'state':'ok'})
        except:
            return Response({'data': [], 'state':'error'})


class CreateDocumentV1(APIView):
    def put(self, request, *args, **kwargs):
        data = request.data
        if data:
            try:
                # update or insert
                if "id" in data:
                    doc = Document.objects.get(id=data["id"])
                    serialized_data = DocumentSerializer(doc, data=data)
                else:
                    serialized_data = DocumentSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response({"msg": "success", "data": serialized_data.data})
                else:
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": serialized_data.error_messages,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    {"msg": "unexpected error", "error": e.__str__()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            {"msg": "called without payload"}, status=status.HTTP_400_BAD_REQUEST
        )
    
class CreateDocumentV2(APIView):
    def put(self, request, *args, **kwargs):
        # User sends DocumentOwnerNationalCode in new version instead of DocumentOwner
        api_client = new_api_client(request)
        
        data = request.data
        if data:
            try:
                # find username, if DocumentOwner has value override it
                if  "DocumentOwnerNationalCode" not in data:
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": "DocumentOwnerNationalCode is required.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                doc_owner_national_code = data["DocumentOwnerNationalCode"]
                
                _, status_code, d_username = services.nationalcode2username(doc_owner_national_code, api_client=api_client)
                
                if not status_code == 200:
                    return Response(d_username, status=status_code)
                
                data["DocumentOwner"] = d_username

                # update or insert
                if "id" in data:
                    doc = Document.objects.get(id=data["id"])
                    serialized_data = DocumentSerializer(doc, data=data)
                else:
                    serialized_data = DocumentSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return Response({"msg": "success", "data": serialized_data.data})
                else:
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": serialized_data.error_messages,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Exception as e:
                return Response(
                    {"msg": "unexpected error", "error": e.__str__()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            {"msg": "called without payload"}, status=status.HTTP_400_BAD_REQUEST
        )


class CreateDocumentFlowV1(APIView):
    def put(self, request, *args, **kwargs):
        data = request.data

        if data:
            try:
                # update or insert
                if "id" in data:
                    doc_flow = DocumentFlow.objects.get(id=data["id"])
                    serialized_data = DocumentFlowSerializer(doc_flow, data=data)

                else:
                    # set visibility
                    data["IsVisible"] = True

                    previous_dataflow_record = (
                        DocumentFlow.objects.filter(DocumentId_id=data["DocumentId"])
                        .order_by("-id")
                        .first()
                    )

                    if not previous_dataflow_record:
                        previous_dataflow_record_id = None

                    else:
                        previous_dataflow_record_id = previous_dataflow_record.id

                    data["PreviousFlow"] = previous_dataflow_record_id
                    serialized_data = DocumentFlowSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()

                    if previous_dataflow_record:
                        previous_dataflow_record.IsVisible = False
                        previous_dataflow_record.SendDate = datetime.now(tz=pytz.timezone("Asia/Tehran"))

                        if not (
                            previous_dataflow_record.IsRead
                            or previous_dataflow_record.ReadDate
                        ):
                            # double check if the record didnt have readdate and is read filled,
                            # this will fill it when trying to exit the document from prevous cartable
                            # also the ReadDocumentFlow API is trying to fill read date when user reads document
                            previous_dataflow_record.IsRead = True
                            previous_dataflow_record.ReadDate = datetime.now(
                                tz=pytz.timezone("Asia/Tehran")
                            )

                        previous_dataflow_record.save()

                    return Response({"msg": "success", "data": serialized_data.data})
                else:
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": serialized_data.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except Exception as e:
                return Response(
                    {"msg": "unexpected error", "error": e.__str__()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            {"msg": "called without payload"}, status=status.HTTP_400_BAD_REQUEST
        )


class CreateDocumentFlowV2(APIView):
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        api_client = new_api_client(request)
        
        data = request.data

        if data:
            try:
                if  ("InboxOwnerNationalCode" not in data and
                "SenderUserNationalCode" not in data):
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": "InboxOwnerNationalCode and SenderUserNationalCode are required.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                inbox_owner_national_code = data["InboxOwnerNationalCode"]
                sender_user_national_code = data["SenderUserNationalCode"]
                
                
                
                _, s1, d1 = services.nationalcode2username(inbox_owner_national_code, api_client=api_client)
                _, s2, d2 = services.nationalcode2username(sender_user_national_code, api_client=api_client)
                
                if not s1 == 200:
                    return Response(d1, status=s1)
                elif not s2 == 200:
                    return Response(d2, status=s2)

                data["SenderUser"] = d2
                data["InboxOwner"] = d1


                # update or insert
                if "id" in data:
                    doc_flow = DocumentFlow.objects.get(id=data["id"])
                    serialized_data = DocumentFlowSerializer(doc_flow, data=data)

                else:
                    # set visibility
                    data["IsVisible"] = True

                    previous_dataflow_record = (
                        DocumentFlow.objects.filter(DocumentId_id=data["DocumentId"])
                        .order_by("-id")
                        .first()
                    )

                    if not previous_dataflow_record:
                        previous_dataflow_record_id = None

                    else:
                        previous_dataflow_record_id = previous_dataflow_record.id

                    data["PreviousFlow"] = previous_dataflow_record_id
                    serialized_data = DocumentFlowSerializer(data=data)
                if serialized_data.is_valid():
                    serialized_data.save()

                    if previous_dataflow_record:
                        previous_dataflow_record.IsVisible = False
                        previous_dataflow_record.SendDate = datetime.now(tz=pytz.timezone("Asia/Tehran"))

                        if not (
                            previous_dataflow_record.IsRead
                            or previous_dataflow_record.ReadDate
                        ):
                            # double check if the record didnt have readdate and is read filled,
                            # this will fill it when trying to exit the document from prevous cartable
                            # also the ReadDocumentFlow API is trying to fill read date when user reads document
                            previous_dataflow_record.IsRead = True
                            previous_dataflow_record.ReadDate = datetime.now(
                                tz=pytz.timezone("Asia/Tehran")
                            )

                        previous_dataflow_record.save()

                    return Response({"msg": "success", "data": serialized_data.data})
                else:
                    return Response(
                        {
                            "msg": "payload is not valid",
                            "error": serialized_data.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            except Exception as e:
                return Response(
                    {"msg": "unexpected error", "error": e.__str__()},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(
            {"msg": "called without payload"}, status=status.HTTP_400_BAD_REQUEST
        )

class ReadDocumentFlow(APIView):
    def post(self, request, doc_flow_id, *args, **kwargs):
        doc_flow = get_object_or_404(DocumentFlow, id=doc_flow_id)
        
        if doc_flow.IsRead and doc_flow.ReadDate: 
            return Response(
                {
                    "state": "error",
                    "description": "already read!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        doc_flow.IsRead = True
        doc_flow.ReadDate = datetime.now(tz=pytz.timezone("Asia/Tehran"))
        doc_flow.save()
        
        return Response(status=status.HTTP_200_OK)

class TerminateDocumentFlow(APIView):
    def post(self, request, document_id, *args, **kwargs):
        doc = get_object_or_404(Document, id=document_id)
        doc.IsVisible = False
        doc.DocState = "توقف فرایند"
        doc.save()
        
        # exit from everyones cartables
        DocumentFlow.objects.filter(DocumentId=doc).update(IsVisible=False)
        
        latest_flow = DocumentFlow.objects.filter(DocumentId=doc).order_by("-id").first()
        latest_flow.SendDate = datetime.now(tz=pytz.timezone("Asia/Tehran"))
        latest_flow.save()


        return Response(status=status.HTTP_200_OK)

class FinishDocumentFlow(APIView):
    def post(self, request, document_id, finish_type, *args, **kwargs):
        doc_state = "نامشخص"
        if finish_type == "success":
            doc_state = "خاتمه موفقیت آمیز"
        elif finish_type == "failed":
            doc_state = "خاتمه ناموفق"
        
        doc = get_object_or_404(Document, id=document_id)
        doc.DocState = doc_state
        doc.save()

        # exit from everyones cartables
        DocumentFlow.objects.filter(DocumentId=doc).update(IsVisible=False)

        latest_flow = DocumentFlow.objects.filter(DocumentId=doc).order_by("-id").first()
        latest_flow.SendDate = datetime.now(tz=pytz.timezone("Asia/Tehran"))
        latest_flow.save()
        
        return Response(status=status.HTTP_200_OK)
    

@api_view(["GET"])
def document_flow_details(request, doc_id):
    username = request.user.username + "@eit"
    flows = DocumentFlow.get_flow_details(doc_id)
    serializer = DocumentFlowDetailsSerializer(flows, many=True, context={"username":username})
    
    return Response(serializer.data, status=200)

    
@api_view(["GET", "POST", "PATCH"])
def comments(request):
    username = request.user.username + "@eit"
    if request.method == "GET":
        doc_id = request.query_params.get("doc_id")
        comments = Comment.objects.filter(Q(IsPublic=True) | Q(commenttargetuser__TargetUser=username) | Q(CreatorUserName=username), Document=doc_id)
        new_comments = comments.exclude(commentviewhistory__CommentId__in=comments)
    
        CommentViewHistory.objects.bulk_create([CommentViewHistory(CommentId=comment, Person=username) for comment in new_comments])

        serializer = CommentSerializer(comments, many=True)
        return Response(data=serializer.data, status=200)
    
    elif request.method == "POST":
        serializer = CreateCommentSerializer(data=request.data)  
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
        req_data = serializer.data

        Comment.create_comment(
            username=username,
            is_public=req_data["IsPublic"],
            comment=req_data["Comment"],
            target_users=req_data.get("PrivateUsers"),
            doc_id=req_data.get("DocId"),
            doc_flow_id=req_data.get("DocFlowId"),
        )
        return Response({"message":"successfull"}, status=200)
    
    elif request.method == "PATCH":
        serializer = UpdateCommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=400)
        
        comment = get_object_or_404(Comment, pk=serializer.data["CommentId"], CreatorUserName=username)
        comment.update_comment(comment=serializer.data["Comment"], username=username)
        return Response({"message":"successfull"}, status=200)