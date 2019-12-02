# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/11/28 0028 21:20'

import xadmin

from .models import Role,Teacher,Student,Grade,Course,CourseGrade,PerformanceType,Performance


# 角色
class RoleAdmin(object):
    list_display = ('name', 'add_time')

# 教师
class TeacherAdmin(object):
    list_display = ('name', 'sex','project', 'phone','college', 'role','add_time')


# 学生
class StudentAdmin(object):
    list_display = ('number', 'name','sex', 'project','phone','college', 'role','grade','add_time')


# 班级
class GradeAdmin(object):
    list_display = ('name', 'teacher','add_time')


# 课程
class CourseAdmin(object):
    list_display = ('name', 'periods','credits','teacher','add_time')

# 班级课程表（课程表：软件一班的html课程）
class CourseGradeAdmin(object):
    list_display = ('grade', 'course','add_time')


# 成绩类型
class PerformanceTypeAdmin(object):
    list_display = ('name','add_time')


# 成绩
class PerformanceAdmin(object):
    list_display = ('student','course','score_num','type','term','add_time')



xadmin.site.register(Role, RoleAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Student, StudentAdmin)
xadmin.site.register(Grade, GradeAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseGrade, CourseGradeAdmin)
xadmin.site.register(PerformanceType, PerformanceTypeAdmin)
xadmin.site.register(Performance, PerformanceAdmin)
