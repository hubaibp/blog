# Generated by Django 5.1.4 on 2024-12-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writers_app', '0007_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='description',
            field=models.TextField(),
        ),
    ]