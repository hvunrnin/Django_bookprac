# Generated by Django 4.2.4 on 2023-08-28 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_user_userbook_user_id_remove_book_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userbook',
            old_name='user_id',
            new_name='user',
        ),
    ]
