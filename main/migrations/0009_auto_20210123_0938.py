# Generated by Django 3.0 on 2021-01-23 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='coment',
            new_name='content',
        ),
    ]
