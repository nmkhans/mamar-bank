# Generated by Django 5.0.6 on 2024-07-04 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='account_no',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
