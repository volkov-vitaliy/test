# Generated by Django 5.1.3 on 2024-11-24 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='translation',
            constraint=models.UniqueConstraint(fields=('content_type', 'object_id', 'field_name', 'language'), name='lang_field_name'),
        ),
    ]
