# Generated by Django 5.1.3 on 2024-11-26 09:02

import django.db.models.deletion
import translation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('birth_date', models.DateField(db_index=True)),
                ('about', models.TextField()),
                ('about_short', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('title', translation.models.TranslationField(editable=False)),
                ('content', translation.models.TranslationField(editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='example.author')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
