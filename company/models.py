
from django.db import models

from authemail.models import User


class Company(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, unique=True)
    info = models.TextField(verbose_name='Описание', blank=True)
    users = models.ManyToManyField(User, through='CompanyUserIx')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        db_table = 'company'


class News(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    content = models.TextField(verbose_name='Содержание')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        db_table = 'company_news'


class CompanyUserIx(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_user_ix'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'company'],
                name='uq__company_user_ix__usr_cmp',
                )
            ]
