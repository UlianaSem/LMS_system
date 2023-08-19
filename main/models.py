from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    profile_photo = models.ImageField(upload_to='students/', verbose_name='фото профиля', **NULLABLE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ('last_name',)

