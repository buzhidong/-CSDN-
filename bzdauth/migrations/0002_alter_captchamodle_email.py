# Generated by Django 5.1.2 on 2024-12-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bzdauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='captchamodle',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
