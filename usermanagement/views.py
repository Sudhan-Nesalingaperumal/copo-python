from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
import traceback
from usermanagement.serializers import user_serializer
from usermanagement.models import user
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


class user_api(APIView):

    def post(self,request):
        try:
            data = request.data
            create = user.objects.create(
                employee_id = data['employee_id'],
                username = data['username'],
                email = data['email'],
                department = data['department'],
                designation = data['designation'],
                password = data['password'],
                role = data['role']
            )
            if data['role'] == 'staff':
                User.objects.create_user(username=data['username'], email=data['email'], password=data['password'],is_staff = True)
            else:
                User.objects.create_user(username=data['username'], email=data['email'], password=data['password'])
            return Response({'result':'success'},status=status.HTTP_201_CREATED)
        except Exception:
            return response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,id):
        try:
            data = request.data
            get_data = user.objects.filter(id=id,active = True)
            serialize = user_serializer(get_data,many = True)
            return Response(serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)   
        
    def put(self,request,id):
        try:
            data = request.data
            create = user.objects.filter(id=id,active = True).update(
                employee_id = data['employee_id'],
                username = data['username'],
                email = data['email'],
                department = data['department'],
                designation = data['designation'],
                password = data['password']
            )
            return Response({'result':'success'},status=status.HTTP_201_CREATED)
        except Exception:
            return response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            create = user.objects.filter(id=id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_201_CREATED)


        except Exception:
            return response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)  


class LogIn(APIView):
    
    def post(self,request):
        try:
            data = request.data
            checker = User.objects.get(email = data['email'],is_active=True)
            if checker:
                details = authenticate(username = checker.username,password = data['password'])
                if details is not None:
                    return Response({'result':'success'},status=status.HTTP_201_CREATED)
                else:
                    return Response({'result':'Not valid'},status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'result':'email is Not valid'},status=status.HTTP_400_BAD_REQUEST) 
        
        
class user_ListView(ListAPIView):

    queryset = user.objects.filter(active=True)
    serializer_class = user_serializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee_id','username']
    
    def list(self,request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
