# Generated by Django 5.1.1 on 2024-09-23 20:34

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
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='foto_img')),
                ('titulo', models.CharField(default='Meu Compromisso', max_length=250)),
                ('data', models.DateTimeField()),
                ('font_color', models.CharField(default='#000000', max_length=7)),
                ('background_color', models.CharField(default='#FFFFFF', max_length=7)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
