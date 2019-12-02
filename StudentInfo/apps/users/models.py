from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    """ 用户扩展 """
    name = models.CharField(max_length=15,null=True,blank=True,verbose_name="姓名")  # 可以用手机号码和密码登录，不用名字
    birthday = models.DateField(null=True,blank=True,verbose_name="生日")
    gender = models.CharField(max_length=6,default='male', choices=(('male','男'), ('female','女')), verbose_name="性别")
    role = models.CharField(max_length=8,default='student', choices=(('student','学生'), ('teacher','老师')),verbose_name="职责")
    mobile = models.CharField(null=True,blank=True,max_length=11,verbose_name="手机号码")
    email = models.EmailField(max_length=100,null=True,blank=True,verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username  # 父类AbstractUser原本的属性
