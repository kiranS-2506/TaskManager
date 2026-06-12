from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

#Local imports
from .models import Task
from .validators import TaskValidator
from .serializer import TaskSerializer
from .permissions import is_admin 
from utils import success_response, error_response, CustomPageNumberPagination,SerializerError


# Create your views here.

class TasksListApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = CustomPageNumberPagination

    def post(self, request):
        try:

            user = request.user

            validator = TaskValidator(data=request.data)

            if not validator.is_valid():
                raise SerializerError(validator.errors)

            validated = validator.validated_data
            task_title = validated.get('title')


            task_obj = Task.objects.create(
                owner=user,
                title=task_title,
                description=validated.get('description', ''),
                status=validated.get('status', False)
            )

            return Response(
                success_response(message="Task created successfully", data={"task_id": task_obj.id}),
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                error_response(message="Something went wrong while creating the Task.", errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    def get(self, request):
        try:
            user = request.user

            search = request.query_params.get("search")
            status_filter = request.query_params.get("status")

            if is_admin(user):
                task_qs = Task.objects.all().select_related("owner")

            else:
                task_qs = Task.objects.filter(owner=user).select_related("owner")


            if not task_qs.exists():
                return Response(
                    success_response(message="No Tasks found.", data="No Matching Records."),
                    status=status.HTTP_200_OK
                )
            
            if search:
                task_qs = task_qs.filter(title__icontains=search) | task_qs.filter(description__icontains=search)

            if status_filter:
                task_qs = task_qs.filter(status=status_filter)

            paginator = self.pagination_class()

            paginated_qs = paginator.paginate_queryset(task_qs, request)
            
            serializer = TaskSerializer(paginated_qs, many=True)

            paginated_response = paginator.get_paginated_response(serializer.data)

            return Response(
                success_response(message="Successfully Fetched Tasks.", data=paginated_response.data),
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                error_response(message="Something went WRONG", errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TaskDetailApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:

            user = request.user


            if is_admin(request.user):
                task = Task.objects.filter(id=id).select_related("owner").first()
            else:
                task = Task.objects.filter(id=id, owner=user).select_related("owner").first()
            
            if not task:
                return Response(
                    error_response(message="Task not Found!", errors="Task id not found or invalid Task Id."),
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer= TaskSerializer(task)

            return Response(success_response(message="Task Fetched Successfully", data= serializer.data),
                            status=status.HTTP_200_OK)
            
        except:
             return Response(
                error_response(message="Something went wrong while fetching Task.", errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, id):

        try:
            user = request.user

            if is_admin(user):
                task_obj = Task.objects.filter(id=id).first()

            else:
                task_obj = Task.objects.filter(id=id, owner=user).first()

            if not task_obj:
                return Response(
                    error_response(message="Task not found.", errors="Invalid ID."),
                    status=status.HTTP_404_NOT_FOUND
                )

            validator = TaskValidator(data=request.data, partial=True)

            if not validator.is_valid():
                raise SerializerError(validator.errors)
                
            validated = validator.validated_data

            if "title" in validated and validated["title"]:
                validated["title"] = validated["title"].strip()

            for key, value in validated.items():
                setattr(task_obj, key, value)

            task_obj.save()

            return Response(
                success_response(message="Task updated successfully.", data={}),
                status=status.HTTP_200_OK
            )
        
   
        except Exception as e:
            return Response(
                error_response(message="Something went wrong while updating Task.", errors="An internal error occurred."),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

    def delete(self, request, id):
        try:
            if is_admin(request.user):
                task_obj = Task.objects.filter(id=id).first()
            else:
                task_obj = Task.objects.filter(id=id, owner=request.user).first()

            if not task_obj:
                return Response(
                    error_response(message="Task not found.", errors="Invalid ID."),
                    status=status.HTTP_404_NOT_FOUND
                )

            task_obj.delete()

            return Response(
                success_response(message="Task deleted successfully.", data={}),
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                error_response(message="Something went wrong while deleting Task.", errors=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )