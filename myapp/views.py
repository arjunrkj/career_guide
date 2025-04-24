from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
import random
import os
from datetime import date as date, datetime as dt
from django.db.models import Q , F, Value ,Sum
from django.db.models.functions import Coalesce
from django.http import FileResponse, Http404
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,"index.html")



# def admin(request):
#     adm=Login.objects.create_user(username='admin',view_password='admin',password='admin',usertype="admin")
#     adm.save()
#     return redirect('/')



from myapp.models import Login


def login(request):
    if request.POST:
        name = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=name, password=password)

        if user is not None:
            # Optional: Log the user in (if using Django sessions)
            auth_login(request, user)

            if user.usertype == 'admin':
                messages.info(request, 'Welcome to admin page')
                return redirect('/adminpg')
            elif user.usertype == 'college':
                messages.info(request, 'Welcome to college page')
                request.session['Uid'] = user.id
                return redirect("/clgpg")
            elif user.usertype == 'student':
                messages.info(request, 'Welcome to student page')
                request.session['Uid'] = user.id
                return redirect("/stdpg")
            elif user.usertype == 'Financer':
                messages.info(request, 'Welcome to Financer page')
                request.session['Uid'] = user.id
                return redirect("/finpg")
            elif user.usertype == 'Mentor':
                messages.info(request, 'Welcome to Mentor page')
                request.session['Uid'] = user.id
                return redirect("/mentorpg")
            else:
                messages.info(request, "Invalid usertype")
        else:
            messages.info(request, "Invalid username or password")
    
    return render(request, 'login.html')



def clgreg(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        location=request.POST['location']
        phone=request.POST['phone']
        image = request.FILES["image"]
        if Login.objects.filter(email=email).exists():
            messages.info( request,"already register")
        else:
            clg=Login.objects.create_user(username=email,view_password=password,password=password,usertype="college",is_active=0)
            print(clg)
            clg.save()
            reg= College.objects.create(name=name, email=email,password=password,image=image,phone=phone,location=location,user=clg)
            print(reg)
            reg.save()
            return redirect('/login')

    return render(request,'college/clgreg.html')
# def studreg(request):
#     if request.POST:
#         name=request.POST['name']
#         email=request.POST['email']
#         password=request.POST['password']
#         location=request.POST['location']
#         phone=request.POST['phone']
#         qualification=request.POST['qualification']
#         image=request.FILES.get('image')
#         if Login.objects.filter(email=email).exists():
#             messages.info( request,"already register")
#         else:
#             stud=Login.objects.create_user(username=email,view_password=password,password=password,usertype="student",is_active=1)
#             stud.save()
#             reg= Student.objects.create(name=name, email=email,password=password,phone=phone,location=location,qualification=qualification,image=image,user=stud)
#             print(reg)
#             reg.save()
#             return redirect('/login')

#     return render(request,'student/studreg.html')
def studreg(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        location=request.POST['location']
        phone=request.POST['phone']
        qualification=request.POST['qualification']
        image = request.FILES["image"]
       

        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=1,
            usertype='student')
        log.save()
        reguser = Student.objects.create(
            user=log,
            name=name,
            qualification=qualification,
            email=email,
            phone=phone,
            location=location,
            image=image,)
        reguser.save()
        messages.success(request, "Registration Successful Wait For Approval")
        return redirect('/login')
    return render(request,'student/studreg.html')

def finReg(request):
    if request.POST:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        location=request.POST['location']
        phone=request.POST['phone']
        if Login.objects.filter(email=email).exists():
            messages.info( request,"already register")
        else:
            fin=Login.objects.create_user(username=email,view_password=password,password=password,usertype="Financer",is_active=1)
            fin.save()
            reg= Financer.objects.create(name=name, email=email,password=password,phone=phone,location=location,user=fin)
            print(reg)
            reg.save()
            return redirect('/login')

    return render(request,'financer/finReg.html')

#admin
def adminpg(request):
    return render(request,'admin/adminpg.html')

def admin_clg_view(request):
    data=College.objects.all()
    return render(request,'admin/admin_clg_view.html' ,{'data':data})

def admin_studview(request):
    data=Student.objects.all()
    return render(request,'admin/admin_studview.html',{'data':data})

def stud_Dlt(request):
    id=request.GET['id']
    clg=Student.objects.filter(id=id).delete()
    clg=Login.objects.filter(id=clg).delete()    
    return redirect('/admin_studview')

# def dltst(request):
#     lo=Login.objects.filter(id="16").delete()
#     lo=Student.objects.filter(id="9").delete()
#     return redirect('/')
def clgapprove(request):
    id=request.GET['id']
    clg=Login.objects.get(id=id)
    clg.is_active = True
    clg.save()
    return redirect('/admin_clg_view')

def clgreject(request):
    id=request.GET['id']
    clg=College.objects.filter(id=id).delete()
    clg=Login.objects.filter(id=id).delete()
    return redirect('/admin_clg_view')


def addquestions(request):
    global qlist, o1, o2, o3, o4, ansl
    msgcount = int(request.POST.get('msgcount', 1))
    if request.method == 'POST':
        qstn = request.POST['qstn']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        ans = request.POST['ans']
        qnaadd = Question.objects.create(question=qstn, option1=op1, option2=op2, option3=op3, option4=op4, answer=ans)
        qnaadd.save()
        messages.success(request, 'Added successfully')
        # try:
        #     messages.success(request, 'Items inserted successfully') 
        #     qlist = []
        #     o1 = []
        #     o2 = []
        #     o3 = []
        #     o4 = []
        #     ansl = []
        #     msgcount = 1
        #     return render(request, 'Admin/add.html', {"msgcount": msgcount})   
        # except:
        #     pass
        #     qlist.append(qstn)
        #     o1.append(op1)
        #     o2.append(op2)
        #     o3.append(op3)
        #     o4.append(op4)
        #     ansl.append(ans)
        #     msg = messages.success(request, f'Enter {msgcount} more to save')
        #     if msgcount == 0:
        #         for a, b, c, d, e, f in zip(qlist, o1, o2, o3, o4, ansl):
        #             qnanewadd = Question.objects.create(question=a, option1=b, option2=c, option3=d, option4=e, answer=f)
        #             qnanewadd.save()
        #         msgcount = 1
        #         messages.success(request, 'Added successfully')
        #         qlist = []
        #         o1 = []
        #         o2 = []
        #         o3 = []
        #         o4 = []
        #         ansl = []
        #         msgcount = 1
        #         return render(request, 'Admin/add.html', {"msgcount": msgcount})   
        #     msgcount -= 1
    return render(request, 'Admin/addquestions.html', {"msgcount": msgcount})





def add_JobDetail(request):
       
    if request.POST:
        name=request.POST['name']
        description=request.POST['description']
        company_name =request.POST['company_name ']
        location=request.POST['location']
        salary=request.POST['salary']
        eligibility_criteria=request.POST['eligibility_criteria']
        created_at=request.POST['created_at']
        application_deadline=request.POST['application_deadline']
        job=Jobs.objects.create(name=name,description=description,company_name= company_name ,location=location,salary=salary,eligibility_criteria=eligibility_criteria,created_at=created_at,application_deadline=application_deadline)
        job.save()
    return render(request,'admin/add_JobDetail.html')

def std_testresult(request):
    data=Answer.objects.all()
    return render(request,'admin/std_testresult.html',{'data':data})





#college 
      


def clgpg(request):
    return render(request,'college/clgpg.html')


def clgview(request):
    id=request.session['Uid']
    print(id,"ggg")
    data=College.objects.filter(user_id=id)
    return render(request,'college/clgview.html',{'data':data})


def studentView(request):
    return render(request,'admin/studentview.html')


def addMentor(request):
    uid = request.session['Uid']
    uid = College.objects.get(user_id=uid)
    if request.POST:
        name=request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        qualification = request.POST['qualification']
        password=request.POST['password']

        log = Login.objects.create_user(
            username=email,
            password=password,
            view_password=password,
            is_active=1,
            usertype='Mentor')
        log.save()

        Mentor.objects.create(
            user=log,
            clg=uid,
            name=name,
            email =email,
            phone=phone,
            location=location,
            qualification=qualification,
        )
        messages.success(request, 'Mentor addeded successfully')
        return redirect('/clgpg')
    return render(request,'college/addMentor.html')

# def addcourse(request):
#     uid=request.session['Uid']
#     print(uid,"kkkkkkkkk")
#     clg=College.objects.get(user_id=uid)
#     if request.POST:
#         name=request.POST['name']
#         duration=request.POST['duration']
#         fees=request.POST['fees']
#         details=request.POST['details']
#         gpa=request.POST['gpa']
#         course=Course.objects.create(name=name,duration=duration,fees=fees,details=details,gpa=gpa,clg=clg)
#         course.save()
#     return render(request,'college/addcourse.html')


def addcourse(request):
    uid = request.session['Uid']
    print(uid, "kkkkkkkkk")
    clg = College.objects.get(user_id=uid)
    mentors = Mentor.objects.filter(clg=clg)  # Fetch mentors associated with the college

    if request.POST:
        name = request.POST['name']
        duration = request.POST['duration']
        fees = request.POST['fees']
        details = request.POST['details']
        gpa = request.POST['gpa']
        mentor_id = request.POST['mentor'] 
        mentor = Mentor.objects.get(id=mentor_id)  

        course = Course.objects.create(
            name=name,
            duration=duration,
            fees=fees,
            details=details,
            gpa=gpa,
            clg=clg,
            mentor=mentor
        )
        course.save()

    return render(request, 'college/addcourse.html', {'mentors': mentors})

def delCourse(request):
    id=request.GET['id']
    data=Course.objects.filter(id=id).delete()
    return redirect('/course_view')


def course_view(request):
    uid = request.session['Uid']
    college = College.objects.filter(user_id=uid).first()
    data = Course.objects.filter(clg=college)  
    return render(request, 'college/course_view.html', {'data': data})




def update(request):
    id = request.GET['id']
    course = Course.objects.get(id=id)  
    if request.method == "POST":
        course.name = request.POST['name']
        course.duration = request.POST['duration']
        course.fees = request.POST['fees']
        course.details = request.POST['details']
        course.gpa = request.POST['gpa']
        course.save()  
        return redirect("/clgview")
    return render(request, "college/update.html", {'ups': [course]})


# def collegeUpdate(request):
#     id=request.GET['id']
#     clg=College.objects.filter(id=id)
#     if request.POST:
#         name=request.POST['name']
#         location=request.POST['location']
#         phone=request.POST['phone']
#         ups=College.objects.filter(id=id).update(name=name,location=location,phone=phone)
        
#         return redirect("/clgview")    
#     return render(request,'college/collegeUpdate.html',{'ups':clg})
def collegeUpdate(request):
    uid = request.GET.get('uid')
    datas = College.objects.filter(user=uid)
    if request.method == 'POST':
        name = request.POST.get("name")
        phone  = request.POST.get("phone")
        location = request.POST.get("location")
        image = request.FILES.get("image")

        if 'image' in request.FILES:
            image = request.FILES.get('image')
            data = College.objects.get(user=uid)
            data.name = name
            data. phone =  phone 
            data.location= location
            data.image = image
            data.save()
        else:
            # If no new image is uploaded, update without changing the image
            Student.objects.filter(user=uid).update(name=name,phone=phone,location=location)

        messages.success(request, ' updated successfully')
        return redirect('/clgview')
    return render(request,"college/collegeUpdate.html",{'datas':datas})

def std_results(request):
    data=Answer.objects.all()
    return render(request,'college/std_results.html',{'data':data})



#student
def stdpg(request):
    return render(request,'student/stdpg.html')

def stud_clg_view(request):
    data=College.objects.all()
    return render(request,'student/stud_clg_view.html',{'data':data})



def student_Profile(request):
    uid=request.session['Uid']
    data=Student.objects.filter(user=uid)
    return render(request,'student/student_Profile.html',{'data':data})

def UpdateStud(request):
    uid = request.GET.get('uid')
    datas = Student.objects.filter(user=uid)
    if request.method == 'POST':
        name = request.POST.get("name")
        phone  = request.POST.get("phone")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")
        image = request.FILES.get("image")

        if 'image' in request.FILES:
            image = request.FILES.get('image')
            data = Student.objects.get(user=uid)
            data.name = name
            data. phone =  phone 
            data.location= location
            data.qualification=qualification
            data.image = image
            data.save()
        else:
            # If no new image is uploaded, update without changing the image
            Student.objects.filter(user=uid).update(name=name,phone=phone,location=location,qualification=qualification)

        messages.success(request, 'Profile updated successfully')
        return redirect('/student_Profile')

    return render(request,"student/UpdateStud.html",{'datas':datas})



# from django.shortcuts import get_object_or_404

# def UpdateStud(request):
#     uid = request.GET.get('uid')  # Fetch user ID from GET request
#     student = get_object_or_404(Student, user=uid)  # Ensure the student exists

#     if request.method == 'POST':
#         name = request.POST["name"]
#         phone = request.POST["phone"]
#         location = request.POST["location"]
#         qualification = request.POST["qualification"]

#         # Handle image upload
#         if 'image' in request.FILES:
#             image = request.FILES['image']
#             student.image = image  # Update the image field

#         # Update other fields
#         student.name = name
#         student.phone = phone
#         student.location = location
#         student.qualification = qualification
#         student.save()

#         # Add success message
#         messages.success(request, 'Profile updated successfully')
#         return redirect('/student_Profile')  # Use the named URL instead of hardcoding

#     return render(request, "student/UpdateStud.html", {'datas': [student]})


def Stud_Course(request):
    search_term = request.POST.get('search_term', "").strip() if request.method == "POST" else ""
    
    if search_term:
        data = Course.objects.filter(
            Q(name__icontains=search_term) |
            Q(gpa__icontains=search_term) |
            Q(duration__icontains=search_term)
        )
    else:
        data = Course.objects.all()

    return render(request, 'student/Stud_Course.html', {
        'data': data,
        'search_term': search_term
    })

# def finacialaid(request):


def join_Course(request):
    student_id = request.session['Uid']
    id=request.GET['id']
    student = Student.objects.get(user=student_id)
    course = Course.objects.get(id=id)
    total_sum=Answer.objects.filter(std=student).aggregate(
        # total_sum=Coalesce(Sum('one'), Value(0))
    )['total_sum']

    if total_sum >= int(course.gpa):
        messages.success(request, 'You have successfully joined the course.')
    else:
        messages.error(request,'Your GPA is too low to join this course.')
 

    return redirect('/Stud_Course')



def generate_final_qna(questions):
    final_qna = []
    random.shuffle(questions)
    for q in questions:
        final_qna.append(q)
    return final_qna

def assign_questions_to_candidate(request, questions):
    final_qna = generate_final_qna(questions)
    qna_primary_keys = [q.pk for q in final_qna]  # Storing primary keys
    request.session['assigned_questions'] = qna_primary_keys
    request.session['obj_index'] = 0
    request.session['qcount'] = 1

def test(request):
    
    student_id = request.session['Uid']

    user = Student.objects.get(user=student_id)
    # if Answer.objects.filter(std=user).exists():
       
    #     return redirect('/testresult')

    if 'assigned_questions' not in request.session:
        questions = list(Question.objects.all())
        assign_questions_to_candidate(request, questions)

    assigned_qna_primary_keys = request.session['assigned_questions']
    assigned_questions = Question.objects.filter(pk__in=assigned_qna_primary_keys)
    curr_obj_index = request.session.get('obj_index', 0)
    qcount = request.session.get('qcount', 1)

    if request.method == 'POST':
        selected = request.POST.get('opt')
        qid = request.POST.get('qid')
        try:
            question = Question.objects.get(id=qid)
        except Question.DoesNotExist:
            return redirect('/error') 
        
        if question.answer == selected:
          
            user_answer, created = Answer.objects.get_or_create(std=user, defaults={'one': 1})

            user_answer.one = F('one') + 1
          
            user_answer.save()
        
        curr_obj_index += 1
        qcount += 1
        request.session['obj_index'] = curr_obj_index
        request.session['qcount'] = qcount

        if curr_obj_index < len(assigned_questions):
            curr_obj = assigned_questions[curr_obj_index]
        else:
            del request.session['assigned_questions']
            del request.session['obj_index']
            del request.session['qcount']
            return redirect('/testresult')

    else:
        if curr_obj_index < len(assigned_questions):
            curr_obj = assigned_questions[curr_obj_index]
        else:
            del request.session['assigned_questions']
            del request.session['obj_index']
            del request.session['qcount']
            return redirect('/userhome')

    return render(request, 'student/test.html', {'obj': curr_obj, 'qcount': qcount})

def testresult(request):
    user_id = request.session.get('Uid')
    user = Student.objects.get(user=user_id)
    answers = Answer.objects.filter(std=user)

    # Calculate total score of the user
    total_sum = answers.aggregate(
        total_sum=Coalesce(Sum('one'), Value(0))
    )['total_sum']

    # Create or update the user's answer record
    try:
        # Attempt to retrieve the existing answer record
        answer = Answer.objects.get(std=user)
        # If the record exists, update its fields
        answer.total_sum = total_sum
        answer.one = total_sum
        answer.save()
    except Answer.DoesNotExist:
        # If the record doesn't exist, create a new one
        answer = Answer.objects.create(std=user, one=total_sum, total_sum=total_sum)

    # Prepare data to pass to the template
    data_to_pass = {
        'total_sum': total_sum,
    }

    return render(request, 'student/testresult.html', data_to_pass)




def eligible_course(student_id):
    student = Student.objects.filter(user=student_id).first()
    if not student:
        return None

    total_sum = Answer.objects.filter(std=student).aggregate(
        total_sum=Coalesce(Sum('one'), Value(0))
    )['total_sum']

    eligible_courses = Course.objects.filter(gpa__lte=total_sum)
    eligible_colleges = College.objects.filter(course__in=eligible_courses).distinct()

    # Attach eligible courses to each college
    for college in eligible_colleges:
        college.eligible_courses = college.course_set.filter(gpa__lte=total_sum)

    return {
        'total_sum': total_sum,
        'eligible_colleges': eligible_colleges,
    }


def eligible_college_course_view(request):
    student_id = request.session['Uid']
    result = eligible_course(student_id)

    if result:
        return render(request, 'student/eligible_colleges.html', {
            'data': result['eligible_colleges'],
            'total_sum': result['total_sum']
        })
    else:
        messages.error(request, "You are not eligible.")
        return redirect('/test')


# def view_loan_options(request):
#     student_id = request.session.get('Uid')
#     result = eligible_course(student_id)

#     if result:

#         loan_options = FinancialAidLoan.objects.filter(
#             Q(course__in=result['eligible_courses']) |
#             Q(college__in=result['eligible_colleges'])
#         )

#         return render(request, 'student/loan_options.html', {
#             'data': result['eligible_colleges'],
#             'cou': result['eligible_courses'],
#             'total_sum': result['total_sum'],
#             'loan_options': loan_options  
#         })
#     else:
#         messages.error(request, "You are not eligible for financial aid.")
#         return redirect('/test')

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.db.models import Sum, Value
# from django.db.models.functions import Coalesce

# def financial_aid_view(request):
#     student_id = request.session.get('Uid')
#     student = Student.objects.filter(user=student_id).first()

#     if not student:
#         messages.error(request, "Student not found.")
#         return redirect('/userhome')

#     # Check if the student has completed the test
#     if not Answer.objects.filter(std=student).exists():
#         messages.warning(request, "Please complete the test to view financial aids.")
#         return redirect('/test')

#     # Calculate the total GPA
#     total_sum = Answer.objects.filter(std=student).aggregate(
#         total_sum=Coalesce(Sum('one'), Value(0))
#     )['total_sum']

#     # Fetch eligible financial aids based on the GPA
#     eligible_loans = Loan.objects.filter(
#         course__gpa__lte=total_sum
#     ).distinct()

#     # Render the financial aid view
#     return render(request, 'student/financial_aid.html', {
#         'loans': eligible_loans,
#         'total_sum': total_sum
#     })

# def financialAidLoan(request):
#     return render(request,'FinancialAid/financialAidLoan.html')


# def student_dashboard(request):
#     student_id = request.session.get('Uid')

#     if not student_id:
#         messages.error(request, "Please log in to access your dashboard.")
#         return redirect('/login')

#     student = Student.objects.filter(user=student_id).first()

#     if not student:
#         messages.error(request, "Student record not found.")
#         return redirect('/userhome')

#     return render(request, 'student/dashboard.html', {'student': student})

def financial_aid(request):
    student_id = request.session.get('Uid')


    if not student_id:
        messages.error(request, "You need to log in first.")
        return redirect('/login')

    student = Student.objects.filter(user=student_id).first()

    if not student:
        messages.error(request, "Student record not found.")
        return redirect('/userhome')

  
    total_score = Answer.objects.filter(std=student).aggregate(
        total_sum=Coalesce(Sum('one'), 0)
    )['total_sum']

    if total_score == 0:
        messages.error(request, "Please attend the test to view financial aid options.")
        return redirect('/test')


    eligible_loans = Loan.objects.filter(eligibile_gpa__lte=total_score).distinct()

    return render(request, 'student/financial_aid.html', {
        'loans': eligible_loans,
        'score': total_score,
    })

def test_result(request):
    student_id = request.session.get('Uid')

    if not student_id:
        messages.error(request, "Please log in to access your test results.")
        return redirect('/login')

    student = Student.objects.filter(user=student_id).first()

    if not student:
        messages.error(request, "Student record not found.")
        return redirect('/userhome')

    
    total_score = Answer.objects.filter(std=student).aggregate(
        total_sum=Coalesce(Sum('one'), 0)
    )['total_sum']

    #
    eligible_courses = Course.objects.filter(gpa__lte=total_score)

    return render(request, 'student/test_result.html', {
        'score': total_score,
        'courses': eligible_courses,
    })



def InterviewNotes(request):
    data=InterviewPreparation.objects.all()
    return render(request,'student/InterviewNotes.html',{'data':data})

def view_interviewnote_details(request):
    note_id=request.GET['id']
    try:

        note = InterviewPreparation.objects.get(id=note_id)
        return render(request, 'student/view_interviewnote_details.html', {'note': note})
    except InterviewPreparation.DoesNotExist:
        raise Http404("Note not found")


# def download_interviewnotes(request):
#     id=request.GET['id']
#     try:
#         interview = InterviewPreparation.objects.get(id=id)
#         if not interview.pdf:
#             raise Http404("Study material not found")
#         file_path = interview.pdf.path 
#         response = FileResponse(open(file_path, 'rb'), as_attachment=True)
#         response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
#         return response
#     except InterviewPreparation.DoesNotExist:
#         raise Http404("Internship not found")
#     except FileNotFoundError:
#         raise Http404("Study material file not found")
def download_interviewnotes(request):
    note_id = request.GET.get('id') 
    if not note_id:
        raise Http404("Note ID not provided")
    try:
        interview = InterviewPreparation.objects.get(id=note_id)
        if not interview.pdf:
            raise Http404("Study material not found")
        file_path = interview.pdf.path
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    except InterviewPreparation.DoesNotExist:
        raise Http404("Interview preparation note not found")
    except FileNotFoundError:
        raise Http404("Study material file not found")

def job_vacancy(request):
    data=Jobs.objects.all()
    return render(request,'student/job_vacancy.html',{'data':data})





#Financer
def finpg(request):
    return render(request,'financer/finpg.html')


def addLoan(request):
    uid=request.session['Uid']
    fin=Financer.objects.get(user_id=uid)
    if request.POST:
        name=request.POST['name']
        provider=request.POST['provider']
        interest_rate =request.POST['interest_rate ']
        max_amount=request.POST['max_amount']
        tenure_years=request.POST['tenure_years']
        eligibile_gpa=request.POST['eligibile_gpa']
        details =request.POST['details']
        loan=Loan.objects.create(name=name,provider=provider,interest_rate=interest_rate ,max_amount= max_amount,tenure_years=tenure_years,eligibile_gpa=eligibile_gpa,details=details,fin=fin)
        loan.save()
    return render(request,'financer/addLoan.html')

def viewLoan(request):
    current_user = Financer.objects.get(user=request.user)
    data = Loan.objects.all()
    return render(request, 'financer/viewLoan.html', {
        'data': data,
        'current_user': current_user
    })




def delLoan(request):
    id=request.GET['id']
    data=Loan.objects.filter(id=id).delete()
    return redirect('/viewLoan')


#mentor
def mentorpg(request):
    return render(request,'Mentor/mentorpg.html')
def view_Course(request):
    data=Course.objects.all()
    return render(request,'Mentor/view_Course.html',{'data':data})

def InterviewPrepare(request):
    uid = request.session['Uid']
    mentor = Mentor.objects.get(user_id=uid)  
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        pdf = request.FILES.get('pdf')  
        note = InterviewPreparation.objects.create(
            mentor=mentor,
            title=title,
            content=content,
            pdf=pdf
        )
        note.save()
    return render(request,'Mentor/InterviewPrepare.html')


def viewnotes(request):
    data=InterviewPreparation.objects.all()
    return render(request,'Mentor/viewnotes.html',{'data':data})





#Chat

def chat(request):
    uid = request.session["Uid"]
    name = ""
    artistData = Mentor.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(sellerid__user=uid) & Q(customerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    userid = Student.objects.get(user=uid)
    if id:
        customerid = Mentor.objects.get(id=id)
        name = customerid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="STUDENT")
        sendMsg.save()
    return render(request, "Student/reciever.html", {"artistData": artistData, "getChatData": getChatData, "customerid": name, "id": id})


def reply(request):
    uid = request.session["Uid"]
    name = ""
    userData = Student.objects.all()
    id = request.GET.get("id")
    getChatData = Chat.objects.filter(
        Q(customerid__user=uid) & Q(sellerid=id))
    current_time = dt.now().time()
    formatted_time = current_time.strftime("%H:%M")
    customerid = Mentor.objects.get(user=uid)
    if id:
        userid =Student.objects.get(id=id)
        name = userid.name
    if request.POST:
        message = request.POST["message"]
        sendMsg = Chat.objects.create(
            sellerid=userid, message=message, customerid=customerid, time=formatted_time, utype="MENTOR")
        sendMsg.save()
    return render(request, "Mentor/sender.html", {"userData": userData, "getChatData": getChatData, "userid": name, "id": id})






