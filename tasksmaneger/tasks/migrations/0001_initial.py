# Generated by Django 3.2.13 on 2022-06-21 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'priority',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'status',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255, null=None)),
                ('description', models.TextField(null=True)),
                ('due', models.DateField(null=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('priority', models.ForeignKey(null=None, on_delete=django.db.models.deletion.CASCADE, to='tasks.priority')),
                ('status', models.ForeignKey(default='Pending', on_delete=django.db.models.deletion.CASCADE, to='tasks.status')),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]
