# Generated by Django 4.2.2 on 2023-06-07 01:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('answer_order', models.CharField(blank=True, choices=[('content', 'Content'), ('random', 'Random'), ('none', 'None')], help_text='The order in which multichoice answer options are displayed to the user', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('single_attempt', models.BooleanField(default=True)),
                ('random_order', models.BooleanField(default=True, help_text='orders with which questions will appear')),
                ('max_questions', models.PositiveIntegerField(help_text='Display the questions in a random order or as they are set?')),
                ('duration', models.IntegerField(help_text='duration in minutes')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cbt_app.courses')),
                ('level', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cbt_app.level')),
                ('questions', models.ManyToManyField(to='cbt_app.question')),
            ],
        ),
        migrations.CreateModel(
            name='UserGuess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guess', models.JSONField()),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cbt_app.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('courses', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cbt_app.courses')),
            ],
            options={
                'unique_together': {('courses', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Sitting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_all', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='All Questions')),
                ('question_attempted', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Answered Questions')),
                ('question_unattempted', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Unanswered Questions')),
                ('question_failed', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Failed Questions')),
                ('question_passed', models.CharField(max_length=1024, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')], verbose_name='Passed Questions')),
                ('question_choice_pair', models.JSONField(blank=True, default=dict, help_text='json format question choice pair')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Is completed')),
                ('current_score', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cbt_app.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.CharField(max_length=10)),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='cbt_app.quiz')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ManyToManyField(to='cbt_app.topic'),
        ),
        migrations.AddField(
            model_name='courses',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cbt_app.level'),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('is_answer', models.BooleanField(default=False)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cbt_app.question')),
            ],
        ),
    ]
