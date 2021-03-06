# Generated by Django 2.2 on 2020-09-15 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('variables', '0001_initial'),
        ('opening', '0001_initial'),
        ('teacher', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewTeacherUnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.ManyToManyField(blank=True, default=None, to='student.Student')),
                ('teacher', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ViewTeacherRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniquecount', models.IntegerField(default=0)),
                ('nonuniquecount', models.IntegerField(default=0)),
                ('msgtocount', models.IntegerField(default=0)),
                ('msgfromcount', models.IntegerField(default=0)),
                ('ordercount', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ViewTeacherNonUnique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='ViewOpening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('opening', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='opening.Opening')),
                ('teacher', models.ManyToManyField(blank=True, default=None, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TagTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('count', models.IntegerField(default=0)),
                ('teacher', models.ManyToManyField(blank=True, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='TagOpening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('count', models.IntegerField(default=0)),
                ('opening', models.ManyToManyField(blank=True, to='opening.Opening')),
            ],
        ),
        migrations.CreateModel(
            name='SearchWordTeacherRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=30)),
                ('date', models.DateField(auto_now=True)),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='variables.Level_Expertise')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='variables.Subject_Expertise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.ManyToManyField(blank=True, default=None, to='student.Student')),
                ('teacher', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='FavOpening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opening', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='opening.Opening')),
                ('teacher', models.ManyToManyField(blank=True, default=None, to='teacher.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='BlockUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('blocked', models.ManyToManyField(blank=True, default=None, related_name='blocked_u', to=settings.AUTH_USER_MODEL)),
                ('blocker', models.OneToOneField(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='blocker_u', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
