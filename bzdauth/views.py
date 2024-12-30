from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail
from .models import CaptchaModle
from django.views.decorators.http import require_http_methods
from .form import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout  #此处login仅在使用默认django给的user对象时，可用，若用户自定义对象则不可用这个login



User = get_user_model()

@require_http_methods(['GET', 'POST'])
def bzdlogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 判断是否14天免登录
                if not remember:
                    # 如果没有点击免登录，设置过期时间为0，即浏览器关闭后密码过期
                    request.session.set_expiry(0)
                    # 如果点击了，无操作，使用默认的2周过期时间
                return redirect('/')
            else:
                print('邮箱或密码错误')
                return redirect(reverse('bzdauth:login'))

def bzdlogout(request):
    logout(request)
    return redirect("/")

@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(email=email, username=username, password=password)
            return redirect(reverse('bzdauth:login'))
        else:
            print(form.errors)
            return redirect(reverse('bzdauth:register'))


def send_email_captcha(request):
    # ?email=xxx使用查询参数表达式
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code":400,"message":"请输入正确的邮箱"})
    #生成验证码（取随机四位数）因取得数字由列表形式排列，依次使用连接来合并成四位数
    captcha="".join(random.sample(string.digits,k=4))
    # 储存到数据库中(本项目体量较小为方便直接存储数据库，不使用缓存)
    CaptchaModle.objects.update_or_create(email=email, defaults={ 'captcha': captcha})
    send_mail(subject='不知冬的博客注册验证码', message=f"您的注册验证码是：{captcha}", recipient_list=[email], from_email=None)
    return JsonResponse({"code":200,"message":"邮箱验证码发送成功"})
