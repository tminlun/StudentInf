from datetime import datetime

from django.db import models
from users.models import UserProfile as User

# Create your models here.


class Role(models.Model):
    name = models.CharField(max_length=15,default="", verbose_name="名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "角色"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,verbose_name="用户")
    name = models.CharField(max_length=15,default="", verbose_name="教师名")
    sex = models.CharField(max_length=6,default='male', choices=(('male','男'), ('female','女')), verbose_name="性别")
    project = models.CharField(max_length=45,null=True,blank=True,verbose_name="专业")
    phone = models.CharField(max_length=11,null=True,blank=True,verbose_name="手机号码")
    college = models.CharField(max_length=45,null=True,blank=True,verbose_name="学院")
    # 角色，一个角色多个教师
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True, blank=True,related_name="teachers", verbose_name="角色")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True,verbose_name="用户")
    number = models.CharField(max_length=30, null=True,blank=True,verbose_name="学号")
    name = models.CharField(max_length=15, default="匿名", verbose_name="名称")
    sex = models.CharField(max_length=6, default='male', choices=(('male', '男'), ('female', '女')), verbose_name="性别")
    project = models.CharField(max_length=45, null=True, blank=True, verbose_name="专业")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    college = models.CharField(max_length=45, null=True, blank=True, verbose_name="学院")
    grade = models.ForeignKey("Grade",on_delete=models.CASCADE,null=True, blank=True,related_name="students",verbose_name="班级")
    # 多个学生担任一个角色
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null=True, blank=True, related_name="students", verbose_name="角色")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 班级
class Grade(models.Model):
    # 一个老师多个班级；一个班级多个学生。
    name = models.CharField(max_length=15, default="", verbose_name="班级名")
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name="grades", verbose_name="辅导员")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "班级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程名
class Course(models.Model):
    name = models.CharField(max_length=15, default="", verbose_name="课程名")
    periods = models.CharField(max_length=30, null=True,blank=True,verbose_name="学时")
    credits = models.CharField(max_length=15, default="2",verbose_name="学分")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name="courses", verbose_name="科任老师")

    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程名"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 班级课程表（课程表：软件一班的html课程）
class CourseGrade(models.Model):
    grade = models.ForeignKey(Grade,on_delete=models.CASCADE,related_name="course_grade",verbose_name="班级名")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="course_grade",verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "班级课程表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}{}".format(self.grade.name, self.course.name)


# 成绩类型
class PerformanceType(models.Model):
    name = models.CharField(max_length=30,default="", verbose_name="类型名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "成绩类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 成绩
class Performance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="performances",verbose_name="学号")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="performances", verbose_name="课程")
    score_num = models.CharField(max_length=45, null=True,blank=True,verbose_name="成绩")
    type = models.ForeignKey(PerformanceType,related_name="performances",on_delete=models.CASCADE,verbose_name="类型名")
    term = models.CharField(max_length=15, default="one",choices=(("one","第一学期"),("two","第二学期")), verbose_name="学期")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")


    class Meta:
        verbose_name = "成绩"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.student.number}的{self.course.name}的成绩为：{self.score_num}"

