# Generated by Django 5.2 on 2025-04-20 10:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message="Номер должен быть в формате '+999999999'. До 15 цифр.", regex='^\\+?1?\\d{9,15}$')], verbose_name='День рождения'),
        ),
    ]
