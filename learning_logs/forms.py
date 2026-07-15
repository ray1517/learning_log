from django import forms
from django.core.validators import MinLengthValidator

from .models import Topic, Entry

# 最小长度校验，避免空内容提交
text_min_validator = MinLengthValidator(1, message="内容不能为空")

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {
            'text': '',
            'public': '设为公开主题'
        }
        widgets = {
            'text': forms.TextInput(attrs={
                # 前端实时校验
                'required': 'required',
                'minlength': '1',
                'placeholder': '请输入主题名称',
                'class': 'form-control'
            })
        }
        validators = {
            'text': [text_min_validator]
        }

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(attrs={
                'cols': 80,
                'rows': 6,
                'required': 'required',
                'minlength': '1',
                'placeholder': '在这里写下你的学习笔记...',
                'class': 'form-control'
            })
        }
        validators = {
            'text': [text_min_validator]
        }