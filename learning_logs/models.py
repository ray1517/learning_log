from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    """A topic the user is learning about."""
    text = models.CharField(max_length=200, verbose_name=_("主题名称"))
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False, verbose_name=_("公开"))

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


class Entry(models.Model):
    """Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name=_("所属主题"))
    text = models.TextField(verbose_name=_("内容"))
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("笔记")
        verbose_name_plural = _("笔记")

    def __str__(self):
        """Return a simple string representing the entry."""
        return f"{self.text[:50]}..."