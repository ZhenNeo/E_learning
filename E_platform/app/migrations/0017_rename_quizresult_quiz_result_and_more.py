# Generated by Django 5.0.4 on 2024-04-30 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_course_category_course_category_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='QuizResult',
            new_name='Quiz_Result',
        ),
        migrations.RemoveField(
            model_name='quizquestion',
            name='quiz',
        ),
        migrations.DeleteModel(
            name='QuizChoice',
        ),
        migrations.DeleteModel(
            name='QuizQuestion',
        ),
    ]
