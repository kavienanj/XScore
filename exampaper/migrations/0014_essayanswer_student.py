# Generated by Django 2.2 on 2020-01-15 13:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('exampaper', '0013_auto_20200115_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='essayanswer',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
