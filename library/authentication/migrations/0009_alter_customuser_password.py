# Generated by Django 5.1 on 2024-08-30 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_customuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
