"""StudentInfo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin

from django.urls import path,include
# 上传图片
from django.conf import settings
from django.conf.urls.static import static

from users.views import LoginView,SingInView,LogoutView
from performance.views import StudentInfo,StudentScore
from performance.views import TeacherInfo,StudentsGrades,TeacherStudents,TeacherCheckScore

urlpatterns = [
    path('xadmin/', xadmin.site.urls, name="xadmin"),
    path('captcha/', include('captcha.urls')),  # 验证码
    path('ueditor/', include('DjangoUeditor.urls')),

    path('login/', LoginView.as_view(), name="login"),  # 登录
    path('sing_in/', SingInView.as_view(), name="sing_in"),  # 登录
    path('logout/',LogoutView.as_view(),name="logout"), #注销

    # performance/views
    # 学生
    path('student_info/', StudentInfo.as_view(), name="student_info"),  # 修改学生个人信息
    path('student_score/', StudentScore.as_view(), name="student_score"),  # 查看成绩
    # 教师
    path('teacher_info/', TeacherInfo.as_view(), name="teacher_info"),  # 个人信息
    path('grades/', StudentsGrades.as_view(), name="grades"),  # 班级列表
    path('teacher-students/', TeacherStudents.as_view(), name="teacher-students"),  # 班级列表
    path('teacher-check/', TeacherCheckScore.as_view(), name="teacher-check"),  # 教师查询学生成绩


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)