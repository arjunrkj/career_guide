from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path('ad',views.admin),
    path('login',views.login),

    #admin---
    path('adminpg',views.adminpg),
    path('clgreject',views.clgreject),
    path('clgapprove',views.clgapprove),
    path('addquestions',views.addquestions),
    path('admin_clg_view',views.admin_clg_view),
    path('add_JobDetail',views.add_JobDetail),
    path('admin_studview',views.admin_studview),
    path('stud_Dlt',views.stud_Dlt),
    # path('dltst',views.dltst),
#    path('view_loan_options',views.view_loan_options),
   
    


    #Student----
    path('studreg',views.studreg),
    path('stdpg',views.stdpg),
    path('stud_clg_view',views.stud_clg_view),
    path('Stud_Course',views.Stud_Course),
    path('job_vacancy',views.job_vacancy),
    path('test',views.test),
    path('testresult',views.testresult),
    path('eligible_colleges',views.eligible_college_course_view),
    path('eligible_course',views.eligible_course),
    path('financial_aid',views.financial_aid),
    path('view_interviewnote_details',views.view_interviewnote_details),
    # path('join_course',views.join_course),
    path('std_testresult',views.std_testresult),
    path('student_Profile',views.student_Profile),
    path('UpdateStud',views.UpdateStud),



    

    #college----
    path('clgreg',views.clgreg),
    path('clgpg',views.clgpg),
    path('addcourse',views.addcourse),
    path('clgview',views.clgview),
    path('course_view',views.course_view),
    path('update',views.update),
    path('addMentor',views.addMentor),
    path('delCourse',views.delCourse),
    path('InterviewNotes',views.InterviewNotes),
    path('download_interviewnotes/',views.download_interviewnotes),
    path('collegeUpdate',views.collegeUpdate),
    path('std_results',views.std_results),

    #finance
    path('finReg',views.finReg),
    path('finpg',views.finpg),
    path('addLoan',views.addLoan),
    path('viewLoan',views.viewLoan),
    path('delLoan',views.delLoan),


    #mentor
    path('mentorpg',views.mentorpg),
    path('view_Course',views.view_Course),
    path('InterviewPrepare',views.InterviewPrepare),

      #CHAT
    path('chat',views.chat),
    path('reply',views.reply),
    
    

]
