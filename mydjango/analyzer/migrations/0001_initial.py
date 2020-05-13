# Generated by Django 2.2.5 on 2020-03-17 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('segment', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'CrawlPage',
            },
        ),
    ]
