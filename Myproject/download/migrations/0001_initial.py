# Generated by Django 2.0.3 on 2019-03-08 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=100)),
                ('imgpath', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
    ]