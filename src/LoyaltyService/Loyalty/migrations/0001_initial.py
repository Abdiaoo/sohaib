# Generated by Django 4.1.2 on 2023-04-18 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserLoyalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, unique=True)),
                ('reservationCount', models.IntegerField(default=0)),
                ('status', models.CharField(default='BRONZE', max_length=10)),
                ('discount', models.IntegerField(default=0)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
    ]