from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
# 导入自定义注册表单
from .forms import CustomRegisterForm


def register(request):
    # 注册页面
    if request.method != 'POST':
        # GET 请求，空白表单
        form = CustomRegisterForm()
    else:
        # POST 提交注册
        form = CustomRegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            # 注册成功提示
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "注册成功，已自动登录"
            else:
                request.session["toast_msg"] = "Register success, logged in automatically"
            return redirect('learning_logs:index')
        else:
            # 表单校验失败，区分用户名重复错误
            err_list = str(form.errors)
            if "username" in form.errors and "already exists" in err_list:
                # 用户名重复
                if request.LANGUAGE_CODE == "zh-hans":
                    request.session["toast_msg"] = "该用户名已被占用，请更换用户名"
                else:
                    request.session["toast_msg"] = "This username already exists, please pick another one"
            else:
                # 其他表单错误（密码不一致、密码强度不足、邮箱格式错误）
                if request.LANGUAGE_CODE == "zh-hans":
                    request.session["toast_msg"] = "表单填写有误，请检查邮箱、密码规则"
                else:
                    request.session["toast_msg"] = "Form validation failed, please check email & password rules"
    context = {"form": form}
    # 模板路径保持 registration/register.html
    return render(request, "registration/register.html", context)


def login_view(request):
    # 登录页面，支持记住我7天免登
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # 设置会话有效期
            if remember:
                request.session.set_expiry(60 * 60 * 24 * 7)
            else:
                request.session.set_expiry(0)
            # 登录成功弹窗
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "登录成功"
            else:
                request.session["toast_msg"] = "Login success"
            return redirect("learning_logs:index")
        else:
            # 账号密码错误弹窗
            if request.LANGUAGE_CODE == "zh-hans":
                request.session["toast_msg"] = "用户名或密码错误，请重新输入"
            else:
                request.session["toast_msg"] = "Incorrect username or password"
    context = {"form": AuthenticationForm()}
    return render(request, "registration/login.html", context)


def logout_view(request):
    # 退出登录，弹窗提示
    logout(request)
    if request.LANGUAGE_CODE == "zh-hans":
        request.session["toast_msg"] = "已成功退出登录"
    else:
        request.session["toast_msg"] = "Logout successfully"
    return redirect("learning_logs:index")