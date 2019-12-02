import random, datetime

from django.shortcuts import render,redirect,reverse
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from performance.models import Role, Teacher, Student

from .models import UserProfile
from .forms import LoginForm,RegisterForm


# Create your views here.


# # 首页
# class IndexView(View):
#     def get(self,request):
#         user = request.user
#         if not user.is_authenticated:
#             return render(request, 'login.html')
#
#         # 返回教师个人信息
#         elif user.role == "teacher":
#             pass
#         else:
#             return render(request, 'reg-homepage.html', {})


class CustomBackend(ModelBackend):
    """
    #邮箱和用户名都可以登录
    # 基础ModelBackend类，因为它有authenticate方法
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        user = request.user
        if user.is_authenticated:
            return render(request, 'login.html', {"placard":"您已经登录"})

        return render(request,'login.html',{"login_form":login_form})

    def post(self,request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            role = request.POST.get('role', '')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                if role == user.role:
                    login(request, user)
                    # 身份判断重定向指定页面
                    if user.role == "student":
                        # 学生（默认为个人信息）
                        return redirect(reverse('student_info'))
                    elif user.role == "teacher":
                        # 老师（默认为个人信息）
                        return redirect(reverse('teacher_info'))
                # 判断身份错误
                else:
                    return render(request, 'login.html', {
                        "login_form": login_form,
                        "msg": "身份错误"
                    })
            # 匹配错误
            else:
                return render(request,'login.html',{
                    "login_form": login_form,
                    "msg": "账号密码错误"
                })
        # 验证错误
        else:
            return render(request, 'login.html', {
                "login_form": login_form
            })


# 注册
class SingInView(View):
    def get(self,request):
        register_form = RegisterForm()
        user = request.user
        
        if user.is_authenticated:
            return render(request, 'reg-homepage.html')
        return render(request, 'sign.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            
            user_name = request.POST.get('username', '')
            user_email = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            pass_word_again = request.POST.get('password_again', '')
            role = request.POST.get('role', '')
            
            # 判断
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'sign.html', {'register_form': register_form, 'msg': '用户名已存在'})
            if UserProfile.objects.filter(email=user_email):
                return render(request, 'sign.html', {'register_form': register_form, 'msg': '用户邮箱已存在'})
            if pass_word != pass_word_again:
                return render(request, 'sign.html', {'register_form': register_form, 'msg': '两次输入不一致'})

            # 实例化一个user_profile对象,根据身份判别学生还是教师
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_email
            user_profile.password = make_password(pass_word_again)  # 对注册的密码加密
            user_profile.role = role  # 身份
            user_profile.is_active = False  # 让用户手动激活,默认为未激活
            user_profile.save()  # 然后保存

            # 身份不为空
            if role is not None:
                # 学生
                if role == "student":
                    # 身份对象
                    role = create_role("学生")

                    # 创建学生对象
                    student = Student.objects.create()
                    student.user = user_profile
                    student.role = role
                    # 学号
                        # 年份
                    year_start = int(datetime.datetime.now().strftime('%Y') + '000')
                    year_end = int(datetime.datetime.now().strftime('%Y') + '999')
                    student.number = random.randint(year_start, year_end)
                    student.save()

                # 教师
                elif role == "teacher":
                    # 身份对象
                    role = create_role("教师")

                    teacher = Teacher.objects.create()
                    teacher.user = user_profile
                    teacher.role = role
                    teacher.save()

                else:
                    # 身份对象
                    role = create_role("其他")


            # 注册成功，转跳到登录页面
            return render(request, 'login.html')
        # 表单自动验证错误
        else:
            return render(request, 'sign.html', {
                "register_form": register_form
            })


def create_role(name):
    """
    有是否记录？获取：创建
    :param name: 身份名称
    :return:
    """
    try:
        role = Role.objects.get(name=name)
    except:
        role = Role.objects.create()
        role.name = name
        role.save()
    return role


class LogoutView(View):
    """注销"""
    def get(self,request):
        logout(request)
        return redirect(reverse('login'))
