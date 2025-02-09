# Generated by Django 5.1.6 on 2025-02-08 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_alter_chapter_description_alter_manga_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='manga',
            name='author',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='manga',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='volume',
            name='description',
            field=models.CharField(blank=True, default='', max_length=256),
            preserve_default=False,
        ),
    ]
