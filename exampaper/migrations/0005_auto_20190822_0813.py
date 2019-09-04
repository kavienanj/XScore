# Generated by Django 2.2 on 2019-08-22 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exampaper', '0004_auto_20190819_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essayanswer',
            name='answer',
            field=models.FileField(upload_to='essay_answers/', verbose_name='Answer submitted'),
        ),
        migrations.AlterField(
            model_name='essayquestion',
            name='working_file',
            field=models.FileField(upload_to='essay_questions/', verbose_name='File to work and submit'),
        ),
    ]
