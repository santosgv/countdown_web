# Generated by Django 5.1.1 on 2024-10-08 01:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arquivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=21, unique=True)),
                ('size', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('S', 'Started'), ('C', 'Complete'), ('E', 'Expire')], default='S', max_length=1)),
                ('file_hash', models.CharField(blank=True, max_length=64, null=True)),
                ('completed_on', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='foto_img')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='Meu Compromisso', max_length=250)),
                ('data', models.DateTimeField()),
                ('font_color', models.CharField(default='#000000', max_length=7)),
                ('background_color', models.CharField(default='#FFFFFF', max_length=7)),
                ('valid_until', models.DateTimeField(blank=True, null=True)),
                ('foto', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.arquivos')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
