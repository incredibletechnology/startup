# Generated by Django 3.0.8 on 2021-03-28 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20210328_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_master',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
