from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import status
import traceback
import pandas as pd
from django.db import connection, connections
from rest_framework import generics, status

from academic.models import course, question_pattern, student, subject
from academic.serializers import course_serializer, coursename_serializer, degree_serializer, department_serializer, question_serializer, student_serializer, subject_serializer
from settings.models import co_import

# Create your views here.

class course_uploadview(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    course_data = course.objects.create(
                        department = row['department'],
                        course_code = row['course_code'],
                        course_name = row['course_name'],
                        semester = row['semester'],
                        degree = row['degree'],
                        academic_year = row['academic_year']
                    )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    child = course(department=obj.get('department'), course_code=obj.get('course_code'),course_name=obj.get('course_name'),semester=obj.get('semester'),degree=obj.get('degree'),academic_year=obj.get('academic_year'))
                    created_objects.append(child)
                course.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 

        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            course_get = course.objects.filter(active = True)
            course_serialize = course_serializer(course_get,many = True)
            return Response(course_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                update_course = course.objects.filter(id =id,active = True).update(
                    department = data['department'],
                    course_code = data['course_code'],
                    course_name = data['course_name'],
                    semester = data['semester'],
                    degree = data['degree'],
                    academic_year = data['academic_year']
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_course = course.objects.filter(id=id).update(active = False)
            return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)  

# class degree_uploadview(APIView):   
#     def post(self,request):
#         try:
#             data = request.data
#             degree_get = course.objects.create(active = True)
#             degree_serialize = degree_serializer(degree_get,many = True)
#             return Response(degree_serialize.data , status=status.HTTP_200_OK)
#         except Exception:
#             return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
class coursename_uploadview(APIView):  
    def get(self,request):
        try:
            data = request.data
            coursename_get = course.objects.filter(degree = data['degree'],active = True)
            coursename_serialize = coursename_serializer(coursename_get,many = True)
            return Response(coursename_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)  
        
class department_uploadview(APIView):  
    def get(self,request):
        try:
            data = request.data
            department_get = course.objects.filter(course_name = data['course_name'] ,active = True)
            department_serialize = department_serializer(department_get,many = True)
            return Response(department_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST) 

class subject_uploadview(APIView):


    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    course_id = course.objects.get(department = row['department'],active = True)

                    subject_data = subject.objects.create(
                        course_details = course_id,
                        subject_code = row['subject_code'],
                        subject = row['subject'],
                        staff_name = row['staff_name']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    department_id = obj['department']
                    try:
                        department = course.objects.get(department=department_id,active = True)
                    except course.DoesNotExist:
                        return Response({'detail': f'Parent with id {department_id} does not exist.'}, status=400)
                    child = subject(course_details=department, subject_code=obj.get('subject_code'),subject=obj.get('subject'),staff_name=obj.get('staff_name'))
                    created_objects.append(child)
                subject.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            subject_get = subject.objects.filter(active = True)
            subject_serialize = subject_serializer(subject_get,many = True)
            return Response(subject_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                course_id = course.objects.get(department = data['department'],active = True)
                update_subject = subject.objects.filter(id = id,active = True).update(
                    course_details = course_id,
                    subject_code = data['subject_code'],
                    subject = data['subject'],
                    staff_name = data['staff_name']
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_subject = subject.objects.filter(id =id).update(active = False)
            return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class student_uploadview(APIView):


    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    course_id = course.objects.get(department = row['department'],active = True)     
                    student_data = student.objects.create(
                        course_details = course_id,
                        register_number = row['register_number'],
                        roll_number = row['roll_number'],
                        student_name = row['student_name']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    department_id = obj.get('department')
                    try:
                        department = course.objects.get(department=department_id,active = True)
                    except course.DoesNotExist:
                        return Response({'detail': f'Parent with id {department_id} does not exist.'}, status=400)
                    child = student(course_details=department, register_number=obj.get('register_number'),roll_number=obj.get('roll_number'),student_name=obj.get('student_name'))
                    created_objects.append(child)
                student.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        try:
            data = request.data
            student_get = student.objects.filter(active = True)
            student_serialize = student_serializer(student_get,many = True)
            return Response(student_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                course_id = course.objects.get(department = data['course_details'],active = True)
                update_student = student.objects.filter(id = id,active = True).update(
                    course_details = course_id,
                    register_number = data['register_number'],
                    roll_number = data['roll_number'],
                    student_name = data['student_name']
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_student = student.objects.filter(id = id).update(active = False)
            return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class question_uploadview(APIView):

    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                print (file)
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    department = course.objects.get(department = row['department'])
                    co_number = co_import.objects.get(co_number = row['co_number'])
                    question = question_pattern.objects.create(
                        department = department,
                        co_number = co_number,
                        unit = row['unit'],
                        question_no = row['question_no'],
                        question = row['question'],
                        marks_allotted = row['marks_allotted'],
                        exam_date = row['exam_date']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                objects_to_create = request.data 
                if not isinstance(objects_to_create, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in objects_to_create:
                    parent_id = obj.get('department')
                    co_number = obj.get('co_number')
                    try:
                        department = course.objects.get(department=parent_id,active = True)
                        conumber = co_import.objects.get(co_number=co_number,active = True)
                    except course.DoesNotExist:
                        return Response({'detail': f'Parent with id {parent_id} does not exist.'}, status=400)
                    child = question_pattern(department=department,co_number=conumber, unit=obj.get('unit'),question_no=obj.get('question_no'),question=obj.get('question'),marks_allotted=obj.get('marks_allotted'),exam_date=obj.get('exam_date'))
                    created_objects.append(child)
                question_pattern.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED)    
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request):
        try:
            data = request.data
            question_get = question_pattern.objects.filter(active = True)
            question_serialize = question_serializer(question_get,many = True)
            return Response(question_serialize.data , status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                department = course.objects.get(department = data['department'],active = True)
                co_number = co_import.objects.get(co_number = data['co_number'],active = True)
                question_details = question_pattern.objects.filter(id = id,active = True).update(
                    department = department,
                    co_number = co_number,
                    unit = data['unit'],
                    question_no = data['question_no'],
                    question = data['question'],
                    marks_allotted = data['marks_allotted'],
                    exam_date = data['exam_date']
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)  


    def delete(self,request,id):
        try:
            data = request.data
            delete_question = question_pattern.objects.filter(id = id).update(active = False)
            return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)   


        