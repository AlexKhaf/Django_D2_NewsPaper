# Generated by Django 4.2.2 on 2023-06-22 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='costCategory',
            new_name='postCategory',
        ),
    ]
