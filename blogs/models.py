from django.db import models
from django.contrib.auth.models import User


class BlogPost(models.Model):
    """Тема, которую изучает пользователь"""
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text
