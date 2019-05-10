# Generated by Django 2.1.8 on 2019-05-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('title', models.TextField()),
                ('original_title', models.TextField()),
                ('runtime', models.IntegerField()),
                ('overview', models.TextField()),
                ('poster_url', models.TextField()),
                ('popularity', models.IntegerField()),
                ('director', models.TextField()),
                ('genres', models.ManyToManyField(related_name='movies', to='movies.Genre')),
            ],
        ),
    ]
