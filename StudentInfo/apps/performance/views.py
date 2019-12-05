import re

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse


from .models import Student,Performance,PerformanceType,Teacher,Course,Role
# Create your views here.
'''
# 学生
    1、个人信息：查询、修改
    2、成绩查询
# 教师
    1、个人信息：查看，修改
    2、课程列表
        2.1 学生列表   
            2.1.1 打分
        2.2成绩查询

'''


def Success(code,msg):
    data = {}
    data['status'] = "success"
    data['code'] = code
    data['msg'] = msg
    return JsonResponse(data)

def Fail(code,msg):
    data = {}
    data['status'] = "fail"
    data['code'] = code
    data['msg'] = msg
    return JsonResponse(data)


# 个人信息
class StudentInfo(View):
    def get(self,request):
        user = request.user

        # 未登录
        if not user.is_authenticated:
            return render(request, 'login.html')

        try:
            student = Student.objects.get(user=user)
        except:
            role, created = Role.objects.get_or_create(name="student")
            student, created = Student.objects.get_or_create(user=user, role=role)

        return render(request, "reg-student-info.html",{
            "current_page": "info",
            "student": student,
        })

    # 修改个人信息
    def post(self,request):
        # 获取值
        req = request.POST
        ipt_name = req.get("ipt_name", "")
        ipt_sex = req.get("ipt_sex", "")
        ipt_phone = req.get("ipt_phone", "")
        student_pk = req.get("student_pk", "")

        # 验证手机号码
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res_phone = re.search(phone_pat, ipt_phone)

        # 验证
        if student_pk != "" and ipt_name != "" and ipt_sex != "" and res_phone:
            try:
                student = Student.objects.get(pk=student_pk)
            except Exception:
                return Fail(500, "获取不到对象！")

            student.name = ipt_name
            student.sex = ipt_sex
            student.phone = ipt_phone
            student.save()
            return Success(200, "修改成功")

        else:
            return Fail(500, "数据格式错误！")


# 成绩查询
class StudentScore(View):
    def get(self,request):
        user = request.user

        # 未登录
        if not user.is_authenticated:
            return render(request, 'login.html')

        try:
            student = Student.objects.get(user=user)
        except Exception:
            student = Student.objects.get(pk=1)

        performs = Performance.objects.all().order_by("-score_num")

        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(performs, 5, request=request)  # 进行分页，每5个作为一页
        performs = p.page(page)  # 获取当前页面

        return render(request, "reg-student-score.html", {
            "current_page": "score",
            "student": student,
            "performs": performs,

        })


class TeacherInfo(View):
    def get(self,request):
        user = request.user

        # 未登录
        if not user.is_authenticated:
            return render(request, 'login.html')

        try:
            teacher = Teacher.objects.get(user=user)
        except Exception:
            teacher = Teacher.objects.get(pk=1)
        return render(request, "teacher-info.html", {
            "current_page": "teacher-info",
            "teacher": teacher,
        })

    # 修改个人信息
    def post(self, request):
        # 获取值
        req = request.POST
        ipt_name = req.get("ipt_name", "")
        ipt_sex = req.get("ipt_sex", "")
        ipt_phone = req.get("ipt_phone", "")
        teacher_pk = req.get("teacher_pk", "")

        # 验证手机号码
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        res_phone = re.search(phone_pat, ipt_phone)

        # 验证
        if teacher_pk != "" and ipt_name != "" and ipt_sex != "" and res_phone:
            try:
                teacher = Teacher.objects.get(pk=teacher_pk)
            except Exception:
                return Fail(500, "获取不到对象！")

            teacher.name = ipt_name
            teacher.sex = ipt_sex
            teacher.phone = ipt_phone
            teacher.save()
            return Success(200, "修改成功")

        else:
            return Fail(500, "数据格式错误！")


class StudentsGrades(View):
    def get(self,request):
        user = request.user

        # 未登录
        if not user.is_authenticated:
            return render(request, 'login.html')

        try:
            teacher = Teacher.objects.get(user=user)
        except Exception:
            teacher = Teacher.objects.get(pk=1)

        # 一个教师管理多个班级
        grades = teacher.grades.all()

        return render(request, "teacher-grades.html",{
            "grades": grades,
            "teacher": teacher,
            "current_page": "grades",
        })


class TeacherStudents(View):
    def get(self,request):
        req = request.GET
        grade_pk = req.get("grade_pk", "")
        teacher_pk = req.get("teacher_pk", "")

        if grade_pk == "" and teacher_pk == "":
            return render(request, "teacher-grades.html")
        # 学生列表
        students = Student.objects.filter(grade=grade_pk)
        # 根据老师获取课程列表
        teacher = Teacher.objects.filter(pk=teacher_pk)[0]
        courses = Course.objects.filter(teacher=teacher)
        perform_types = PerformanceType.objects.all()

        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(students, 2, request=request)  # 进行分页，每5个作为一页
        students = p.page(page)  # 获取当前页面

        return render(request, "teacher-students.html",{
            "students": students,
            "courses":courses,
            "perform_types": perform_types,

            "current_page": "grades",
        })

    def post(self,request):
        req = request.POST
        student_pk = req.get("student_pk", 0)
        ipt_course_pk = req.get("ipt_course", 0)
        ipt_score = req.get("ipt_score", "")
        ipt_term = req.get("ipt_term", "")
        ipt_perform_type = req.get("perform_type", 0)

        # 验证
        if ipt_course_pk == 0 or ipt_score == "" or ipt_term == "" or ipt_perform_type == 0:
            return Fail(500, "数据格式错误")

        try:
            student = Student.objects.get(pk=student_pk)
            course = Course.objects.get(pk=ipt_course_pk)
            perform_type = PerformanceType.objects.get(pk=ipt_perform_type)
        except Exception:
            return Fail(500, "获取对象失败")

        try:
            perform = Performance()
            perform.student = student
            perform.course = course
            perform.score_num = ipt_score
            perform.term = ipt_term
            perform.type = perform_type
            perform.save()
            return Success(200, "添加成功")
        except Exception:
            return Fail(500, "保存失败！")


class TeacherCheckScore(View):
    def get(self,request):
        # 获取值
        student_pk = request.GET.get("student_pk", 0)
        if student_pk == 0:
            return render(request, "teacher-students.html")
        # 获取对象
        try:
            student = Student.objects.get(pk=student_pk)
        except Exception:
            return render(request, "teacher-students.html")
        performs = Performance.objects.filter(student=student).order_by("-score_num")
        # 返回对象
        return render(request,"teacher-check.html",{
            "student": student,
            "performs": performs,
            "current_page": "teacher_score_refer",
        })

