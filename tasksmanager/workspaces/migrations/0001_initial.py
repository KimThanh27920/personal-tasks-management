# Generated by Django 3.2.13 on 2022-06-21 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tilte', models.CharField(max_length=255, null=None)),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'workspaces',
            },
        ),
        migrations.CreateModel(
            name='Images_Workspace',
            fields=[
                ('workspace', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='workspaces.workspace')),
                ('url', models.ImageField(upload_to='workspaces_img/')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'image_workspace',
            },
        ),
    ]
