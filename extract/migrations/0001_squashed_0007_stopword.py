# Generated by Django 2.0.4 on 2018-04-20 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('extract', '0001_initial'), ('extract', '0002_auto_20180418_1758'), ('extract', '0003_auto_20180419_0212'), ('extract', '0004_auto_20180419_0310'), ('extract', '0005_auto_20180419_0315'), ('extract', '0006_auto_20180419_0605'), ('extract', '0007_stopword')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword', models.CharField(max_length=30)),
                ('id', models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StopWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_word', models.CharField(max_length=30)),
            ],
        ),
    ]