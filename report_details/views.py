from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import status
import traceback
from academic.models import question_pattern, student, subject
from django.db.models import F
from mark_details.models import CO_Data, Mark_Details
from report_details.serializers import CO_serializer, Report_One_serializer, Target_serializer, assessment_serializer, attainment_serializer, mark_serializer, seatallocate_serializer, subject_serializer, units_serializer, year_serializer
from settings.models import Attainment, College_Details, assessment, target_value, unit_details
from usermanagement.models import user
from collections import defaultdict

# Create your views here.

def mark_data(self,request,var):

    try:
        data = request.data
        users = request.user.email
        user_email = user.objects.filter(email = users).values('department')
        user_depart = user_email[0]['department']
        unit_one = Mark_Details.objects.filter(student_id__course_details__department = user_depart ,unit = var,active = True)
        unit_serialize = Report_One_serializer(unit_one , many = True)

        return unit_serialize
        
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        
    
def table_one(self,request,var):

    try:

        unit_serialize = mark_data(self,request,var)
   
        unit_add=[]
        mark_details = {}

        for ques_data in unit_serialize.data:
            question = ques_data['question'].values()
            unit_one = sum(question)
            unit = unit_one * 2
            
            ques_data['total(50)'] = unit_one
            ques_data['total(100)'] = unit
            unit_add.append(ques_data)
            mark_details['mark_details'] = unit_add

        return mark_details
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

def table_two(self,request):

    try:
        data = request.data
        users = request.user.email
        user_email = user.objects.filter(email = users).values('department')
        user_depart = user_email[0]['department']
        subject_data = subject.objects.filter(course_details__department = user_depart,active = True)
        subjects_serialize = subject_serializer(subject_data,many =True)
        year_data = student.objects.filter(course_details__department = user_depart, active = True)
        year_serialize = year_serializer(year_data,many =True)
        subject_list = []
        subject_details = {}
        for year in year_serialize.data:
            year_data = year
        subject_list.append(subjects_serialize.data)
        subject_list.append(year_data)
        subject_details['subject_details'] = subject_list
        return subject_details
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

def table_three(self,request,var):

    try:
        mark_details = table_one(self,request,var)
        unit_add = mark_details['mark_details']
        id_values = [item['total(50)'] for item in unit_add]
        total_student = len(id_values)
        
        var = '25'
        student_pass = 0
        student_fail = 0
        student_absent = 0
        max_data = []
        Test_Analysis = []

        global max_pass 
        global max_fail 
        global max_absent 

        for value in id_values:
            if value >= int(var):
                student_pass += 1
                max_pass = student_pass
            if value < int(var) and value != 0:
                student_fail +=1
                max_fail = student_fail
            if value == 0 :
                student_absent += 1
                max_absent = student_absent

            Total_Attended = total_student - student_absent
            multi_value = value * 2
            max_data.append(multi_value)
            Maximum_Mark = max(max_data)
            sum_value = sum(max_data) / Total_Attended
            Average_Mark = round(sum_value,2)
        value = {}  
        value['total_student'] = int(total_student)
        value['student_pass'] = max_pass
        value['student_fail'] = max_fail
        value['student_absent'] = student_absent
        value['Total_Attended'] = Total_Attended
        value['Maximum_Mark'] = Maximum_Mark
        value['Average_Mark'] = Average_Mark
        Test_Analysis.append(value) 
        
        return Test_Analysis
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
                
def retrieve_data(self,request):

    try:
        data = request.data
        mark_get = question_pattern.objects.filter(question_no = data["question_no"],active=True).order_by(F("marks_allotted").asc(nulls_last=True))
        mark_serialize = mark_serializer(mark_get, many = True)
    
        questions = [item['marks_allotted'] for item in mark_serialize.data]
        question_value = [item['question'] for item in mark_serialize.data]
        co_number = [item['co_number']['co_number'] for item in mark_serialize.data]
    
        Q1_value = questions[0]
        Q2_value = questions[1]
        Q3_value = questions[2]
        Q4_value = questions[3]
        Q5_value = questions[4]
        Q6_value = questions[5]
        Q7_value = questions[6]
        Q8_value = questions[7]
        Q9_value = questions[8]
        Q10_value = questions[9]
        Q11_value = questions[10]
        Q12_value= questions[11]
        Q13_value = questions[12]
        Q14_value = questions[13]
        Q15_value = questions[14]
        Q16_value = questions[15]
        Q17_value = questions[16]
            

        add_Q6a = Q6_value + Q7_value
        Q6a_value = add_Q6a / 2

        add_Q6b = Q8_value + Q9_value
        Q6b_value = add_Q6b / 2

        add_Q7a = Q10_value + Q11_value
        Q7a_value = add_Q7a / 2
        
        add_Q7b = Q12_value + Q13_value
        Q7b_value = add_Q7b / 2

        add_Q8a = Q14_value + Q15_value
        Q8a_value = add_Q8a / 2

        add_Q8b = Q16_value + Q17_value
        Q8b_value = add_Q8b / 2

        return co_number,question_value,Q1_value,Q2_value,Q3_value,Q4_value,Q5_value,Q6a_value,Q6b_value,Q7a_value,Q7b_value,Q8a_value,Q8b_value
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    
def table_four(self,request,var):

    try:
        data = retrieve_data(self,request)
        questions = data
        Q1_value = questions[2]
        Q2_value = questions[3]
        Q3_value = questions[4]
        Q4_value = questions[5]
        Q5_value = questions[6]
        Q6a_value = questions[7]
        Q6b_value = questions[8]
        Q7a_value = questions[9]
        Q7b_value = questions[10]
        Q8a_value = questions[11]
        Q8b_value = questions[12]

        mark_details = table_one(self,request,var)
        data_from_first = mark_details['mark_details']

        Full_mark1 = 0  
        Full_mark2 = 0  
        Full_mark3 = 0  
        Full_mark4 = 0  
        Full_mark5 = 0 
        Full_mark_6a = 0 
        Full_mark_6b = 0 
        Full_mark_7a = 0 
        Full_mark_7b = 0 
        Full_mark_8a = 0 
        Full_mark_8b = 0 

        Average_Mark1 = 0
        Average_Mark2 = 0
        Average_Mark3 = 0
        Average_Mark4 = 0
        Average_Mark5 = 0
        Average_Mark_6a = 0
        Average_Mark_6b = 0
        Average_Mark_7a = 0
        Average_Mark_7b = 0
        Average_Mark_8a = 0
        Average_Mark_8b = 0

        below_mark1 = 0
        below_mark2 = 0
        below_mark3 = 0
        below_mark4 = 0
        below_mark5 = 0
        below_mark_6a = 0
        below_mark_6b = 0
        below_mark_7a = 0
        below_mark_7b = 0
        below_mark_8a = 0
        below_mark_8b = 0

        low_mark1 = 0
        low_mark2 = 0
        low_mark3 = 0
        low_mark4 = 0
        low_mark5 = 0
        low_mark_6a = 0
        low_mark_6b = 0
        low_mark_7a = 0
        low_mark_7b = 0
        low_mark_8a = 0
        low_mark_8b = 0

        Secured_FullMark = []
        Secured_Mark = {}
        for qus_value in data_from_first:
            var = qus_value['question']
            for index, key in enumerate(var):
                
                if index == 0:
                    question1 = var[key]
                    if question1 == Q1_value:
                        Full_mark1 += 1
                    elif question1 >= 1:
                        Average_Mark1 +=1 
                    elif question1 < 1 and question1 !=0:
                        below_mark1 += 1
                    elif question1 == 0:
                        low_mark1 += 1
                        
                if index == 1:
                    question2 = var[key]
                    if question2 == Q2_value:
                        Full_mark2 += 1
                    elif question2 >= 1:
                        Average_Mark2 +=1 
                    elif question2 < 1 and question2 !=0:
                        below_mark2 += 1
                    elif question2 == 0:
                        low_mark2 += 1

                if index == 2:
                    question3 = var[key]
                    if question3 == Q3_value:
                        Full_mark3 += 1
                    elif question3 >= 1:
                        Average_Mark3 +=1
                    elif question3 < 1 and question3 !=0:
                        below_mark3 += 1
                    elif question3 == 0:
                        low_mark3 += 1
                    
                if index == 3:
                    question4 = var[key]
                    if question4 == Q4_value:
                        Full_mark4 += 1
                    elif question4 >= 1:
                        Average_Mark4 +=1
                    elif question4 < 1 and question4 !=0:
                        below_mark4 += 1
                    elif question4 == 0:
                        low_mark4 += 1

                if index == 4:
                    question5 = var[key]
                    if question5 == Q5_value:
                        Full_mark5 += 1
                    elif question5 >= 1:
                        Average_Mark5 +=1
                    elif question5 < 1 and question5 !=0:
                        below_mark5 += 1
                    elif question5 == 0:
                        low_mark5 += 1

                if index == 5:
                    question6 = var[key]
                if index == 6:
                    question7 = var[key]
                if index == 7:
                    question8 = var[key]
                if index == 8:
                    question9 = var[key]
                if index == 9:
                    question10 = var[key]
                if index == 10:
                    question11 = var[key]
                if index == 11:
                    question12 = var[key]
                if index == 12:
                    question13 = var[key]
                if index == 13:
                    question14 = var[key]
                if index == 14:
                    question15 = var[key]
                if index == 15:
                    question16 = var[key]
                if index == 16:
                    question17 = var[key]
                    
            add_mark_6a = int(question6) + int(question7)
            add_mark_6b = int(question8) + int(question9)
            add_mark_7a = int(question10) + int(question11)
            add_mark_7b = int(question12) + int(question13)
            add_mark_8a = int(question14) + int(question15)
            add_mark_8b = int(question16) + int(question17)
        

            if add_mark_6a == Q6a_value:
                Full_mark_6a += 1
            elif add_mark_6a < Q6a_value and add_mark_6a > 6:
                Average_Mark_6a +=1
            elif add_mark_6a <= 6 and add_mark_6a !=0:
                below_mark_6a += 1
            elif add_mark_6a == 0:
                low_mark_6a += 1

            if add_mark_6b == Q6b_value:
                Full_mark_6b += 1
            elif add_mark_6b < Q6b_value and add_mark_6b > 6:
                Average_Mark_6b +=1
            elif add_mark_6b <= 6 and add_mark_6b !=0:
                below_mark_6b += 1
            elif add_mark_6b == 0:
                low_mark_6b += 1

                
            if add_mark_7a == Q7a_value:
                Full_mark_7a += 1
            elif add_mark_7a < Q7a_value and add_mark_7a > 6:
                Average_Mark_7a +=1
            elif add_mark_7a <= 6 and add_mark_7a !=0:
                below_mark_7a += 1
            elif add_mark_7a == 0:
                low_mark_7a += 1
        
            if add_mark_7b == Q7b_value:
                Full_mark_7b += 1
            elif add_mark_7b < Q7b_value and add_mark_7b > 6:
                Average_Mark_7b +=1
            elif add_mark_7b <= 6 and add_mark_7b !=0:
                below_mark_7b += 1
            elif add_mark_7b == 0:
                low_mark_7b += 1

                
            if add_mark_8a == Q8a_value:
                Full_mark_8a += 1
            elif add_mark_8a < Q8a_value and add_mark_8a > 6:
                Average_Mark_8a +=1
            elif add_mark_8a <= 6 and add_mark_8a !=0:
                below_mark_8a += 1
            elif add_mark_8a == 0:
                low_mark_8a += 1
        
            if add_mark_8b == Q8b_value:
                Full_mark_8b += 1
            elif add_mark_8b < Q8b_value and add_mark_8b > 6:
                Average_Mark_8b +=1
            elif add_mark_8b <= 6 and add_mark_8b !=0:
                below_mark_8b += 1
            elif add_mark_8b == 0:
                low_mark_8b += 1

        total_mark1 = Full_mark1 + Average_Mark1 + below_mark1 + low_mark1
        total_mark2 = Full_mark2 + Average_Mark2 + below_mark2 + low_mark2
        total_mark3 = Full_mark3 + Average_Mark3 + below_mark3 + low_mark3
        total_mark4 = Full_mark4 + Average_Mark4 + below_mark4 + low_mark4
        total_mark5 = Full_mark5 + Average_Mark5 + below_mark5 + low_mark5
        total_mark_6a = Full_mark_6a + Average_Mark_6a + below_mark_6a + low_mark_6a
        total_mark_6b = Full_mark_6b + Average_Mark_6b + below_mark_6b + low_mark_6b
        total_mark_7a = Full_mark_7a + Average_Mark_7a + below_mark_7a + low_mark_7a
        total_mark_7b = Full_mark_7b + Average_Mark_7b + below_mark_7b + low_mark_7b
        total_mark_8a = Full_mark_8a + Average_Mark_8a + below_mark_8a + low_mark_8a
        total_mark_8b = Full_mark_8b + Average_Mark_8b + below_mark_8b + low_mark_8b

        FullMark = {}
        FullMark['Fullmark_Q1'] = Full_mark1
        FullMark['Fullmark_Q2'] = Full_mark2
        FullMark['Fullmark_Q3'] = Full_mark3
        FullMark['Fullmark_Q4'] = Full_mark4
        FullMark['Fullmark_Q5'] = Full_mark5
        FullMark['Fullmark_6a'] = Full_mark_6a
        FullMark['Fullmark_6b'] = Full_mark_6b
        FullMark['Fullmark_7a'] = Full_mark_7a
        FullMark['Fullmark_7b'] = Full_mark_7b
        FullMark['Fullmark_8a'] = Full_mark_8a
        FullMark['Fullmark_8b'] = Full_mark_8b
        Secured_FullMark.append(FullMark) 
        
        Average_Mark = {}
        Average_Mark['AverageMark_Q1'] = Average_Mark1
        Average_Mark['AverageMark_Q2'] = Average_Mark2
        Average_Mark['AverageMark_Q3'] = Average_Mark3
        Average_Mark['AverageMark_Q4'] = Average_Mark4
        Average_Mark['AverageMark_Q5'] = Average_Mark5
        Average_Mark['AverageMark_6a'] = Average_Mark_6a
        Average_Mark['AverageMark_6b'] = Average_Mark_6b
        Average_Mark['AverageMark_7a'] = Average_Mark_7a
        Average_Mark['AverageMark_7b'] = Average_Mark_7b
        Average_Mark['AverageMark_8a'] = Average_Mark_8a
        Average_Mark['AverageMark_8b'] = Average_Mark_8b
        Secured_FullMark.append(Average_Mark) 

        Below_Mark = {}
        Below_Mark['BelowMark_Q1'] = below_mark1
        Below_Mark['BelowMark_Q2'] = below_mark2
        Below_Mark['BelowMark_Q3'] = below_mark3
        Below_Mark['BelowMark_Q4'] = below_mark4
        Below_Mark['BelowMark_Q5'] = below_mark5
        Below_Mark['BelowMark_6a'] = below_mark_6a
        Below_Mark['BelowMark_6b'] = below_mark_6b
        Below_Mark['BelowMark_7a'] = below_mark_7a
        Below_Mark['BelowMark_7b'] = below_mark_7b
        Below_Mark['BelowMark_8a'] = below_mark_8a
        Below_Mark['BelowMark_8b'] = below_mark_8b
        Secured_FullMark.append(Below_Mark) 

        low_Mark = {}
        low_Mark['lowMark_Q1'] = low_mark1
        low_Mark['lowMark_Q2'] = low_mark2
        low_Mark['lowMark_Q3'] = low_mark3
        low_Mark['lowMark_Q4'] = low_mark4
        low_Mark['lowMark_Q5'] = low_mark5
        low_Mark['lowMark_6a'] = low_mark_6a
        low_Mark['lowMark_6b'] = low_mark_6b
        low_Mark['lowMark_7a'] = low_mark_7a
        low_Mark['lowMark_7b'] = low_mark_7b
        low_Mark['lowMark_8a'] = low_mark_8a
        low_Mark['lowMark_8b'] = low_mark_8b
        Secured_FullMark.append(low_Mark) 

        Total_Mark = {}
        Total_Mark['TotalMark_Q1'] = total_mark1
        Total_Mark['TotalMark_Q2'] = total_mark2
        Total_Mark['TotalMark_Q3'] = total_mark3
        Total_Mark['TotalMark_Q4'] = total_mark4
        Total_Mark['TotalMark_Q5'] = total_mark5
        Total_Mark['TotalMark_6a'] = total_mark_6a
        Total_Mark['TotalMark_6b'] = total_mark_6b
        Total_Mark['TotalMark_7a'] = total_mark_7a
        Total_Mark['TotalMark_7b'] = total_mark_7b
        Total_Mark['TotalMark_8a'] = total_mark_8a
        Total_Mark['TotalMark_8b'] = total_mark_8b
        Secured_FullMark.append(Total_Mark) 

        Secured_Mark['Secured_FullMark'] = Secured_FullMark

        return Secured_Mark
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

def table_five(self,request,var):

    try:
        mark_details = table_one(self,request,var)
        data_from_first = mark_details['mark_details']

        sum_question1 = 0 
        sum_question2 = 0 
        sum_question3 = 0 
        sum_question4 = 0 
        sum_question5 = 0 
        sum_question6a_1 = 0 
        sum_question6a_2 = 0 
        sum_question6b_1 = 0 
        sum_question6b_2 = 0 
        sum_question7a_1 = 0 
        sum_question7a_2 = 0 
        sum_question7b_1 = 0 
        sum_question7b_2 = 0 
        sum_question8a_1 = 0 
        sum_question8a_2 = 0 
        sum_question8b_1 = 0 
        sum_question8b_2 = 0 

        attend1 = 0
        attend2 = 0
        attend3 = 0
        attend4 = 0
        attend5 = 0
        attend_6a = 0
        attend_6b = 0
        attend_7a = 0
        attend_7b = 0
        attend_8a = 0
        attend_8b = 0

        Not_attend1 = 0
        Not_attend2 = 0
        Not_attend3 = 0
        Not_attend4 = 0
        Not_attend5 = 0
        Not_attend_6a = 0
        Not_attend_6b = 0
        Not_attend_7a = 0
        Not_attend_7b = 0
        Not_attend_8a = 0
        Not_attend_8b = 0


        Secured_TotalMark = []
        Secured_Total = {}

        for qus_value in data_from_first:
            var = qus_value['question']

            global attend6a_1
            global attend6a_2
            global attend6b_1
            global attend6b_2
            global attend7a_1
            global attend7a_2
            global attend7b_1
            global attend7b_2
            global attend8a_1
            global attend8a_2
            global attend8b_1
            global attend8b_2
            

            for index, key in enumerate(var):
                if index == 0:
                    question1 = var[key]
                    if isinstance(question1, (int, float)):
                        sum_question1 += question1
                        if question1 !=0 :
                            attend1 += 1
                        elif question1 == 0:
                            Not_attend1 +=1             
                if index == 1:
                    question2 = var[key]
                    if isinstance(question2, (int, float)):
                        sum_question2 += question2 
                        if question2 !=0 :
                            attend2 += 1 
                        elif question2 == 0:
                            Not_attend2 +=1
                if index == 2:
                    question3 = var[key]
                    if isinstance(question3, (int, float)):
                        sum_question3 += question3 
                        if question3 !=0 :
                            attend3 += 1
                        elif question3 == 0:
                            Not_attend3 +=1
                if index == 3:
                    question4 = var[key]
                    if isinstance(question4, (int, float)):
                        sum_question4 += question4 
                        if question4 !=0 :
                            attend4 += 1
                        elif question4 == 0:
                            Not_attend4 +=1
                if index == 4:
                    question5 = var[key]
                    if isinstance(question5, (int, float)):
                        sum_question5 += question5 
                        if question5 !=0 :
                            attend5 += 1
                        elif question5 == 0:
                            Not_attend5 += 1

                if index == 5:
                    question6a_1 = var[key]
                    if isinstance(question6a_1, (int, float)):
                        sum_question6a_1 += question6a_1 
                        attend6a_1 = question6a_1 
                if index == 6:
                    question6a_2 = var[key]
                    if isinstance(question6a_2, (int, float)):
                        sum_question6a_2 += question6a_2
                        attend6a_2 = question6a_2
                if index == 7:
                    question6b_1 = var[key]
                    if isinstance(question6b_1, (int, float)):
                        sum_question6b_1 += question6b_1
                        attend6b_1 = question6b_1
                if index == 8:
                    question6b_2 = var[key]
                    if isinstance(question6b_2, (int, float)):
                        sum_question6b_2 += question6b_2
                        attend6b_2 = question6b_2

                if index == 9:
                    question7a_1 = var[key]
                    if isinstance(question7a_1, (int, float)):
                        sum_question7a_1 += question7a_1 
                        attend7a_1 = question7a_1
                if index == 10:
                    question7a_2 = var[key]
                    if isinstance(question7a_2, (int, float)):
                        sum_question7a_2 += question7a_2
                        attend7a_2 = question7a_2
                if index == 11:
                    question7b_1 = var[key]
                    if isinstance(question7b_1, (int, float)):
                        sum_question7b_1 += question7b_1
                        attend7b_1 = question7b_1
                if index == 12:
                    question7b_2 = var[key]
                    if isinstance(question7b_2, (int, float)):
                        sum_question7b_2 += question7b_2
                        attend7b_2 = question7b_2

                if index == 13:
                    question8a_1 = var[key]
                    if isinstance(question8a_1, (int, float)):
                        sum_question8a_1 += question8a_1 
                        attend8a_1 = question8a_1
                if index == 14:
                    question8a_2 = var[key]
                    if isinstance(question8a_2, (int, float)):
                        sum_question8a_2 += question8a_2
                        attend8a_2 = question8a_2
                if index == 15:
                    question8b_1 = var[key]
                    if isinstance(question8b_1, (int, float)):
                        sum_question8b_1 += question8b_1
                        attend8b_1 = question8b_1
                if index == 16:
                    question8b_2 = var[key]
                    if isinstance(question8b_2, (int, float)):
                        sum_question8b_2 += question8b_2
                        attend8b_2 = question8b_2

                mark_6a = sum_question6a_1 + sum_question6a_2
                mark_6b = sum_question6b_1 + sum_question6b_2
                mark_7a = sum_question7a_1 + sum_question7a_2
                mark_7b = sum_question7b_1 + sum_question7b_2
                mark_8a = sum_question8a_1 + sum_question8a_2
                mark_8b = sum_question8b_1 + sum_question8b_2

            attend6_a = attend6a_1 + attend6a_2
            attend6_b = attend6b_1 + attend6b_2
            attend7_a = attend7a_1 + attend7a_2
            attend7_b = attend7b_1 + attend7b_2
            attend8_a = attend8a_1 + attend8a_2
            attend8_b = attend8b_1 + attend8b_2
            
            if attend6_a != 0 :
                attend_6a += 1
            elif attend6_a == 0 :
                Not_attend_6a += 1
            if attend6_b != 0 :
                attend_6b += 1
            elif attend6_b == 0 :
                Not_attend_6b += 1
            if attend7_a != 0 :
                attend_7a += 1
            elif attend7_a == 0 :
                Not_attend_7a += 1
            if attend7_b != 0 :
                attend_7b += 1
            elif attend7_b == 0 :
                Not_attend_7b += 1
            if attend8_a != 0 :
                attend_8a += 1
            elif attend8_a == 0 :
                Not_attend_8a += 1
            if attend8_b != 0 :
                attend_8b += 1
            elif attend8_b == 0 :
                Not_attend_8b += 1


        Average_Q1 = sum_question1 / attend1
        Average_Q2 = sum_question2 / attend2
        Average_Q3 = sum_question3 / attend3
        Average_Q4 = sum_question4 / attend4
        Average_Q5 = sum_question5 / attend5
        Average_6a = mark_6a / attend_6a
        Average_6b = mark_6b / attend_6b
        Average_7a = mark_7a / attend_7a
        Average_7b = mark_7b / attend_7b
        Average_8a = mark_8a / attend_8a
        Average_8b = mark_8b / attend_8b
            

        data = retrieve_data(self,request)
        questions = data
        q1 = questions[2]
        q2 = questions[3]
        q3 = questions[4]
        q4 = questions[5]
        q5 = questions[6]
        q6a = questions[7]
        q6b = questions[8]
        q7a = questions[9]
        q7b = questions[10]
        q8a = questions[11]
        q8b = questions[12]
        

        Percentage_Q1 = (Average_Q1 * 100) / q1
        Percentage_Q2 = (Average_Q2 * 100) / q2
        Percentage_Q3 = (Average_Q3 * 100) / q3
        Percentage_Q4 = (Average_Q4 * 100) / q4
        Percentage_Q5 = (Average_Q5 * 100) / q5
        Percentage_6a = (Average_6a * 100) / q6a
        Percentage_6b = (Average_6b * 100) / q6b
        Percentage_7a = (Average_7a * 100) / q7a
        Percentage_7b = (Average_7b * 100) / q7b
        Percentage_8a = (Average_8a * 100) / q8a
        Percentage_8b = (Average_8b * 100) / q8b
        
        
        TotalNotAttend = {}
        TotalNotAttend['Total_NotAttend_Q1'] = Not_attend1
        TotalNotAttend['Total_NotAttend_Q2'] = Not_attend2
        TotalNotAttend['Total_NotAttend_Q3'] = Not_attend3
        TotalNotAttend['Total_NotAttend_Q4'] = Not_attend4
        TotalNotAttend['Total_NotAttend_Q5'] = Not_attend5
        TotalNotAttend['Total_NotAttend_Q6a'] = Not_attend_6a
        TotalNotAttend['Total_NotAttend_Q6b'] = Not_attend_6b
        TotalNotAttend['Total_NotAttend_Q7a'] = Not_attend_7a
        TotalNotAttend['Total_NotAttend_Q7b'] = Not_attend_7b
        TotalNotAttend['Total_NotAttend_Q8a'] = Not_attend_8a
        TotalNotAttend['Total_NotAttend_Q8b'] = Not_attend_8b
        Secured_TotalMark.append(TotalNotAttend)

        TotalAttend = {}
        TotalAttend['Total_Attend_Q1'] = attend1
        TotalAttend['Total_Attend_Q2'] = attend2
        TotalAttend['Total_Attend_Q3'] = attend3
        TotalAttend['Total_Attend_Q4'] = attend4
        TotalAttend['Total_Attend_Q5'] = attend5
        TotalAttend['Total_Attend_Q6a'] = attend_6a
        TotalAttend['Total_Attend_Q6b'] = attend_6b
        TotalAttend['Total_Attend_Q7a'] = attend_7a
        TotalAttend['Total_Attend_Q7b'] = attend_7b
        TotalAttend['Total_Attend_Q8a'] = attend_8a
        TotalAttend['Total_Attend_Q8b'] = attend_8b
        Secured_TotalMark.append(TotalAttend)

        TotalSecured = {}
        TotalSecured['Total_Secured_Q1'] = sum_question1
        TotalSecured['Total_Secured_Q2'] = sum_question2
        TotalSecured['Total_Secured_Q3'] = sum_question3
        TotalSecured['Total_Secured_Q4'] = sum_question4
        TotalSecured['Total_Secured_Q5'] = sum_question5
        TotalSecured['Total_Secured_Q6a'] = mark_6a
        TotalSecured['Total_Secured_Q6b'] = mark_6b
        TotalSecured['Total_Secured_Q7a'] = mark_7a
        TotalSecured['Total_Secured_Q7b'] = mark_7b
        TotalSecured['Total_Secured_Q8a'] = mark_8a
        TotalSecured['Total_Secured_Q8b'] = mark_8b
        Secured_TotalMark.append(TotalSecured) 

        TotalAverageMarks = {}
        TotalAverageMarks['Total_AverageMarks_Q1'] = round(Average_Q1,2)
        TotalAverageMarks['Total_AverageMarks_Q2'] = round(Average_Q2,2)
        TotalAverageMarks['Total_AverageMarks_Q3'] = round(Average_Q3,2)
        TotalAverageMarks['Total_AverageMarks_Q4'] = round(Average_Q4,2)
        TotalAverageMarks['Total_AverageMarks_Q5'] = round(Average_Q5,2)
        TotalAverageMarks['Total_AverageMarks_Q6a'] = round(Average_6a,2)
        TotalAverageMarks['Total_AverageMarks_Q6b'] = round(Average_6b,2)
        TotalAverageMarks['Total_AverageMarks_Q7a'] = round(Average_7a,2)
        TotalAverageMarks['Total_AverageMarks_Q7b'] = round(Average_7b,2)
        TotalAverageMarks['Total_AverageMarks_Q8a'] = round(Average_8a,2)
        TotalAverageMarks['Total_AverageMarks_Q8b'] = round(Average_8b,2)
        Secured_TotalMark.append(TotalAverageMarks)

        TotalPercentageMarks = {}
        TotalPercentageMarks['Total_PercentageMarks_Q1'] = round(Percentage_Q1,2)
        TotalPercentageMarks['Total_PercentageMarks_Q2'] = round(Percentage_Q2,2)
        TotalPercentageMarks['Total_PercentageMarks_Q3'] = round(Percentage_Q3,2)
        TotalPercentageMarks['Total_PercentageMarks_Q4'] = round(Percentage_Q4,2)
        TotalPercentageMarks['Total_PercentageMarks_Q5'] = round(Percentage_Q5,2)
        TotalPercentageMarks['Total_PercentageMarks_Q6a'] = round(Percentage_6a,2)
        TotalPercentageMarks['Total_PercentageMarks_Q6b'] = round(Percentage_6b,2)
        TotalPercentageMarks['Total_PercentageMarks_Q7a'] = round(Percentage_7a,2)
        TotalPercentageMarks['Total_PercentageMarks_Q7b'] = round(Percentage_7b,2)
        TotalPercentageMarks['Total_PercentageMarks_Q8a'] = round(Percentage_8a,2)
        TotalPercentageMarks['Total_PercentageMarks_Q8b'] = round(Percentage_8b,2)
        Secured_TotalMark.append(TotalPercentageMarks)

        Secured_Total['Secured_TotalMark'] = Secured_TotalMark

        return Secured_Total
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
            

def table_six(self,request,var):

    try:
        data = request.data
        get_target = target_value.objects.filter(active = True)
        target_serialize = Target_serializer(get_target,many  = True)
        for target in target_serialize.data:
            target_grade_value = target['target_value']
            if target_grade_value != 0 :
                target_val = target_grade_value
        data_question = retrieve_data(self,request)
        questions = data_question
          
        co_number = questions[0]
        question_no = questions[1]
        q1 = questions[2]
        q2 = questions[3]
        q3 = questions[4]
        q4 = questions[5]
        q5 = questions[6]
        q6a = questions[7]
        q6b = questions[8]
        q7a = questions[9]
        q7b = questions[10]
        q8a = questions[11]
        q8b = questions[12]
        
        add_question = q1 + q2 + q3 + q4 + q5 + q6a + q7a + q8a

        student_id_CO1 = 0
        attend_CO1 = 0
        CO_Attained_CO1 = 0
        total_attend_CO1 = 0
        total_50_values_CO1 = []

        #  <-----CO3------>

        student_id_CO2 = 0
        attend_CO2 = 0
        CO_Attained_CO2 = 0
        total_attend_CO2 = 0
        total_50_values_CO2 = []

        #  <-----CO3------>

        student_id_CO3 = 0
        attend_CO3 = 0
        CO_Attained_CO3 = 0
        total_attend_CO3 = 0
        total_50_values_CO3 = []

            #  <-----CO4------>

        student_id_CO4 = 0
        attend_CO4 = 0
        CO_Attained_CO4 = 0
        total_attend_CO4 = 0
        total_50_values_CO4 = []

        #  <-----CO5------>

        student_id_CO5 = 0
        attend_CO5 = 0
        CO_Attained_CO5 = 0
        total_attend_CO5 = 0
        total_50_values_CO5 = []

        Course_Outcome_Analysis = []


        unit_serialize = mark_data(self,request,var)

        for student in unit_serialize.data:
            stud = student['student_id']['register_number']
            question1 = student['question'].keys()

            for key in question1:
                co1_key = key    

                for pattern in question_no:
                    co1 = pattern + 'CO1'

                if co1_key == co1 :
                    question_CO1 = student['question'].values()
                    
                    total_50_CO1 = sum(question_CO1)
                    total_50_values_CO1.append(total_50_CO1)

                    maximum_total_50_CO1 = max(total_50_values_CO1)
                
                    attend_CO1 += total_50_CO1
                    
                    if total_50_CO1:
                        total_attend_CO1 +=1

                    if stud:
                        student_id_CO1 += 1

                    Alloted_CO1 = add_question * student_id_CO1
                    
                    div_target_CO1 = target_val / 100

                    Max_of_Target_CO1 = maximum_total_50_CO1 * div_target_CO1
                    break

                else:
                    Alloted_CO1 = 0
                    maximum_total_50_CO1 = 0
                    Max_of_Target_CO1 = 0 

                        #  <-----CO2------>
                
            for key in question1:
                co2_key = key    

                for pattern in question_no:
                    co2 = pattern + 'CO2'
                    
                if co2_key == co2 :
                    question_CO2 = student['question'].values()
                    
                    total_50_CO2 = sum(question_CO2)
                    total_50_values_CO2.append(total_50_CO2)

                    maximum_total_50_CO2 = max(total_50_values_CO2)
                
                    attend_CO2 += total_50_CO2
                    
                    if total_50_CO2:
                        total_attend_CO2 +=1

                    if stud:
                        student_id_CO2 += 1

                    Alloted_CO2 = add_question * student_id_CO2
                    
                    div_target_CO2 = target_val / 100

                    Max_of_Target_CO2 = maximum_total_50_CO2 * div_target_CO2
                    break
                else:
                    Alloted_CO2 = 0
                    maximum_total_50_CO2 = 0
                    Max_of_Target_CO2 = 0 

                        #  <-----CO3------>
                            
            for key in question1:
                co3_key = key    

                for pattern in question_no:
                    co3 = pattern + 'CO3'

                if co3_key == co3 :
                    question_CO3 = student['question'].values()
                    
                    total_50_CO3 = sum(question_CO3)
                    total_50_values_CO3.append(total_50_CO3)

                    maximum_total_50_CO3 = max(total_50_values_CO3)
                
                    attend_CO3 += total_50_CO3
                    
                    if total_50_CO3:
                        total_attend_CO3 +=1

                    if stud:
                        student_id_CO3 += 1

                    Alloted_CO3 = add_question * student_id_CO3
                    
                    div_target_CO3 = target_val / 100

                    Max_of_Target_CO3 = maximum_total_50_CO3 * div_target_CO3
                    break
                else:
                    Alloted_CO3 = 0
                    maximum_total_50_CO3 = 0
                    Max_of_Target_CO3 = 0 

                #  <-----CO4------>
                            
            for key in question1:
                co4_key = key    

                for pattern in question_no:
                    co4 = pattern + 'CO4'
                    
                if co4_key == co4 :
                    question_CO4 = student['question'].values()
                    
                    total_50_CO4 = sum(question_CO4)
                    total_50_values_CO4.append(total_50_CO4)

                    maximum_total_50_CO4 = max(total_50_values_CO4)
                
                    attend_CO4 += total_50_CO4
                    
                    if total_50_CO4:
                        total_attend_CO4 +=1

                    if stud:
                        student_id_CO4 += 1

                    Alloted_CO4 = add_question * student_id_CO4
                    
                    div_target_CO4 = target_val / 100

                    Max_of_Target_CO4 = maximum_total_50_CO4 * div_target_CO4
                    break
                else:
                    Alloted_CO4 = 0
                    maximum_total_50_CO4 = 0
                    Max_of_Target_CO4 = 0 

                #  <-----CO5------>
                            
            for key in question1:
                co5_key = key    

                for pattern in question_no:
                    co5 = pattern + 'CO5'
                    
                if co5_key == co5 :
                    question_CO5 = student['question'].values()
                    
                    total_50_CO5 = sum(question_CO5)
                    total_50_values_CO5.append(total_50_CO5)
                   
                    maximum_total_50_CO5 = max(total_50_values_CO5)
                    
                    attend_CO5 += total_50_CO5
                    
                    if total_50_CO5:
                        total_attend_CO5 +=1

                    if stud:
                        student_id_CO5 += 1

                    Alloted_CO5 = add_question * student_id_CO5
                    
                    div_target_CO5 = target_val / 100

                    Max_of_Target_CO5 = maximum_total_50_CO5 * div_target_CO5
                    
                    break
                else:
                    Alloted_CO5 = 0
                    maximum_total_50_CO5 = 0
                    Max_of_Target_CO5 = 0 
    
        for value_50_CO1 in total_50_values_CO1:
            if value_50_CO1 >= Max_of_Target_CO1:
                CO_Attained_CO1 += 1
        
        if CO_Attained_CO1 != 0:
            Percentage_CO1 = (CO_Attained_CO1 / total_attend_CO1) * 100
        elif CO_Attained_CO1 == 0:
            Percentage_CO1 = 0

        if Percentage_CO1 > 80 :
            Attainment_Level_CO1 = 3
        elif Percentage_CO1 > 70 :
            Attainment_Level_CO1 = 2
        elif Percentage_CO1 > 60 :
            Attainment_Level_CO1 = 1
        else:
            Attainment_Level_CO1 = 0

                #  <-----CO2------>

        for value_50_CO2 in total_50_values_CO2:
            if value_50_CO2 >= Max_of_Target_CO2:
                CO_Attained_CO2 += 1
                
        if CO_Attained_CO2 != 0:
            Percentage_CO2 = (CO_Attained_CO2 / total_attend_CO2) * 100
        elif CO_Attained_CO2 == 0:
            Percentage_CO2 = 0

        if Percentage_CO2 > 80 :
            Attainment_Level_CO2 = 3
        elif Percentage_CO2 > 70 :
            Attainment_Level_CO2 = 2
        elif Percentage_CO2 > 60 :
            Attainment_Level_CO2 = 1
        else:
            Attainment_Level_CO2 = 0

            #  <-----CO3------>

        for value_50_CO3 in total_50_values_CO3:
            if value_50_CO3 >= Max_of_Target_CO3:
                CO_Attained_CO3 += 1
                
        if CO_Attained_CO3 != 0:
            Percentage_CO3 = (CO_Attained_CO3 / total_attend_CO3) * 100
        elif CO_Attained_CO3 == 0:
            Percentage_CO3 = 0

        if Percentage_CO3 > 80 :
            Attainment_Level_CO3 = 3
        elif Percentage_CO3 > 70 :
            Attainment_Level_CO3 = 2
        elif Percentage_CO3 > 60 :
            Attainment_Level_CO3 = 1
        else:
            Attainment_Level_CO3 = 0

                #  <-----CO4------>

        for value_50_CO4 in total_50_values_CO4:
            if value_50_CO4 >= Max_of_Target_CO4:
                CO_Attained_CO4 += 1
                
        if CO_Attained_CO4 != 0:
            Percentage_CO4 = (CO_Attained_CO4 / total_attend_CO4) * 100
        elif CO_Attained_CO4 == 0:
            Percentage_CO4 = 0

        if Percentage_CO4 > 80 :
            Attainment_Level_CO4 = 3
        elif Percentage_CO4 > 70 :
            Attainment_Level_CO4 = 2
        elif Percentage_CO4 > 60 :
            Attainment_Level_CO4 = 1
        else:
            Attainment_Level_CO4 = 0

                #  <-----CO5------>
       
        for value_50_CO5 in total_50_values_CO5:
            
            if value_50_CO5 >= Max_of_Target_CO5:
                CO_Attained_CO5 += 1
                
        if CO_Attained_CO5 != 0:
            Percentage_CO5 = (CO_Attained_CO5 / total_attend_CO5) * 100
        elif CO_Attained_CO5 == 0:
            Percentage_CO5 = 0

        if Percentage_CO5 > 80 :
            Attainment_Level_CO5 = 3
        elif Percentage_CO5 > 70 :
            Attainment_Level_CO5 = 2
        elif Percentage_CO5 > 60 :
            Attainment_Level_CO5 = 1
        else:
            Attainment_Level_CO5 = 0

        Course_Outcome_CO1 = {}
        Course_Outcome_CO1['alloted'] = Alloted_CO1
        Course_Outcome_CO1['attend'] = attend_CO1
        Course_Outcome_CO1['Maximum'] = maximum_total_50_CO1
        Course_Outcome_CO1['max_of_target'] = Max_of_Target_CO1
        Course_Outcome_CO1['co_attained'] = CO_Attained_CO1
        Course_Outcome_CO1['percentage'] = round(Percentage_CO1 , 2)
        Course_Outcome_CO1['attainment_level'] = Attainment_Level_CO1
        Course_Outcome_Analysis.append(Course_Outcome_CO1)

        Course_Outcome_CO2 = {}
        Course_Outcome_CO2['alloted'] = Alloted_CO2
        Course_Outcome_CO2['attend'] = attend_CO2
        Course_Outcome_CO2['Maximum'] = maximum_total_50_CO2
        Course_Outcome_CO2['max_of_target'] = round(Max_of_Target_CO2 , 2)
        Course_Outcome_CO2['co_attained'] = CO_Attained_CO2
        Course_Outcome_CO2['percentage'] = round(Percentage_CO2 , 2)
        Course_Outcome_CO2['attainment_level'] = Attainment_Level_CO2
        Course_Outcome_Analysis.append(Course_Outcome_CO2)
            
        Course_Outcome_CO3 = {}
        Course_Outcome_CO3['alloted'] = Alloted_CO3
        Course_Outcome_CO3['attend'] = attend_CO3
        Course_Outcome_CO3['Maximum'] = maximum_total_50_CO3
        Course_Outcome_CO3['max_of_target'] = round(Max_of_Target_CO3 , 2)
        Course_Outcome_CO3['co_attained'] = CO_Attained_CO3
        Course_Outcome_CO3['percentage'] = round(Percentage_CO3 , 2)
        Course_Outcome_CO3['attainment_level'] = Attainment_Level_CO3
        Course_Outcome_Analysis.append(Course_Outcome_CO3)

        Course_Outcome_CO4 = {}
        Course_Outcome_CO4['alloted'] = Alloted_CO4
        Course_Outcome_CO4['attend'] = attend_CO4
        Course_Outcome_CO4['Maximum'] = maximum_total_50_CO4
        Course_Outcome_CO4['max_of_target'] = round(Max_of_Target_CO4 , 2)
        Course_Outcome_CO4['co_attained'] = CO_Attained_CO4
        Course_Outcome_CO4['percentage'] = round(Percentage_CO4 , 2)
        Course_Outcome_CO4['attainment_level'] = Attainment_Level_CO4
        Course_Outcome_Analysis.append(Course_Outcome_CO4)

        Course_Outcome_CO5 = {}
        Course_Outcome_CO5['alloted'] = Alloted_CO5
        Course_Outcome_CO5['attend'] = attend_CO5
        Course_Outcome_CO5['Maximum'] = maximum_total_50_CO5
        Course_Outcome_CO5['max_of_target'] = round(Max_of_Target_CO5 , 2)
        Course_Outcome_CO5['co_attained'] = CO_Attained_CO5
        Course_Outcome_CO5['percentage'] = round(Percentage_CO5 , 2)
        Course_Outcome_CO5['attainment_level'] = Attainment_Level_CO5
        Course_Outcome_Analysis.append(Course_Outcome_CO5)

       
        return Course_Outcome_Analysis
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

def table_seven(self,request,var):
    try:
        data = request.data
        get_allocated = College_Details.objects.filter(active = True)
        allocated_serialize = seatallocate_serializer(get_allocated,many = True)
        
        for allocated in allocated_serialize.data:
            seat_allocated = allocated['seat_allocated']
            
        data_question = retrieve_data(self,request)
        questions = data_question
        
        co_number = questions[0]
        question_no = questions[1]
        q1 = questions[2]
        q2 = questions[3]
        q3 = questions[4]
        q4 = questions[5]
        q5 = questions[6]
        q6a = questions[7]
        q6b = questions[8]
        q7a = questions[9]
        q7b = questions[10]
        q8a = questions[11]
        q8b = questions[12]
        
        add_question = q1 + q2 + q3 + q4 + q5 + q6a + q7a + q8a
        

        unit_serialize = mark_data(self,request,var)
      
        
        
        count_fullmark_CO1 = 0
        count_mediummark_CO1 = 0
        count_lowmark_CO1 = 0
        student_id_CO1 = 0
        total_attend_CO1 = 0

        count_fullmark_CO2 = 0
        count_mediummark_CO2 = 0
        count_lowmark_CO2 = 0
        student_id_CO2 = 0
        total_attend_CO2 = 0

        count_fullmark_CO3 = 0
        count_mediummark_CO3 = 0
        count_lowmark_CO3 = 0
        student_id_CO3 = 0
        total_attend_CO3 = 0

        count_fullmark_CO4 = 0
        count_mediummark_CO4 = 0
        count_lowmark_CO4 = 0
        student_id_CO4 = 0
        total_attend_CO4 = 0

        count_fullmark_CO5 = 0
        count_mediummark_CO5 = 0
        count_lowmark_CO5 = 0
        student_id_CO5 = 0
        total_attend_CO5 = 0

        count_mark = 0
        
        Secured_Mark = []

        
        absent_data = table_three(self,request,var)
        for student in unit_serialize.data:
            stud = student['student_id']['register_number']
            question1 = student['question'].keys()

            for key in question1:
                co1_key = key    

                for pattern in question_no:
                    co1 = pattern + 'CO1'

                if co1_key == co1 :
                    question_CO1 = student['question'].values()
                    total_50_CO1 = sum(question_CO1)
                    
                    total_alloted =  add_question

                    count_mark += total_50_CO1
                    
                    if total_50_CO1 == total_alloted:
                        fullmark_CO1 = 1
                    else:
                        fullmark_CO1 = 0
                    if total_50_CO1 >= (total_alloted / 2):
                        mediummark_CO1 = 1
                    else:
                        mediummark_CO1 = 0
                    if total_50_CO1 < (total_alloted / 2):
                        lowmark_CO1 = 1
                    else:
                        lowmark_CO1 = 0

                    count_fullmark_CO1 += fullmark_CO1
                    count_mediummark_CO1 += mediummark_CO1
                    count_lowmark_CO1 += lowmark_CO1

                    if stud:
                        student_id_CO1 += 1

                    if total_50_CO1:
                        total_attend_CO1 +=1

            total_fullmark = count_fullmark_CO1
            total_mediummark = count_mediummark_CO1 - count_fullmark_CO1

            total_seat = seat_allocated - student_id_CO1

            for absent in absent_data:
                total_absent_CO1 = absent['student_absent']
            if total_attend_CO1 == 0:
                total_absent_CO1 = 0
            else:
                total_absent_CO1

            Secured_Zero_CO1 = seat_allocated - total_attend_CO1 -  total_seat - total_absent_CO1
            
            total_lowmark_CO1 = count_lowmark_CO1 - Secured_Zero_CO1 - total_absent_CO1


                #  <-----CO2------>

            for key in question1:
                co2_key = key    

                for pattern in question_no:
                    co2 = pattern + 'CO2'

                if co2_key == co2 :
                    question_CO2 = student['question'].values()
                    total_50_CO2 = sum(question_CO2)
                    
                    total_alloted =  add_question

                    count_mark += total_50_CO2
                    
                    if total_50_CO2 == total_alloted:
                        fullmark_CO2 = 1
                    else:
                        fullmark_CO2 = 0
                    if total_50_CO2 >= (total_alloted / 2):
                        mediummark_CO2 = 1
                    else:
                        mediummark_CO2 = 0
                    if total_50_CO2 < (total_alloted / 2):
                        lowmark_CO2 = 1
                    else:
                        lowmark_CO2 = 0

                    count_fullmark_CO2 += fullmark_CO2
                    count_mediummark_CO2 += mediummark_CO2
                    count_lowmark_CO2 += lowmark_CO2

                    if stud:
                        student_id_CO2 += 1

                    if total_50_CO2:
                        total_attend_CO2 +=1

            total_fullmark_CO2 = count_fullmark_CO2
            total_mediummark_CO2 = count_mediummark_CO2 - count_fullmark_CO2

            total_seat = seat_allocated - student_id_CO2

            for absent in absent_data:
                total_absent_CO2 = absent['student_absent']

            if total_attend_CO2 == 0:
                total_absent_CO2 = 0
            else:
                total_absent_CO2
                
            Secured_Zero_CO2 = seat_allocated - total_attend_CO2 -  total_seat - total_absent_CO2

            total_lowmark_CO2 = count_lowmark_CO2 - Secured_Zero_CO2 - total_absent_CO2


                        #  <-----CO3------>

            for key in question1:
                co3_key = key    

                for pattern in question_no:
                    co3 = pattern + 'CO3'

                if co3_key == co3 :
                    question_CO3 = student['question'].values()
                    total_50_CO3 = sum(question_CO3)
                    
                    total_alloted =  add_question

                    count_mark += total_50_CO3
                    
                    if total_50_CO3 == total_alloted:
                        fullmark_CO3 = 1
                    else:
                        fullmark_CO3 = 0
                    if total_50_CO3 >= (total_alloted / 2):
                        mediummark_CO3 = 1
                    else:
                        mediummark_CO3 = 0
                    if total_50_CO3 < (total_alloted / 2):
                        lowmark_CO3 = 1
                    else:
                        lowmark_CO3 = 0

                    count_fullmark_CO3 += fullmark_CO3
                    count_mediummark_CO3 += mediummark_CO3
                    count_lowmark_CO3 += lowmark_CO3

                    if stud:
                        student_id_CO3 += 1

                    if total_50_CO3:
                        total_attend_CO3 +=1

            total_fullmark_CO3 = count_fullmark_CO3
            total_mediummark_CO3 = count_mediummark_CO3 - count_fullmark_CO3

            total_seat = seat_allocated - student_id_CO3

            for absent in absent_data:
                total_absent_CO3 = absent['student_absent']

            if total_attend_CO3 == 0:
                total_absent_CO3 = 0
            else:
                total_absent_CO3
                
            Secured_Zero_CO3 = seat_allocated - total_attend_CO3 -  total_seat - total_absent_CO3

            total_lowmark_CO3 = count_lowmark_CO3 - Secured_Zero_CO3 - total_absent_CO3
            
                        #  <-----CO4------>

            for key in question1:
                co4_key = key    

                for pattern in question_no:
                    co4 = pattern + 'CO4'

                if co4_key == co4 :
                    question_CO4 = student['question'].values()
                    total_50_CO4 = sum(question_CO4)
                    
                    total_alloted =  add_question

                    count_mark += total_50_CO4
                    
                    if total_50_CO4 == total_alloted:
                        fullmark_CO4 = 1
                    else:
                        fullmark_CO4 = 0
                    if total_50_CO4 >= (total_alloted / 2):
                        mediummark_CO4 = 1
                    else:
                        mediummark_CO4 = 0
                    if total_50_CO4 < (total_alloted / 2):
                        lowmark_CO4 = 1
                    else:
                        lowmark_CO4 = 0

                    count_fullmark_CO4 += fullmark_CO4
                    count_mediummark_CO4 += mediummark_CO4
                    count_lowmark_CO4 += lowmark_CO4

                    if stud:
                        student_id_CO4 += 1

                    if total_50_CO4:
                        total_attend_CO4 +=1


            total_fullmark_CO4 = count_fullmark_CO4
            total_mediummark_CO4 = count_mediummark_CO4 - count_fullmark_CO4

            total_seat = seat_allocated - student_id_CO4

            for absent in absent_data:
                total_absent_CO4 = absent['student_absent']

            if total_attend_CO4 == 0:
                total_absent_CO4 = 0
            else:
                total_absent_CO4
                
            Secured_Zero_CO4 = seat_allocated - total_attend_CO4 -  total_seat - total_absent_CO4
            
            total_lowmark_CO4 = count_lowmark_CO4 - Secured_Zero_CO4- total_absent_CO4

                        #  <-----CO5------>

            for key in question1:
                co5_key = key    

                for pattern in question_no:
                    co5 = pattern + 'CO5'

                if co5_key == co5 :
                    question_CO5 = student['question'].values()
                    total_50_CO5 = sum(question_CO5)
                    
                    total_alloted =  add_question

                    count_mark += total_50_CO5
                    
                    if total_50_CO5 == total_alloted:
                        fullmark_CO5 = 1
                    else:
                        fullmark_CO5 = 0
                    if total_50_CO5 >= (total_alloted / 2):
                        mediummark_CO5 = 1
                    else:
                        mediummark_CO5 = 0
                    if total_50_CO5 < (total_alloted / 2):
                        lowmark_CO5 = 1
                    else:
                        lowmark_CO5 = 0

                    count_fullmark_CO5 += fullmark_CO5
                    count_mediummark_CO5 += mediummark_CO5
                    count_lowmark_CO5 += lowmark_CO5

                    if stud:
                        student_id_CO5 += 1

                    if total_50_CO5:
                        total_attend_CO5 +=1

            total_fullmark_CO5 = count_fullmark_CO5
            total_mediummark_CO5 = count_mediummark_CO5 - count_fullmark_CO5

            total_seat = seat_allocated - student_id_CO5

            for absent in absent_data:
                total_absent_CO5 = absent['student_absent']

            if total_attend_CO5 == 0:
                total_absent_CO5 = 0
            else:
                total_absent_CO5
                
            Secured_Zero_CO5 = seat_allocated - total_attend_CO5 -  total_seat - total_absent_CO5

            
            total_lowmark_CO5 = count_lowmark_CO5 - Secured_Zero_CO5 - total_absent_CO5
        

        Secured_Mark_CO1 = {}
        Secured_Mark_CO1['Secured_FullMark'] = total_fullmark
        Secured_Mark_CO1['Secured_AverageMark'] = total_mediummark
        Secured_Mark_CO1['Secured_LowMark'] = total_lowmark_CO1
        Secured_Mark_CO1['Secured_Zero'] = Secured_Zero_CO1
        Secured_Mark.append(Secured_Mark_CO1)
        
        Secured_Mark_CO2 = {}
        Secured_Mark_CO2['Secured_FullMark'] = total_fullmark_CO2
        Secured_Mark_CO2['Secured_AverageMark'] = total_mediummark_CO2
        Secured_Mark_CO2['Secured_LowMark'] = total_lowmark_CO2
        Secured_Mark_CO2['Secured_Zero'] = Secured_Zero_CO2
        Secured_Mark.append(Secured_Mark_CO2)

        Secured_Mark_CO3 = {}
        Secured_Mark_CO3['Secured_FullMark'] = total_fullmark_CO3
        Secured_Mark_CO3['Secured_AverageMark'] = total_mediummark_CO3
        Secured_Mark_CO3['Secured_LowMark'] = total_lowmark_CO3
        Secured_Mark_CO3['Secured_Zero'] = Secured_Zero_CO3
        Secured_Mark.append(Secured_Mark_CO3)

        Secured_Mark_CO4 = {}
        Secured_Mark_CO4['Secured_FullMark'] = total_fullmark_CO4
        Secured_Mark_CO4['Secured_AverageMark'] = total_mediummark_CO4
        Secured_Mark_CO4['Secured_LowMark'] = total_lowmark_CO4
        Secured_Mark_CO4['Secured_Zero'] = Secured_Zero_CO4
        Secured_Mark.append(Secured_Mark_CO4)

        Secured_Mark_CO5 = {}
        Secured_Mark_CO5['Secured_FullMark'] = total_fullmark_CO5
        Secured_Mark_CO5['Secured_AverageMark'] = total_mediummark_CO5
        Secured_Mark_CO5['Secured_LowMark'] = total_lowmark_CO5
        Secured_Mark_CO5['Secured_Zero'] = Secured_Zero_CO5
        Secured_Mark.append(Secured_Mark_CO5)



        return Secured_Mark
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    
def table_eight(self,request,var):
    try:
        data = request.data
        attainment_get = Attainment.objects.filter(active = True).order_by(F("id").asc(nulls_last=True))
        attainment_serialize = attainment_serializer(attainment_get,many=True)
        po_pso_CO1 = []
        po_pso_CO2 = []
        po_pso_CO3 = []
        po_pso_CO4 = []
        po_pso_CO5 = []
        po_list = []
        pso_list = []

        attainment_value = []

        for attain in attainment_serialize.data:
            po = attain['po_details'].values()
            pso = attain['pso_details'].values()
            po_value = list(po)
            pso_value = list(pso)
            po_list.append(po_value)
            pso_list.append(pso_value)

        po_co1 = po_list[0]
        po_co2 = po_list[1]
        po_co3 = po_list[2]
        po_co4 = po_list[3]
        po_co5 = po_list[4]

        pso_co1 = pso_list[0]
        pso_co2 = pso_list[1]
        pso_co3 = pso_list[2]
        pso_co4 = pso_list[3]
        pso_co5 = pso_list[4]

        for po_value_CO1 in po_co1:
            if po_value_CO1 == "L":
                po_attain_Co1 = 1
            elif po_value_CO1 == "M":
                po_attain_Co1 = 2
            elif po_value_CO1 == "H":
                po_attain_Co1 = 3
            else:
                po_attain_Co1 = 0

            po_pso_CO1.append(po_attain_Co1)

        for po_value_CO2 in po_co2:
            
            if po_value_CO2 == "L":
                po_attain_Co2 = 1
            elif po_value_CO2 == "M":
                po_attain_Co2 = 2
            elif po_value_CO1 == "H":
                po_attain_Co2 = 3
            else:
                po_attain_Co2 = 0
        
            po_pso_CO2.append(po_attain_Co2)

        for po_value_CO3 in po_co3:
            
            if po_value_CO3 == "L":
                po_attain_Co3 = 1
            elif po_value_CO3 == "M":
                po_attain_Co3 = 2
            elif po_value_CO3 == "H":
                po_attain_Co3 = 3
            else:
                po_attain_Co3 = 0

            po_pso_CO3.append(po_attain_Co3)

        for po_value_CO4 in po_co4:
            
            if po_value_CO4 == "L":
                po_attain_Co4 = 1
            elif po_value_CO4 == "M":
                po_attain_Co4 = 2
            elif po_value_CO4 == "H":
                po_attain_Co4 = 3
            else:
                po_attain_Co4 = 0

            po_pso_CO4.append(po_attain_Co4)

        for po_value_CO5 in po_co5:
            
            if po_value_CO5 == "L":
                po_attain_Co5 = 1
            elif po_value_CO5 == "M":
                po_attain_Co5 = 2
            elif po_value_CO5 == "H":
                po_attain_Co5 = 3
            else:
                po_attain_Co5 = 0
        
            po_pso_CO5.append(po_attain_Co5)

        for pso_value_CO1 in pso_co1:
            if pso_value_CO1 == "L":
                pso_attain_CO1 = 1
            elif pso_value_CO1 == "M":
                pso_attain_CO1 = 2
            elif pso_value_CO1 == "H":
                pso_attain_CO1 = 3
            else:
                pso_attain_CO1 = 0

            po_pso_CO1.append(pso_attain_CO1)
        
        for pso_value_CO2 in pso_co2:
            if pso_value_CO2 == "L":
                pso_attain_CO2 = 1
            elif pso_value_CO2 == "M":
                pso_attain_CO2 = 2
            elif pso_value_CO2 == "H":
                pso_attain_CO2 = 3
            else:
                pso_attain_CO2 = 0

            po_pso_CO2.append(pso_attain_CO2)

        for pso_value_CO3 in pso_co3:
            if pso_value_CO3 == "L":
                pso_attain_CO3 = 1
            elif pso_value_CO3 == "M":
                pso_attain_CO3 = 2
            elif pso_value_CO3 == "H":
                pso_attain_CO3 = 3
            else:
                pso_attain_CO3 = 0

            po_pso_CO3.append(pso_attain_CO3)

        for pso_value_CO4 in pso_co4:
            if pso_value_CO4 == "L":
                pso_attain_CO4 = 1
            elif pso_value_CO4 == "M":
                pso_attain_CO4 = 2
            elif pso_value_CO4 == "H":
                pso_attain_CO4 = 3
            else:
                pso_attain_CO4 = 0

            po_pso_CO4.append(pso_attain_CO4)

        for pso_value_CO5 in pso_co5:
            if pso_value_CO5 == "L":
                pso_attain_CO5 = 1
            elif pso_value_CO5 == "M":
                pso_attain_CO5 = 2
            elif pso_value_CO5 == "H":
                pso_attain_CO5 = 3
            else:
                pso_attain_CO5 = 0
        
            po_pso_CO5.append(pso_attain_CO5)
        

        attainment_level = table_six(self,request,var)

        data = request.data
        unit_get = unit_details.objects.filter(active = True).order_by(F("id").asc(nulls_last=True))
        unit_serialize = units_serializer(unit_get,many=True)
        
        attain_list = []
        for attain_level in attainment_level:
            overall_attain = attain_level['attainment_level']
            attain_list.append(overall_attain)

        attainment_CO1 = attain_list[0]
        attainment_CO2 = attain_list[1]
        attainment_CO3 = attain_list[2]
        attainment_CO4 = attain_list[3]
        attainment_CO5 = attain_list[4]

        for unit in unit_serialize.data:
            unit_1 = unit['unit_one']
            unit_2 = unit['unit_two']
            unit_3 = unit['unit_three']
            unit_4 = unit['unit_four']
            unit_5 = unit['unit_five']
            if unit_1 !=0:
                unit_CO1 = unit_1
            elif unit_2 !=0:
                unit_CO2 = unit_2
            elif unit_3 !=0:
                unit_CO3 = unit_3
            elif unit_4 !=0:
                unit_CO4 = unit_4
            elif unit_5 !=0:
                unit_CO5 = unit_5
        
        attain_CO1_list =  []
        for CO1_data in po_pso_CO1:
            add_CO1 = (CO1_data * attainment_CO1) / 3
            attain_valueCO1 = (add_CO1 * unit_CO1) / 100
            attain_CO1 = round(attain_valueCO1,2)
            attain_CO1_list.append(attain_CO1)

        attain_CO2_list =  []   
        for CO2_data in po_pso_CO2:
            add_CO2 = (CO2_data * attainment_CO2) / 3
            attain_valueCO2 = (add_CO2 * unit_CO2) / 100
            attain_CO2 = round(attain_valueCO2,2)
            attain_CO2_list.append(attain_CO2)

        attain_CO3_list =  []  
        for CO3_data in po_pso_CO3:
            add_CO3 = (CO3_data * attainment_CO3) / 3
            attain_valueCO3 = (add_CO3 * unit_CO3) / 100
            attain_CO3 = round(attain_valueCO3,2)
            attain_CO3_list.append(attain_CO3)

        attain_CO4_list =  [] 
        for CO4_data in po_pso_CO4:
            add_CO4 = (CO4_data * attainment_CO4) / 3
            attain_valueCO4 = (add_CO4 * unit_CO4) / 100  
            attain_CO4 = round(attain_valueCO4,2)
            attain_CO4_list.append(attain_CO4) 

        attain_CO5_list =  [] 
       
        for CO5_data in po_pso_CO5:
            add_CO5 = (CO5_data * attainment_CO5) / 3
            attain_valueCO5 = (add_CO5 * unit_CO5) / 100
            attain_CO5 = round(attain_valueCO5,2)
            attain_CO5_list.append(attain_CO5)
        
        
        attainment_val = {}
  
        attainment_val['CO1_value'] = po_pso_CO1
        attainment_val['CO2_value'] = po_pso_CO2
        attainment_val['CO3_value'] = po_pso_CO3
        attainment_val['CO4_value'] = po_pso_CO4
        attainment_val['CO5_value'] = po_pso_CO5

        attainment_score = {}
        attainment_score['CO1'] = attain_CO1_list
        attainment_score['CO2'] = attain_CO2_list
        attainment_score['CO3'] = attain_CO3_list
        attainment_score['CO4'] = attain_CO4_list
        attainment_score['CO5'] = attain_CO5_list
             
        attainment_value.append(attainment_score)
        attainment_value.append(attainment_val)

        

        return attainment_value
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

def table_nine(self,request,var):

    try:

        mark_detail = table_one(self,request,var)
        unit = mark_detail['mark_details']
        id_value = [value['total(100)'] for value in unit]

        total_90 = 0 
        total_80 = 0 
        total_70 = 0 
        total_60 = 0 
        total_50 = 0 
        total_40 = 0 
        total_30 = 0 
        total_20 = 0 
        total_10 = 0 
        total_10less = 0

        total_mak_list = []

        for total in id_value:
            if total >= 90:
                total_90 += 1 
            elif total >= 80:
                total_80 += 1
            elif total >= 70:
                total_70 += 1
            elif total >= 60:
                total_60 += 1
            elif total >= 50:
                total_50 += 1
            elif total >= 40:
                total_40 += 1
            elif total >= 30:
                total_30 += 1
            elif total >= 20:
                total_20 += 1
            elif total >= 10:
                total_10 += 1
            elif total < 10 and total != 0:
                total_10less += 1
  
        total_attend = total_90 + total_80 + total_70 + total_60 + total_50 + total_40 + total_30 + total_20 + total_10 + total_10less

        total_mark_100 = {}
        total_mark_100['total_90'] = total_90
        total_mark_100['total_80'] = total_80
        total_mark_100['total_70'] = total_70
        total_mark_100['total_60'] = total_60
        total_mark_100['total_50'] = total_50
        total_mark_100['total_40'] = total_40
        total_mark_100['total_30'] = total_30
        total_mark_100['total_20'] = total_20
        total_mark_100['total_10'] = total_10
        total_mark_100['total_1'] = total_10less
        total_mark_100['total_attend'] = total_attend
        total_mak_list.append(total_mark_100)



        return total_mak_list
    
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

class Report_Mark(APIView):
   
    def get(self,request):
            try:
                data = request.data
                unit = data['unit']
                score_details = {}
                student_marks = {}
                Course_Outcome_Analysis = {}
                Secured_Value = {}
                attainment_details = {}

                attainment = {}
                attainment_data = {}
                report_mark = []
                
                if isinstance(unit, int):
                    
                    value = mark_data(self,request,unit)

                    marks = table_one(self,request,unit)
                    report_mark.append(marks)

                    subject_data = table_two(self,request)
                    report_mark.append(subject_data)
                    
                    score_details['totalscore_details'] = table_three(self,request,unit)
                    report_mark.append(score_details)

                    tablefour_data = table_four(self,request,unit)
                    report_mark.append(tablefour_data)

                    student_marks['student_marks'] = table_nine(self,request,unit)
                    report_mark.append(student_marks)

                    tablefive_data = table_five(self,request,unit)
                    report_mark.append(tablefive_data)

                    Course_Outcome_Analysis['Course_Outcome_Analysis'] = table_six(self,request,unit)
                    report_mark.append(Course_Outcome_Analysis)

                    Secured_Value['Secured_All_Mark'] = table_seven(self,request,unit)
                    report_mark.append(Secured_Value)

                    attainment_details['attainment_deails'] = table_eight(self,request,unit)
                    report_mark.append(attainment_details)

                elif isinstance(unit, list):

                    for data in unit:
                        value = mark_data(self,request,data)
                        score_details['totalscore_details_'+str(data)] = table_three(self,request,data)
                        student_marks['student_marks_'+str(data)] = table_nine(self,request,data)
                        
                        Course_Outcome_Analysis['Course_Outcome_Analysis_'+str(data)] = table_six(self,request,data)
                        merged_data = defaultdict(list)
                        for course, analysis in Course_Outcome_Analysis.items():
                            merged_dict = defaultdict(int)
                            for item in analysis:
                                for key, value in item.items():
                                    merged_dict[key] += value
                            merged_data[course].append(merged_dict)

                        Secured_Value['Secured_All_Mark_'+str(data)] = table_seven(self,request,data)
                        Secured_data = defaultdict(list)
                        for Secured, analysis in Secured_Value.items():
                            Secured_dict = defaultdict(int)
                            for item in analysis:
                                for key, value in item.items():
                                    Secured_dict[key] += value
                            Secured_data[Secured].append(Secured_dict)
                        attainment_details['attainment_details_'+str(data)] = table_eight(self,request,data)

                        attain_list = []
                        attain = attainment_details['attainment_details_'+str(data)]
                        attai_val = attain[0]
                        attain_list.append(attai_val)
                        attainment['attainment_'+str(data)] = attain_list
                    attaiment_val = attain[1]
                    attainment_data['attaiment_value'] = attaiment_val

                    for att_key in attainment.keys(): 
                        for item in attainment[att_key]:
                            for co_key, values in item.items():
                                if co_key not in attainment_data:
                                    attainment_data[co_key] = values
                                    
                                else:
                                    attainment_data[co_key] = [sum(x) for x in zip(attainment_data[co_key], values)]

                    report_mark.append(score_details)
                    report_mark.append(student_marks)
                    report_mark.append(merged_data)
                    report_mark.append(Secured_data)
                    report_mark.append(attainment_data)
    
                return Response(report_mark,status=status.HTTP_200_OK)
                  
            except Exception:
                  return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)


def CO_Marks(self,request):

    try:
        data = request.data
        users = request.user.email
        user_email = user.objects.filter(email = users).values('department')
        user_depart = user_email[0]['department']
        mark = CO_Data.objects.filter(student_id__course_details__department = user_depart ,active = True)
        CO_serlialize = CO_serializer(mark ,many = True)

        return CO_serlialize.data
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)



def CO_table_one(self,request):

    try:
        mark = CO_Marks(self,request)

        Au_Value = []
        Au_finalResult = {}
        for au_value in mark:

            au_result = au_value['au_results']
    
            if au_result == 'E':
                Au_Results = 5
            elif au_result == 'D':
                Au_Results = 6
            elif au_result == 'C':
                Au_Results = 7
            elif au_result == 'B':
                Au_Results = 8
            elif au_result == 'A':
                Au_Results = 9
            elif au_result == 'S':
                Au_Results = 10
            else:
                Au_Results = 0
        
            au_value['Au_values'] = Au_Results
            Au_Value.append(au_value)
            Au_finalResult['Au_Results'] = Au_Value

        return Au_finalResult

    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

def CO_table_two(self,request):
    try:
        mark = CO_table_one(self,request)
        table_one = mark['Au_Results']
        result_count = 0
        count_one = 0
        count_two = 0
        count_three = 0
        count_four = 0
        count_five = 0
        count_value = 0

        result_pass = 0
        pass_Assignment1 = 0
        pass_Assignment2 = 0
        pass_Assignment3 = 0
        pass_Assignment4 = 0
        pass_Assignment5 = 0
        count_pass = 0

        result_fail = 0
        count_fail = 0

        result_absent = 0
        absent_Assignment1 = 0
        absent_Assignment2 = 0
        absent_Assignment3 = 0
        absent_Assignment4 = 0
        absent_Assignment5 = 0
        au_absent = 0

        Students_Attended = []
        Total_StudentAttended = {}

        for attend in table_one:
            au_result = attend['au_results']
            Assignment_1 = attend['Assignment_1']
            Assignment_2 = attend['Assignment_1']
            Assignment_3 = attend['Assignment_1']
            Assignment_4 = attend['Assignment_1']
            Assignment_5 = attend['Assignment_1']
            Au_values = attend['Au_values']

            if au_result or au_result == 0:
                result_count += 1
            if Assignment_1 or Assignment_1 == 0:
                count_one += 1
            if Assignment_2 or Assignment_2 == 0:
                count_two += 1
            if Assignment_3 or Assignment_3 == 0:
                count_three += 1
            if Assignment_4 or Assignment_4 == 0:
                count_four += 1
            if Assignment_5 or Assignment_5 == 0:
                count_five += 1
            if Au_values or Au_values == 0:
                count_value += 1

            if au_result != 'U':
                result_pass += 1
            if Assignment_1 >= 50:
                pass_Assignment1 += 1
            if Assignment_2 >= 50:
                pass_Assignment2 += 1
            if Assignment_3 >= 50:
                pass_Assignment3 += 1
            if Assignment_4 >= 50:
                pass_Assignment4 += 1
            if Assignment_5 >= 50:
                pass_Assignment5 += 1
            if Au_values != 0:
                count_pass += 1

            if au_result == 'U':
                result_fail += 1

            if Au_values == 0:
                count_fail += 1


            if au_result == 'AB':
                result_absent += 1
            if Assignment_1 == 'AB':
                absent_Assignment1 += 1
            if Assignment_2 == 'AB':
                absent_Assignment2 += 1
            if Assignment_3 == 'AB':
                absent_Assignment3 += 1
            if Assignment_4 == 'AB':
                absent_Assignment4 += 1
            if Assignment_5 == 'AB':
                absent_Assignment5 += 1
            if Au_values == 'AB':
                au_absent += 1

            TotalAttended_au_result = result_count - result_absent
            TotalAttended_Assignment1 = count_one - absent_Assignment1
            TotalAttended_Assignment2 = count_two - absent_Assignment2
            TotalAttended_Assignment3 = count_three - absent_Assignment3
            TotalAttended_Assignment4 = count_four - absent_Assignment4
            TotalAttended_Assignment5 = count_five - absent_Assignment5
            TotalAttended_Auvalues = count_value - au_absent

            Fail_Assignment1 = count_one - pass_Assignment1
            Fail_Assignment2 = count_two - pass_Assignment2
            Fail_Assignment3 = count_three - pass_Assignment3
            Fail_Assignment4 = count_four - pass_Assignment4
            Fail_Assignment5 = count_four - pass_Assignment5


        Percentage_Result = (result_pass / result_count) * 100 
        Percentage_Assignment1  = (pass_Assignment1 / count_one) * 100 
        Percentage_Assignment2  = (pass_Assignment2 / count_two) * 100 
        Percentage_Assignment3  = (pass_Assignment3 / count_three) * 100 
        Percentage_Assignment4  = (pass_Assignment4 / count_four) * 100 
        Percentage_Assignment5  = (pass_Assignment5 / count_five) * 100 
        Percentage_marks  = (count_pass / count_value) * 100 
        

            
        No_Students_Attended = {}
        No_Students_Attended['au_result'] = result_count
        No_Students_Attended['count_one'] = count_one
        No_Students_Attended['count_two'] = count_two
        No_Students_Attended['count_three'] = count_three
        No_Students_Attended['count_four'] = count_four
        No_Students_Attended['count_five'] = count_five
        No_Students_Attended['au_marks'] = count_value
        Students_Attended.append(No_Students_Attended)

        Students_pass ={}
        Students_pass['result_pass'] = result_pass
        Students_pass['pass_Assignment1'] = pass_Assignment1
        Students_pass['pass_Assignment2'] = pass_Assignment2
        Students_pass['pass_Assignment3'] = pass_Assignment3
        Students_pass['pass_Assignment4'] = pass_Assignment4
        Students_pass['pass_Assignment5'] = pass_Assignment5
        Students_pass['au_pass'] = count_pass
        Students_Attended.append(Students_pass)

        Students_fail ={}
        Students_fail['result_fail'] = result_fail
        Students_fail['fail_Assignment1'] = Fail_Assignment1
        Students_fail['fail_Assignment2'] = Fail_Assignment2
        Students_fail['fail_Assignment3'] = Fail_Assignment3
        Students_fail['fail_Assignment4'] = Fail_Assignment4
        Students_fail['fail_Assignment5'] = Fail_Assignment5
        Students_fail['au_fail'] = count_fail
        Students_Attended.append(Students_fail)

        Percentage ={}
        Percentage['Percentage_Result'] = round(Percentage_Result , 2 )
        Percentage['Percentage_Assignment1'] = round(Percentage_Assignment1 , 2)
        Percentage['Percentage_Assignment2'] = round(Percentage_Assignment2 , 2)
        Percentage['Percentage_Assignment3'] = round(Percentage_Assignment3 , 2)
        Percentage['Percentage_Assignment4'] = round(Percentage_Assignment4 , 2)
        Percentage['Percentage_Assignment5'] = round(Percentage_Assignment5 , 2)
        Percentage['Percentage_marks'] = round(Percentage_marks , 2)
        Students_Attended.append(Percentage)

        Students_absent ={}
        Students_absent['result_absent'] = result_absent
        Students_absent['absent_Assignment1'] = absent_Assignment1
        Students_absent['absent_Assignment2'] = absent_Assignment2
        Students_absent['absent_Assignment3'] = absent_Assignment3
        Students_absent['absent_Assignment4'] = absent_Assignment4
        Students_absent['absent_Assignment5'] = absent_Assignment5
        Students_absent['au_absent'] = au_absent
        Students_Attended.append(Students_absent)

        Total_Attended ={}
        Total_Attended['result_TotalAttended'] = TotalAttended_au_result
        Total_Attended['Total_Attended_Assignment1'] = TotalAttended_Assignment1
        Total_Attended['Total_Attended_Assignment2'] = TotalAttended_Assignment2
        Total_Attended['Total_Attended_Assignment3'] = TotalAttended_Assignment3
        Total_Attended['Total_Attended_Assignment4'] = TotalAttended_Assignment4
        Total_Attended['Total_Attended_Assignment5'] = TotalAttended_Assignment5
        Total_Attended['au_Total_Attended'] = TotalAttended_Auvalues
        Students_Attended.append(Total_Attended)

        Total_StudentAttended['Total_StudentAttended'] = Students_Attended
        

        return Total_StudentAttended

    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

def CO_table_three(self,request):
    try:

        data = request.data
        get_target = target_value.objects.filter(active = True)
        target_serialize = Target_serializer(get_target,many  = True)
        for target in target_serialize.data:
            target_grade_value = target['grade_target_value']
            if target_grade_value != '0' :
               target_grade = target_grade_value
            

        mark_data = CO_table_one(self,request)
        table_one = mark_data['Au_Results']

        total_tagetvalue = 0
        count_tagetvalue = 0
        total_GPA = []
        Final_GPA = {}
        for tar_value in table_one:
            target_val = tar_value['Au_values']
            if target_val:
                total_tagetvalue += target_val
                
            if target_val or target_val == 0 :
                count_tagetvalue += 1
                
        GPA_Value = total_tagetvalue / count_tagetvalue

        GPA_grade ={}
        GPA_grade['target_value'] = target_grade
        GPA_grade['Total_Attended_Assignment1'] = round(GPA_Value , 2 )
        total_GPA.append(GPA_grade)
        Final_GPA['Final_GPA'] = total_GPA
        return Final_GPA
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

def CO_table_four(self,request):
    try:
        data = request.data
        get_target = target_value.objects.filter(active = True)
        target_serialize = Target_serializer(get_target,many  = True)
        target_list = []
        target_details = {}
        for target in target_serialize.data:
            target_mark = target['target_mark']
            target_list.append(target_mark)
            
            target_grade_value = target['grade_target_value']
            if target_grade_value != '0' :
                target_grade = target_grade_value
                if target_grade == 'E':
                   grade = 5
                elif target_grade == 'D':
                   grade = 6
                elif target_grade == 'C':
                   grade = 7
                elif target_grade == 'B':
                   grade = 8
                elif target_grade == 'A':
                   grade = 9
                elif target_grade == 'S':
                   grade = 10
                else:
                    grade = 0

        target_mark1 = target_list[0]
        target_mark2 = target_list[1]
        target_mark3 = target_list[2]
        target_mark4 = target_list[3]
        target_mark5 = target_list[4]

        mark_data = CO_table_one(self,request)
        table_one = mark_data['Au_Results']

        student_taget_value = []
        max_one = []
        max_two = []
        max_three = []
        max_four = []
        max_five = []

        count_value = 0
        count_Assignment_1 = 0
        count_Assignment_2 = 0
        count_Assignment_3 = 0
        count_Assignment_4 = 0
        count_Assignment_5 = 0

        for mark in table_one:
            Assignment_1 = mark['Assignment_1']
            Assignment_2 = mark['Assignment_2']
            Assignment_3 = mark['Assignment_3']
            Assignment_4 = mark['Assignment_4']
            Assignment_5 = mark['Assignment_5']
            Au_values = mark['Au_values']
            if Au_values >= grade:
                count_value += 1
            if str(Assignment_1) <= str(target_mark1):
                count_Assignment_1 += 1
            if str(Assignment_2) <= str(target_mark2):
                count_Assignment_2 += 1
            if str(Assignment_3) <= str(target_mark3):
                count_Assignment_3 += 1
            if str(Assignment_4) <= str(target_mark4):
                count_Assignment_4 += 1
            if str(Assignment_5) <= str(target_mark5):
                count_Assignment_5 += 1

            max_one.append(Assignment_1) 
            max_two.append(Assignment_2) 
            max_three.append(Assignment_3) 
            max_four.append(Assignment_4) 
            max_five.append(Assignment_5) 
            
        max_Assignment_1 = max(max_one)
        max_Assignment_2 = max(max_two)
        max_Assignment_3 = max(max_three)
        max_Assignment_4 = max(max_four)
        max_Assignment_5 = max(max_five)

        max_Assignment ={}
        max_Assignment['max_Assignment_1'] = max_Assignment_1
        max_Assignment['max_Assignment_2'] = max_Assignment_2
        max_Assignment['max_Assignment_3'] = max_Assignment_3
        max_Assignment['max_Assignment_4'] = max_Assignment_4
        max_Assignment['max_Assignment_5'] = max_Assignment_5
        student_taget_value.append(max_Assignment)

        target_mark_value ={}
        target_mark_value['target_mark1'] = target_mark1
        target_mark_value['target_mark2'] = target_mark2
        target_mark_value['target_mark3'] = target_mark3
        target_mark_value['target_mark4'] = target_mark4
        target_mark_value['target_mark5'] = target_mark5
        student_taget_value.append(target_mark_value)

        count_Assignment ={}
        count_Assignment['count_value'] = count_value
        count_Assignment['count_Assignment1'] = count_Assignment_1
        count_Assignment['count_Assignment2'] = count_Assignment_2
        count_Assignment['count_Assignment3'] = count_Assignment_3
        count_Assignment['count_Assignment4'] = count_Assignment_4
        count_Assignment['count_Assignment5'] = count_Assignment_5
        student_taget_value.append(count_Assignment)

        target_details['target'] = student_taget_value

        return target_details
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)


def CO_table_five(self,request):

    try:

        Percentage_attain = []
        Percentage_attainment = {}
        mark = CO_table_two(self,request)
        table_two_value = mark['Total_StudentAttended']

        result_TotalAttended = table_two_value[-1]['result_TotalAttended']
        Total_Attended_Assignment1 = table_two_value[-1]['Total_Attended_Assignment1']
        Total_Attended_Assignment2 = table_two_value[-1]['Total_Attended_Assignment2']
        Total_Attended_Assignment3 = table_two_value[-1]['Total_Attended_Assignment3']
        Total_Attended_Assignment4 = table_two_value[-1]['Total_Attended_Assignment4']
        Total_Attended_Assignment5 = table_two_value[-1]['Total_Attended_Assignment5']

        target_mark = CO_table_four(self,request)
        table_four_value = target_mark['target']

        count_value = table_four_value[-1]['count_value']
        count_Assignment1 = table_four_value[-1]['count_Assignment1']
        count_Assignment2 = table_four_value[-1]['count_Assignment2']
        count_Assignment3 = table_four_value[-1]['count_Assignment3']
        count_Assignment4 = table_four_value[-1]['count_Assignment4']
        count_Assignment5 = table_four_value[-1]['count_Assignment5']

        Percentage_value = (count_value / result_TotalAttended) * 100
        Percentage_Assignment1 = (count_Assignment1 / Total_Attended_Assignment1) * 100
        Percentage_Assignment2 = (count_Assignment2 / Total_Attended_Assignment2) * 100
        Percentage_Assignment3 = (count_Assignment3 / Total_Attended_Assignment3) * 100
        Percentage_Assignment4 = (count_Assignment4 / Total_Attended_Assignment4) * 100
        Percentage_Assignment5 = (count_Assignment5 / Total_Attended_Assignment5) * 100

        if Percentage_value >= 80:
            value_level = 3
        elif Percentage_value >= 70:
            value_level = 2
        elif Percentage_value >= 60:
            value_level = 1
        else:
            value_level = 0

        if Percentage_Assignment1 >= 80:
            Assignment1_level = 3
        elif Percentage_Assignment1 >= 70:
            Assignment1_level = 2
        elif Percentage_Assignment1 >= 60:
            Assignment1_level = 1
        else:
            Assignment1_level = 0

        if Percentage_Assignment2 >= 80:
            Assignment2_level = 3
        elif Percentage_Assignment2 >= 70:
            Assignment2_level = 2
        elif Percentage_Assignment2 >= 60:
            Assignment2_level = 1
        else:
            Assignment2_level = 0

        if Percentage_Assignment3 >= 80:
            Assignment3_level = 3
        elif Percentage_Assignment3 >= 70:
            Assignment3_level = 2
        elif Percentage_Assignment3 >= 60:
            Assignment3_level = 1
        else:
            Assignment3_level = 0

        if Percentage_Assignment4 >= 80:
            Assignment4_level = 3
        elif Percentage_Assignment4 >= 70:
            Assignment4_level = 2
        elif Percentage_Assignment4 >= 60:
            Assignment4_level = 1
        else:
            Assignment4_level = 0

        if Percentage_Assignment5 >= 80:
            Assignment5_level = 3
        elif Percentage_Assignment5 >= 70:
            Assignment5_level = 2
        elif Percentage_Assignment5 >= 60:
            Assignment5_level = 1
        else:
            Assignment5_level = 0


        Percentage ={}
        Percentage['Percentage_value'] = round(Percentage_value , 2)
        Percentage['Percentage_Assignment1'] = round(Percentage_Assignment1 , 2 )
        Percentage['Percentage_Assignment2'] = round(Percentage_Assignment2 , 2 )
        Percentage['Percentage_Assignment3'] = round(Percentage_Assignment3 , 2 )
        Percentage['Percentage_Assignment4'] = round(Percentage_Assignment4 , 2 ) 
        Percentage['Percentage_Assignment5'] = round(Percentage_Assignment5 , 2 )
        Percentage_attain.append(Percentage)

        
        level ={}
        level['value_level'] = value_level
        level['Assignment1_level'] = Assignment1_level
        level['Assignment2_level'] = Assignment2_level
        level['Assignment3_level'] = Assignment3_level
        level['Assignment4_level'] = Assignment4_level
        level['Assignment5_level'] = Assignment5_level
        Percentage_attain.append(level)

        Percentage_attainment['Percentage_attainment'] = Percentage_attain
        return Percentage_attainment
    except Exception:
        return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)

class Co_Data(APIView):


    def get(self,request):

        try:
            Co_data = []

            mark_data = CO_table_one(self,request)
            Co_data.append(mark_data)

            student_attend = CO_table_two(self,request)
            Co_data.append(student_attend)

            target_value = CO_table_three(self,request)
            Co_data.append(target_value)

            target_mark = CO_table_four(self,request)
            Co_data.append(target_mark)

            Atainment = CO_table_five(self,request)
            Co_data.append(Atainment)
      
            return Response(Co_data,status=status.HTTP_200_OK)
                  
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        

def CO_Attainment_table_one(self,request):

    try:
     
        data = request.data
        assessment_get = assessment.objects.filter(active = True).order_by(F("co_name").asc(nulls_last=True))
        assessment_serialize = assessment_serializer(assessment_get,many=True)
        co_no = []
        co_name = []
        weight = []
        tool = []
        for assess in assessment_serialize.data:
            co_number = assess['co_name']['co_number']
            course_outcome = assess['co_name']['course_outcome']
            assessment_tools = assess['assessment_tools']
            assessment_weight = assess['assessment_weightages']
            co_no.append(co_number)
            co_name.append(course_outcome)
            weight.append(assessment_weight)
            tool.append(assessment_tools)

        first_view = Report_Mark()
        data_from_first = first_view.get(request)
        co = data_from_first.data[4]
        
        co1 = co['CO1']
        co2 = co['CO2']
        co3 = co['CO3']
        co4 = co['CO4']
        co5 = co['CO5']

        co_value = co['attaiment_value']
        value_co1 = co_value['CO1_value']
        value_co2 = co_value['CO2_value']
        value_co3 = co_value['CO3_value']
        value_co4 = co_value['CO4_value']
        value_co5 = co_value['CO5_value']

        Co_view = Co_Data()
        Co_mark = Co_view.get(request)
        Co_data = Co_mark.data[4]
        co_value = Co_data['Percentage_attainment'][1]
        high1 = co_value['Assignment1_level']
        high2 = co_value['Assignment2_level']
        high3 = co_value['Assignment3_level']
        high4 = co_value['Assignment4_level']
        high5 = co_value['Assignment5_level']

        medium1 = high1*(2/3)
        medium2 = high2*(2/3)
        medium3 = high3*(2/3)
        medium4 = high4*(2/3)
        medium5 = high5*(2/3)

        low1 = high1*(1/3)
        low2 = high2*(1/3)
        low3 = high3*(1/3)
        low4 = high4*(1/3)
        low5 = high5*(1/3)

        weight1 = weight[0]
        weight2 = weight[1]
        weight3 = weight[2]
        weight4 = weight[3]
        weight5 = weight[4]
  
        weight_high1 = (int(weight1)*high1) / 100
        weight_high2 = (int(weight2)*high2) / 100
        weight_high3 = (int(weight3)*high3) / 100
        weight_high4 = (int(weight4)*high4) / 100
        weight_high5 = (int(weight5)*high5) / 100

        weight_medium1 = (int(weight1)*medium1) / 100
        weight_medium2 = (int(weight2)*medium2) / 100
        weight_medium3 = (int(weight3)*medium3) / 100
        weight_medium4 = (int(weight4)*medium4) / 100
        weight_medium5 = (int(weight5)*medium5) / 100

        weight_low1 = (int(weight1)*low1) / 100
        weight_low2 = (int(weight2)*low2) / 100
        weight_low3 = (int(weight3)*low3) / 100
        weight_low4 = (int(weight4)*low4) / 100
        weight_low5 = (int(weight5)*low5) / 100

        tool1 = tool[0]
        tool2 = tool[1]
        tool3 = tool[2]
        tool4 = tool[3]
        tool5 = tool[4]

        unit_test1 = []
        unit_test2 = []
        unit_test3 = []
        unit_test4 = []
        unit_test5 = []

        for co_value1 in co1:
            unit_1 = co_value1 * (int(tool1) / 100)
            unit_test1.append(round(unit_1 , 2))
        for co_value2 in co2:
            unit_2 = co_value2 * (int(tool2) / 100)
            unit_test2.append(round(unit_2 , 2 ))
        for co_value3 in co3:
            unit_3 = co_value3 * (int(tool3) / 100)
            unit_test3.append(round(unit_3 , 2 ))
        for co_value4 in co4:
            unit_4 = co_value4 * (int(tool4) / 100)
            unit_test4.append(round(unit_4 , 2 ))
        for co_value5 in co5:
            unit_5 = co_value5 * (int(tool5) / 100)
            unit_test5.append(round(unit_5 , 2 ))


        Assignment_1 = []
        Assignment_2 = []
        Assignment_3 = []
        Assignment_4 = []
        Assignment_5 = []

        for attain_CO1 in value_co1:
            if attain_CO1 == high1:
                attain_weightCo1  = weight_high1
            elif attain_CO1 == medium1:
                attain_weightCo1  = weight_medium1
            elif attain_CO1 == low1:
                attain_weightCo1 = weight_low1
            else:
                attain_weightCo1 = 0
            Assignment_1.append(attain_weightCo1)

        for attain_CO2 in value_co2:
            if attain_CO2 == high2:
                attain_weightCo2  = weight_high2
            elif attain_CO2 == medium2:
                attain_weightCo2  = weight_medium2
            elif attain_CO2 == low2:
                attain_weightCo2 = weight_low2
            else:
                attain_weightCo2 = 0
            Assignment_2.append(attain_weightCo2)
                
        for attain_CO3 in value_co3:
            if attain_CO3 == high3:
                attain_weightCo3  = weight_high3
            elif attain_CO3 == medium3:
                attain_weightCo3  = weight_medium3
            elif attain_CO3 == low3:
                attain_weightCo3 = weight_low3
            else:
                attain_weightCo3 = 0
            Assignment_3.append(attain_weightCo3)

        for attain_CO4 in value_co4:
            if attain_CO4 == high4:
                attain_weightCo4  = weight_high4
            elif attain_CO4 == medium4:
                attain_weightCo4  = weight_medium4
            elif attain_CO4 == low4:
                attain_weightCo4 = weight_low4
            else:
                attain_weightCo4 = 0
            Assignment_4.append(attain_weightCo4)

        for attain_CO5 in value_co5:
            if attain_CO5 == high5:
                attain_weightCo5  = weight_high5
            elif attain_CO5 == medium5:
                attain_weightCo5  = weight_medium5
            elif attain_CO5 == low5:
                attain_weightCo5 = weight_low5
            else:
                attain_weightCo5 = 0
            Assignment_5.append(attain_weightCo5)


        CO1_Attainment = [x + y for x, y in zip(unit_test1, Assignment_1)]
        CO2_Attainment = [x + y for x, y in zip(unit_test2, Assignment_2)]
        CO3_Attainment = [x + y for x, y in zip(unit_test3, Assignment_3)]
        CO4_Attainment = [x + y for x, y in zip(unit_test4, Assignment_4)]
        CO5_Attainment = [x + y for x, y in zip(unit_test5, Assignment_5)]

        unit_val ={}
 
        unit1 = []
        Codata1 = {}
        Codata1['CO_Number'] = co_no[0]
        Codata1['course_outcome'] = co_name[0]
        unit1.append(Codata1)
        unit1_test = {}
        unit1_test['unit_test1'] = unit_test1
        unit1.append(unit1_test)
        Assignment1 = {}
        Assignment1['Assignment_1'] = Assignment_1
        unit1.append(Assignment1)
        Co_attaiment1 = {}
        Co_attaiment1['CO1_Attainment'] = CO1_Attainment
        unit1.append(Co_attaiment1)

        unit2 = []
        Codata2 = {}
        Codata2['CO_Number'] = co_no[1]
        Codata2['course_outcome'] = co_name[1]
        unit2.append(Codata2)
        unit2_test = {}
        unit2_test['unit_test2'] = unit_test2
        unit2.append(unit2_test)
        Assignment2 = {}
        Assignment2['Assignment_2'] = Assignment_2
        unit2.append(Assignment2)
        Co_attaiment2 = {}
        Co_attaiment2['CO2_Attainment'] = CO2_Attainment
        unit2.append(Co_attaiment2)

        unit3 = []
        Codata3 = {}
        Codata3['CO_Number'] = co_no[2]
        Codata3['course_outcome'] = co_name[2]
        unit3.append(Codata3)
        unit3_test = {}
        unit3_test['unit_test3'] = unit_test3
        unit3.append(unit3_test)
        Assignment3 = {}
        Assignment3['Assignment_3'] = Assignment_3
        unit3.append(Assignment3)
        Co_attaiment3 = {}
        Co_attaiment3['CO3_Attainment'] = CO3_Attainment
        unit3.append(Co_attaiment3)

        unit4 = []
        Codata4 = {}
        Codata4['CO_Number'] = co_no[3]
        Codata4['course_outcome'] = co_name[3]
        unit4.append(Codata4)
        unit4_test = {}
        unit4_test['unit_test4'] = unit_test4
        unit4.append(unit4_test)
        Assignment4 = {}
        Assignment4['Assignment_4'] = Assignment_4
        unit4.append(Assignment4)
        Co_attaiment4 = {}
        Co_attaiment4['CO4_Attainment'] = CO4_Attainment
        unit4.append(Co_attaiment4)

        unit5 = []
        Codata5 = {}
        Codata5['CO_Number'] = co_no[3]
        Codata5['course_outcome'] = co_name[3]
        unit5.append(Codata5)
        unit5_test = {}
        unit5_test['unit_test5'] = unit_test5
        unit5.append(unit5_test)
        Assignment5 = {}
        Assignment5['Assignment_5'] = Assignment_5
        unit5.append(Assignment5)
        Co_attaiment5 = {}
        Co_attaiment5['CO5_Attainment'] = CO5_Attainment
        unit5.append(Co_attaiment5)

        unit_val['Unit_1'] = unit1
        unit_val['Unit_2'] = unit2
        unit_val['Unit_3'] = unit3   
        unit_val['Unit_4'] = unit4
        unit_val['Unit_5'] = unit5

        return unit_val
                  
    except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)


def internal_table_two(self,request):
    try:
        subject = CO_Attainment_table_one(self,request)

        unit_val = {}

        co1_value = subject['Unit_1'][0]['CO_Number']
        co1_name = subject['Unit_1'][0]['course_outcome']
        CO1_Attainment = subject['Unit_1'][-1]['CO1_Attainment']

        unit1 = []
        Codata1 = {}
        Codata1['CO_Number'] = co1_value
        Codata1['course_outcome'] = co1_name
        unit1.append(Codata1)
        Co_attaiment1 = {}
        Co_attaiment1['CO1_Attainment'] = CO1_Attainment
        unit1.append(Co_attaiment1)

        co2_value = subject['Unit_2'][0]['CO_Number']
        co2_name = subject['Unit_2'][0]['course_outcome']
        CO2_Attainment = subject['Unit_2'][-1]['CO2_Attainment']

        unit2 = []
        Codata2 = {}
        Codata2['CO_Number'] = co2_value
        Codata2['course_outcome'] = co2_name
        unit2.append(Codata2)
        Co_attaiment2 = {}
        Co_attaiment2['CO2_Attainment'] = CO2_Attainment
        unit2.append(Co_attaiment2)

        co3_value = subject['Unit_3'][0]['CO_Number']
        co3_name = subject['Unit_3'][0]['course_outcome']
        CO3_Attainment = subject['Unit_3'][-1]['CO3_Attainment']

        unit3 = []
        Codata3 = {}
        Codata3['CO_Number'] = co3_value
        Codata3['course_outcome'] = co3_name
        unit3.append(Codata3)
        Co_attaiment3 = {}
        Co_attaiment3['CO3_Attainment'] = CO3_Attainment
        unit3.append(Co_attaiment3)

        co4_value = subject['Unit_4'][0]['CO_Number']
        co4_name = subject['Unit_4'][0]['course_outcome']
        CO4_Attainment = subject['Unit_4'][-1]['CO4_Attainment']

        unit4 = []
        Codata4 = {}
        Codata4['CO_Number'] = co4_value
        Codata4['course_outcome'] = co4_name
        unit4.append(Codata4)
        Co_attaiment4 = {}
        Co_attaiment4['CO4_Attainment'] = CO4_Attainment
        unit4.append(Co_attaiment4)

        co5_value = subject['Unit_5'][0]['CO_Number']
        co5_name = subject['Unit_5'][0]['course_outcome']
        CO5_Attainment = subject['Unit_5'][-1]['CO5_Attainment']
       
        unit5 = []
        Codata5 = {}
        Codata5['CO_Number'] = co5_value
        Codata5['course_outcome'] = co5_name
        unit5.append(Codata5)
        Co_attaiment5 = {}
        Co_attaiment5['CO5_Attainment'] = CO5_Attainment
        unit5.append(Co_attaiment5)

        internal = [(a + b + c + d + e) / 5 for a, b, c, d, e in zip(CO1_Attainment, CO2_Attainment, CO3_Attainment, CO4_Attainment, CO5_Attainment)]
      
        unit_val['internal_Unit_1'] = unit1
        unit_val['internal_Unit_2'] = unit2
        unit_val['internal_Unit_3'] = unit3   
        unit_val['internal_Unit_4'] = unit4
        unit_val['internal_Unit_5'] = unit5
        unit_val['internal_assesment'] = internal

        return unit_val
                  
    except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
    

def result_table_three(self,request):
    try:

        Co_view = Co_Data()
        Co_mark = Co_view.get(request)
        Co_data = Co_mark.data[4]
        co_value = Co_data['Percentage_attainment'][1]

        subject = CO_Attainment_table_one(self,request)

        unit_val = {}

        High = co_value['value_level']
        medium = High * (2/3)
        low = High * (1/3)
  
        first_view = Report_Mark()
        data_from_first = first_view.get(request)
        co = data_from_first.data[4]
        
        co_value = co['attaiment_value']
        value_co1 = co_value['CO1_value']
        value_co2 = co_value['CO2_value']
        value_co3 = co_value['CO3_value']
        value_co4 = co_value['CO4_value']
        value_co5 = co_value['CO5_value']

        result_CO1=[]
        for attain_CO1 in value_co1:
            if attain_CO1 == 3:
                attain_weightCo1  = High
            elif attain_CO1 == 2:
                attain_weightCo1  = medium
            elif attain_CO1 == 1:
                attain_weightCo1 = low
            else:
                attain_weightCo1 = 0
            result_CO1.append(round(attain_weightCo1 , 2 ))

        co1_value = subject['Unit_1'][0]['CO_Number']
        co1_name = subject['Unit_1'][0]['course_outcome']

        unit1 = []
        Codata1 = {}
        Codata1['CO_Number'] = co1_value
        Codata1['course_outcome'] = co1_name
        unit1.append(Codata1)
        Co_attaiment1 = {}
        Co_attaiment1['Result_CO1'] = result_CO1
        unit1.append(Co_attaiment1)

        result_CO2=[]
        for attain_CO2 in value_co2:
            if attain_CO2 == 3:
                attain_weightCo2  = High
            elif attain_CO2 == 2:
                attain_weightCo2  = medium
            elif attain_CO2 == 1:
                attain_weightCo2 = low
            else:
                attain_weightCo2 = 0
            result_CO2.append(round(attain_weightCo2 , 2))

        co2_value = subject['Unit_2'][0]['CO_Number']
        co2_name = subject['Unit_2'][0]['course_outcome']

        unit2 = []
        Codata2 = {}
        Codata2['CO_Number'] = co2_value
        Codata2['course_outcome'] = co2_name
        unit2.append(Codata2)
        Co_attaiment2 = {}
        Co_attaiment2['Result_CO2'] = result_CO2
        unit2.append(Co_attaiment2)


        result_CO3=[]
        for attain_CO3 in value_co3:
            if attain_CO3 == 3:
                attain_weightCo3  = High
            elif attain_CO3 == 2:
                attain_weightCo3  = medium
            elif attain_CO3 == 1:
                attain_weightCo3 = low
            else:
                attain_weightCo3 = 0
            result_CO3.append(round(attain_weightCo3 , 2))

        co3_value = subject['Unit_3'][0]['CO_Number']
        co3_name = subject['Unit_3'][0]['course_outcome']

        unit3 = []
        Codata3 = {}
        Codata3['CO_Number'] = co3_value
        Codata3['course_outcome'] = co3_name
        unit3.append(Codata3)
        Co_attaiment3 = {}
        Co_attaiment3['Result_CO3'] = result_CO3
        unit3.append(Co_attaiment3)

        result_CO4=[]
        for attain_CO4 in value_co4:
            if attain_CO4 == 3:
                attain_weightCo4  = High
            elif attain_CO4 == 2:
                attain_weightCo4  = medium
            elif attain_CO4 == 1:
                attain_weightCo4 = low
            else:
                attain_weightCo4 = 0
            result_CO4.append(round(attain_weightCo4 ,2))

        co4_value = subject['Unit_4'][0]['CO_Number']
        co4_name = subject['Unit_4'][0]['course_outcome']

        unit4 = []
        Codata4 = {}
        Codata4['CO_Number'] = co4_value
        Codata4['course_outcome'] = co4_name
        unit4.append(Codata4)
        Co_attaiment4 = {}
        Co_attaiment4['Result_CO1'] = result_CO4
        unit4.append(Co_attaiment4)

        result_CO5=[]
        for attain_CO5 in value_co5:
            if attain_CO5 == 3:
                attain_weightCo5  = High
            elif attain_CO5 == 2:
                attain_weightCo5  = medium
            elif attain_CO5 == 1:
                attain_weightCo5 = low
            else:
                attain_weightCo5 = 0
            result_CO5.append(round(attain_weightCo5 , 2))

        co5_value = subject['Unit_5'][0]['CO_Number']
        co5_name = subject['Unit_5'][0]['course_outcome']

        unit5 = []
        Codata5 = {}
        Codata5['CO_Number'] = co5_value
        Codata5['course_outcome'] = co5_name
        unit5.append(Codata5)
        Co_attaiment5 = {}
        Co_attaiment5['Result_CO5'] = result_CO5
        unit5.append(Co_attaiment5)
        
        result = [round((a + b + c + d + e) / 5 ,2 )for a, b, c, d, e in zip(result_CO1, result_CO2, result_CO3, result_CO4, result_CO5) ]

        unit_val['result_Unit_1'] = unit1
        unit_val['result_Unit_2'] = unit2
        unit_val['result_Unit_3'] = unit3   
        unit_val['result_Unit_4'] = unit4
        unit_val['result_Unit_5'] = unit5
        unit_val['result'] = result

        return unit_val
                  
    except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)




class CO_Attainment(APIView):


    def get(self,request):

        try:

            over_all = []
           
            subject = CO_Attainment_table_one(self,request)
            over_all.append(subject)

            internal = internal_table_two(self,request)
            over_all.append(internal)

            result = result_table_three(self,request)
            over_all.append(result)
            
            return Response(over_all,status=status.HTTP_200_OK)
                  
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)
        


def po_result_table_one(self,request):

    try:
        
        result = result_table_three(self,request)

        Result_value = 80
        internal_assessment = 20
        
        co1_value = result['result_Unit_1'][0]['CO_Number']
        co1_name = result['result_Unit_1'][0]['course_outcome']
        co1_result = result['result_Unit_1'][-1]['Result_CO1']

        multiplied_CO1 = [round(item * (Result_value / 100 ) , 2) for item in co1_result]

        co2_value = result['result_Unit_2'][0]['CO_Number']
        co2_name = result['result_Unit_2'][0]['course_outcome']
        co2_result = result['result_Unit_2'][-1]['Result_CO2']

        multiplied_CO2 = [round(item * (Result_value / 100 ) , 2) for item in co2_result]

        co3_value = result['result_Unit_3'][0]['CO_Number']
        co3_name = result['result_Unit_3'][0]['course_outcome']
        co3_result = result['result_Unit_3'][-1]['Result_CO3']

        multiplied_CO3 = [round(item * (Result_value / 100 ) , 2) for item in co3_result]

        co4_value = result['result_Unit_2'][0]['CO_Number']
        co4_name = result['result_Unit_2'][0]['course_outcome']
        co4_result = result['result_Unit_2'][-1]['Result_CO2']

        multiplied_CO4 = [round(item * (Result_value / 100 ) , 2) for item in co4_result]

        co5_value = result['result_Unit_5'][0]['CO_Number']
        co5_name = result['result_Unit_5'][0]['course_outcome']
        co5_result = result['result_Unit_5'][-1]['Result_CO5']

        multiplied_CO5 = [round(item * (Result_value / 100 ) , 2) for item in co5_result]

        internal = internal_table_two(self,request)

        co1_internal = internal['internal_Unit_1'][-1]['CO1_Attainment']
        internal_CO1 = [round(item * (internal_assessment / 100 ) , 2) for item in co1_internal]

        co2_internal = internal['internal_Unit_2'][-1]['CO2_Attainment']
        internal_CO2 = [round(item * (internal_assessment / 100 ) , 2) for item in co2_internal]

        co3_internal = internal['internal_Unit_3'][-1]['CO3_Attainment']
        internal_CO3 = [round(item * (internal_assessment / 100 ) , 2) for item in co3_internal]

        co4_internal = internal['internal_Unit_4'][-1]['CO4_Attainment']
        internal_CO4 = [round(item * (internal_assessment / 100 ) , 2) for item in co4_internal]

        co5_internal = internal['internal_Unit_5'][-1]['CO5_Attainment']
        internal_CO5 = [round(item * (internal_assessment / 100 ) , 2) for item in co5_internal]


        CO1_Assess = [round(x + y , 2) for x, y in zip(multiplied_CO1, internal_CO1)]
        CO2_Assess = [round(x + y , 2) for x, y in zip(multiplied_CO2, internal_CO2)]
        CO3_Assess = [round(x + y , 2) for x, y in zip(multiplied_CO3, internal_CO3)]
        CO4_Assess = [round(x + y , 2) for x, y in zip(multiplied_CO4, internal_CO4)]
        CO5_Assess = [round(x + y , 2) for x, y in zip(multiplied_CO5, internal_CO5)]


        unit_val ={}
 
        unit1 = []
        Codata1 = {}
        Codata1['CO_Number'] = co1_value
        Codata1['course_outcome'] = co1_name
        unit1.append(Codata1)
        unit1_test = {}
        unit1_test['Result_1'] = multiplied_CO1
        unit1.append(unit1_test)
        internal1 = {}
        internal1['internal_1'] = internal_CO1
        unit1.append(internal1)
        Co_assessment1 = {}
        Co_assessment1['CO1_assessment'] = CO1_Assess
        unit1.append(Co_assessment1)

        unit2 = []
        Codata2 = {}
        Codata2['CO_Number'] = co2_value
        Codata2['course_outcome'] = co2_name
        unit2.append(Codata2)
        unit2_test = {}
        unit2_test['Result_2'] = multiplied_CO2
        unit2.append(unit2_test)
        internal2 = {}
        internal2['internal_2'] = internal_CO2
        unit2.append(internal2)
        Co_assessment2 = {}
        Co_assessment2['CO2_assessment'] = CO2_Assess
        unit2.append(Co_assessment2)

        unit3 = []
        Codata3 = {}
        Codata3['CO_Number'] = co3_value
        Codata3['course_outcome'] = co3_name
        unit3.append(Codata3)
        unit3_test = {}
        unit3_test['Result_3'] = multiplied_CO3
        unit3.append(unit3_test)
        internal3 = {}
        internal3['internal_3'] = internal_CO3
        unit3.append(internal3)
        Co_assessment3 = {}
        Co_assessment3['CO3_assessment'] = CO3_Assess
        unit3.append(Co_assessment3)

        unit4 = []
        Codata4 = {}
        Codata4['CO_Number'] = co4_value
        Codata4['course_outcome'] = co4_name
        unit4.append(Codata4)
        unit4_test = {}
        unit4_test['Result_4'] = multiplied_CO4
        unit4.append(unit4_test)
        internal4 = {}
        internal4['internal_4'] = internal_CO4
        unit4.append(internal4)
        Co_assessment4 = {}
        Co_assessment4['CO4_assessment'] = CO4_Assess
        unit4.append(Co_assessment4)

        unit5 = []
        Codata5 = {}
        Codata5['CO_Number'] = co5_value
        Codata5['course_outcome'] = co5_name
        unit5.append(Codata5)
        unit5_test = {}
        unit5_test['Result_5'] = multiplied_CO5
        unit4.append(unit5_test)
        internal5 = {}
        internal5['internal_5'] = internal_CO5
        unit5.append(internal5)
        Co_assessment5 = {}
        Co_assessment5['CO5_assessment'] = CO5_Assess
        unit5.append(Co_assessment5)


        unit_val['Direct_Attainment_1'] = unit1
        unit_val['Direct_Attainment_2'] = unit2
        unit_val['Direct_Attainment_3'] = unit3   
        unit_val['Direct_Attainment_4'] = unit4
        unit_val['Direct_Attainment_5'] = unit5
      

        return unit_val
                  
    except Exception:
            return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)



        

class PO_Attainment(APIView):


    def get(self,request):

        try:
            po_attain = []

            subject = po_result_table_one(self,request)
            po_attain.append(subject)


            return Response(po_attain,status=status.HTTP_200_OK)
                  
        except Exception:
                return Response(traceback.format_exc(),status=status.HTTP_400_BAD_REQUEST)


            



