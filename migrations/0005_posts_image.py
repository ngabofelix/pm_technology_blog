# Generated by Django 4.0.2 on 2022-03-19 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_posts_author_alter_posts_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='image',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]
