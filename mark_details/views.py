from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
import traceback
from academic.models import question_pattern, student
from mark_details.models import CO_Data, Mark_Details
from mark_details.serializers import CO_serializer, mark_serializer, question_serializer,student_serializer
from usermanagement.models import user


# Create your views here.

class mark_detail(APIView):
 
    def get(self,request):  
        try:
            data = request.data
            users = request.user.email
            user_email = user.objects.filter(email = users).values('department')
            user_depart = user_email[0]['department']
            details = student.objects.filter(course_details__department = user_depart,active = True)
            student_serialize = student_serializer(details,many = True)
            question = question_pattern.objects.filter(question_no=data['question_no'],active = True)
            question_serialize = question_serializer(question,many = True)
            co = question_serialize.data
            final = []
            global data_ques
            ques = []
            for obj_values in co:
                co_value = obj_values['co_number']['co_number']
                question_value = obj_values['question']
                add_value = question_value + co_value
                obj_values['question_number'] = add_value
                var_value = obj_values['question_number']
                # data_ques.append(var_value)
                data_ques = var_value
                ques.append(data_ques)
            final.append(student_serialize.data)
            final.append({"quesion_no":ques})
            return Response(final,status=status.HTTP_200_OK)
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

class marks(APIView):


    def post(self,request):
            try:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    register_number = obj['register_number']
                    try:
                        register = student.objects.get(register_number=register_number,active = True)
                    except student.DoesNotExist:
                        return Response({'detail': f'Parent with id {register_number} does not exist.'}, status=400)
                    child = Mark_Details(student_id=register,unit=obj.get('unit'), question=obj.get('question'))
                    created_objects.append(child)
                Mark_Details.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
            except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
            
    def get(self,request):
        try:
            data = request.data
            users = request.user.email
            user_email = user.objects.filter(email = users).values('department')
            user_depart = user_email[0]['department']
            mark = Mark_Details.objects.filter(student_id__course_details__department = user_depart ,active = True)
            mark_serlialize = mark_serializer(mark ,many = True)
            return Response(mark_serlialize.data,status=status.HTTP_200_OK)
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                register = student.objects.get(register_number = data['register_number'],active = True)
                update_marks = Mark_Details.objects.filter(id = id,active = True).update(
                    student_id = register,
                    unit = data['unit'],
                    question = data['question'],
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete = Mark_Details.objects.filter(id=id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
              
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
class Co_Data(APIView):
     

    def post(self,request):
        try:
            data = request.data 
            if not isinstance(data, list):
                return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
            created_objects = []

            for obj in data:
                register_number = obj['register_number']
                try:
                    register = student.objects.get(register_number=register_number,active = True)
                except student.DoesNotExist:
                    return Response({'detail': f'Parent with id {register_number} does not exist.'}, status=400)
                child = CO_Data(student_id=register,au_results=obj.get('au_results'), Assignment_1=obj.get('Assignment_1'), Assignment_2=obj.get('Assignment_2'), Assignment_3=obj.get('Assignment_3'), Assignment_4=obj.get('Assignment_4'), Assignment_5=obj.get('Assignment_5'))
                created_objects.append(child)
            CO_Data.objects.bulk_create(created_objects)
            return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            users = request.user.email
            user_email = user.objects.filter(email = users).values('department')
            user_depart = user_email[0]['department']
            mark = CO_Data.objects.filter(student_id__course_details__department = user_depart ,active = True)
            CO_serlialize = CO_serializer(mark ,many = True)
            return Response(CO_serlialize.data,status=status.HTTP_200_OK)
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                register = student.objects.get(register_number = data['register_number'],active = True)
                update_marks = CO_Data.objects.filter(id = id,active = True).update(
                    student_id = register,
                    au_results = data['au_results'],
                    Assignment_1 = data['Assignment_1'],
                    Assignment_2 = data['Assignment_2'],
                    Assignment_3 = data['Assignment_3'],
                    Assignment_4 = data['Assignment_4'],
                    Assignment_5 = data['Assignment_5']
                )
                return Response({'result' : 'success'}, status = status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request,id):
        try:
            data = request.data
            delete = CO_Data.objects.filter(id=id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
              
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
            

        
            



 




