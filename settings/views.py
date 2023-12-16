from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import status
import traceback
import pandas as pd
from django.db import connection, connections

from settings.models import Attainment, College_Details, assessment, co_import, po_import, pso_import, target_value, unit_details
from settings.serializers import Target_serializer, assessment_serializer, attainment_serializer, co_serializer, college_serializer, po_serializer, pso_serializer, units_serializer

# Create your views here.

class College_Detail(APIView):
    def post(self,request):
        try:
            data = request.data
            create_college = College_Details.objects.create(
                college_name = data['college_name'],
                phonenumber = data['phonenumber'],
                email = data['email'],
                department = data['department'],
                address = data['address'],
                seat_allocated = data['seat_allocated'],
                img_name = data['img_name']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,id):
        try:
            data = request.data
            get_college = College_Details.objects.filter(id = id ,active = True)
            college_serialize = college_serializer(get_college , many = True)
            return Response(college_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            put_college = College_Details.objects.filter(id = id,active = True).update(
                college_name = data['college_name'],
                phonenumber = data['phonenumber'],
                email = data['email'],
                department = data['department'],
                address = data['address'],
                seat_allocated = data['seat_allocated'],
                img_name = data['img_name']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_college = College_Details.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
class co_uploadview(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    co_data = co_import.objects.create(
                        co_number = row['co_number'],
                        course_outcome = row['course_outcome']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    child = co_import(co_number=obj.get('co_number'), course_outcome=obj.get('course_outcome'))
                    created_objects.append(child)
                co_import.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            co_get = co_import.objects.filter(active = True)
            co_serialize = co_serializer(co_get,many=True)
            return Response(co_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            put_co = co_import.objects.filter(id = id,active = True).update(
                co_number = data['co_number'],
                course_outcome = data['course_outcome']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_co = co_import.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class po_uplodview(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    po_data = po_import.objects.create(
                        po_number = row['po_number'],
                        po = row['po']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    child = po_import(po_number=obj.get('po_number'), po=obj.get('po'))
                    created_objects.append(child)
                po_import.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            po_get = po_import.objects.filter(active = True)
            po_serialize = po_serializer(po_get,many=True)
            return Response(po_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            put_po = po_import.objects.filter(id = id ,active = True).update(
                po_number = data['po_number'],
                    po = data['po']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_po = po_import.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class pso_uploadview(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    pso_data = pso_import.objects.create(
                        pso_number = row['pso_number'],
                        pso = row['pso']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    child = pso_import(pso_number=obj.get('pso_number'), pso=obj.get('pso'))
                    created_objects.append(child)
                pso_import.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            pso_get = pso_import.objects.filter(active = True)
            pso_serialize = pso_serializer(pso_get,many=True)
            return Response(pso_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            put_pso = pso_import.objects.filter(id = id,active = True).update(
                pso_number = data['pso_number'],
                    pso = data['pso']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_pso = pso_import.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class attainment_uploadView(APIView):
    # def post(self, request):
    #     try:
    #         with connection.cursor() as cursor:
    #             cursor.execute(
    #                 """
    #                 SELECT table_name
    #                 FROM information_schema.tables
    #                 WHERE table_schema = 'public';
    #                 """
    #             )
    #             table_names = [row[0] for row in cursor.fetchall()]
    #             tab_value = []
    #             for table in table_names:
    #                 if table == 'attainment':
    #                     tab_value.append(table)
    #             unit_tab = 'attainment'
                
    #             if tab_value == [unit_tab]:
    #                 file = request.FILES['file']
    #                 df = pd.read_excel(file)
    #                 array_values = df.values.tolist()
    #                 table_name = 'attainment'
    #                 with connection.cursor() as cursor:
    #                     placeholders = ', '.join(['%s'] * len(array_values[0]))
    #                     insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    #                     cursor.executemany(insert_query, array_values)
    #                 return Response({'message': 'Data inserted successfully.'})
    #             else:
    #                 file = request.FILES['file']
    #                 df = pd.read_excel(file, engine='openpyxl')
    #                 table_name = 'attainment' 
    #                 create_table_query = f"CREATE TABLE {table_name} ("
    #                 for column in df.columns:
    #                     column_name = column.replace(' ', '_') 
    #                     column_data_type = df[column].dtype
    #                     if column_data_type == 'object':
    #                         column_data_type = 'text'
    #                     elif column_data_type == 'int64': 
    #                         column_data_type = 'bigint'
    #                     elif column_data_type == 'float64':
    #                         column_data_type = 'real'
    #                     elif column_data_type == 'datetime64[ns]':
    #                         column_data_type = 'timestamp'
    #                     else:
    #                         column_data_type = column_data_type.name
    #                     create_table_query += f"{column_name} {column_data_type}, "
    #                 create_table_query = create_table_query[:-2]  
    #                 create_table_query += ");"
                    
    #                 # Execute the CREATE TABLE SQL query
    #                 with connection.cursor() as cursor:
    #                     cursor.execute(create_table_query)
                
    #                 with connection.cursor() as cursor:
    #                     placeholders = ', '.join(['%s'] * len(df.columns))
    #                     insert_query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    #                     cursor.executemany(insert_query, df.values.tolist())
    #                     print(df.values.tolist())
                
    #                 return Response({'message': 'Table created successfully.'})        
    #     except Exception:
    #         return Response(traceback.format_exc(),status = status.HTTP_400_BAD_REQUEST)
    def post(self,request):
        try:
            data = request.data 
            if not isinstance(data, list):
                return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
            created_objects = []
            for obj in data:
                co_name = obj['co_number']

                try:
                    co_name = co_import.objects.get(co_number=co_name,active = True)
                except Attainment.DoesNotExist:
                    return Response({'detail': f'Parent with id {co_name} does not exist.'}, status=400)
                child = Attainment(co_name=co_name,po_details=obj.get('po_details'), pso_details=obj.get('pso_details'))
                created_objects.append(child)
            Attainment.objects.bulk_create(created_objects)
            return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        try:
            # table_name = 'attainment'
            # # Execute the SQL query to fetch table data in JSON format
            # with connection.cursor() as cursor:
            #     cursor.execute(f"SELECT row_to_json(t) FROM (SELECT * FROM {table_name}) t;")
            #     rows = cursor.fetchall()
            # data = [row[0] for row in rows]
            # for i in data:
            #     for key, value in i.items():
            #         if value == 'NaN':
            #             i[key] = '0'
            data = request.data
            attainment_get = Attainment.objects.filter(active = True)
            attainment_serialize = attainment_serializer(attainment_get,many=True)
            return Response(attainment_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status = status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        # data = request.data
        # table_name = 'attainment'
        # record_id = id
        # if not record_id:
        #     return Response({'error': 'Missing record ID.'}, status=400)
        # with connections['default'].cursor() as cursor:
        #         for i in data:
        #             if int(record_id) == i['id']:
        #                 update_params = []
        #                 for key, value in i.items():
        #                         update_params.append(f"{key} = '{value}'")
        #                 if update_params:
        #                     query = f"UPDATE {table_name} SET {', '.join(update_params)} WHERE id = {record_id};"
        #                     cursor.execute(query)
        # return Response({"message": "Data updated successfully."})
        try:
            data_list = request.data
            for data in data_list:
                co_name = co_import.objects.get(id = data["co_name"],active = True)
                put_attainment = Attainment.objects.filter(id = id,active = True).update(
                    co_name = co_name,
                    po_details = data['po_details'],
                    pso_details = data['pso_details'],

                )
                return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request,id):
        # data = request.data
        # table_name = 'attainment'
        # record_id = id

        # if not record_id:
        #     return Response({'error': 'Missing record ID.'}, status=400)

        # query = f"DELETE FROM {table_name} WHERE id = {record_id};"
        # with connections['default'].cursor() as cursor:
        #     cursor.execute(query)
        # return Response({"message": "Data deleted successfully."})
        try:
            data = request.data
            delete_attainment = Attainment.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    


class assessment_uploadview(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    co_name = co_import.objects.get(co_number = row['co_number'],active = True)
                    assessment_create = assessment.objects.create(
                        co_name = co_name,
                        course_outcome = row['course_outcome'],
                        assessment_tools = row['assessment_tools'],
                        assessment_weightages = row['assessment_weightages']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    co_name = obj['co_number']
                    try:
                        co_name = co_import.objects.get(co_number=co_name,active = True)
                    except co_import.DoesNotExist:
                        return Response({'detail': f'Parent with id {co_name} does not exist.'}, status=400)
                    child = assessment(co_name=co_name, course_outcome=obj.get('course_outcome'),assessment_tools=obj.get('assessment_tools'),assessment_weightages=obj.get('assessment_weightages'))
                    created_objects.append(child)
                assessment.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

    def get(self,request):
        try:
            data = request.data
            assessment_get = assessment.objects.filter(active = True)
            assessment_serialize = assessment_serializer(assessment_get,many=True)
            return Response(assessment_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                co_name = co_import.objects.get(id = data["co_name"],active = True)
                put_assessment = assessment.objects.filter(id = id,active = True).update(
                    co_name = co_name,
                    course_outcome = data['course_outcome'],
                    assessment_tools = data['assessment_tools'],
                    assessment_weightages = data['assessment_weightages']
                )
                return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_assessment = assessment.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class unit_datail(APIView):
    def post(self,request):
        try:
            if 'multipart/form-data' in request.content_type:
                file = request.FILES['file']
                df = pd.read_excel(file, engine='openpyxl')
                for _, row in df.iterrows():
                    co_name = co_import.objects.get(co_number = row['co_number'],active = True)
                    unit_create = unit_details.objects.create(
                        co_name = co_name,
                        unit_one = row['unit_one'],
                        unit_two = row['unit_two'],
                        unit_three = row['unit_three'],
                        unit_four = row['unit_four'],
                        unit_five = row['unit_five']
                    )
                return Response({'result':'success'},status=status.HTTP_200_OK)
            else:
                data = request.data 
                if not isinstance(data, list):
                    return Response({'detail': 'Invalid data format. Expected a list.'}, status=400)
                created_objects = []

                for obj in data:
                    co_name = obj['co_number']
                    try:
                        co_name = co_import.objects.get(co_number=co_name,active = True)
                    except co_import.DoesNotExist:
                        return Response({'detail': f'Parent with id {co_name} does not exist.'}, status=400)
                    child = unit_details(co_name=co_name, unit_one=obj.get('unit_one'),unit_two=obj.get('unit_two'),unit_three=obj.get('unit_three'),unit_four=obj.get('unit_four'),unit_five=obj.get('unit_five'))
                    created_objects.append(child)
                unit_details.objects.bulk_create(created_objects)
                return Response({'detail': f'Successfully created {len(created_objects)} objects.'}, status=status.HTTP_201_CREATED) 
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            units_get = unit_details.objects.filter(active = True)
            units_serialize = units_serializer(units_get,many=True)
            return Response(units_serialize.data,status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data_list = request.data
            for data in data_list:
                co_name = co_import.objects.get(id = data["co_name"],active = True)
                put_units = unit_details.objects.filter(id = id,active = True).update(
                    co_name = co_name,
                    unit_one = data['unit_one'],
                    unit_two = data['unit_two'],
                    unit_three = data['unit_three'],
                    unit_four = data['unit_four'],
                    unit_five = data['unit_five']
                )
                return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_units = unit_details.objects.filter(id = id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

class Target_Value(APIView):
    def post(self,request):
        try:
            data = request.data
            create_target = target_value.objects.create(
                target_value = data['target_value'],
                grade_target_value = data['grade_target_value'],
                target_mark = data['target_mark']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        try:
            data = request.data
            get_target = target_value.objects.filter(active = True)
            target_serialize = Target_serializer(get_target,many  = True)
            return Response(target_serialize.data,status=status.HTTP_200_OK)

        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request,id):
        try:
            data = request.data
            update_target = target_value.objects.filter(id = id,active = True).update(
                target_value = data['target_value'],
                grade_target_value = data['grade_target_value'], 
                target_mark = data['target_mark']
            )
            return Response({'result':'success'},status=status.HTTP_200_OK)
        
        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)  
        
    def delete(self,request,id):
        try:
            data = request.data
            delete_target = target_value.objects.filter(id =id).update(active = False)
            return Response({'result':'success'},status=status.HTTP_200_OK)

        except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST) 









