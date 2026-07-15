from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# 密码强度规则：大小写字母+数字，至少8位
pwd_validator = RegexValidator(
    regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$',
    message="密码必须包含小写字母、大写字母、数字，长度不少于8位"
)

class CustomRegisterForm(UserCreationForm):
    # 新增必填邮箱
    email = forms.EmailField(
        label="邮箱",
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "请输入邮箱，用于找回账号",
            "class": "form-control"
        })
    )
    password1 = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={
            "placeholder": "大小写+数字，至少8位",
            "class": "form-control"
        }),
        validators=[pwd_validator]
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={
            "placeholder": "再次输入密码",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "用户名不可重复",
                "class": "form-control"
            })
        }

    # 校验两次密码是否一致
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("两次输入的密码不一致")
        return p2