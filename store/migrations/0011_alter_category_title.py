# Generated by Django 4.2 on 2023-04-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_comment_is_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
