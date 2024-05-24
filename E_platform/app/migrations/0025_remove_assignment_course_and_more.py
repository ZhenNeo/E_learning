# Generated by Django 4.1.4 on 2024-05-03 13:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0024_alter_quiz_result_score"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assignment",
            name="course",
        ),
        migrations.RemoveField(
            model_name="assignmentfeedback",
            name="assignment",
        ),
        migrations.RemoveField(
            model_name="assignmentfeedback",
            name="student",
        ),
        migrations.RemoveField(
            model_name="choice",
            name="question",
        ),
        migrations.RemoveField(
            model_name="question",
            name="quiz",
        ),
        migrations.RemoveField(
            model_name="quiz",
            name="course",
        ),
        migrations.RemoveField(
            model_name="quiz_result",
            name="quiz",
        ),
        migrations.RemoveField(
            model_name="quiz_result",
            name="student",
        ),
        migrations.RemoveField(
            model_name="studentassignment",
            name="assignment",
        ),
        migrations.RemoveField(
            model_name="studentassignment",
            name="student",
        ),
        migrations.RemoveField(
            model_name="voucher",
            name="created_by",
        ),
        migrations.DeleteModel(
            name="Answer",
        ),
        migrations.DeleteModel(
            name="Assignment",
        ),
        migrations.DeleteModel(
            name="AssignmentFeedback",
        ),
        migrations.DeleteModel(
            name="Choice",
        ),
        migrations.DeleteModel(
            name="Course",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
        migrations.DeleteModel(
            name="Quiz",
        ),
        migrations.DeleteModel(
            name="Quiz_Result",
        ),
        migrations.DeleteModel(
            name="StudentAssignment",
        ),
        migrations.DeleteModel(
            name="Voucher",
        ),
    ]
